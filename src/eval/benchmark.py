"""RAG benchmark runner — retrieval-only and full (retrieval + generation)."""
from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from ingest.config import DEFAULT_CHROMA_DIR, DEFAULT_COLLECTION, DEFAULT_PROCESSED_DIR
from qa.chain import build_vectorstore
from qa.hybrid import BM25Index, bm25_search, hybrid_search

K_VALUES = [1, 3, 5, 10, 20]

MODES = ("hybrid", "semantic", "keyword")


# ── Retrieval-only benchmark ─────────────────────────────────────────────────

def run_retrieval_benchmark(
    queries_path: Path,
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection: str = DEFAULT_COLLECTION,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    k_retrieve: int = 20,
    mode: str = "hybrid",      # "hybrid" | "semantic" | "keyword"
    use_rerank: bool = False,
    output_path: Path | None = None,
) -> dict:
    """Evaluate retrieval quality only. No LLM calls, runs in ~seconds.

    mode:
      hybrid   — BM25 + vector with RRF merge  (default)
      semantic — vector / embedding search only
      keyword  — BM25 keyword search only
    """
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")

    from eval.retrieval import eval_retrieval

    queries = json.loads(queries_path.read_text())

    print("Loading vectorstore...", end=" ", flush=True)
    vs = build_vectorstore(chroma_dir, collection)
    print(f"{vs._collection.count()} docs")

    bm25 = None
    if mode in ("hybrid", "keyword") and processed_dir.exists():
        print("Building BM25 index...", end=" ", flush=True)
        bm25 = BM25Index(processed_dir)
        print(f"{len(bm25._stems)} docs")

    if use_rerank:
        from qa.rerank import rerank

    results = []
    t_total = time.monotonic()

    for i, q in enumerate(queries, 1):
        qid = q["id"]
        query = q["query"]
        gold_ids = q.get("gold_doc_ids", [])

        t0 = time.monotonic()

        if mode == "hybrid" and bm25 is not None:
            docs = hybrid_search(query, vs, bm25, k_retrieve=k_retrieve, k_final=k_retrieve)
        elif mode == "keyword" and bm25 is not None:
            docs = bm25_search(query, vs, bm25, k=k_retrieve)
        else:
            docs = vs.similarity_search(query, k=k_retrieve)

        if use_rerank and docs:
            docs = rerank(query, docs, top_k=k_retrieve)

        elapsed_ms = round((time.monotonic() - t0) * 1000)
        metrics = eval_retrieval(docs, gold_ids, k_values=K_VALUES)

        results.append({
            "id": qid,
            "query": query,
            "topic": q.get("topic", ""),
            "gold_doc_ids": gold_ids,
            "metrics": metrics,
            "elapsed_ms": elapsed_ms,
        })

        r5 = metrics.get("recall@5", 0)
        mrr = metrics.get("mrr", 0)
        found = metrics.get("gold_found", [])
        missed = metrics.get("gold_missed", [])
        status = "✓" if r5 > 0 else "✗"
        print(
            f"[{i:>3}/{len(queries)}] {status} {qid[:45]:<45}  "
            f"rec@5={r5:.2f}  mrr={mrr:.2f}  "
            f"found={found}  missed={missed}"
        )

    total_s = time.monotonic() - t_total
    aggregate = _aggregate_retrieval(results)

    report = {
        "type": "retrieval",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "config": {
            "k_retrieve": k_retrieve,
            "mode": mode,
            "use_rerank": use_rerank,
            "collection": collection,
        },
        "aggregate": aggregate,
        "results": results,
        "total_seconds": round(total_s, 1),
    }

    if output_path:
        output_path.write_text(json.dumps(report, indent=2))
        print(f"\nSaved → {output_path}")

    return report


def _aggregate_retrieval(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {}
    agg: dict = {}
    for k in K_VALUES:
        agg[f"recall@{k}"] = round(sum(r["metrics"].get(f"recall@{k}", 0) for r in results) / n, 4)
        agg[f"precision@{k}"] = round(sum(r["metrics"].get(f"precision@{k}", 0) for r in results) / n, 4)
    agg["mrr"] = round(sum(r["metrics"].get("mrr", 0) for r in results) / n, 4)
    agg["any_hit@5"] = round(sum(1 for r in results if r["metrics"].get("recall@5", 0) > 0) / n, 4)
    agg["any_hit@10"] = round(sum(1 for r in results if r["metrics"].get("recall@10", 0) > 0) / n, 4)
    agg["avg_ms"] = round(sum(r["elapsed_ms"] for r in results) / n)
    return agg


# ── Print helpers ─────────────────────────────────────────────────────────────

def print_retrieval_summary(report: dict) -> None:
    agg = report["aggregate"]
    cfg = report.get("config", {})
    print("\n" + "=" * 65)
    print(f"  RETRIEVAL BENCHMARK  —  {report['timestamp'][:19]}")
    print("=" * 65)
    print(f"  mode={cfg.get('mode')}  rerank={cfg.get('use_rerank')}  "
          f"k_retrieve={cfg.get('k_retrieve')}")
    print("-" * 65)
    for k in K_VALUES:
        print(f"  recall@{k:<4}    {agg.get(f'recall@{k}', 0):.4f}")
    print()
    for k in K_VALUES:
        print(f"  precision@{k:<2}   {agg.get(f'precision@{k}', 0):.4f}")
    print()
    print(f"  MRR             {agg.get('mrr', 0):.4f}")
    print(f"  any_hit@5       {agg.get('any_hit@5', 0):.4f}   "
          f"({round(agg.get('any_hit@5',0) * len(report['results']))}/{len(report['results'])} queries)")
    print(f"  any_hit@10      {agg.get('any_hit@10', 0):.4f}")
    print(f"  avg latency     {agg.get('avg_ms')}ms")
    print(f"  total time      {report.get('total_seconds')}s")
    print("=" * 65)

    # Per-topic breakdown
    from collections import defaultdict
    by_topic: dict[str, list] = defaultdict(list)
    for r in report["results"]:
        by_topic[r["topic"]].append(r["metrics"].get("recall@5", 0))

    print("\nPer-topic recall@5:")
    for topic, scores in sorted(by_topic.items(), key=lambda x: -sum(x[1]) / len(x[1])):
        avg = sum(scores) / len(scores)
        bar = "█" * round(avg * 10) + "░" * (10 - round(avg * 10))
        print(f"  {topic:<40} {bar}  {avg:.2f}  (n={len(scores)})")


def compare_retrieval_reports(baseline: dict, current: dict) -> None:
    b, c = baseline["aggregate"], current["aggregate"]
    print("\n" + "=" * 65)
    print("  REGRESSION COMPARISON")
    print(f"  Baseline: {baseline['timestamp'][:19]}  "
          f"mode={baseline['config'].get('mode')}  rerank={baseline['config'].get('use_rerank')}")
    print(f"  Current:  {current['timestamp'][:19]}  "
          f"mode={current['config'].get('mode')}  rerank={current['config'].get('use_rerank')}")
    print("=" * 65)

    def _row(label, key, higher_is_better=True):
        bv, cv = b.get(key, 0), c.get(key, 0)
        delta = cv - bv
        flag = ""
        if abs(delta) >= 0.02:
            flag = "  ✓ improved" if (delta > 0) == higher_is_better else "  ✗ REGRESSED"
        print(f"  {label:<18} {bv:.4f} → {cv:.4f}  ({delta:+.4f}){flag}")

    for k in K_VALUES:
        _row(f"recall@{k}", f"recall@{k}")
    _row("MRR",           "mrr")
    _row("any_hit@5",     "any_hit@5")
    _row("precision@5",   "precision@5")
    _row("avg_ms",        "avg_ms", higher_is_better=False)
    print("=" * 65)
