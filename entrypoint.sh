#!/bin/bash
set -e

PYTHON=".venv/bin/python"
GUNICORN=".venv/bin/gunicorn"

# Auto-run ingestion if ChromaDB is empty
if [ ! -d "./chroma_db" ] || [ -z "$(ls -A ./chroma_db 2>/dev/null)" ]; then
    echo "ChromaDB is empty — running ingestion pipeline..."
    $PYTHON -m retrieval --verbose
    echo "Ingestion complete."
else
    echo "ChromaDB data found — skipping ingestion."
fi

# Start gunicorn
exec $GUNICORN wsgi:app \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile -
