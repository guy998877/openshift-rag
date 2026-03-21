"""CLI for the RAG evaluation benchmark."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m eval",
        description="Evaluate OpenShift RAG retrieval quality.",
    )
    parser.add_argument(
        "--queries", type=Path, default=Path("./data/ground_truth/queries.json"),
        help="Benchmark queries file (default: data/ground_truth/queries.json)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("./data/eval_results"), metavar="DIR",
        help="Parent directory for run output (default: data/eval_results). "
             "A timestamped subdirectory is created automatically.",
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Skip saving results to disk (print summary only)",
    )
    parser.add_argument(
        "--baseline", type=Path, default=None, metavar="PATH",
        help="Path to a metrics.json from a previous run for regression comparison",
    )
    parser.add_argument(
        "--k", type=int, default=20, metavar="K",
        help="Docs to retrieve per query (default: 20)",
    )
    parser.add_argument(
        "--n", type=int, default=None, metavar="N",
        help="Number of queries to evaluate (default: all)",
    )
    parser.add_argument(
        "--mode", default="hybrid", choices=["hybrid", "semantic", "keyword"],
        help="Retrieval mode: hybrid (default) | semantic (vector only) | keyword (BM25 only)",
    )
    parser.add_argument(
        "--rerank", action="store_true",
        help="Apply cross-encoder reranking after retrieval",
    )
    parser.add_argument(
        "--chroma-dir", type=Path, default=Path("./chroma_db"),
    )
    parser.add_argument(
        "--collection", default="openshift_docs_v0",
    )
    parser.add_argument(
        "--processed-dir", type=Path, default=Path("./data/processed"),
    )

    args = parser.parse_args()

    if not args.queries.exists():
        print(f"Error: queries file not found: {args.queries}", file=sys.stderr)
        sys.exit(1)

    from eval.benchmark import (
        compare_retrieval_reports,
        print_retrieval_summary,
        run_retrieval_benchmark,
    )

    report = run_retrieval_benchmark(
        queries_path=args.queries,
        chroma_dir=args.chroma_dir,
        collection=args.collection,
        processed_dir=args.processed_dir,
        k_retrieve=args.k,
        mode=args.mode,
        use_rerank=args.rerank,
        n_queries=args.n,
        output_dir=None if args.no_save else args.output_dir,
    )

    print_retrieval_summary(report)

    if args.baseline and args.baseline.exists():
        baseline = json.loads(args.baseline.read_text())
        compare_retrieval_reports(baseline, report)


main()
