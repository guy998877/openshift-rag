# openshift-rag

> RAG system for OpenShift documentation — answers operational questions from platform engineers, cluster admins, and SREs using the official OpenShift docs corpus.

![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)
![ChromaDB](https://img.shields.io/badge/vector--store-ChromaDB-orange)
![License](https://img.shields.io/badge/license-MIT-green)

<video src="https://github.com/user-attachments/assets/56261b95-a12f-4167-a48d-8b5c99d284a9" controls width="100%"></video>

---

## What it does

Ask operational questions in plain English and get answers grounded in the official OpenShift documentation:

```
"How do I drain a node before maintenance?"
"What is the difference between a Route and an Ingress?"
"How do I configure cluster autoscaling on ROSA?"
```

The pipeline runs **query rewriting → hybrid BM25 + vector retrieval → cross-encoder reranking → GPT-4o-mini generation**, all against ~11,000 AsciiDoc modules from the OpenShift docs corpus.

---

## Getting started

### Prerequisites

| Requirement | Version |
|---|---|
| Python | ≥ 3.13 |
| [`uv`](https://docs.astral.sh/uv/getting-started/installation/) | latest |
| OpenAI API key | — |

### Install

```bash
uv sync
```

### Configure

```bash
# Create .env with your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env
```

### Ingest the docs corpus

> Only needs to be run once (or again if the corpus changes).

```bash
uv run python -m retrieval --verbose
```

This will:
1. Discover ~1,500 modules across 14 topic directories
2. Convert AsciiDoc → Markdown (resolving attributes and conditionals)
3. Embed with `text-embedding-3-small` and store in `chroma_db/`

---

## Usage

### Web UI

```bash
uv run python -m api
```

Open **http://127.0.0.1:5000** — use the **Query** tab to ask questions and adjust retrieval settings (model, k, topic filter, content type).

```bash
uv run python -m api --port 8080   # custom port
```

### CLI

```bash
uv run python -m services "how do I drain a node before maintenance?"
```

| Flag | Effect |
|---|---|
| `--show-pipeline` | Print timing + rewritten query |
| `--retrieve-only` | Show retrieved chunks, skip generation |
| `--no-rewrite` | Skip query rewriting |
| `--no-hybrid` | Vector search only |
| `--no-rerank` | Skip cross-encoder reranking |
| `--grounding` | Enable grounding check |
| `--n-results N` | Number of chunks (default: 5) |

---

## Evaluation

The project includes a full eval suite with LLM-as-judge scoring, a hyperparameter grid search, and both synthetic and real-user (Stack Overflow) benchmarks.

### Run retrieval benchmark

```bash
uv run python -m eval                        # hybrid (default)
uv run python -m eval --mode semantic        # vector only
uv run python -m eval --mode keyword         # BM25 only
uv run python -m eval --n 10                 # quick sanity check
```

### Run LLM-as-judge grid search

Sweeps all combinations of model / k / retrieval mode / rerank / rewrite and ranks by composite score:

```bash
uv run python -m eval.grid_search
uv run python -m eval.grid_search --n 10 --workers 8
```

### Collect real-user benchmark from Stack Overflow

```bash
uv run python -m eval.collect_so_benchmark --max 500
```

### Analyse grid search results

```bash
uv run python -m eval.analysis --results-dir data/eval_results/grid_search/<run>
```

---

## Project structure

```
src/
├── core/        # Shared config (paths, embedding model, attributes)
├── retrieval/   # Ingestion pipeline + BM25 / vector / hybrid search
├── services/    # RAG pipeline (rewrite → retrieve → rerank → generate)
├── api/         # Flask web UI
└── eval/        # Benchmarks, grid search, LLM-as-judge, SO collector
data/
└── ground_truth/
    └── queries.json    # 100-query synthetic benchmark
chroma_db/              # ChromaDB vector store (generated)
openshift-docs/         # AsciiDoc corpus (~11k files)
```
