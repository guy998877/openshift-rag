"""Orchestrates all ingestion stages."""

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm

from retrieval import attributes, discover, embed, meta_extract, store
from core.config import DEFAULT_BATCH_SIZE, KEEP_CONTENT_TYPES, TARGET_DIRS
from retrieval.discover import ModuleInfo
from retrieval.preprocess import preprocess

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    docs_root: Path
    processed_dir: Path
    chroma_dir: Path
    collection_name: str
    target_dirs: list[str] = None
    content_types: set[str] = None
    skip_embed: bool = False
    skip_store: bool = False
    reprocess: bool = False
    dry_run: bool = False
    batch_size: int = DEFAULT_BATCH_SIZE

    def __post_init__(self):
        if self.target_dirs is None:
            self.target_dirs = TARGET_DIRS
        if self.content_types is None:
            self.content_types = KEEP_CONTENT_TYPES


@dataclass
class PipelineResult:
    discovered: int = 0
    processed: int = 0
    skipped: int = 0
    stored: int = 0
    skip_log: list[dict] = None

    def __post_init__(self):
        if self.skip_log is None:
            self.skip_log = []


def run(cfg: PipelineConfig, openai_client: OpenAI | None = None) -> PipelineResult:
    result = PipelineResult()

    # Stage 1: Discover
    logger.info("Discovering modules in %s ...", cfg.docs_root)
    attrs = attributes.load(cfg.docs_root)
    modules = discover.discover(cfg.docs_root, cfg.target_dirs, cfg.content_types)
    result.discovered = len(modules)
    logger.info("Discovered %d modules", result.discovered)

    if cfg.dry_run:
        _print_dry_run_stats(modules)
        return result

    cfg.processed_dir.mkdir(parents=True, exist_ok=True)

    # Stage 2: Preprocess
    ready_modules: list[ModuleInfo] = []
    ready_texts: list[str] = []
    ready_titles: list[str] = []
    ready_metas: list[dict] = []

    for mod in tqdm(modules, desc="Preprocessing", unit="file"):
        out_path = cfg.processed_dir / (mod.filename.removesuffix(".adoc") + ".md")

        if out_path.exists() and not cfg.reprocess:
            # Load from cache
            try:
                content = out_path.read_text(encoding="utf-8")
                title = _extract_title(content)
                ready_modules.append(mod)
                ready_texts.append(content)
                ready_titles.append(title)
                ready_metas.append(meta_extract.extract(content, mod))
                result.processed += 1
                continue
            except OSError:
                pass

        try:
            title, markdown = preprocess(mod.path, attrs)
            out_path.write_text(markdown, encoding="utf-8")
            ready_modules.append(mod)
            ready_texts.append(markdown)
            ready_titles.append(title)
            ready_metas.append(meta_extract.extract(markdown, mod))
            result.processed += 1
        except Exception as e:
            reason = str(e)
            logger.error("Preprocess failed for %s: %s", mod.filename, reason)
            result.skipped += 1
            result.skip_log.append(
                {"file": mod.filename, "stage": "preprocess", "reason": reason}
            )

    logger.info("Preprocessed: %d | Skipped: %d", result.processed, result.skipped)

    if cfg.skip_embed:
        logger.info("--skip-embed set, stopping after preprocess")
        _write_skip_log(cfg, result.skip_log)
        return result

    if not openai_client:
        openai_client = OpenAI()

    # Stage 3: Embed + Stage 4: Store (in batches)
    collection = None
    if not cfg.skip_store:
        cfg.chroma_dir.mkdir(parents=True, exist_ok=True)
        collection = store.get_collection(cfg.chroma_dir, cfg.collection_name)

    for start in tqdm(
        range(0, len(ready_modules), cfg.batch_size),
        desc="Embedding+Storing",
        unit="batch",
    ):
        end = start + cfg.batch_size
        batch_modules = ready_modules[start:end]
        batch_texts = ready_texts[start:end]
        batch_titles = ready_titles[start:end]
        batch_metas = ready_metas[start:end]

        try:
            vectors = embed.embed_texts(
                batch_texts, openai_client, batch_size=len(batch_texts)
            )
        except Exception as e:
            logger.error("Embedding batch %d-%d failed: %s", start, end, e)
            for m in batch_modules:
                result.skipped += 1
                result.skip_log.append(
                    {"file": m.filename, "stage": "embed", "reason": str(e)}
                )
            continue

        if cfg.skip_store or collection is None:
            continue

        n = store.upsert_batch(
            collection, batch_modules, batch_texts, vectors, batch_titles, batch_metas
        )
        result.stored += n
        if n < len(batch_modules):
            skipped_in_batch = len(batch_modules) - n
            result.skipped += skipped_in_batch
            for m in batch_modules[n:]:
                result.skip_log.append(
                    {"file": m.filename, "stage": "store", "reason": "upsert failed"}
                )

    logger.info(
        "Done. Processed: %d | Skipped: %d | Stored: %d",
        result.processed,
        result.skipped,
        result.stored,
    )

    _write_skip_log(cfg, result.skip_log)
    return result


def _extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _write_skip_log(cfg: PipelineConfig, skip_log: list[dict]) -> None:
    skip_path = Path("data/skipped.jsonl")
    skip_path.parent.mkdir(parents=True, exist_ok=True)
    with skip_path.open("w", encoding="utf-8") as f:
        for entry in skip_log:
            f.write(json.dumps(entry) + "\n")
    if skip_log:
        logger.info("Skip log written to %s (%d entries)", skip_path, len(skip_log))


def _print_dry_run_stats(modules: list[ModuleInfo]) -> None:
    from collections import Counter

    type_counts = Counter(m.content_type for m in modules)
    topic_counts = Counter(m.topic for m in modules)
    print("\n=== Dry Run ===")
    print(f"Total modules: {len(modules)}")
    print("\nBy content type:")
    for ct, n in sorted(type_counts.items()):
        print(f"  {ct}: {n}")
    print("\nBy topic:")
    for topic, n in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {topic}: {n}")
