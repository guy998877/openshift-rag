"""ChromaDB upsert operations."""
import logging
from pathlib import Path

import chromadb

from retrieval.discover import ModuleInfo

logger = logging.getLogger(__name__)

COLLECTION_NAME = "openshift_docs_v0"


def get_collection(chroma_dir: Path, collection_name: str) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def upsert_batch(
    collection: chromadb.Collection,
    modules: list[ModuleInfo],
    texts: list[str],
    embeddings: list[list[float]],
    titles: list[str],
    extracted_metas: list[dict] | None = None,
) -> int:
    """Upsert a batch of documents. Returns count of successfully upserted items."""
    ids = [_chunk_id(m.filename) for m in modules]
    if extracted_metas is None:
        extracted_metas = [{} for _ in modules]
    metadatas = [
        {**_make_metadata(m, t), **em}
        for m, t, em in zip(modules, titles, extracted_metas)
    ]

    try:
        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(ids)
    except Exception as e:
        logger.error("ChromaDB upsert failed: %s", e)
        return 0


def _chunk_id(filename: str) -> str:
    return filename.removesuffix(".adoc")


def _make_metadata(m: ModuleInfo, title: str) -> dict:
    return {
        "file": m.filename,
        "content_type": m.content_type,
        "title": title,
        "topic": m.topic,
        "source_dir": m.source_dirs[0] if m.source_dirs else "",
        "source_dirs_all": ",".join(m.source_dirs),
    }
