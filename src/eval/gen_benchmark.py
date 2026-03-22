"""Generation benchmark runner — full RAG pipeline + LLM-as-judge evaluation."""
from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from core.config import DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION, DEFAULT_PROCESSED_DIR


# ── Output helpers ─────────────────────────────────────────────────────────────

def _run_dir(output_dir: Path, k: int, timestamp: str) -> Path:
    slug = timestamp[:16].replace(":", "-")
    name = f"{slug}_gen_k{k}"
    run_dir = output_dir / name
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _save_run(run_dir: Path, report: dict) -> None:
    # metrics.json — aggregate + per-query (no full answer text)
    metrics_report = {k: v for k, v in report.items() if k != "results"}
    metrics_report["results"] = [
        {
            "id": r["id"],
            "query": r["query"],
            "topic": r["topic"],
            "elapsed_ms": r["elapsed_ms"],
            "retrieval_metrics": {
                k: v for k, v in r["retrieval_metrics"].items()
                if k != "retrieved_stems"
            },
            "generation_metrics": r["generation_metrics"],
        }
        for r in report["results"]
    ]
    (run_dir / "metrics.json").write_text(json.dumps(metrics_report, indent=2))

    # predictions.jsonl — one line per query with full answer + scores
    with (run_dir / "predictions.jsonl").open("w") as f:
        for r in report["results"]:
            line = {
                "id": r["id"],
                "query": r["query"],
                "topic": r["topic"],
                "rewritten_query": r.get("rewritten_query", ""),
                "answer": r["answer"],
                "retrieved_stems": r["retrieval_metrics"].get("retrieved_stems", []),
                "recall@5": r["retrieval_metrics"].get("recall@5"),
                "mrr": r["retrieval_metrics"].get("mrr"),
                "answer_relevance": r["generation_metrics"].get("answer_relevance", {}).get("score"),
                "faithfulness": r["generation_metrics"].get("faithfulness", {}).get("score"),
                "context_relevance": r["generation_metrics"].get("context_relevance", {}).get("score"),
                "avg_gen": r["generation_metrics"].get("avg"),
                "elapsed_ms": r["elapsed_ms"],
            }
            f.write(json.dumps(line) + "\n")

    # run.json — full data loadable by the UI history feature
    n = report["config"]["n_queries"]
    flat_results = []
    for r in report["results"]:
        gm = r["generation_metrics"]
        rm = r["retrieval_metrics"]
        flat_results.append({
            "i": r.get("i", 0),
            "n": n,
            "id": r["id"],
            "query": r["query"],
            "topic": r["topic"],
            "gold_doc_ids": r.get("gold_doc_ids", []),
            "rewritten_query": r.get("rewritten_query", ""),
            "answer": r.get("answer", ""),
            "sources": r.get("sources", []),
            "pipeline_log": r.get("pipeline_log", {}),
            "answer_relevance": gm.get("answer_relevance", {}).get("score"),
            "faithfulness":     gm.get("faithfulness",     {}).get("score"),
            "context_relevance":gm.get("context_relevance",{}).get("score"),
            "ar_explanation":   gm.get("answer_relevance", {}).get("explanation", ""),
            "faith_explanation":gm.get("faithfulness",     {}).get("explanation", ""),
            "ctx_explanation":  gm.get("context_relevance",{}).get("explanation", ""),
            "recall_5":   rm.get("recall@5"),
            "mrr":        rm.get("mrr"),
            "gold_found": rm.get("gold_found", []),
            "gold_missed":rm.get("gold_missed", []),
            "elapsed_ms": r["elapsed_ms"],
        })
    run_json = {
        "type": "generation",
        "source": "cli",
        "timestamp": report["timestamp"],
        "config": report["config"],
        "aggregate": report["aggregate"],
        "results": flat_results,
        "total_seconds": report.get("total_seconds"),
    }
    (run_dir / "run.json").write_text(json.dumps(run_json, indent=2))

    print(f"  metrics.json      → {run_dir / 'metrics.json'}")
    print(f"  predictions.jsonl → {run_dir / 'predictions.jsonl'}")
    print(f"  run.json          → {run_dir / 'run.json'}")


# ── Generation benchmark ───────────────────────────────────────────────────────

def run_generation_benchmark(
    queries_path: Path,
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection: str = DEFAULT_COLLECTION,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    k_retrieve: int = 5,
    mode: str = "hybrid",
    use_rerank: bool = True,
    n_queries: int | None = None,
    output_dir: Path | None = None,
    model: str = "gpt-4o-mini",
) -> dict:
    """Evaluate end-to-end RAG quality using LLM-as-judge.

    Runs the full pipeline (rewrite → retrieve → rerank → generate) for each
    query and scores the output on three reference-free metrics:
      answer_relevance  — does the answer address the question?
      faithfulness      — are all claims supported by the retrieved context?
      context_relevance — what fraction of retrieved docs are relevant?

    Also records retrieval metrics (recall@k, MRR) for a combined view.
    """
    from langchain_openai import ChatOpenAI

    from eval.generation import eval_generation
    from eval.retrieval import eval_retrieval
    from services.pipeline import build_vectorstore, run_pipeline
    from retrieval.hybrid import BM25Index

    queries = json.loads(queries_path.read_text())
    if n_queries is not None:
        queries = queries[:n_queries]

    print("Loading vectorstore...", end=" ", flush=True)
    vs = build_vectorstore(chroma_dir, collection)
    print(f"{vs._collection.count()} docs")

    bm25 = None
    if mode in ("hybrid", "keyword") and processed_dir.exists():
        print("Building BM25 index...", end=" ", flush=True)
        bm25 = BM25Index(processed_dir)
        print(f"{len(bm25._stems)} docs")

    judge_llm = ChatOpenAI(model=model, temperature=0)

    results = []
    t_total = time.monotonic()
    timestamp = datetime.utcnow().isoformat() + "Z"

    for i, q in enumerate(queries, 1):
        qid = q["id"]
        query = q["query"]
        gold_ids = q.get("gold_doc_ids", [])

        t0 = time.monotonic()

        result = run_pipeline(
            question=query,
            vectorstore=vs,
            bm25=bm25,
            model=model,
            n_results=k_retrieve,
            rewrite=True,
            hybrid=(mode == "hybrid"),
            do_rerank=use_rerank,
            ground=False,
        )

        gen_metrics = eval_generation(query, result.answer, result.docs, judge_llm)
        ret_metrics = eval_retrieval(result.docs, gold_ids)

        elapsed_ms = round((time.monotonic() - t0) * 1000)

        results.append({
            "i": i,
            "id": qid,
            "query": query,
            "topic": q.get("topic", ""),
            "gold_doc_ids": gold_ids,
            "answer": result.answer,
            "sources": result.sources,
            "rewritten_query": result.rewritten_query,
            "pipeline_log": result.pipeline_log,
            "retrieval_metrics": ret_metrics,
            "generation_metrics": gen_metrics,
            "elapsed_ms": elapsed_ms,
        })

        rel = gen_metrics["answer_relevance"]["score"]
        faith = gen_metrics["faithfulness"]["score"]
        ctx = gen_metrics["context_relevance"]["score"]
        rec5 = ret_metrics.get("recall@5", 0.0)
        status = "✓"

        def _fmt(v):
            return f"{v:.2f}" if v is not None else "n/a"

        print(
            f"[{i:>3}/{len(queries)}] {status} {qid[:45]:<45}  "
            f"rel={_fmt(rel)}  faith={_fmt(faith)}  ctx={_fmt(ctx)}  rec@5={rec5:.2f}"
        )

    total_s = time.monotonic() - t_total
    aggregate = _aggregate(results)

    report = {
        "type": "generation",
        "timestamp": timestamp,
        "config": {
            "k_retrieve": k_retrieve,
            "mode": mode,
            "use_rerank": use_rerank,
            "model": model,
            "n_queries": len(queries),
            "collection": collection,
        },
        "aggregate": aggregate,
        "results": results,
        "total_seconds": round(total_s, 1),
    }

    if output_dir:
        run_dir = _run_dir(output_dir, k_retrieve, timestamp)
        print(f"\nSaving run to {run_dir}/")
        _save_run(run_dir, report)

    return report


def _aggregate(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {}

    def _avg(key_path):
        vals = []
        for r in results:
            gm = r["generation_metrics"]
            parts = key_path.split(".")
            v = gm
            for p in parts:
                v = v.get(p) if isinstance(v, dict) else None
                if v is None:
                    break
            if v is not None:
                vals.append(v)
        return round(sum(vals) / len(vals), 4) if vals else None

    def _ret_avg(key):
        vals = [r["retrieval_metrics"].get(key, 0) for r in results]
        return round(sum(vals) / len(vals), 4)

    return {
        "answer_relevance": _avg("answer_relevance.score"),
        "faithfulness": _avg("faithfulness.score"),
        "context_relevance": _avg("context_relevance.score"),
        "avg_gen": _avg("avg"),
        "recall@5": _ret_avg("recall@5"),
        "mrr": _ret_avg("mrr"),
        "avg_ms": round(sum(r["elapsed_ms"] for r in results) / n),
    }


# ── Print helper ───────────────────────────────────────────────────────────────

def print_generation_summary(report: dict) -> None:
    agg = report["aggregate"]
    cfg = report.get("config", {})
    print("\n" + "=" * 65)
    print(f"  GENERATION BENCHMARK  —  {report['timestamp'][:19]}")
    print("=" * 65)
    print(
        f"  model={cfg.get('model')}  mode={cfg.get('mode')}  "
        f"rerank={cfg.get('use_rerank')}  k={cfg.get('k_retrieve')}  "
        f"n={cfg.get('n_queries')}"
    )
    print("-" * 65)

    def _row(label, key):
        v = agg.get(key)
        val = f"{v:.4f}" if v is not None else "n/a"
        print(f"  {label:<22} {val}")

    _row("answer_relevance", "answer_relevance")
    _row("faithfulness", "faithfulness")
    _row("context_relevance", "context_relevance")
    print()
    _row("recall@5", "recall@5")
    _row("mrr", "mrr")
    print()
    print(f"  avg latency          {agg.get('avg_ms')}ms")
    print(f"  total time           {report.get('total_seconds')}s")
    print("=" * 65)
