"""Flask backend for the AsciiDoc vs Markdown comparison viewer."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ingest import discover, meta_extract
from ingest.config import DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION, DEFAULT_PROCESSED_DIR

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

    app = Flask(__name__)
    app.register_blueprint(_bp)
    return app


from flask import Blueprint

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
        from qa.chain import build_vectorstore, run_pipeline

        # Lazy-init vectorstore
        if _qa_vectorstore is None:
            _qa_vectorstore = build_vectorstore(DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION)

        count = _qa_vectorstore._collection.count()
        if count == 0:
            return jsonify({"error": "ChromaDB is empty — run: python -m ingest --verbose",
                            "answer": None, "sources": [], "model": model,
                            "rewritten_query": "", "is_grounded": True})

        # Lazy-init BM25 index
        if not _bm25_loaded and do_hybrid:
            from qa.hybrid import BM25Index
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
