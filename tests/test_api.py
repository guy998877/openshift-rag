"""Flask API tests — unit-level (no API key) and integration (real OpenAI).

This module tests the Flask backend in two tiers:

1. **Unit tests** (no OPENAI_API_KEY needed):
   - Endpoint routing and response structure
   - Input validation and error handling
   - Mock/temp data scenarios
   - Run on every CI job

2. **Integration tests** (requires OPENAI_API_KEY):
   - Full end-to-end pipeline: embed docs → query → generate answer
   - Real OpenAI API calls for embeddings and LLM
   - Validates the entire RAG flow works together
   - Marked with @pytest.mark.integration and only run when secret is available

Design: Tests use tmp_path fixtures to isolate state. No shared dependencies on
local chroma_db/ or openshift-docs/. Each test creates minimal fixtures inline.
"""

import pytest

from api.routes import create_app


@pytest.fixture
def client(tmp_path):
    """Create a Flask test client with minimal preprocessed docs.

    Args:
        tmp_path: pytest fixture providing a temporary directory

    Returns:
        Flask test client ready for making requests

    Example:
        >>> def test_example(client):
        ...     response = client.get('/healthz')
        ...     assert response.status_code == 200
    """
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    (processed_dir / "install-ocp.md").write_text(
        "# Installing OpenShift\n"
        "Install OpenShift Container Platform with 3 control plane nodes."
    )
    (processed_dir / "upgrade-cluster.md").write_text(
        "# Upgrading OpenShift\n"
        "Run oc adm upgrade to upgrade your cluster."
    )
    docs_root = tmp_path / "openshift-docs"
    (docs_root / "modules").mkdir(parents=True)
    app = create_app(docs_root=docs_root, processed_dir=processed_dir)
    app.config["TESTING"] = True
    return app.test_client()


class TestHealthz:
    """Health check endpoint — used by K8s readiness probes.

    The /healthz endpoint is the first thing clients call to verify the app is alive.
    K8s will repeatedly probe this endpoint and remove the pod from service if it fails.
    """

    def test_returns_ok_status(self, client):
        """Verify /healthz returns 200 with status: ok.

        Example:
            GET /healthz
            → {"status": "ok"}
        """
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.get_json()["status"] == "ok"

    def test_content_type_is_json(self, client):
        """Verify response is JSON, not HTML or plain text.

        Example:
            GET /healthz
            → Content-Type: application/json
        """
        r = client.get("/healthz")
        assert "application/json" in r.content_type


class TestListFiles:
    """File listing endpoint — used by web UI to populate document dropdown.

    /api/files returns metadata for all preprocessed markdown files in data/processed/.
    Each file corresponds to an AsciiDoc module from the OpenShift docs.
    """

    def test_returns_list_of_processed_files(self, client):
        """Verify /api/files returns a JSON list of file objects.

        Example:
            GET /api/files
            → [
                {"id": "install-ocp", "filename": "install-ocp.adoc", ...},
                {"id": "upgrade-cluster", "filename": "upgrade-cluster.adoc", ...}
              ]
        """
        r = client.get("/api/files")
        assert r.status_code == 200
        files = r.get_json()
        assert isinstance(files, list)
        assert len(files) == 2

    def test_file_ids_match_stems(self, client):
        """Verify file IDs match the markdown file stems (no .adoc extension).

        Example:
            File: data/processed/install-ocp.md
            → id: "install-ocp"
        """
        r = client.get("/api/files")
        stems = {f["id"] for f in r.get_json()}
        assert stems == {"install-ocp", "upgrade-cluster"}

    def test_each_file_has_required_fields(self, client):
        """Verify each file object has all required metadata fields.

        Example:
            {
              "id": "install-ocp",
              "filename": "install-ocp.adoc",
              "content_type": "PROCEDURE",
              "topic": "installing",
              "source_dir": "installing"
            }
        """
        r = client.get("/api/files")
        for f in r.get_json():
            assert "id" in f
            assert "filename" in f
            assert "content_type" in f
            assert f["filename"].endswith(".adoc")

    def test_empty_processed_dir_returns_empty_list(self, tmp_path):
        """Gracefully handle missing or empty processed directory.

        Example:
            processed_dir = /nonexistent/path
            GET /api/files
            → []
        """
        docs_root = tmp_path / "openshift-docs"
        (docs_root / "modules").mkdir(parents=True)
        app = create_app(docs_root=docs_root, processed_dir=tmp_path / "empty")
        app.config["TESTING"] = True
        r = app.test_client().get("/api/files")
        assert r.get_json() == []


class TestQuery:
    """Question-answering endpoint — the core RAG API.

    /api/query accepts a question and returns an answer grounded in documentation
    using the full 5-stage pipeline: rewrite → retrieve → rerank → generate → ground.
    """

    def test_missing_question_returns_validation_error(self, client):
        """Reject requests with missing 'question' field.

        Example:
            POST /api/query
            Body: {} (no question)
            → {"error": "question is required", "answer": null, "sources": []}
        """
        r = client.post("/api/query", json={})
        assert r.status_code == 200
        body = r.get_json()
        assert body["error"] is not None
        assert body["answer"] is None
        assert body["sources"] == []

    def test_empty_question_returns_validation_error(self, client):
        """Reject whitespace-only questions.

        Example:
            POST /api/query
            Body: {"question": "   "}
            → {"error": "question is required", ...}
        """
        r = client.post("/api/query", json={"question": "   "})
        body = r.get_json()
        assert body["error"] is not None

    def test_no_api_key_returns_error(self, client, monkeypatch):
        """Fail gracefully when OPENAI_API_KEY is not set.

        Example:
            OPENAI_API_KEY=unset
            POST /api/query
            Body: {"question": "How do I install OpenShift?"}
            → {"error": "OPENAI_API_KEY not set — add it to .env", ...}
        """
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        r = client.post("/api/query", json={"question": "How do I install OpenShift?"})
        body = r.get_json()
        assert body["error"] is not None
        assert "OPENAI_API_KEY" in body["error"]

    @pytest.mark.integration
    def test_full_pipeline_returns_grounded_answer(self, tmp_path):
        """End-to-end RAG pipeline test with real OpenAI embeddings and LLM.

        This integration test validates that the complete pipeline works together:
        1. Create realistic OpenShift documentation (install, upgrade, network)
        2. Embed each doc using real OpenAI text-embedding-3-small
        3. Store in in-memory Qdrant (no local chroma_db needed)
        4. Run run_pipeline() with a natural question
        5. Assert the LLM returns a meaningful answer + document sources

        Example:
            Question: "How many nodes do I need to install OpenShift?"
            Context: 3 docs about install, upgrade, network
            Expected: Answer mentions "3 control plane nodes" + 2+ sources

        Requires OPENAI_API_KEY environment variable (set in GitHub Actions secrets).
        Takes ~30-60s due to API latency. Only runs when marked integration.
        """
        import uuid

        from langchain_openai import OpenAIEmbeddings
        from langchain_qdrant import QdrantVectorStore
        from openai import OpenAI
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, PointStruct, VectorParams

        from services.pipeline import run_pipeline

        COLLECTION = "test_openshift"
        VECTOR_SIZE = 1536
        EMBED_MODEL = "text-embedding-3-small"

        # Realistic OpenShift docs matching the kind of questions the app answers
        docs = [
            {
                "stem": "install-requirements",
                "text": (
                    "Installing OpenShift Container Platform requires 3 control plane nodes "
                    "and 2 worker nodes. Each control plane node needs 4 vCPUs and 16 GB RAM."
                ),
                "title": "Installation Requirements",
            },
            {
                "stem": "upgrade-procedure",
                "text": (
                    "To upgrade OpenShift, run: oc adm upgrade --to-latest. "
                    "This initiates a rolling upgrade across all cluster operators."
                ),
                "title": "Upgrade Procedure",
            },
            {
                "stem": "network-policy",
                "text": (
                    "NetworkPolicy resources control traffic between pods. "
                    "Apply them with: oc apply -f networkpolicy.yaml"
                ),
                "title": "Network Policy Configuration",
            },
        ]

        # Embed with real OpenAI
        oai = OpenAI()
        texts = [d["text"] for d in docs]
        response = oai.embeddings.create(input=texts, model=EMBED_MODEL)
        embeddings = [e.embedding for e in response.data]

        # Upsert into in-memory Qdrant (no server needed)
        qdrant = QdrantClient(":memory:")
        qdrant.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        points = [
            PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, d["stem"])),
                vector=emb,
                payload={
                    "page_content": d["text"],
                    "file": d["stem"] + ".adoc",
                    "title": d["title"],
                    "content_type": "PROCEDURE",
                    "topic": "installing",
                    "source_dir": "installing",
                    "source_dirs_all": "installing",
                },
            )
            for d, emb in zip(docs, embeddings)
        ]
        qdrant.upsert(COLLECTION, points=points)

        vs = QdrantVectorStore(
            client=qdrant,
            collection_name=COLLECTION,
            embedding=OpenAIEmbeddings(model=EMBED_MODEL),
        )

        result = run_pipeline(
            question="How many nodes do I need to install OpenShift?",
            vectorstore=vs,
            bm25=None,
            model="gpt-4o-mini",
            n_results=3,
            rewrite=False,
            hybrid=False,
            do_rerank=False,
        )

        assert result.answer, "Pipeline returned empty answer"
        assert len(result.answer) > 20, "Answer too short to be meaningful"
        assert result.sources, "No sources returned by pipeline"
        assert result.model == "gpt-4o-mini"
        # The answer should reference node counts from the context
        assert any(
            word in result.answer.lower()
            for word in ["node", "control", "worker", "3", "three"]
        ), f"Answer doesn't reference node info: {result.answer}"
