"""Hyperparameter grid search over the full RAG pipeline.

Iterates all combinations of k / mode / rerank / rewrite, runs the
generation benchmark (LLM-as-judge) on a fixed subset of queries, and
prints a ranked summary table.

Usage:
    python -m eval.grid_search                  # 20 queries, default grid
    python -m eval.grid_search --n 10           # smaller subset
    python -m eval.grid_search --no-save        # skip writing results
    python -m eval.grid_search --model gpt-4.1   # different judge model
    python -m eval.grid_search --workers 8      # parallel queries per config
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Hyperparameter grid ─────────────────────────────────────────────────────

GRID = {
    "model": ["gpt-4o-mini", "gpt-4.1"],
    "k": [3, 5],
    "mode": ["hybrid", "semantic", "keyword"],
    "rerank": [True, False],
    "rewrite": [True],
}

# Metrics to rank by (all weighted equally in the composite score)
QUALITY_METRICS = [
    "answer_relevance",
    "faithfulness",
    "context_relevance",
    "recall@5",
    "mrr",
]


# ── Formatting helpers ──────────────────────────────────────────────────────


def _fmt(v: float | None, w: int = 6) -> str:
    return f"{v:.4f}".rjust(w) if v is not None else "  n/a ".rjust(w)


def _color(v: float | None) -> str:
    """ANSI colour for a 0-1 metric value."""
    if v is None:
        return "\033[90m"  # grey
    if v >= 0.80:
        return "\033[92m"  # green
    if v >= 0.60:
        return "\033[93m"  # yellow
    return "\033[91m"  # red


RESET = "\033[0m"
BOLD = "\033[1m"


def _cval(v: float | None) -> str:
    return f"{_color(v)}{_fmt(v)}{RESET}"


# ── Per-query worker (thread-safe: creates its own ChatOpenAI instance) ──────

_RETRY_AFTER_RE = re.compile(r"try again in (\d+(?:\.\d+)?)s", re.IGNORECASE)
_MAX_RETRIES = 6


def _run_query(q, vs, bm25, model, k, mode, use_bm25, do_rerank, do_rewrite):
    from langchain_openai import ChatOpenAI
    from eval.generation import eval_generation
    from eval.retrieval import eval_retrieval
    from services.pipeline import run_pipeline

    judge = ChatOpenAI(model=model, temperature=0)
    t0 = time.monotonic()
    last_exc: Exception | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            result = run_pipeline(
                question=q["query"],
                vectorstore=vs,
                bm25=bm25 if use_bm25 else None,
                model=model,
                n_results=k,
                rewrite=do_rewrite,
                hybrid=(mode == "hybrid"),
                do_rerank=do_rerank,
                ground=False,
            )
            gen = eval_generation(q["query"], result.answer, result.docs, judge)
            ret = eval_retrieval(result.docs, q.get("gold_doc_ids", []))
            return {
                "id": q["id"],
                "query": q["query"],
                "topic": q.get("topic", ""),
                "gold_doc_ids": q.get("gold_doc_ids", []),
                "answer": result.answer,
                "retrieval_metrics": ret,
                "generation_metrics": gen,
                "elapsed_ms": round((time.monotonic() - t0) * 1000),
            }
        except Exception as e:
            last_exc = e
            err_str = str(e)
            is_rate_limit = (
                "rate_limit_exceeded" in err_str or "RateLimitError" in type(e).__name__
            )
            if is_rate_limit and attempt < _MAX_RETRIES - 1:
                m = _RETRY_AFTER_RE.search(err_str)
                wait = float(m.group(1)) + 1.0 if m else 10.0 * (2**attempt)
                print(
                    f"         [rate limit] query {q.get('id', '?')} — waiting {wait:.1f}s (attempt {attempt + 1})",
                    flush=True,
                )
                time.sleep(wait)
                continue
            break

    return {
        "id": q.get("id", ""),
        "query": q.get("query", ""),
        "topic": "",
        "gold_doc_ids": [],
        "answer": None,
        "retrieval_metrics": {},
        "generation_metrics": {},
        "elapsed_ms": round((time.monotonic() - t0) * 1000),
        "_error": str(last_exc),
    }


# ── Run one configuration ───────────────────────────────────────────────────


def run_config(
    cfg: dict,
    queries_path: Path,
    chroma_dir: Path,
    collection: str,
    processed_dir: Path,
    n_queries: int,
    output_dir: Path | None,
    vs,  # pre-loaded vectorstore (shared, read-only)
    bm25,  # pre-loaded BM25 index  (shared, read-only, may be None)
    workers: int = 8,
) -> dict:
    """Run gen benchmark for one config, reusing pre-loaded indices."""
    model = cfg["model"]
    queries = json.loads(queries_path.read_text())[:n_queries]
    mode = cfg["mode"]
    use_bm25 = bm25 is not None and mode in ("hybrid", "keyword")
    do_rerank = cfg["rerank"]
    do_rewrite = cfg["rewrite"]
    k = cfg["k"]

    results = []
    t_total = time.monotonic()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_idx = {
            pool.submit(
                _run_query, q, vs, bm25, model, k, mode, use_bm25, do_rerank, do_rewrite
            ): i
            for i, q in enumerate(queries)
        }
        for future in as_completed(future_to_idx):
            r = future.result()
            results.append(r)
            status = (
                f"_error: {r['_error']}"
                if "_error" in r
                else f"ok  {r['elapsed_ms']}ms"
            )
            print(f"         query {r['id']:>4} — {status}", flush=True)

    # Restore original query order
    id_to_pos = {q["id"]: i for i, q in enumerate(queries)}
    results.sort(key=lambda r: id_to_pos.get(r["id"], 0))

    total_s = time.monotonic() - t_total

    # Aggregate
    def _avg_gen(key):
        vals = [
            r["generation_metrics"].get(key, {}).get("score")
            for r in results
            if r["generation_metrics"].get(key, {}).get("score") is not None
        ]
        return round(sum(vals) / len(vals), 4) if vals else None

    def _avg_ret(key):
        vals = [r["retrieval_metrics"].get(key, 0) for r in results]
        return round(sum(vals) / len(vals), 4) if vals else None

    aggregate = {
        "answer_relevance": _avg_gen("answer_relevance"),
        "faithfulness": _avg_gen("faithfulness"),
        "context_relevance": _avg_gen("context_relevance"),
        "recall@1": _avg_ret("recall@1"),
        "recall@3": _avg_ret("recall@3"),
        "recall@5": _avg_ret("recall@5"),
        "precision@1": _avg_ret("precision@1"),
        "precision@3": _avg_ret("precision@3"),
        "precision@5": _avg_ret("precision@5"),
        "mrr": _avg_ret("mrr"),
        "avg_ms": round(sum(r["elapsed_ms"] for r in results) / len(results)),
    }
    quality_vals = [aggregate[m] for m in QUALITY_METRICS if aggregate[m] is not None]
    aggregate["composite"] = (
        round(sum(quality_vals) / len(quality_vals), 4) if quality_vals else None
    )

    report = {
        "config": {**cfg, "n_queries": n_queries},
        "aggregate": aggregate,
        "total_seconds": round(total_s, 1),
        "results": results,
    }

    # Optionally save
    if output_dir is not None:
        mdl_slug = model.replace("gpt-", "").replace("-", "")  # e.g. "4omini"
        slug = f"{mdl_slug}_k{k}_{mode}_{'rerank' if do_rerank else 'norerank'}_{'rewrite' if do_rewrite else 'nowrite'}"
        run_dir = output_dir / slug
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(
            json.dumps(
                {
                    "config": report["config"],
                    "aggregate": aggregate,
                    "total_seconds": report["total_seconds"],
                },
                indent=2,
            )
        )
        # Per-query detail — needed by eval.analysis failure-mode taxonomy.
        per_query = [{**r, "config": report["config"]} for r in report["results"]]
        (run_dir / "results.json").write_text(json.dumps(per_query, indent=2))

    return report


# ── Print progress line ─────────────────────────────────────────────────────


def _cfg_label(cfg: dict) -> str:
    r = "rerank" if cfg["rerank"] else "no-rerank"
    w = "rewrite" if cfg["rewrite"] else "no-rewrite"
    return (
        f"model={cfg['model']:<12}  k={cfg['k']:<2}  mode={cfg['mode']:<8}  {r:<9}  {w}"
    )


# ── Print final ranked table ─────────────────────────────────────────────────


def print_grid_summary(rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: r["aggregate"]["composite"] or 0, reverse=True)

    W = 128
    print("\n" + "=" * W)
    print(f"  GRID SEARCH RESULTS — ranked by composite score  ({len(rows)} configs)")
    print("=" * W)
    header = (
        f"  {'Rank':<5} {'Model':<13} {'k':<4} {'Mode':<9} {'Rerank':<8} {'Rewrite':<9}"
        f" {'Ans.Rel':>8} {'Faith':>8} {'Ctx.Rel':>8} {'Recall@5':>9} {'MRR':>8}"
        f" {'Composite':>10} {'ms':>7}"
    )
    print(header)
    print("-" * W)

    for rank, row in enumerate(rows, 1):
        cfg = row["config"]
        agg = row["aggregate"]
        comp = agg.get("composite")
        comp_color = _color(comp)

        line = (
            f"  {rank:<5}"
            f" {cfg.get('model', '?'):<13}"
            f" {cfg['k']:<4}"
            f" {cfg['mode']:<9}"
            f" {'on' if cfg['rerank'] else 'off':<8}"
            f" {'on' if cfg['rewrite'] else 'off':<9}"
            f" {_cval(agg.get('answer_relevance'))}"
            f" {_cval(agg.get('faithfulness'))}"
            f" {_cval(agg.get('context_relevance'))}"
            f" {_cval(agg.get('recall@5'))}"
            f" {_cval(agg.get('mrr'))}"
            f"  {comp_color}{BOLD}{_fmt(comp, 8)}{RESET}"
            f" {str(agg.get('avg_ms', '?')).rjust(7)}"
        )
        print(line)

    print("=" * W)
    best = rows[0]
    bcfg = best["config"]
    bagg = best["aggregate"]
    print(
        f"\n  {BOLD}Best config:{RESET}  model={bcfg.get('model', '?')}, k={bcfg['k']}, mode={bcfg['mode']}, "
        f"rerank={'on' if bcfg['rerank'] else 'off'}, rewrite={'on' if bcfg['rewrite'] else 'off'}"
    )
    print(
        f"  Composite: {_color(bagg['composite'])}{bagg['composite']}{RESET}  "
        f"(ans_rel={bagg['answer_relevance']}, faith={bagg['faithfulness']}, "
        f"ctx_rel={bagg['context_relevance']}, recall@5={bagg['recall@5']}, mrr={bagg['mrr']})"
    )
    print()


# ── CLI ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m eval.grid_search",
        description="Grid search over RAG hyperparameters with LLM-as-judge.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=20,
        metavar="N",
        help="Queries per config (default: 20)",
    )
    parser.add_argument(
        "--queries", type=Path, default=Path("./data/ground_truth/queries.json")
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("./data/eval_results/grid_search")
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Skip saving per-run metrics to disk"
    )
    parser.add_argument("--chroma-dir", type=Path, default=Path("./chroma_db"))
    parser.add_argument("--collection", default="openshift_docs_v0")
    parser.add_argument("--processed-dir", type=Path, default=Path("./data/processed"))
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        metavar="N",
        help="Parallel query workers per config (default: 8)",
    )
    args = parser.parse_args()

    if not args.queries.exists():
        print(f"Error: queries not found: {args.queries}", file=sys.stderr)
        sys.exit(1)

    # Build all combos
    keys = list(GRID.keys())
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*GRID.values())]
    total = len(combos)

    print(f"\n{'=' * 60}")
    print("  RAG HYPERPARAMETER GRID SEARCH")
    print(f"{'=' * 60}")
    print(f"  Configs : {total}")
    print(f"  Queries : {args.n} per config  ({total * args.n} total LLM calls)")
    print(f"  Workers : {args.workers} parallel queries per config")
    print(f"  Grid    : model={GRID['model']}")
    print(f"            k={GRID['k']}  mode={GRID['mode']}")
    print(f"            rerank={GRID['rerank']}  rewrite={GRID['rewrite']}")
    print(f"{'=' * 60}\n")

    # Load indices once
    print("Loading vectorstore...", end=" ", flush=True)
    from services.pipeline import build_vectorstore

    vs = build_vectorstore(args.chroma_dir, args.collection)
    print(f"{vs._collection.count()} docs")

    bm25 = None
    if args.processed_dir.exists():
        print("Building BM25 index...", end=" ", flush=True)
        from retrieval.hybrid import BM25Index

        bm25 = BM25Index(args.processed_dir)
        print(f"{len(bm25._stems)} docs")

    print()

    output_dir = None if args.no_save else args.output_dir
    if output_dir:
        ts_slug = datetime.utcnow().strftime("%Y-%m-%dT%H-%M")
        output_dir = output_dir / ts_slug
        output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    t_wall = time.monotonic()

    for idx, cfg in enumerate(combos, 1):
        label = _cfg_label(cfg)
        eta_str = ""
        if idx > 1:
            elapsed = time.monotonic() - t_wall
            avg_per = elapsed / (idx - 1)
            remaining = avg_per * (total - idx + 1)
            eta_str = f"  ETA ~{remaining / 60:.1f}min"

        print(f"[{idx:>2}/{total}] {label}{eta_str}", flush=True)

        row = run_config(
            cfg=cfg,
            queries_path=args.queries,
            chroma_dir=args.chroma_dir,
            collection=args.collection,
            processed_dir=args.processed_dir,
            n_queries=args.n,
            output_dir=output_dir,
            vs=vs,
            bm25=bm25,
            workers=args.workers,
        )
        agg = row["aggregate"]
        print(
            f"       → composite={_color(agg['composite'])}{agg['composite']}{RESET}  "
            f"ans_rel={agg['answer_relevance']}  faith={agg['faithfulness']}  "
            f"ctx={agg['context_relevance']}  r@5={agg['recall@5']}  "
            f"mrr={agg['mrr']}  {agg['avg_ms']}ms",
            flush=True,
        )
        rows.append(row)

    total_wall = time.monotonic() - t_wall
    print(f"\nTotal wall time: {total_wall / 60:.1f} min")

    # Save combined summary
    if output_dir:
        summary = [{"config": r["config"], "aggregate": r["aggregate"]} for r in rows]
        summary_sorted = sorted(
            summary, key=lambda r: r["aggregate"]["composite"] or 0, reverse=True
        )
        (output_dir / "summary.json").write_text(json.dumps(summary_sorted, indent=2))
        print(f"Summary saved → {output_dir / 'summary.json'}")

    print_grid_summary(rows)


main()
