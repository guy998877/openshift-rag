"""CLI entry point for the OpenShift docs ingestion pipeline."""
import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from ingest.config import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_CHROMA_DIR,
    DEFAULT_COLLECTION,
    DEFAULT_DOCS_ROOT,
    DEFAULT_PROCESSED_DIR,
    TARGET_DIRS,
)
from ingest.pipeline import PipelineConfig, run


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="python -m ingest",
        description="Preprocess and ingest OpenShift docs into ChromaDB",
    )
    parser.add_argument("--docs-root", type=Path, default=DEFAULT_DOCS_ROOT)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--chroma-dir", type=Path, default=DEFAULT_CHROMA_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--topics", nargs="+", metavar="TOPIC", help="Override target dirs")
    parser.add_argument(
        "--content-types",
        nargs="+",
        metavar="TYPE",
        default=["PROCEDURE", "CONCEPT"],
        choices=["PROCEDURE", "CONCEPT", "REFERENCE", "ASSEMBLY"],
    )
    parser.add_argument("--skip-embed", action="store_true", help="Preprocess only")
    parser.add_argument("--skip-store", action="store_true", help="Embed but don't write to Chroma")
    parser.add_argument("--reprocess", action="store_true", help="Re-run preprocessing even if .md exists")
    parser.add_argument("--dry-run", action="store_true", help="Discover + report counts only")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    _setup_logging(args.verbose)

    cfg = PipelineConfig(
        docs_root=args.docs_root,
        processed_dir=args.processed_dir,
        chroma_dir=args.chroma_dir,
        collection_name=args.collection,
        target_dirs=args.topics or TARGET_DIRS,
        content_types=set(args.content_types),
        skip_embed=args.skip_embed,
        skip_store=args.skip_store,
        reprocess=args.reprocess,
        dry_run=args.dry_run,
        batch_size=args.batch_size,
    )

    try:
        result = run(cfg)
    except FileNotFoundError as e:
        logging.critical("Fatal: %s", e)
        sys.exit(2)
    except KeyboardInterrupt:
        logging.warning("Interrupted by user")
        sys.exit(1)

    if result.skip_log:
        sys.exit(1)
    sys.exit(0)


def _setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            _rotating_file_handler(),
        ],
    )


def _rotating_file_handler() -> logging.Handler:
    from logging.handlers import RotatingFileHandler
    log_path = Path("data/pipeline.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,
        encoding="utf-8",
    )
