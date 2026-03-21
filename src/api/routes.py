"""Flask backend for the AsciiDoc vs Markdown comparison viewer."""
import json
import logging
import os
import queue
import threading
from pathlib import Path

from dotenv import load_dotenv
from flask import Blueprint, Flask, Response, jsonify, render_template, request, stream_with_context

from retrieval import discover, meta_extract
from core.config import DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION, DEFAULT_PROCESSED_DIR

load_dotenv()

logger = logging.getLogger(__name__)

_docs_root: Path | None = None
_processed_dir: Path | None = None
_module_map: dict = {}

# Lazy-initialised QA state
_qa_vectorstore = None
_bm25 = None
_bm25_loaded = False


def create_app(docs_root: Path, processed_dir: Path) -> Flask:
    global _docs_root, _processed_dir, _module_map

    _docs_root = docs_root
    _processed_dir = processed_dir

    print("Loading module index...", end=" ", flush=True)
    try:
        modules = discover.discover(docs_root)
        _module_map = {m.filename: m for m in modules}
        print(f"{len(_module_map)} modules indexed.")
    except Exception as e:
        print(f"WARNING: discover failed: {e}")
        _module_map = {}

    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(_bp)
    return app


_bp = Blueprint("viewer", __name__)


@_bp.route("/")
def index():
    return render_template("index.html")


@_bp.route("/api/files")
def list_files():
    if not _processed_dir or not _processed_dir.exists():
        return jsonify([])

    files = []
    for md_path in sorted(_processed_dir.glob("*.md")):
        stem = md_path.stem
        filename = stem + ".adoc"
        mod = _module_map.get(filename)
        files.append({
            "id": stem,
            "filename": filename,
            "content_type": mod.content_type if mod else "UNKNOWN",
            "topic": mod.topic if mod else "",
            "source_dir": mod.source_dirs[0] if mod and mod.source_dirs else "",
        })
    return jsonify(files)


@_bp.route("/api/file/<path:stem>")
def get_file(stem: str):
    filename = stem + ".adoc"
    md_path = _processed_dir / (stem + ".md")
    adoc_path = _docs_root / "modules" / filename

    md_content = _read(md_path)
    adoc_content = _read(adoc_path)

    mod = _module_map.get(filename)
    metadata: dict = {}

    if mod:
        if md_content:
            metadata = meta_extract.extract(md_content, mod)
        metadata["file"] = mod.filename
        metadata["content_type"] = mod.content_type
        metadata["title"] = _extract_title(md_content)
        metadata["topic"] = mod.topic
        metadata["source_dirs_all"] = ", ".join(mod.source_dirs)

    return jsonify({
        "adoc": adoc_content,
        "md": md_content,
        "metadata": metadata,
    })


@_bp.route("/api/query", methods=["POST"])
def query():
    global _qa_vectorstore, _bm25, _bm25_loaded

    body = request.get_json(force=True, silent=True) or {}
    question = (body.get("question") or "").strip()
    if not question:
        return jsonify({"error": "question is required", "answer": None, "sources": [],
                        "model": None, "rewritten_query": "", "is_grounded": True})

    n_results = int(body.get("n_results", 5))
    filter_topic = body.get("filter_topic") or None
    filter_type = body.get("filter_type") or None
    model = body.get("model") or "gpt-4o-mini"

    do_rewrite = body.get("rewrite", True)
    do_hybrid = body.get("hybrid", True)
    do_rerank = body.get("rerank", True)
    do_ground = body.get("ground", False)

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY not set — add it to .env", "answer": None,
                        "sources": [], "model": model, "rewritten_query": "", "is_grounded": True})

    try:
        from services.pipeline import build_vectorstore, run_pipeline

        # Lazy-init vectorstore
        if _qa_vectorstore is None:
            _qa_vectorstore = build_vectorstore(DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION)

        count = _qa_vectorstore._collection.count()
        if count == 0:
            return jsonify({"error": "ChromaDB is empty — run: python -m retrieval --verbose",
                            "answer": None, "sources": [], "model": model,
                            "rewritten_query": "", "is_grounded": True})

        # Lazy-init BM25 index
        if not _bm25_loaded and do_hybrid:
            from retrieval.hybrid import BM25Index
            pdir = DEFAULT_PROCESSED_DIR
            if pdir.exists():
                _bm25 = BM25Index(pdir)
            _bm25_loaded = True

        result = run_pipeline(
            question=question,
            vectorstore=_qa_vectorstore,
            bm25=_bm25 if do_hybrid else None,
            model=model,
            n_results=n_results,
            filter_topic=filter_topic,
            filter_content_type=filter_type,
            rewrite=do_rewrite,
            hybrid=do_hybrid and _bm25 is not None,
            do_rerank=do_rerank,
            ground=do_ground,
        )

        return jsonify({
            "answer": result.answer,
            "sources": result.sources,
            "model": result.model,
            "rewritten_query": result.rewritten_query,
            "is_grounded": result.is_grounded,
            "error": None,
        })
    except Exception as e:
        logger.exception("QA pipeline error")
        return jsonify({"error": str(e), "answer": None, "sources": [], "model": model,
                        "rewritten_query": "", "is_grounded": True})


@_bp.route("/api/eval", methods=["POST"])
def eval_run():
    global _qa_vectorstore, _bm25, _bm25_loaded

    body = request.get_json(force=True, silent=True) or {}
    n_queries = min(max(int(body.get("n_queries", 10)), 1), 100)
    model = body.get("model", "gpt-4o-mini")
    k = min(max(int(body.get("k", 5)), 1), 20)

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY not set — add it to .env"}), 400

    queries_path = Path("data/ground_truth/queries.json")
    if not queries_path.exists():
        return jsonify({"error": f"Benchmark not found: {queries_path}. Run the ground-truth generator first."}), 400

    # Lazy-init in main thread before spawning worker (avoids cross-thread write races)
    try:
        from services.pipeline import build_vectorstore
        if _qa_vectorstore is None:
            _qa_vectorstore = build_vectorstore(DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION)
        if not _bm25_loaded:
            from retrieval.hybrid import BM25Index
            if DEFAULT_PROCESSED_DIR.exists():
                _bm25 = BM25Index(DEFAULT_PROCESSED_DIR)
            _bm25_loaded = True
    except Exception as exc:
        return jsonify({"error": f"Init failed: {exc}"}), 500

    # Capture references for the worker closure (read-only from here on)
    vs = _qa_vectorstore
    bm25 = _bm25
    result_q: queue.Queue = queue.Queue()

    def worker() -> None:
        import time as _time
        try:
            from langchain_openai import ChatOpenAI
            from eval.generation import eval_generation
            from eval.retrieval import eval_retrieval
            from services.pipeline import run_pipeline

            queries = json.loads(queries_path.read_text())[:n_queries]
            judge = ChatOpenAI(model=model, temperature=0)

            for i, q in enumerate(queries, 1):
                t0 = _time.monotonic()
                try:
                    result = run_pipeline(
                        question=q["query"],
                        vectorstore=vs,
                        bm25=bm25,
                        model=model,
                        n_results=k,
                        rewrite=True,
                        hybrid=bm25 is not None,
                        do_rerank=True,
                        ground=False,
                    )
                    gen = eval_generation(q["query"], result.answer, result.docs, judge)
                    ret = eval_retrieval(result.docs, q.get("gold_doc_ids", []))
                    elapsed_ms = round((_time.monotonic() - t0) * 1000)
                    result_q.put({
                        "type": "result",
                        "i": i, "n": len(queries),
                        "id": q["id"],
                        "query": q["query"],
                        "topic": q.get("topic", ""),
                        "gold_doc_ids": q.get("gold_doc_ids", []),
                        "rewritten_query": result.rewritten_query,
                        "answer": result.answer,
                        "sources": result.sources,
                        "pipeline_log": result.pipeline_log,
                        "answer_relevance": gen["answer_relevance"]["score"],
                        "faithfulness": gen["faithfulness"]["score"],
                        "context_relevance": gen["context_relevance"]["score"],
                        "ar_explanation": gen["answer_relevance"]["explanation"],
                        "faith_explanation": gen["faithfulness"]["explanation"],
                        "ctx_explanation": gen["context_relevance"]["explanation"],
                        "recall_5": ret.get("recall@5"),
                        "mrr": ret.get("mrr"),
                        "gold_found": ret.get("gold_found", []),
                        "gold_missed": ret.get("gold_missed", []),
                        "elapsed_ms": elapsed_ms,
                    })
                except Exception as qe:
                    result_q.put({
                        "type": "result",
                        "i": i, "n": len(queries),
                        "id": q.get("id", ""),
                        "query": q.get("query", ""),
                        "topic": q.get("topic", ""),
                        "gold_doc_ids": q.get("gold_doc_ids", []),
                        "rewritten_query": "",
                        "answer": None,
                        "sources": [],
                        "pipeline_log": {},
                        "answer_relevance": None, "faithfulness": None, "context_relevance": None,
                        "ar_explanation": str(qe), "faith_explanation": "", "ctx_explanation": "",
                        "recall_5": None, "mrr": None,
                        "gold_found": [], "gold_missed": [],
                        "elapsed_ms": round((_time.monotonic() - t0) * 1000),
                    })

            result_q.put({"type": "done"})
        except Exception as exc:
            result_q.put({"type": "error", "message": str(exc)})

    threading.Thread(target=worker, daemon=True).start()

    def generate():
        while True:
            item = result_q.get()
            yield f"data: {json.dumps(item)}\n\n"
            if item["type"] in ("done", "error"):
                break

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    except OSError:
        return ""


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""
