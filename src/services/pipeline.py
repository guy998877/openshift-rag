"""LangChain RAG pipeline for OpenShift docs QA."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

SYSTEM_PROMPT = """\
You are an expert OpenShift documentation assistant for platform engineers,
cluster admins, and SRE/DevOps users.

Answer questions using ONLY the documentation excerpts provided below.
Rules:
1. Be concise and specific — include exact commands, YAML, or flags when present in the docs
2. If a task requires cluster-admin privileges, state this clearly
3. If the answer is not in the provided context, say exactly:
   "The provided documentation does not cover this. Try rephrasing or asking about a related topic."
4. Do not add information not present in the context

Context:
{context}"""


@dataclass
class QAResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    docs: list[Document] = field(default_factory=list)
    model: str = ""
    rewritten_query: str = ""
    is_grounded: bool = True
    pipeline_log: dict = field(default_factory=dict)


def build_vectorstore(chroma_dir: Path, collection_name: str) -> Chroma:
    """Wrap existing ChromaDB collection with LangChain + OpenAI embeddings."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    client = chromadb.PersistentClient(path=str(chroma_dir))
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )


def _format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def doc_stem(doc) -> str:
    """Return the canonical document stem (filename without .adoc)."""
    return doc.metadata.get("file", "").replace(".adoc", "")


def _doc_to_source(doc: Document) -> dict:
    m = doc.metadata
    content = doc.page_content
    stem = doc_stem(doc)
    return {
        "id": stem,
        "title": m.get("title", stem),
        "content_type": m.get("content_type", ""),
        "topic": m.get("topic", ""),
        "source_dir": m.get("source_dir", ""),
        "snippet": content[:300] if content else "",
    }


def run_pipeline(
    question: str,
    vectorstore: Chroma,
    bm25=None,
    model: str = "gpt-4o-mini",
    n_results: int = 5,
    filter_topic: str | None = None,
    filter_content_type: str | None = None,
    rewrite: bool = True,
    hybrid: bool = True,
    do_rerank: bool = True,
    ground: bool = False,
) -> QAResult:
    """Full pipeline: rewrite → retrieve → rerank → generate → ground."""
    from services.grounding import grounding_check
    from retrieval.hybrid import hybrid_search
    from retrieval.rerank import rerank
    from services.rewrite import rewrite_query

    t_total = time.monotonic()
    log: dict = {}

    llm = ChatOpenAI(model=model, temperature=0)

    # 1. Query rewriting
    t0 = time.monotonic()
    if rewrite:
        rewritten = rewrite_query(question, llm)
    else:
        rewritten = question
    log["rewrite_ms"] = round((time.monotonic() - t0) * 1000)

    search_query = rewritten if rewritten else question

    # 2. Retrieval
    t0 = time.monotonic()
    filter_kwargs: dict = {}
    filters: dict = {}
    if filter_topic:
        filters["topic"] = filter_topic
    if filter_content_type:
        filters["content_type"] = filter_content_type
    if filters:
        filter_kwargs["filter"] = filters

    if hybrid and bm25 is not None:
        docs = hybrid_search(
            search_query, vectorstore, bm25,
            k_retrieve=50, k_final=50,
            filter_kwargs=filter_kwargs or None,
        )
        log["n_bm25_hits"] = len(docs)
        log["n_vector_hits"] = len(docs)
    else:
        docs = vectorstore.similarity_search(search_query, k=50, **filter_kwargs)
        log["n_bm25_hits"] = 0
        log["n_vector_hits"] = len(docs)
    log["retrieval_ms"] = round((time.monotonic() - t0) * 1000)

    # 3. Re-ranking
    t0 = time.monotonic()
    if do_rerank and docs:
        docs = rerank(search_query, docs, top_k=n_results * 2)
        docs = docs[:n_results]
        log["n_reranked"] = len(docs)
    else:
        docs = docs[:n_results]
        log["n_reranked"] = len(docs)
    log["rerank_ms"] = round((time.monotonic() - t0) * 1000)

    # 4. Generation
    t0 = time.monotonic()
    context_str = _format_docs(docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    answer = (prompt | llm | StrOutputParser()).invoke({
        "input": search_query,
        "context": context_str,
    })
    log["generate_ms"] = round((time.monotonic() - t0) * 1000)

    # 5. Grounding check
    t0 = time.monotonic()
    is_grounded = True
    if ground and docs:
        answer, is_grounded = grounding_check(answer, docs, llm)
    log["ground_ms"] = round((time.monotonic() - t0) * 1000)

    log["total_ms"] = round((time.monotonic() - t_total) * 1000)

    sources = [_doc_to_source(doc) for doc in docs]
    return QAResult(
        answer=answer,
        sources=sources,
        docs=docs,
        model=model,
        rewritten_query=rewritten if rewritten != question else "",
        is_grounded=is_grounded,
        pipeline_log=log,
    )


# ── Backwards-compatible wrappers ────────────────────────────────────────────

def build_chain(
    vectorstore: Chroma,
    model: str = "gpt-4o-mini",
    n_results: int = 5,
    filter_topic: str | None = None,
    filter_content_type: str | None = None,
) -> Runnable:
    """Build LCEL retrieval chain (legacy wrapper kept for compatibility)."""
    search_kwargs: dict = {"k": n_results}
    filters = {}
    if filter_topic:
        filters["topic"] = filter_topic
    if filter_content_type:
        filters["content_type"] = filter_content_type
    if filters:
        search_kwargs["filter"] = filters

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    llm = ChatOpenAI(model=model, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    chain = (
        RunnablePassthrough.assign(context=lambda x: retriever.invoke(x["input"]))
        | RunnablePassthrough.assign(
            answer=lambda x: (
                prompt | llm | StrOutputParser()
            ).invoke({"input": x["input"], "context": _format_docs(x["context"])})
        )
    )
    return chain


def ask(chain: Runnable, question: str, model: str = "gpt-4o-mini") -> QAResult:
    """Run the chain and return answer + structured sources (legacy wrapper)."""
    result = chain.invoke({"input": question})
    sources = [_doc_to_source(doc) for doc in result.get("context", [])]
    return QAResult(answer=result["answer"], sources=sources, model=model)
