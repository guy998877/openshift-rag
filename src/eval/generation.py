"""Generation evaluation metrics (LLM-as-judge)."""
from __future__ import annotations

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

_FAITHFULNESS_PROMPT = """\
Context retrieved from documentation:
{context}

Answer given:
{answer}

Score the faithfulness of the answer to the context on a scale of 1-5:
1 = answer contradicts or ignores the context entirely
3 = answer is mostly supported but adds unsourced claims
5 = every claim in the answer is directly supported by the context

Reply with a single integer 1-5, nothing else."""

_CORRECTNESS_PROMPT = """\
Question: {query}

Reference answer (what a correct answer should cover):
{reference}

Actual answer:
{answer}

Score how well the actual answer addresses the question compared to the reference, on a scale of 1-5:
1 = misses the point entirely or is wrong
3 = partially correct, covers some key points
5 = correct and complete, covers all key points in the reference

Reply with a single integer 1-5, nothing else."""


def _score(prompt: str, llm: ChatOpenAI) -> int:
    try:
        resp = llm.invoke([{"role": "user", "content": prompt}])
        text = resp.content.strip()
        return int(text[0]) if text and text[0].isdigit() else 1
    except Exception:
        return 1


def eval_generation(
    query: str,
    answer: str,
    docs: list[Document],
    reference_answer: str,
    llm: ChatOpenAI,
) -> dict:
    """Score a generated answer on faithfulness and correctness (1-5 each)."""
    context = "\n\n".join(doc.page_content[:500] for doc in docs[:5])

    faithfulness = _score(
        _FAITHFULNESS_PROMPT.format(context=context, answer=answer),
        llm,
    )
    correctness = _score(
        _CORRECTNESS_PROMPT.format(query=query, reference=reference_answer, answer=answer),
        llm,
    )

    return {
        "faithfulness": faithfulness,
        "correctness": correctness,
        "avg": round((faithfulness + correctness) / 2, 2),
    }
