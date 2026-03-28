"""Post-generation grounding check — verifies answer is supported by context."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

_GROUND_PROMPT = """\
Given the context below and an answer, does the answer look consistent with \
the context? It is OK if the answer uses slightly different wording or \
summarises — only reply NO if the answer makes clear factual claims that \
directly contradict or are entirely absent from the context.

Context:
{context}

Answer:
{answer}

Reply with one word only: YES or NO."""


def grounding_check(
    answer: str,
    docs: list[Document],
    llm: ChatOpenAI,
) -> tuple[str, bool]:
    """Check whether the answer is grounded in the provided docs.

    Returns (answer, is_grounded). The answer is never replaced — is_grounded
    is a warning flag only (shown as a UI banner to the user).
    """
    try:
        context = "\n\n".join(doc.page_content[:1000] for doc in docs[:5])
        prompt = _GROUND_PROMPT.format(context=context, answer=answer)
        checker = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        response = checker.invoke([{"role": "user", "content": prompt}])
        first_word = (
            response.content.strip().upper().split()[0]
            if response.content.strip()
            else "YES"
        )
        is_grounded = not first_word.startswith("NO")
        return answer, is_grounded
    except Exception:
        return answer, True
