"""LLM-based query rewriting for improved retrieval."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

_REWRITE_PROMPT = (
    "You are helping improve a search query for OpenShift documentation. "
    "Rewrite the following user question into a clear, explicit search query. "
    "Expand abbreviations, add the product name if implied, and make it specific. "
    "Return ONLY the rewritten query, no explanation."
)


def rewrite_query(question: str, llm: ChatOpenAI) -> str:
    """Rewrite a user question into a better search query.

    Returns the rewritten query, or the original if rewriting fails.
    """
    try:
        rewriter = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        response = rewriter.invoke(
            [
                {"role": "system", "content": _REWRITE_PROMPT},
                {"role": "user", "content": question},
            ]
        )
        rewritten = response.content.strip()
        return rewritten if rewritten else question
    except Exception:
        return question
