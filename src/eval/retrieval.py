"""Retrieval evaluation — pure exact-match, no LLM calls required.

Metrics
-------
recall@k        fraction of gold docs that appear in the top-k results
                (averaged over queries gives macro recall)
mrr             Mean Reciprocal Rank — 1/rank of the first gold doc hit;
                0 if no gold doc found within the retrieved set
precision@k     fraction of top-k retrieved docs that are gold docs
                (a.k.a. context precision)

All metrics are computed solely from doc stems vs gold_doc_ids, so the
eval is deterministic, cheap, and can run at 100-query scale in seconds.
"""
from __future__ import annotations

from langchain_core.documents import Document


def _stem(doc: Document) -> str:
    return doc.metadata.get("file", "").replace(".adoc", "")


def eval_retrieval(
    docs: list[Document],
    gold_doc_ids: list[str],
    k_values: list[int] | None = None,
) -> dict:
    """Compute recall@k, MRR, and precision@k for one query.

    Parameters
    ----------
    docs        Ranked list of retrieved Documents (position 0 = rank 1)
    gold_doc_ids  Ground-truth doc stems that should appear in results
    k_values    Which k cutoffs to evaluate (default: [1, 3, 5, 10, 20])

    Returns a flat dict of metric_name → value, plus bookkeeping fields.
    """
    if k_values is None:
        k_values = [1, 3, 5, 10, 20]

    gold_set = set(gold_doc_ids)
    retrieved_stems = [_stem(d) for d in docs]

    metrics: dict = {"retrieved_stems": retrieved_stems}

    # Recall@k and Precision@k
    for k in k_values:
        top = retrieved_stems[:k]
        hits = [s for s in top if s in gold_set]
        metrics[f"recall@{k}"] = round(len(hits) / len(gold_set), 4) if gold_set else 0.0
        metrics[f"precision@{k}"] = round(len(hits) / k, 4) if k > 0 else 0.0

    # MRR — rank of first gold doc (1-indexed)
    rr = 0.0
    for rank, stem in enumerate(retrieved_stems, 1):
        if stem in gold_set:
            rr = 1.0 / rank
            break
    metrics["mrr"] = round(rr, 4)
    metrics["first_hit_rank"] = round(1.0 / rr) if rr > 0 else None

    # Which gold docs were found / missed
    metrics["gold_found"] = [g for g in gold_doc_ids if g in set(retrieved_stems)]
    metrics["gold_missed"] = [g for g in gold_doc_ids if g not in set(retrieved_stems)]

    return metrics
