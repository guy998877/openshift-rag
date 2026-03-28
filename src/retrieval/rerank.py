"""Cross-encoder re-ranking using sentence-transformers."""

from __future__ import annotations

from langchain_core.documents import Document

_model = None
_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder

        _model = CrossEncoder(_MODEL_NAME)
    return _model


def rerank(query: str, docs: list[Document], top_k: int = 8) -> list[Document]:
    """Re-rank docs with a cross-encoder and return top_k with rerank_score metadata."""
    if not docs:
        return docs

    model = _get_model()
    pairs = [(query, doc.page_content[:512]) for doc in docs]
    scores = model.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:top_k]
    result = []
    for doc, score in ranked:
        doc.metadata["rerank_score"] = float(score)
        result.append(doc)
    return result
