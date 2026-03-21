"""Batch text embeddings via OpenAI text-embedding-3-small."""
import logging
import time

from openai import APIError, OpenAI, RateLimitError

from core.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

_MAX_RETRIES = 5
_BASE_DELAY = 1.0


def embed_texts(
    texts: list[str],
    client: OpenAI,
    batch_size: int = 100,
) -> list[list[float]]:
    """Embed all texts in batches. Returns list of embedding vectors in input order."""
    results: list[list[float] | None] = [None] * len(texts)

    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        vectors = _embed_batch_with_retry(batch, client)
        for j, vec in enumerate(vectors):
            results[start + j] = vec

    # Mypy: all should be filled now
    return [v for v in results if v is not None]


def _embed_batch_with_retry(texts: list[str], client: OpenAI) -> list[list[float]]:
    delay = _BASE_DELAY
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=texts,
            )
            # response.data is ordered by index
            return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
        except RateLimitError:
            if attempt == _MAX_RETRIES - 1:
                logger.error("Rate limit exceeded after %d retries, skipping batch", _MAX_RETRIES)
                raise
            logger.warning("Rate limit hit, retrying in %.1fs (attempt %d/%d)", delay, attempt + 1, _MAX_RETRIES)
            time.sleep(delay)
            delay *= 2
        except APIError as e:
            if attempt == _MAX_RETRIES - 1:
                logger.error("API error after %d retries: %s", _MAX_RETRIES, e)
                raise
            logger.warning("API error %s, retrying in %.1fs (attempt %d/%d)", e, delay, attempt + 1, _MAX_RETRIES)
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("embed_batch_with_retry exhausted without returning")
