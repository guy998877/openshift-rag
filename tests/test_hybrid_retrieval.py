"""Tests for BM25 index and hybrid retrieval scoring.

BM25 (Best Matching 25) is a probabilistic keyword search algorithm used in the RAG pipeline.
These tests verify that keyword-based retrieval correctly ranks relevant documents.

Key points:
- BM25 scores keywords in the query against document text
- Used alongside vector search for hybrid retrieval (Reciprocal Rank Fusion)
- No API calls — all tests use temporary markdown files
- Fast and deterministic — same query always returns same ranking

Test categories:
1. Ranking accuracy — topic-specific queries rank correct documents first
2. Score normalization — BM25 scores are [0, 1] range
3. Edge cases — empty queries, k limits, missing docs
"""

import pytest

from retrieval.hybrid import BM25Index


@pytest.fixture
def index_dir(tmp_path):
    """Create 5 realistic OpenShift markdown docs covering distinct topics.

    This fixture simulates the data/processed/ directory with preprocessed
    documentation. Each doc has realistic OpenShift content on a different topic.

    Topics:
        - install-requirements: node count, CPU/RAM specs
        - upgrade-cluster: oc adm upgrade command
        - network-policy: NetworkPolicy Kubernetes resource
        - storage-pvc: PersistentVolumeClaim configuration
        - rbac-roles: ClusterRole and RoleBinding for access control

    Returns:
        Path to temp directory containing all 5 .md files
    """
    docs = {
        "install-requirements": (
            "# Installation Requirements\n"
            "Installing OpenShift Container Platform requires 3 control plane nodes "
            "and 2 worker nodes with specific CPU and RAM configuration."
        ),
        "upgrade-cluster": (
            "# Upgrade Procedure\n"
            "To upgrade your OpenShift cluster run oc adm upgrade. "
            "The cluster operators perform a rolling upgrade across all nodes."
        ),
        "network-policy": (
            "# Network Policy Configuration\n"
            "Configure NetworkPolicy resources to restrict traffic between pods "
            "and namespaces in your OpenShift cluster."
        ),
        "storage-pvc": (
            "# Persistent Storage\n"
            "Create PersistentVolumeClaims to provision storage for stateful "
            "workloads running on OpenShift Container Platform."
        ),
        "rbac-roles": (
            "# RBAC Configuration\n"
            "Define ClusterRoles and RoleBindings to control access to OpenShift "
            "API resources and enforce least-privilege permissions."
        ),
    }
    for stem, text in docs.items():
        (tmp_path / f"{stem}.md").write_text(text)
    return tmp_path


class TestBM25IndexSearch:
    """Verify BM25 ranking — topic-specific queries should rank relevant docs first.

    BM25 is a probabilistic keyword search algorithm. It scores documents based on
    how many query keywords appear in each document, with penalties for term frequency.
    More specific queries should rank more relevant documents higher.
    """

    def test_installation_query_ranks_install_doc_first(self, index_dir):
        """Installation-related query should rank install-requirements doc highest.

        Example:
            Query: "install OpenShift nodes requirements"
            Corpus: [install-requirements, upgrade-cluster, network-policy, ...]
            Expected: install-requirements ranks 1st
        """
        index = BM25Index(index_dir)
        results = index.search("install OpenShift nodes requirements", k=5)
        assert results, "Expected non-empty results"
        assert results[0][0] == "install-requirements"

    def test_upgrade_query_ranks_upgrade_doc_first(self, index_dir):
        """Upgrade-related query should rank upgrade-cluster doc highest.

        Example:
            Query: "upgrade cluster oc adm rolling"
            Expected: upgrade-cluster ranks 1st
        """
        index = BM25Index(index_dir)
        results = index.search("upgrade cluster oc adm rolling", k=5)
        assert results[0][0] == "upgrade-cluster"

    def test_network_query_ranks_network_doc_first(self, index_dir):
        """Network-related query should rank network-policy doc highest.

        Example:
            Query: "NetworkPolicy restrict pod traffic namespaces"
            Expected: network-policy ranks 1st
        """
        index = BM25Index(index_dir)
        results = index.search("NetworkPolicy restrict pod traffic namespaces", k=5)
        assert results[0][0] == "network-policy"

    def test_storage_query_ranks_storage_doc_first(self, index_dir):
        """Storage-related query should rank storage-pvc doc highest.

        Example:
            Query: "PersistentVolumeClaim storage stateful workload"
            Expected: storage-pvc ranks 1st
        """
        index = BM25Index(index_dir)
        results = index.search("PersistentVolumeClaim storage stateful workload", k=5)
        assert results[0][0] == "storage-pvc"

    def test_rbac_query_ranks_rbac_doc_first(self, index_dir):
        """RBAC-related query should rank rbac-roles doc highest.

        Example:
            Query: "ClusterRole RoleBinding RBAC permissions"
            Expected: rbac-roles ranks 1st
        """
        index = BM25Index(index_dir)
        results = index.search("ClusterRole RoleBinding RBAC permissions", k=5)
        assert results[0][0] == "rbac-roles"


class TestBM25IndexScoring:
    """Verify BM25 scoring is correct — normalized to [0, 1] and sorted descending.

    BM25 scores must be normalized and sorted consistently so hybrid retrieval
    (combining with vector search) can use Reciprocal Rank Fusion fairly.
    """

    def test_scores_normalised_between_zero_and_one(self, index_dir):
        """All BM25 scores must be in [0.0, 1.0] range.

        Normalization ensures BM25 scores can be fairly combined with vector
        similarity scores (which are also [0, 1]) using Reciprocal Rank Fusion.

        Example:
            Raw BM25 scores: [15.2, 8.5, 3.1]
            Normalized: [1.0, 0.559, 0.204]
        """
        index = BM25Index(index_dir)
        results = index.search("OpenShift cluster", k=5)
        for _, score in results:
            assert 0.0 <= score <= 1.0, f"Score {score} out of [0, 1]"

    def test_top_score_is_one(self, index_dir):
        """The highest-ranked document should have a score of 1.0 (normalized).

        Example:
            Results: [("install-requirements", 1.0), ("storage-pvc", 0.45), ...]
        """
        index = BM25Index(index_dir)
        results = index.search("install OpenShift nodes control plane", k=5)
        assert results[0][1] == pytest.approx(1.0)

    def test_scores_are_descending(self, index_dir):
        """Results must be sorted in descending order by score.

        Example:
            Scores: [1.0, 0.85, 0.72, 0.15] ✓
            Scores: [1.0, 0.15, 0.72, 0.85] ✗
        """
        index = BM25Index(index_dir)
        results = index.search("OpenShift nodes upgrade cluster", k=5)
        scores = [s for _, s in results]
        assert scores == sorted(scores, reverse=True), "Scores not in descending order"

    def test_k_parameter_limits_number_of_results(self, index_dir):
        """The k parameter correctly limits results returned.

        Example:
            search("OpenShift", k=2) → returns 2 results max
            search("OpenShift", k=5) → returns 5 results max
        """
        index = BM25Index(index_dir)
        assert len(index.search("OpenShift", k=1)) == 1
        assert len(index.search("OpenShift", k=2)) == 2
        assert len(index.search("OpenShift", k=5)) == 5

    def test_k_larger_than_corpus_returns_all_docs(self, index_dir):
        """When k exceeds corpus size, return all available documents.

        Example:
            Corpus: 5 docs
            search("OpenShift", k=100) → returns all 5 docs
        """
        index = BM25Index(index_dir)
        results = index.search("OpenShift", k=100)
        assert len(results) == 5  # only 5 docs in fixture


class TestBM25IndexEdgeCases:
    """Test error handling and robustness of BM25Index.

    Ensures the BM25 implementation handles missing data, irrelevant queries,
    and malformed input gracefully without crashing.
    """

    def test_empty_processed_dir_returns_empty_list(self, tmp_path):
        """BM25 gracefully handles empty document corpus.

        Example:
            processed_dir = /empty/path (no .md files)
            search("anything", k=5) → []
        """
        index = BM25Index(tmp_path)
        assert index.search("anything") == []

    def test_unrelated_query_still_returns_list(self, index_dir):
        """BM25 returns a list even for completely off-topic queries.

        BM25 doesn't reject queries — it ranks all docs, even with zero score.
        This ensures the pipeline never crashes on unexpected user input.

        Example:
            Query: "banana mango tropical fruit" (not in OpenShift docs)
            Result: Still returns list of (stem, score) tuples
                    Scores may be very low (e.g., 0.0) but structure is valid
        """
        index = BM25Index(index_dir)
        results = index.search("banana mango tropical fruit", k=3)
        assert isinstance(results, list)

    def test_result_is_list_of_stem_score_tuples(self, index_dir):
        """Verify return type is always list of (stem: str, score: float) tuples.

        Example:
            search("OpenShift", k=3)
            → [
                ("install-requirements", 1.0),
                ("storage-pvc", 0.45),
                ("upgrade-cluster", 0.32)
              ]
        """
        index = BM25Index(index_dir)
        results = index.search("OpenShift", k=3)
        for item in results:
            assert len(item) == 2
            stem, score = item
            assert isinstance(stem, str)
            assert isinstance(score, float)
