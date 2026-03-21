"""CLI for OpenShift docs QA."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m services",
        description="Ask questions about OpenShift documentation.",
    )
    parser.add_argument("question", help="The question to ask")
    parser.add_argument("--n-results", type=int, default=5, metavar="N",
                        help="Number of chunks to retrieve (default: 5)")
    parser.add_argument("--model", default="gpt-4o-mini", metavar="MODEL",
                        help="OpenAI chat model (default: gpt-4o-mini)")
    parser.add_argument("--filter-topic", default=None, metavar="T",
                        help="Restrict retrieval to a topic (nodes, storage, etc.)")
    parser.add_argument("--filter-type", default=None, metavar="TYPE",
                        help="PROCEDURE or CONCEPT")
    parser.add_argument("--retrieve-only", action="store_true",
                        help="Print retrieved chunks, skip answer generation")
    parser.add_argument("--chroma-dir", default="./chroma_db", metavar="PATH",
                        help="ChromaDB directory (default: ./chroma_db)")
    parser.add_argument("--collection", default="openshift_docs_v0", metavar="NAME",
                        help="Collection name (default: openshift_docs_v0)")
    parser.add_argument("--verbose", action="store_true",
                        help="Show retrieval scores")
    parser.add_argument("--processed-dir", default="./data/processed", metavar="PATH",
                        help="Processed markdown directory for BM25 (default: ./data/processed)")

    # Pipeline stage toggles
    parser.add_argument("--no-rewrite", action="store_true",
                        help="Skip query rewriting")
    parser.add_argument("--no-hybrid", action="store_true",
                        help="Vector search only (no BM25)")
    parser.add_argument("--no-rerank", action="store_true",
                        help="Skip cross-encoder re-ranking")
    parser.add_argument("--grounding", action="store_true",
                        help="Enable grounding check (off by default)")
    parser.add_argument("--show-pipeline", action="store_true",
                        help="Print timing breakdown and rewritten query")

    args = parser.parse_args()

    from services.pipeline import QAResult, _doc_to_source, build_vectorstore

    chroma_dir = Path(args.chroma_dir)
    try:
        vs = build_vectorstore(chroma_dir, args.collection)
    except Exception as e:
        print(f"Error: failed to open ChromaDB at {chroma_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        count = vs._collection.count()
    except Exception:
        count = 0

    if count == 0:
        print(
            "Error: ChromaDB is empty — run: python -m retrieval --verbose",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build BM25 index unless --no-hybrid
    bm25 = None
    if not args.no_hybrid:
        processed_dir = Path(args.processed_dir)
        if processed_dir.exists():
            from retrieval.hybrid import BM25Index
            bm25 = BM25Index(processed_dir)
        else:
            print(f"Warning: processed dir {processed_dir} not found, falling back to vector-only.",
                  file=sys.stderr)

    if args.retrieve_only:
        # Retrieve and print chunks — no LLM call
        use_hybrid = not args.no_hybrid and bm25 is not None
        if use_hybrid:
            from retrieval.hybrid import hybrid_search
            docs = hybrid_search(args.question, vs, bm25, k_retrieve=50, k_final=args.n_results)
        else:
            search_kwargs: dict = {"k": args.n_results}
            filters = {}
            if args.filter_topic:
                filters["topic"] = args.filter_topic
            if args.filter_type:
                filters["content_type"] = args.filter_type
            if filters:
                search_kwargs["filter"] = filters

            if args.verbose:
                docs_scores = vs.similarity_search_with_score(args.question, **search_kwargs)
                docs = [d for d, _ in docs_scores]
            else:
                docs = vs.similarity_search(args.question, **search_kwargs)

        print(f"\nRetrieved {len(docs)} chunks for: {args.question!r}\n")
        for i, doc in enumerate(docs, 1):
            src = _doc_to_source(doc)
            score_str = ""
            if args.verbose:
                rrf = doc.metadata.get("rrf_score")
                if rrf is not None:
                    score_str = f"  rrf={rrf:.4f}"
            print(f"[{i}] [{src['content_type']}] {src['title']:<45} {src['source_dir']}{score_str}")
            print(f"    {src['snippet'][:200]!r}")
            print()
        return

    from services.pipeline import run_pipeline

    try:
        result = run_pipeline(
            question=args.question,
            vectorstore=vs,
            bm25=bm25,
            model=args.model,
            n_results=args.n_results,
            filter_topic=args.filter_topic,
            filter_content_type=args.filter_type,
            rewrite=not args.no_rewrite,
            hybrid=not args.no_hybrid,
            do_rerank=not args.no_rerank,
            ground=args.grounding,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose or args.show_pipeline:
        log = result.pipeline_log
        if result.rewritten_query:
            print(f'Rewritten query: "{result.rewritten_query}"')
        n_bm25 = log.get("n_bm25_hits", 0)
        n_vec  = log.get("n_vector_hits", 0)
        n_rer  = log.get("n_reranked", 0)
        r_ms   = log.get("retrieval_ms", 0)
        g_ms   = log.get("generate_ms", 0)
        gr_ms  = log.get("ground_ms", 0)
        ground_str = "✓ supported" if result.is_grounded else "✗ unverified"
        print(f"Retrieval:  BM25={n_bm25}, vector={n_vec} → reranked={n_rer}   ({r_ms}ms)")
        print(f"Generate:   {args.model}   ({g_ms}ms)")
        print(f"Grounding:  {ground_str}   ({gr_ms}ms)")
        print()

    print(f"\nAnswer:\n  {result.answer}\n")
    if result.sources:
        print(f"Sources ({len(result.sources)}):")
        for src in result.sources:
            ct = f"[{src['content_type']}]" if src["content_type"] else "[?]"
            title = src["title"] or src["id"]
            print(f"  {ct:<12} {title:<45} {src['source_dir']}")
