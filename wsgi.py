"""WSGI entry point for gunicorn."""

from pathlib import Path

from core.config import DEFAULT_DOCS_ROOT, DEFAULT_PROCESSED_DIR
from api.routes import create_app

app = create_app(
    docs_root=Path(DEFAULT_DOCS_ROOT), processed_dir=Path(DEFAULT_PROCESSED_DIR)
)
