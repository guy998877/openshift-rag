"""Flask backend for the AsciiDoc vs Markdown comparison viewer."""
import datetime
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

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    collected: list[dict] = []

    threading.Thread(target=worker, daemon=True).start()

    def generate():
        while True:
            item = result_q.get()
            yield f"data: {json.dumps(item)}\n\n"
            if item["type"] == "result":
                collected.append(item)
            elif item["type"] == "done":
                if collected:
                    run_id = _save_ui_eval_run(
                        collected,
                        {"n_queries": n_queries, "model": model, "k_retrieve": k},
                        timestamp,
                    )
                    if run_id:
                        yield f"data: {json.dumps({'type': 'saved', 'run_id': run_id})}\n\n"
                break
            elif item["type"] == "error":
                break

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _save_ui_eval_run(results: list[dict], config: dict, timestamp: str) -> str | None:
    """Persist a UI eval run to data/eval_results/<id>/run.json. Returns run_id or None."""
    try:
        results_dir = Path("data/eval_results")
        results_dir.mkdir(parents=True, exist_ok=True)

        def _avg(key: str) -> float | None:
            vals = [r[key] for r in results if r.get(key) is not None]
            return round(sum(vals) / len(vals), 4) if vals else None

        aggregate = {
            "answer_relevance":  _avg("answer_relevance"),
            "faithfulness":      _avg("faithfulness"),
            "context_relevance": _avg("context_relevance"),
            "recall@5":          _avg("recall_5"),
            "mrr":               _avg("mrr"),
        }

        slug = timestamp[:16].replace(":", "-")
        run_id = f"{slug}_gen_k{config.get('k_retrieve', 5)}"
        run_dir = results_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        run_data = {
            "type": "generation",
            "source": "ui",
            "timestamp": timestamp,
            "config": config,
            "aggregate": aggregate,
            "results": results,
        }
        (run_dir / "run.json").write_text(json.dumps(run_data, indent=2))
        logger.info("Saved eval run → %s/run.json", run_dir)
        return run_id
    except Exception as exc:
        logger.warning("Failed to save eval run: %s", exc)
        return None


@_bp.route("/api/eval/runs", methods=["GET"])
def list_eval_runs():
    """List all saved evaluation runs (UI and CLI) that have a run.json."""
    results_dir = Path("data/eval_results")
    if not results_dir.exists():
        return jsonify([])

    runs = []
    for d in sorted(results_dir.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        rj = d / "run.json"
        if not rj.exists():
            continue
        try:
            data = json.loads(rj.read_text())
            runs.append({
                "id":        d.name,
                "source":    data.get("source", "unknown"),
                "timestamp": data.get("timestamp", ""),
                "config":    data.get("config", {}),
                "aggregate": data.get("aggregate", {}),
                "n_results": len(data.get("results", [])),
            })
        except Exception:
            pass

    return jsonify(runs)


@_bp.route("/api/eval/runs/<path:run_id>", methods=["GET"])
def get_eval_run(run_id: str):
    """Return the full run.json for a single saved run."""
    # Guard against path traversal
    safe_id = Path(run_id).name
    rj = Path("data/eval_results") / safe_id / "run.json"
    if not rj.exists():
        return jsonify({"error": f"Run '{safe_id}' not found or has no run.json"}), 404
    try:
        return jsonify(json.loads(rj.read_text()))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@_bp.route("/api/experiment", methods=["POST"])
def run_experiment():
    """Run two pipeline configurations on the same queries and stream a comparison."""
    global _qa_vectorstore, _bm25, _bm25_loaded

    body = request.get_json(force=True, silent=True) or {}
    n_queries   = min(max(int(body.get("n_queries", 10)), 1), 100)
    control_cfg = body.get("control", {})
    exp_cfg     = body.get("experiment", {})

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY not set — add it to .env"}), 400

    queries_path = Path("data/ground_truth/queries.json")
    if not queries_path.exists():
        return jsonify({"error": "Benchmark not found. Run the ground-truth generator first."}), 400

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

    vs        = _qa_vectorstore
    bm25_idx  = _bm25
    result_q: queue.Queue = queue.Queue()
    queries   = json.loads(queries_path.read_text())[:n_queries]
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    def run_arm(arm: str, cfg: dict) -> None:
        import time as _time
        try:
            from langchain_openai import ChatOpenAI
            from eval.generation import eval_generation
            from eval.retrieval import eval_retrieval
            from services.pipeline import run_pipeline

            model      = cfg.get("model", "gpt-4o-mini")
            k_final    = min(max(int(cfg.get("k_final", 5)), 1), 20)
            mode       = cfg.get("mode", "hybrid")
            do_rerank  = bool(cfg.get("rerank", True))
            do_rewrite = bool(cfg.get("rewrite", True))

            use_bm25   = bm25_idx is not None and mode in ("hybrid",)
            judge      = ChatOpenAI(model=model, temperature=0)

            for i, q in enumerate(queries, 1):
                t0 = _time.monotonic()
                try:
                    result = run_pipeline(
                        question=q["query"],
                        vectorstore=vs,
                        bm25=bm25_idx if use_bm25 else None,
                        model=model,
                        n_results=k_final,
                        rewrite=do_rewrite,
                        hybrid=use_bm25,
                        do_rerank=do_rerank,
                        ground=False,
                    )
                    gen = eval_generation(q["query"], result.answer, result.docs, judge)
                    ret = eval_retrieval(result.docs, q.get("gold_doc_ids", []))
                    elapsed_ms = round((_time.monotonic() - t0) * 1000)
                    result_q.put({
                        "type": "result", "arm": arm,
                        "i": i, "n": len(queries),
                        "id": q["id"], "query": q["query"], "topic": q.get("topic", ""),
                        "gold_doc_ids": q.get("gold_doc_ids", []),
                        "rewritten_query": result.rewritten_query,
                        "answer": result.answer,
                        "sources": result.sources,
                        "pipeline_log": result.pipeline_log,
                        "answer_relevance": gen["answer_relevance"]["score"],
                        "faithfulness":     gen["faithfulness"]["score"],
                        "context_relevance":gen["context_relevance"]["score"],
                        "ar_explanation":   gen["answer_relevance"]["explanation"],
                        "faith_explanation":gen["faithfulness"]["explanation"],
                        "ctx_explanation":  gen["context_relevance"]["explanation"],
                        "recall_5": ret.get("recall@5"),
                        "mrr":      ret.get("mrr"),
                        "gold_found":  ret.get("gold_found", []),
                        "gold_missed": ret.get("gold_missed", []),
                        "elapsed_ms": elapsed_ms,
                    })
                except Exception as qe:
                    result_q.put({
                        "type": "result", "arm": arm,
                        "i": i, "n": len(queries),
                        "id": q.get("id",""), "query": q.get("query",""), "topic": q.get("topic",""),
                        "gold_doc_ids": [], "rewritten_query": "",
                        "answer": None, "sources": [], "pipeline_log": {},
                        "answer_relevance": None, "faithfulness": None, "context_relevance": None,
                        "ar_explanation": str(qe), "faith_explanation": "", "ctx_explanation": "",
                        "recall_5": None, "mrr": None, "gold_found": [], "gold_missed": [],
                        "elapsed_ms": round((_time.monotonic() - t0) * 1000),
                    })
            result_q.put({"type": "arm_done", "arm": arm})
        except Exception as exc:
            result_q.put({"type": "error", "arm": arm, "message": str(exc)})

    def sequential_worker() -> None:
        run_arm("control", control_cfg)
        run_arm("experiment", exp_cfg)
        result_q.put({"type": "done"})

    threading.Thread(target=sequential_worker, daemon=True).start()

    def generate():
        arm_results: dict[str, list] = {"control": [], "experiment": []}
        while True:
            item = result_q.get()
            yield f"data: {json.dumps(item)}\n\n"
            if item["type"] == "result":
                arm_results[item["arm"]].append(item)
            elif item["type"] == "done":
                comparison = _compute_exp_comparison(arm_results)
                yield f"data: {json.dumps({'type': 'comparison', 'data': comparison})}\n\n"
                _save_experiment_run(arm_results, comparison, control_cfg, exp_cfg, n_queries, timestamp)
                break
            elif item["type"] == "error":
                break

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _compute_exp_comparison(arm_results: dict) -> dict:
    def _avg(results: list, key: str) -> float | None:
        vals = [r[key] for r in results if r.get(key) is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    ctrl = arm_results.get("control", [])
    exp  = arm_results.get("experiment", [])
    keys = ["answer_relevance", "faithfulness", "context_relevance", "recall_5", "mrr", "elapsed_ms"]

    ctrl_agg = {k: _avg(ctrl, k) for k in keys}
    exp_agg  = {k: _avg(exp,  k) for k in keys}
    deltas   = {
        k: round(exp_agg[k] - ctrl_agg[k], 4)
        if ctrl_agg[k] is not None and exp_agg[k] is not None else None
        for k in keys
    }
    quality_keys = ["answer_relevance", "faithfulness", "context_relevance", "recall_5", "mrr"]
    improvements = sum(1 for k in quality_keys if (deltas.get(k) or 0) > 0.01)
    regressions  = sum(1 for k in quality_keys if (deltas.get(k) or 0) < -0.01)
    return {
        "control": ctrl_agg, "experiment": exp_agg, "deltas": deltas,
        "summary": {"improvements": improvements, "regressions": regressions},
    }


def _save_experiment_run(
    arm_results: dict, comparison: dict,
    control_cfg: dict, exp_cfg: dict,
    n_queries: int, timestamp: str,
) -> None:
    try:
        results_dir = Path("data/eval_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        slug   = timestamp[:16].replace(":", "-")
        run_id = f"{slug}_experiment"
        run_dir = results_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        run_data = {
            "type": "experiment", "source": "ui", "timestamp": timestamp,
            "n_queries": n_queries,
            "control_config": control_cfg,
            "experiment_config": exp_cfg,
            "comparison": comparison,
            "control_results": arm_results.get("control", []),
            "experiment_results": arm_results.get("experiment", []),
        }
        (run_dir / "run.json").write_text(json.dumps(run_data, indent=2))
        logger.info("Saved experiment → %s/run.json", run_dir)
    except Exception as exc:
        logger.warning("Failed to save experiment: %s", exc)


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
