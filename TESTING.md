# Testing & CI/CD Strategy

This document explains the automated testing and CI infrastructure for the RAG OpenShift Documentation project.

---

## Overview

The project uses a **multi-layer testing strategy** to catch bugs at different stages:

```
                     ┌─ Lint (code quality)
                     │
  Every Push    ─────┼─ Unit Tests (preprocessing, evaluation logic)
  to main/PR    │
                     ├─ API Tests (endpoints, validation)
                     │
                     ├─ Retrieval Tests (BM25 ranking)
                     │
                     ├─ Integration Test (real OpenAI pipeline) [if secret]
                     │
                     ├─ K8s Validation (manifest syntax)
                     │
                     ├─ Docker Build (dependency check)
                     │
                     └─ Secret Scan (credential leaks)
```

---

## Test Layers

### 1. Unit Tests (Existing)

**Files:** `tests/test_preprocess.py`, `tests/test_attributes.py`, `tests/test_collect_so.py`

These test low-level utility functions — no external dependencies, no API calls.

| Test | Purpose | Example |
|---|---|---|
| `test_process_conditionals` | Verify AsciiDoc `ifdef` block handling | `ifdef::openshift-enterprise[]` removes ROSA-only content |
| `test_convert_markup` | Verify AsciiDoc → Markdown conversion | `== Heading` → `## Heading` |
| `test_resolve_text` | Verify attribute substitution | `{product-title}` → "OpenShift Container Platform" |
| `test_infer_topic` | Verify Stack Overflow topic classification | Tags `["openshift", "operator"]` → topic="operators" |

**Run locally:**
```bash
uv run pytest tests/test_preprocess.py tests/test_attributes.py tests/test_collect_so.py -v
```

---

### 2. API Tests (New)

**File:** `tests/test_api.py`

Tests the Flask backend using a test client. Each test creates minimal fixtures (temp docs) — no dependency on local `chroma_db/` or `openshift-docs/`.

#### Endpoint: `/healthz` (Health Check)

Used by Kubernetes readiness probes. Must respond quickly with JSON status.

| Test | What | Example |
|---|---|---|
| `test_returns_ok_status` | Status code 200 + JSON | `GET /healthz` → `{"status": "ok"}` |
| `test_content_type_is_json` | Response type is JSON | Content-Type header contains `application/json` |

**Run locally:**
```bash
uv run pytest tests/test_api.py::TestHealthz -v
```

#### Endpoint: `/api/files` (List Documents)

Returns metadata for all preprocessed markdown files. Used by web UI file dropdown.

| Test | What | Example |
|---|---|---|
| `test_returns_list_of_processed_files` | Returns JSON list | `GET /api/files` → 2 file objects |
| `test_file_ids_match_stems` | IDs are markdown filenames without `.adoc` | File `install-ocp.md` → `id="install-ocp"` |
| `test_each_file_has_required_fields` | All required metadata present | Fields: `id`, `filename`, `content_type`, `topic` |
| `test_empty_processed_dir_returns_empty_list` | Gracefully handle missing data | No docs → `[]` |

**Run locally:**
```bash
uv run pytest tests/test_api.py::TestListFiles -v
```

#### Endpoint: `/api/query` (Question Answering)

The core RAG endpoint. Accepts a question, returns an answer + sources.

| Test | What | Example |
|---|---|---|
| `test_missing_question_returns_validation_error` | Reject empty body | `POST /api/query` `{}` → error |
| `test_empty_question_returns_validation_error` | Reject whitespace query | `{"question": "   "}` → error |
| `test_no_api_key_returns_error` | Fail gracefully without OpenAI key | `OPENAI_API_KEY=unset` → error message |

**Run locally:**
```bash
uv run pytest tests/test_api.py::TestQuery -m "not integration" -v
```

---

### 3. Retrieval Tests (New)

**File:** `tests/test_hybrid_retrieval.py`

Tests the BM25 keyword search index. Fast (no API calls) and deterministic.

#### BM25 Ranking (Relevance)

Verify that topic-specific queries rank relevant documents first.

| Test | Query | Expected Top Rank |
|---|---|---|
| `test_installation_query_ranks_install_doc_first` | "install OpenShift nodes requirements" | `install-requirements` |
| `test_upgrade_query_ranks_upgrade_doc_first` | "upgrade cluster oc adm rolling" | `upgrade-cluster` |
| `test_network_query_ranks_network_doc_first` | "NetworkPolicy restrict pod traffic" | `network-policy` |
| `test_storage_query_ranks_storage_doc_first` | "PersistentVolumeClaim storage stateful" | `storage-pvc` |
| `test_rbac_query_ranks_rbac_doc_first` | "ClusterRole RoleBinding RBAC permissions" | `rbac-roles` |

**Run locally:**
```bash
uv run pytest tests/test_hybrid_retrieval.py::TestBM25IndexSearch -v
```

#### BM25 Scoring (Normalization & Sorting)

Verify scores are normalized and sorted consistently.

| Test | What | Example |
|---|---|---|
| `test_scores_normalised_between_zero_and_one` | All scores in [0.0, 1.0] | Raw `[15.2, 8.5]` → normalized `[1.0, 0.56]` |
| `test_top_score_is_one` | Highest score is always 1.0 | First result has score=1.0 |
| `test_scores_are_descending` | Results sorted by score descending | `[1.0, 0.85, 0.72, ...]` |
| `test_k_parameter_limits_number_of_results` | Parameter `k` limits results | `search(query, k=2)` returns 2 max |
| `test_k_larger_than_corpus_returns_all_docs` | Don't return non-existent results | `search(k=1000)` with 5 docs → 5 results |

**Run locally:**
```bash
uv run pytest tests/test_hybrid_retrieval.py::TestBM25IndexScoring -v
```

#### Edge Cases

Robustness under unusual inputs.

| Test | Scenario | Expected |
|---|---|---|
| `test_empty_processed_dir_returns_empty_list` | No documents at all | Returns `[]` |
| `test_unrelated_query_still_returns_list` | Query has no keywords in docs | Still returns list (scores may be 0) |
| `test_result_is_list_of_stem_score_tuples` | Return type is always consistent | Each result is `(stem: str, score: float)` |

**Run locally:**
```bash
uv run pytest tests/test_hybrid_retrieval.py::TestBM25IndexEdgeCases -v
```

---

### 4. Integration Test (New)

**File:** `tests/test_api.py::TestQuery::test_full_pipeline_returns_grounded_answer`

**Mark:** `@pytest.mark.integration`

End-to-end test using real OpenAI API. Validates the complete RAG pipeline works together.

#### What It Does

1. Create 3 realistic OpenShift docs (install, upgrade, network)
2. Call OpenAI's `text-embedding-3-small` to embed each doc
3. Store embeddings in in-memory Qdrant (no local chroma_db needed)
4. Run `run_pipeline()` with a natural question
5. Assert the LLM returns a meaningful answer + document sources

#### Example

```python
# Question about installation
question = "How many nodes do I need to install OpenShift?"

# Context (3 docs with embeddings)
docs = [
    "Installing OpenShift requires 3 control plane nodes and 2 worker nodes...",
    "To upgrade your cluster run oc adm upgrade...",
    "Configure NetworkPolicy to restrict pod traffic..."
]

# Expected output
result.answer = "You need 3 control plane nodes and 2 worker nodes to install OpenShift..."
result.sources = [
    {"id": "install-requirements", "title": "Installation Requirements", ...},
    {"id": "upgrade-cluster", "title": "Upgrade Procedure", ...}
]
```

#### Requirements

- `OPENAI_API_KEY` environment variable must be set
- ~30-60s runtime (API latency)
- Only runs when marked `@pytest.mark.integration`

#### Run Locally

```bash
# Run only if OPENAI_API_KEY is set
OPENAI_API_KEY=sk-... uv run pytest tests/test_api.py -m integration -v

# Skip integration tests (no API key)
uv run pytest tests/test_api.py -m "not integration" -v
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/ci.yml`

Runs automatically on every push and pull request to `main`.

#### Jobs (Parallel)

| Job | Purpose | Duration | Failure = PR blocked? |
|---|---|---|---|
| **lint** | `ruff check` + format | 5-10s | ✓ Yes |
| **test** | `pytest tests/` (unit + retrieval) | 10-15s | ✓ Yes |
| **smoke-test** | Import check | 5s | ✓ Yes |
| **check-secrets** | TruffleHog credential scan | 10-20s | ✓ Yes |
| **lockfile-check** | Verify `uv.lock` sync | 5s | ✓ Yes |
| **integration-test** | Real OpenAI pipeline (if secret set) | 30-60s | ✓ Yes (if runs) |
| **k8s-validate** | `kubeconform` manifest validation | 5s | ✓ Yes |
| **docker-build** | Build Docker image | 45-60s | ✓ Yes |

#### Total Time

- **Without integration test:** ~1-2 minutes (secret not set)
- **With integration test:** ~2-3 minutes (secret set in GitHub)

### Job Details

#### `integration-test` Job

```yaml
if: ${{ secrets.OPENAI_API_KEY != '' }}  # Only runs if secret configured
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
run: uv run pytest tests/ -m integration -v --tb=short
```

**When it runs:**
- ✓ In repositories with the `OPENAI_API_KEY` GitHub secret configured
- ✗ In forks without the secret (skipped gracefully)

**What it tests:**
- Full end-to-end RAG pipeline with real OpenAI calls
- Proves embeddings + storage + retrieval + generation all work together

#### `k8s-validate` Job

```yaml
download: kubeconform
run: kubeconform -strict -summary k8s/*.yaml
```

**What it validates:**
- K8s manifests against official JSON schemas
- YAML syntax errors
- Invalid field names or types
- Missing required fields

**Example error caught:**
```yaml
# Bad: typo in metadata
apiVersion: v1
kind: Deployment
metadata:
  name: my-app
  lables:  # ✗ Wrong — should be 'labels'
    app: my-app
```

Output:
```
k8s/deployment.yaml - JSON Schema validation error: unexpected field 'lables'
```

#### `docker-build` Job

```yaml
run: mkdir -p chroma_db data/processed data/ground_truth
run: docker build -t rag-openshift-doco:ci .
```

**What it catches:**
- Missing base image from registry
- Broken dependencies in `RUN` commands
- COPY source paths that don't exist
- Syntax errors in multi-stage build

**Example error caught:**
```
Step 5/10: RUN uv sync --frozen --no-dev
ERROR: package 'nonexistent-package>=1.0.0' not found in PyPI registry
```

---

## Running Tests Locally

### Quick (Unit + Retrieval)

```bash
# All tests except integration (fast, no API key)
uv run pytest tests/ -m "not integration" -v

# Only specific test class
uv run pytest tests/test_api.py::TestHealthz -v
```

### Full (Including Integration)

```bash
# All tests with real API calls
OPENAI_API_KEY=sk-... uv run pytest tests/ -v
```

### By Category

```bash
# Unit only (preprocess, attributes, SO eval)
uv run pytest tests/test_preprocess.py tests/test_attributes.py -v

# API only
uv run pytest tests/test_api.py -v

# BM25/retrieval only
uv run pytest tests/test_hybrid_retrieval.py -v

# Integration only
OPENAI_API_KEY=sk-... uv run pytest tests/test_api.py -m integration -v
```

### K8s Validation

```bash
# Install kubeconform
brew install kubeconform

# Validate manifests
kubeconform -strict -summary k8s/*.yaml
```

### Docker Build

```bash
# Create placeholder dirs
mkdir -p chroma_db data/processed data/ground_truth

# Build image
docker build -t rag-openshift-doco:ci .
```

---

## Test Markers

Tests are organized with pytest markers for selective execution.

**Defined markers:**
- `integration` — requires OPENAI_API_KEY, ~30-60s per test

**Usage:**
```bash
# Run only integration tests
pytest -m integration

# Run everything except integration
pytest -m "not integration"

# Run tests matching a pattern
pytest -k "test_healthz"
```

---

## CI/CD for Interview

**What to emphasize:**

1. **Comprehensive coverage** — tests cover API endpoints, retrieval logic, and end-to-end RAG pipeline
2. **Real-world validation** — integration test uses actual OpenAI embeddings to prove the pipeline works
3. **Infrastructure validation** — K8s manifests and Docker image are always deployable
4. **Fast feedback** — ~2 min total, failures block PRs immediately
5. **Accessible** — tests run locally with `uv run pytest`; CI replicates the same environment

**Example talking points for the interview:**

> "I built a CI pipeline that validates the system at multiple layers. The integration test uses real OpenAI embeddings to prove the entire RAG pipeline works end-to-end. K8s manifest validation catches configuration errors before deploy. Docker build validation ensures dependencies are always available. Everything runs in parallel and fails fast — total time ~2 minutes per PR."

---

## Troubleshooting

### Import Errors in Tests

```
ImportError: cannot import name 'DEFAULT_CHROMA_DIR' from 'core.config'
```

**Cause:** Tests are running against a different branch version than expected.

**Fix:**
```bash
git checkout main
uv sync
uv run pytest tests/
```

### Integration Test Timeout

```
TimeoutError: test took too long
```

**Cause:** OpenAI API is slow or unreachable.

**Fix:**
- Check internet connection
- Verify `OPENAI_API_KEY` is valid
- Run locally with longer timeout: `pytest --timeout=120`

### K8s Validation Fails on CRDs

```
error: JSON schema not found for kubevirt.io/VirtualMachine
```

**Reason:** KubeVirt CRDs don't have public JSON schemas.

**Fix:** The CI job currently skips `k8s/kubevirt/` — it's in a separate directory.

---

## References

- [pytest documentation](https://docs.pytest.org)
- [GitHub Actions workflows](https://docs.github.com/en/actions/using-workflows)
- [kubeconform documentation](https://www.kubewarden.io/docs/validation/)
