"""BM25 index + hybrid BM25/vector search with Reciprocal Rank Fusion."""
from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Index:
    """BM25 index over the preprocessed markdown files."""

    def __init__(self, processed_dir: Path) -> None:
        self._stems: list[str] = []
        corpus: list[list[str]] = []

        for md_path in sorted(processed_dir.glob("*.md")):
            text = md_path.read_text(encoding="utf-8", errors="replace")
            self._stems.append(md_path.stem)
            corpus.append(text.lower().split())

        self._bm25 = BM25Okapi(corpus) if corpus else None

    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]:
        """Return top-k (stem, normalised_score) pairs."""
        if self._bm25 is None or not self._stems:
            return []

        tokens = query.lower().split()
        scores = self._bm25.get_scores(tokens)

        # Pair with stems and sort descending
        ranked = sorted(
            zip(self._stems, scores), key=lambda x: x[1], reverse=True
        )[:k]

        # Normalise scores to [0, 1]
        max_score = ranked[0][1] if ranked else 1.0
        if max_score == 0:
            return [(stem, 0.0) for stem, _ in ranked]
        return [(stem, score / max_score) for stem, score in ranked]


def bm25_search(
    query: str,
    vectorstore: Chroma,
    bm25: BM25Index,
    k: int = 20,
) -> list[Document]:
    """Keyword-only search: BM25 ranking, docs fetched from ChromaDB."""
    hits = bm25.search(query, k=k)
    if not hits:
        return []

    stems = [stem for stem, _ in hits]
    scores = {stem: score for stem, score in hits}

    try:
        result = vectorstore.get(ids=stems, include=["documents", "metadatas"])
        docs = []
        for doc_id, content, metadata in zip(
            result.get("ids", []),
            result.get("documents", []),
            result.get("metadatas", []),
        ):
            doc = Document(page_content=content or "", metadata=metadata or {})
            doc.metadata["bm25_score"] = scores.get(doc_id, 0.0)
            docs.append((doc_id, doc))

        # Re-sort by original BM25 rank order
        stem_rank = {stem: i for i, stem in enumerate(stems)}
        docs.sort(key=lambda x: stem_rank.get(x[0], 999))
        return [d for _, d in docs]
    except Exception:
        return []


def hybrid_search(
    query: str,
    vectorstore: Chroma,
    bm25: BM25Index,
    k_retrieve: int = 50,
    k_final: int = 50,
    filter_kwargs: dict | None = None,
) -> list[Document]:
    """Hybrid BM25 + vector search merged via Reciprocal Rank Fusion.

    Returns up to k_final Documents with metadata["rrf_score"] attached.
    """
    # --- BM25 results ---
    bm25_results = bm25.search(query, k=k_retrieve)
    bm25_stems = [stem for stem, _ in bm25_results]

    # --- Vector results ---
    search_kwargs: dict = {"k": k_retrieve}
    if filter_kwargs:
        search_kwargs.update(filter_kwargs)

    try:
        vector_results = vectorstore.similarity_search_with_score(query, **search_kwargs)
    except Exception:
        vector_results = []

    # Build a stem → rank map for BM25
    bm25_rank: dict[str, int] = {stem: rank for rank, stem in enumerate(bm25_stems, 1)}

    # Build a stem → rank map and doc map for vector results
    vector_rank: dict[str, int] = {}
    vector_docs: dict[str, Document] = {}
    for rank, (doc, _score) in enumerate(vector_results, 1):
        stem = doc.metadata.get("id", "")
        if stem:
            vector_rank[stem] = rank
            vector_docs[stem] = doc

    # Union of all stems
    all_stems = set(bm25_rank) | set(vector_rank)

    # RRF: score = sum of 1 / (60 + rank) across lists
    K = 60
    rrf_scores: dict[str, float] = {}
    for stem in all_stems:
        score = 0.0
        if stem in bm25_rank:
            score += 1.0 / (K + bm25_rank[stem])
        if stem in vector_rank:
            score += 1.0 / (K + vector_rank[stem])
        rrf_scores[stem] = score

    # Sort by RRF score descending
    ranked_stems = sorted(rrf_scores, key=lambda s: rrf_scores[s], reverse=True)[:k_final]

    # Fetch BM25-only docs from ChromaDB (vector docs already have Document objects)
    bm25_only_stems = [s for s in ranked_stems if s not in vector_docs]
    fetched_docs: dict[str, Document] = {}
    if bm25_only_stems:
        try:
            result = vectorstore.get(ids=bm25_only_stems, include=["documents", "metadatas"])
            for doc_id, content, metadata in zip(
                result.get("ids", []),
                result.get("documents", []),
                result.get("metadatas", []),
            ):
                fetched_docs[doc_id] = Document(page_content=content or "", metadata=metadata or {})
        except Exception:
            pass

    # Assemble final list
    docs: list[Document] = []
    for stem in ranked_stems:
        doc = vector_docs.get(stem) or fetched_docs.get(stem)
        if doc is None:
            continue
        doc.metadata["rrf_score"] = rrf_scores[stem]
        docs.append(doc)

    return docs
