"""Generation evaluation — LLM-as-judge (reference-free, binary scoring)."""
from __future__ import annotations

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

# ── Prompt templates ──────────────────────────────────────────────────────────

_ANSWER_RELEVANCE_PROMPT = """\
Question: {query}

Answer: {answer}

Does the answer directly address the question?
Reply YES or NO on the first line, then a one-sentence explanation."""

_FAITHFULNESS_PROMPT = """\
Context:
{context}

Answer: {answer}

Given ONLY the context above, does the answer make any claims that are NOT supported by the context?
Reply YES if the answer is fully supported, NO if it contains unsupported claims.
Reply on the first line (YES or NO), then a one-sentence explanation."""

_CONTEXT_RELEVANCE_PROMPT = """\
Query: {query}

Documents:
{docs_block}

For each document above (D1, D2, ...), answer YES if it is relevant to answering the query, or NO if it is not.
Reply with one line per document in the format:
D1: YES
D2: NO
..."""


# ── Internal helpers ──────────────────────────────────────────────────────────

def _invoke(prompt: str, llm: ChatOpenAI) -> str:
    try:
        resp = llm.invoke([{"role": "user", "content": prompt}])
        return resp.content.strip()
    except Exception:
        return ""


def _parse_yes_no(text: str) -> float | None:
    """Return 1.0 for YES, 0.0 for NO, None if unparseable."""
    first_line = text.splitlines()[0].strip().upper() if text else ""
    if first_line.startswith("YES"):
        return 1.0
    if first_line.startswith("NO"):
        return 0.0
    return None


def _explanation(text: str) -> str:
    lines = text.splitlines()
    return lines[1].strip() if len(lines) > 1 else text[:120]


# ── Public evaluators ─────────────────────────────────────────────────────────

def eval_answer_relevance(query: str, answer: str, llm: ChatOpenAI) -> dict:
    """Binary: does the answer directly address the question?"""
    try:
        raw = _invoke(_ANSWER_RELEVANCE_PROMPT.format(query=query, answer=answer), llm)
        score = _parse_yes_no(raw)
        return {
            "label": "answer_relevance",
            "score": score,
            "explanation": _explanation(raw),
        }
    except Exception as exc:
        return {"label": "answer_relevance", "score": None, "explanation": str(exc)}


def eval_faithfulness(answer: str, docs: list[Document], llm: ChatOpenAI) -> dict:
    """Binary: is every claim in the answer supported by the retrieved context?"""
    try:
        context = "\n\n".join(doc.page_content[:800] for doc in docs[:5])
        raw = _invoke(_FAITHFULNESS_PROMPT.format(context=context, answer=answer), llm)
        score = _parse_yes_no(raw)
        return {
            "label": "faithfulness",
            "score": score,
            "explanation": _explanation(raw),
        }
    except Exception as exc:
        return {"label": "faithfulness", "score": None, "explanation": str(exc)}


def eval_context_relevance(query: str, docs: list[Document], llm: ChatOpenAI) -> dict:
    """Fractional: what share of retrieved chunks are relevant to the query?"""
    try:
        if not docs:
            return {"label": "context_relevance", "score": None, "explanation": "no docs"}

        docs_block = "\n\n".join(
            f"D{i}: {doc.page_content[:400]}" for i, doc in enumerate(docs, 1)
        )
        raw = _invoke(
            _CONTEXT_RELEVANCE_PROMPT.format(query=query, docs_block=docs_block), llm
        )

        # Parse "D1: YES", "D2: NO", ...
        yes_count = 0
        parsed = 0
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            upper = line.upper()
            if ": YES" in upper or upper.endswith("YES"):
                yes_count += 1
                parsed += 1
            elif ": NO" in upper or upper.endswith("NO"):
                parsed += 1

        if parsed == 0:
            return {"label": "context_relevance", "score": None, "explanation": "parse error"}

        score = round(yes_count / len(docs), 4)
        return {
            "label": "context_relevance",
            "score": score,
            "explanation": f"{yes_count}/{len(docs)} relevant",
        }
    except Exception as exc:
        return {"label": "context_relevance", "score": None, "explanation": str(exc)}


def eval_generation(
    query: str,
    answer: str,
    docs: list[Document],
    llm: ChatOpenAI,
) -> dict:
    """Run all three evaluators and return a combined result dict."""
    ar = eval_answer_relevance(query, answer, llm)
    fa = eval_faithfulness(answer, docs, llm)
    cr = eval_context_relevance(query, docs, llm)

    scores = [m["score"] for m in (ar, fa, cr) if m["score"] is not None]
    avg = round(sum(scores) / len(scores), 4) if scores else None

    return {
        "answer_relevance": ar,
        "faithfulness": fa,
        "context_relevance": cr,
        "avg": avg,
    }
