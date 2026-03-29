# ---- Builder stage ----
FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code and install the project
COPY src/ src/
COPY wsgi.py .
RUN uv sync --frozen --no-dev

# Pre-download cross-encoder model to avoid cold-start delay
RUN uv run python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# ---- Runtime stage ----
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy venv, source, and model cache from builder
COPY --from=builder /app/.venv .venv/
COPY --from=builder /app/pyproject.toml /app/uv.lock ./
COPY --from=builder /app/src/ src/
COPY --from=builder /app/wsgi.py .
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

# Copy pre-built ingestion data (baked into image — no runtime ingestion needed)
COPY chroma_db/ chroma_db/
COPY data/processed/ data/processed/

# Copy ground truth data (needed for eval endpoints)
COPY data/ground_truth/ data/ground_truth/

# Copy docs corpus (needed for file viewer)
COPY openshift-docs/ openshift-docs/

EXPOSE 8000

CMD [".venv/bin/gunicorn", "wsgi:app", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "300", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
