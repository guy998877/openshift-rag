# CI/CD Pipeline Explained

A comprehensive guide to Continuous Integration (CI) in this project, how it works, and why each job exists.

---

## What is CI (Continuous Integration)?

### The Problem It Solves

Imagine working on a team where:

```
Developer A writes code ─→ Works on their machine
Developer B writes code ─→ Works on their machine
They merge together    ─→ Everything breaks! 🔥
```

**Why?** Because they only tested their own changes locally. They never:
- Tested together in the same environment
- Ran comprehensive tests
- Checked for broken dependencies
- Validated the actual deployment

### The Solution: Continuous Integration

**CI is an automated system that:**

1. **Watches** for code changes (every push, every PR)
2. **Builds** the project in a clean environment
3. **Tests** everything automatically (no human needed)
4. **Reports** results back to you in seconds
5. **Blocks** merging if tests fail

**Benefits:**
- ✅ Catch bugs **before** they reach users
- ✅ Prevent broken code from merging to `main`
- ✅ Everyone knows the code status without asking
- ✅ Faster feedback: issues found in seconds, not days
- ✅ Confidence that deployments will work

---

## How CI Works in This Project

### Architecture

```
You push code to GitHub
         │
         ▼
GitHub detects push/PR
         │
         ▼
Triggers CI workflow (.github/workflows/ci.yml)
         │
         ▼
Spins up clean Ubuntu VM (no local environment)
         │
         ▼
Runs all jobs in parallel:
  ├─ Lint
  ├─ Test
  ├─ Smoke-test
  ├─ Secret-scan
  ├─ Lockfile-check
  ├─ Integration-test [if OPENAI_API_KEY secret]
  ├─ K8s-validate
  └─ Docker-build
         │
         ▼
All jobs must pass
         │
         ▼
✅ PR can merge to main
   OR
❌ PR blocked with failure details
```

### Technology: GitHub Actions

**GitHub Actions** is GitHub's built-in CI/CD platform. It's:
- Free for public repos
- Includes 2000 free minutes/month for private repos
- Runs on GitHub's servers (no setup needed)
- Triggered by events (push, PR, schedule, manual)
- Defined in YAML files in `.github/workflows/`

---

## The CI Workflow File

**Location:** `.github/workflows/ci.yml`

**Structure:**
```yaml
name: CI

on:                           # ← When does this trigger?
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel_in_progress: true

jobs:                         # ← What runs?
  lint:
    ...
  test:
    ...
  integration-test:
    ...
  # ... more jobs
```

### Trigger Events

**When do tests run?**

```yaml
on:
  push:
    branches: [main]           ← Every commit pushed to main
  pull_request:
    branches: [main]           ← Every PR created/updated targeting main
```

#### Example Scenarios

**Scenario 1: Commit to Feature Branch**
```
git checkout -b feature/my-feature
git commit -m "Add new test"
git push origin feature/my-feature

❌ CI does NOT run (not pushing to main)
```

**Scenario 2: Create Pull Request**
```
You create PR: feature/my-feature → main

✅ CI runs automatically
   (GitHub detects PR targets main branch)

Results appear in the PR:
[✓ All checks passed]  ← Click to see details
```

**Scenario 3: Push to Main**
```
git push origin main

✅ CI runs immediately
   (GitHub detects push to main)

You see status in commit history:
[✓] abc1234 Add feature (1 min ago) ← Click for details
```

### Concurrency Control

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel_in_progress: true
```

**What it does:**
- Only one CI run per branch at a time
- If you push twice quickly, the first run cancels
- Saves time and GitHub Actions minutes

**Example:**
```
You push commit A → CI starts (Lint, Test, ...)
You push commit B → Commit A's CI cancels
                 → CI starts fresh for commit B
```

---

## The Jobs (Explained)

### Overview

| Job | Time | Purpose | Failure = Block? |
|---|---|---|---|
| **lint** | 5-10s | Code quality (ruff) | ✅ Yes |
| **test** | 10-15s | Unit + retrieval tests | ✅ Yes |
| **smoke-test** | 5s | Import check | ✅ Yes |
| **check-secrets** | 10-20s | Credential leak scan | ✅ Yes |
| **lockfile-check** | 5s | Dependency lock validation | ✅ Yes |
| **integration-test** | 30-60s | Real OpenAI pipeline | ✅ Yes (if runs) |
| **k8s-validate** | 5s | K8s manifest syntax | ✅ Yes |
| **docker-build** | 45-60s | Docker image build | ✅ Yes |

---

## Job #1: Lint

### What It Does

Checks code style and formatting using `ruff`.

```yaml
lint:
  name: Lint & Format
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    - run: uv python install 3.13
    - run: uv sync --dev
    - run: uv run ruff check src/ tests/        # ← Lint check
    - run: uv run ruff format --check src/ tests/  # ← Format check
```

### Why It Matters

**Problem:** Without linting, code can have:
- Inconsistent style (spaces vs tabs, naming conventions)
- Unused imports (`import os` but never used)
- Unused variables (`x = 5` but never referenced)
- Syntax issues

**Ruff catches:**
```python
# ❌ Unused import
import os
from pathlib import Path

def process_file():
    return Path("file.txt")  # os never used
```

Output:
```
src/api/routes.py:1:1: F401 [*] `os` imported but unused
```

### Example Failure

```bash
# Developer writes bad code
x = 5  # unused variable

# CI runs lint job
$ ruff check src/

src/core/config.py:15:1: F841 [*] Local variable `x` is assigned to but never used

❌ Lint fails
❌ PR cannot merge
👉 Developer fixes it (delete x = 5) and pushes again
```

### When It Runs

✅ Every push to any branch
✅ Every PR (even draft)
✅ Fast feedback (~5-10s)

---

## Job #2: Test

### What It Does

Runs all unit and retrieval tests using pytest.

```yaml
test:
  name: Tests
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    - run: uv python install 3.13
    - run: uv sync --dev
    - run: uv run pytest tests/ -v --tb=short   # ← Run all tests
```

### Why It Matters

Tests verify that your code actually works. Without tests, you can have:

**Example:** Preprocessing function breaks

```python
# Old code (works)
def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:]
    return ""

# Developer changes it (breaks)
def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("#"):  # ← Forgot the space!
            return line[1:]       # ← Wrong index!
    return ""

# Tests catch the error
$ pytest tests/test_preprocess.py -v

tests/test_preprocess.py::TestExtractTitle::test_extracts_first_h1 FAILED
AssertionError: assert 'y Title' == 'My Title'
                           ^^^^^^

❌ Test fails
❌ PR cannot merge
👉 Developer sees test failure and fixes the bug
```

### What Gets Tested

```
77 tests total:

├─ test_preprocess.py (24 tests)
│  └─ Tests AsciiDoc → Markdown conversion
│     └─ Example: "== Heading" → "## Heading"
│
├─ test_attributes.py (8 tests)
│  └─ Tests variable substitution
│     └─ Example: "{product-title}" → "OpenShift"
│
├─ test_collect_so.py (13 tests)
│  └─ Tests Stack Overflow benchmark collection
│     └─ Example: Filter low-quality questions
│
├─ test_api.py (9 tests)      [NEW]
│  └─ Tests Flask endpoints
│     └─ Example: GET /healthz → {"status": "ok"}
│
└─ test_hybrid_retrieval.py (12 tests)  [NEW]
   └─ Tests BM25 keyword search
      └─ Example: Query "install" → ranks install-doc first
```

### Example Success

```bash
$ pytest tests/ -v

tests/test_api.py::TestHealthz::test_returns_ok_status PASSED [11%]
tests/test_api.py::TestListFiles::test_returns_list_of_processed_files PASSED [22%]
...
====================== 77 passed in 0.39s ======================

✅ All tests pass
✅ PR can proceed to next job
```

### When It Runs

✅ Every push to any branch
✅ Every PR
✅ Takes ~10-15 seconds
✅ Fast feedback

---

## Job #3: Smoke Test

### What It Does

Quick sanity check: can Python even import your modules?

```yaml
smoke-test:
  name: Import Smoke Test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    - run: uv python install 3.13
    - run: uv sync
    - run: |
        uv run python -c "import core; print('core OK')"
        uv run python -c "import retrieval; print('retrieval OK')"
        uv run python -c "import services; print('services OK')"
      env:
        OPENAI_API_KEY: "sk-fake-key-for-import-check"
```

### Why It Matters

Sometimes your code has **syntax errors** that prevent Python from even importing it.

**Example:**

```python
# ❌ Syntax error
def build_vectorstore(chroma_dir: Path, collection_name: str) -> Chroma
    # Missing colon at end!
    client = chromadb.PersistentClient(path=str(chroma_dir))
```

**What happens:**
```bash
$ python -c "import services"

SyntaxError: invalid syntax (services/pipeline.py, line 47)

❌ Smoke test fails
❌ The unittest job would fail too, but smoke-test fails FIRST
   (faster feedback)
```

### When It Runs

✅ Every push/PR
✅ Very fast (~5s)
✅ Catches obvious errors before running full tests

---

## Job #4: Check Secrets

### What It Does

Scans code for accidentally committed API keys, passwords, credentials.

```yaml
check-secrets:
  name: Secret Leak Check
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # ← Get full commit history
    - name: TruffleHog scan
      uses: trufflesecurity/trufflehog@main
      with:
        extra_args: --only-verified  # ← Only high-confidence matches
```

### Why It Matters

**The Disaster Scenario:**

```python
# ❌ Developer accidentally commits API key
OPENAI_API_KEY = "sk-proj-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0"

# They push to GitHub
git push origin feature/my-feature

# Now the key is on GitHub forever!
# Even if they delete it later, it's in git history

# Attackers scan for exposed keys
# They use the key to make expensive API calls on your dime!
```

### How TruffleHog Catches It

```bash
$ trufflehog git https://github.com/you/your-repo

Found verified secret: OpenAI API Key
  File: src/core/config.py
  Line: 42
  Secret: sk-proj-A1b2C3d4E5f...

❌ CI blocks the PR
👉 Developer removes the secret and re-pushes
```

### Real Example: `.env` File

```bash
# ❌ Never commit .env!
OPENAI_API_KEY=sk-proj-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0
SO_API_KEY=E6gow3RcHEzkMNLMeEo6gfJ6F

# CI catches this and blocks the PR
```

### When It Runs

✅ Every push/PR
✅ Scans commit history (so you can't hide it)
✅ Takes ~10-20s
✅ **Critical security check**

---

## Job #5: Lockfile Check

### What It Does

Verifies that `uv.lock` matches `pyproject.toml`.

```yaml
lockfile-check:
  name: Lockfile Integrity
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    - run: uv python install 3.13
    - run: uv lock --check  # ← Verify lock file is up to date
```

### Why It Matters

**The Problem:**

```
pyproject.toml (what you want):
  dependencies = [
    "openai>=2.29.0",
    "qdrant-client>=1.9.0",
  ]

uv.lock (what actually gets installed):
  openai==2.25.0    # ← Outdated!
  qdrant-client==1.8.0  # ← Outdated!
```

**If lock file is out of date:**
- Local dev: installs old versions
- CI: installs different old versions
- Production: installs yet different versions
- Result: "works on my machine" but not in production

### The Fix

```bash
# Developer adds new dependency
# They update pyproject.toml

[project]
dependencies = [
  "openai>=2.29.0",
  "qdrant-client>=1.9.0",
  "langchain>=1.2.12",  # ← NEW
]

# But they forget to run:
$ uv lock

# CI catches it:
$ uv lock --check
uv lock is out of date. Run `uv lock` to update

❌ CI fails
👉 Developer runs uv lock, commits uv.lock, and pushes again
```

### When It Runs

✅ Every push/PR
✅ Very fast (~5s)
✅ Ensures reproducible installs everywhere

---

## Job #6: Integration Test ⭐ (NEW)

### What It Does

**Runs a single test that exercises the ENTIRE RAG pipeline with real OpenAI API calls.**

```yaml
integration-test:
  name: Integration Tests (Real OpenAI)
  runs-on: ubuntu-latest
  if: ${{ secrets.OPENAI_API_KEY != '' }}  # ← Only if secret is set
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}  # ← Pass secret to test
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    - run: uv python install 3.13
    - run: uv sync --dev
    - run: uv run pytest tests/ -m integration -v --tb=short
```

### Why It Matters

**Unit tests are good, but they're isolated:**

```python
# ✅ Unit test: "Does BM25 ranking work?"
def test_bm25_ranks_correctly():
    index = BM25Index(tmp_files)
    results = index.search("query")
    assert results[0][0] == "expected-doc"

# ✅ But does the ENTIRE pipeline work together?
```

**Integration test answers:**

```python
@pytest.mark.integration
def test_full_pipeline_returns_grounded_answer():
    """
    Step 1: Create realistic docs
    Step 2: Embed with REAL OpenAI API
    Step 3: Store in Qdrant
    Step 4: Run the full RAG pipeline
    Step 5: Check if answer + sources are returned
    """
    # If this passes: The entire system works end-to-end!
```

### Example Test Flow

```
1. Input question:
   "How many nodes do I need to install OpenShift?"

2. System processes:
   ├─ Query rewriting (LLM rewrites query)
   ├─ Retrieval (BM25 + vector search)
   ├─ Re-ranking (Cross-encoder selects best docs)
   ├─ Generation (LLM generates answer from context)
   └─ Grounding check (Verify answer matches docs)

3. Output:
   answer = "You need 3 control plane nodes and 2 worker nodes..."
   sources = [
     {"id": "install-requirements", "title": "Installation Requirements"},
     {"id": "upgrade-cluster", "title": "Upgrade Procedure"}
   ]

4. Test asserts:
   ✅ answer is not empty
   ✅ answer mentions "node" / "3" / "control"
   ✅ sources are returned
   ✅ sources have correct structure
```

### When It Runs

⚠️ **Only if `OPENAI_API_KEY` secret is set in GitHub**

```yaml
if: ${{ secrets.OPENAI_API_KEY != '' }}
```

**Why conditional?**
- Expensive (costs money for real API calls: ~$0.001 per test)
- Takes time (30-60s per run vs 10s for unit tests)
- Only configured in your main repo, NOT in forks

**Scenarios:**

| Scenario | Secret Set? | Runs? |
|---|---|---|
| Push to main branch | ✅ Yes | ✅ Runs (~$0.001 cost) |
| PR from fork | ❌ No | ❌ Skipped (forks don't have secret) |
| GitHub Actions runner (self-hosted) | ✅ Yes | ✅ Runs |

### Real Example: When It Would Fail

```python
# Your code has a bug in the reranking module

result = run_pipeline(
    question="How do I install OpenShift?",
    vectorstore=vs,
    do_rerank=True  # ← This crashes internally
)

# Integration test runs and crashes:
$ pytest tests/test_api.py -m integration

FAILED tests/test_api.py::test_full_pipeline_returns_grounded_answer
CrossEncoderError: Model failed to load
  File "retrieval/rerank.py", line 45, in rerank
    ...

❌ Integration test fails
❌ PR cannot merge
👉 Developer sees the error, fixes rerank.py, pushes again
```

### When It Runs

✅ Every push/PR (if secret set)
✅ Takes ~30-60s (API latency)
✅ **Most important test** — proves system works end-to-end

---

## Job #7: K8s Validate

### What It Does

Validates all Kubernetes manifests against JSON schemas using `kubeconform`.

```yaml
k8s-validate:
  name: K8s Manifest Validation
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Download kubeconform
      run: |
        curl -sLo /tmp/kubeconform.tar.gz \
          https://github.com/yannh/kubeconform/releases/latest/download/kubeconform-linux-amd64.tar.gz
        tar -xf /tmp/kubeconform.tar.gz -C /usr/local/bin
    - name: Validate k8s manifests
      run: kubeconform -strict -summary k8s/*.yaml  # ← Validate manifests
```

### Why It Matters

**K8s manifests are like "deployment instructions" for the cluster.**

If they're wrong, deployment fails or behaves unexpectedly:

```yaml
# ❌ Bad: Typo in field name
apiVersion: v1
kind: Deployment
metadata:
  name: rag-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rag-app
  template:
    metadata:
      labels:
        app: rag-app
    spec:
      containers:
        - name: rag-app
          image: rag-openshift-doco:local
          immagePullPolicy: Never  # ← Typo! Should be 'imagePullPolicy'
```

### Kubeconform Catches It

```bash
$ kubeconform -strict -summary k8s/deployment.yaml

k8s/deployment.yaml - Deployment rag-app -
  [error] - additionalProperties false:
    property 'immagePullPolicy' not defined in schema

❌ K8s validation fails
👉 Developer sees the error and fixes the typo
```

### Real Example: Invalid Resource Type

```yaml
# ❌ Wrong: "Pod" instead of "Deployment"
apiVersion: v1
kind: Pod   # ← Should be 'Deployment'
metadata:
  name: rag-app
spec:
  containers:
    - name: rag-app
      image: rag-openshift-doco:local
```

**Kubeconform output:**
```
k8s/deployment.yaml -
  [error] - 'Pod' is not a valid Kubernetes kind
```

### When It Runs

✅ Every push/PR
✅ Very fast (~5s, no cluster needed)
✅ Prevents invalid deployments

---

## Job #8: Docker Build

### What It Does

Builds the Docker image to verify all dependencies are available.

```yaml
docker-build:
  name: Docker Build Check
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Create placeholder data dirs
      run: mkdir -p chroma_db data/processed data/ground_truth
    - name: Build Docker image
      run: docker build -t rag-openshift-doco:ci .
```

### Why It Matters

**Docker image build catches:**

1. **Missing dependencies** in `pyproject.toml`
2. **Broken base images** (can't download from registry)
3. **Missing files** in COPY commands
4. **Syntax errors** in Dockerfile
5. **Build step failures**

### Example Failure #1: Missing Dependency

```dockerfile
# Dockerfile tries to use a package
RUN uv sync --no-dev

# But pyproject.toml is missing it
```

**CI output:**
```
Step 5/10: RUN uv sync --no-dev
ERROR: package 'some-package>=1.0.0' not found in PyPI registry

❌ Docker build fails
👉 Developer adds package to pyproject.toml and pushes again
```

### Example Failure #2: Missing File

```dockerfile
# Dockerfile tries to copy a file
COPY chroma_db/ chroma_db/

# But chroma_db/ doesn't exist locally yet
# (It would be created by the first deployment)
```

**CI output:**
```
Step 7/10: COPY chroma_db/ chroma_db/
COPY failed: stat /var/lib/docker/tmp/xyz/chroma_db: no such file or directory

❌ Docker build fails
```

**Solution:** The CI job creates placeholder dirs first:
```bash
mkdir -p chroma_db data/processed data/ground_truth
```

Now the `COPY` commands succeed.

### When It Runs

✅ Every push/PR
✅ Takes ~45-60s (image download + build)
✅ **Critical for deployment** — proves image can be built

---

## Timeline: What Happens When You Push

### Scenario: You Push to a Feature Branch

```
12:34 PM
├─ You: git push origin feature/my-feature
│
├─ 12:34:05 PM ─ GitHub receives push
│
├─ 12:34:06 PM ─ GitHub sees trigger:
│                 on: push / on: pull_request
│                 ❌ This is NOT pushing to main
│                 ❌ This is NOT a PR to main
│                 → No CI runs
│
└─ Result: ✅ Code pushed, 🚫 CI did not run
```

### Scenario: You Create a Pull Request

```
12:35 PM
├─ You: Create PR: feature/my-feature → main
│
├─ 12:35:05 PM ─ GitHub detects PR to main
│
├─ 12:35:06 PM ─ GitHub triggers CI workflow
│
├─ 12:35:10 PM ─ All 8 jobs start IN PARALLEL on GitHub runners:
│  ├─ Lint (5-10s)
│  ├─ Test (10-15s)
│  ├─ Smoke-test (5s)
│  ├─ Check-secrets (10-20s)
│  ├─ Lockfile-check (5s)
│  ├─ Integration-test (30-60s) [if secret set]
│  ├─ K8s-validate (5s)
│  └─ Docker-build (45-60s)
│
├─ 12:35:30 PM ─ Fast jobs finish:
│  ✅ Lint
│  ✅ Smoke-test
│  ✅ Lockfile-check
│  ❌ Test (test_api.py::TestHealthz::test_returns_ok_status FAILED)
│
├─ 12:35:35 PM ─ GitHub shows in PR:
│  "Some checks are failing"
│  [❌ test] Fix this test failure
│
├─ 12:35:45 PM ─ You see the error in the PR:
│  assert r.get_json()["status"] == "ok"
│  AssertionError: KeyError 'status'
│
├─ 12:36:00 PM ─ You fix the bug:
│  git commit -m "Fix healthz response"
│  git push origin feature/my-feature
│
├─ 12:36:10 PM ─ GitHub detects PR update
│
├─ 12:36:15 PM ─ CI runs AGAIN (fresh run)
│  ├─ Lint → ✅ (5s)
│  ├─ Test → ✅ (15s)
│  ├─ All 8 jobs → ✅ (60s total)
│
├─ 12:37:15 PM ─ GitHub shows in PR:
│  "All checks passed! ✅"
│
└─ Result: 🎉 PR ready to merge!
```

### Scenario: You Push to Main

```
12:40 PM
├─ You: git push origin main
│
├─ 12:40:05 PM ─ GitHub detects push to main
│
├─ 12:40:06 PM ─ GitHub triggers CI workflow
│
├─ 12:40:10 PM ─ All 8 jobs start IN PARALLEL
│
├─ 12:41:10 PM ─ All jobs finish (or some fail)
│  ├─ ✅ Lint
│  ├─ ✅ Test
│  ├─ ✅ Smoke-test
│  ├─ ✅ Check-secrets
│  ├─ ✅ Lockfile-check
│  ├─ ✅ Integration-test (if secret set)
│  ├─ ✅ K8s-validate
│  └─ ✅ Docker-build
│
├─ 12:41:10 PM ─ GitHub commits/workflow view shows:
│  ✅ All checks passed
│
└─ Result: 🚀 Code is live on main
             (Ready for deployment)
```

---

## Real Example: A Developer's Day

### 9:00 AM - Start New Feature

```bash
# Create branch
git checkout -b feature/add-logging

# Make changes
echo "logger.info('Starting pipeline')" >> src/services/pipeline.py
git add .
git commit -m "Add pipeline logging"

# Push (NOT to main, so no CI)
git push origin feature/add-logging
```

**CI Status:** No CI runs (not pushing to main)

---

### 9:15 AM - Create Pull Request

```bash
# Go to GitHub and create PR: feature/add-logging → main
```

**CI Status:**
```
[🟡 Checks in progress...]
├─ ✅ lint (5s)
├─ ✅ smoke-test (5s)
├─ ✅ lockfile-check (5s)
├─ 🔄 test (running... 8s elapsed)
├─ 🔄 integration-test (running... 20s elapsed)
├─ 🔄 k8s-validate (5s)
└─ 🔄 docker-build (running... 30s elapsed)
```

---

### 9:20 AM - Test Fails!

```
[❌ Test failed]

tests/test_api.py::TestQuery::test_no_api_key_returns_error FAILED

monkeypatch.delenv("OPENAI_API_KEY", raising=False)
r = client.post("/api/query", json={"question": "Test?"})
body = r.get_json()
> assert body["error"] is not None
E AssertionError: assert None is not None

src/api/routes.py:152: Check if OPENAI_API_KEY is set
```

**PR shows:**
```
[❌ Some checks are failing]

test —
  tests/test_api.py::TestQuery::test_no_api_key_returns_error
  Assertion failed: body["error"] is not None

Click for details →
```

---

### 9:25 AM - Developer Fixes Bug

```python
# Looking at the test failure, developer realizes:
# The code doesn't check if OPENAI_API_KEY is set!

# Fix in src/api/routes.py:
if not os.environ.get("OPENAI_API_KEY"):
    return jsonify({
        "error": "OPENAI_API_KEY not set — add it to .env",
        "answer": None,
        ...
    })

git add src/api/routes.py
git commit -m "Fix: check OPENAI_API_KEY before querying"
git push origin feature/add-logging
```

---

### 9:30 AM - CI Runs Again

```
[🟡 Checks in progress...]
├─ ✅ lint (5s)
├─ ✅ smoke-test (5s)
├─ ✅ lockfile-check (5s)
├─ 🔄 test (running... 10s elapsed)
├─ 🔄 integration-test (running... 35s elapsed)
├─ ✅ k8s-validate (5s)
└─ 🔄 docker-build (running... 45s elapsed)
```

---

### 9:35 AM - All Green!

```
[✅ All checks passed]

├─ ✅ lint — Code style check passed
├─ ✅ test — All 77 tests passed
├─ ✅ smoke-test — Imports successful
├─ ✅ check-secrets — No credentials found
├─ ✅ lockfile-check — Dependencies up to date
├─ ✅ integration-test — End-to-end pipeline works
├─ ✅ k8s-validate — Manifests valid
└─ ✅ docker-build — Image builds successfully

[Merge pull request]  ← Button is now clickable!
```

---

### 9:36 AM - Merge to Main

```bash
# Developer clicks "Merge pull request" on GitHub
```

**What happens:**
```
1. PR merged into main
2. GitHub deletes the feature branch
3. CI runs AGAIN on main (final check)
4. All jobs pass again
5. Code is now on main, ready for deployment
```

---

## Costs & Efficiency

### GitHub Actions Pricing

| Repo Type | Free Minutes | Cost After |
|---|---|---|
| Public repo | ∞ Unlimited | Free |
| Private repo | 2,000 min/month | $0.24 per 100 min |

### Cost Per PR

```
Typical PR cost (private repo):
├─ Lint + Smoke + Lockfile:          20s = $0.0008
├─ Tests (77 unit tests):            15s = $0.0006
├─ K8s validate:                      5s = $0.0002
├─ Docker build:                     60s = $0.0024
└─ Integration test:                 45s = $0.0018
                           Total: ~3 min = $0.0072
```

**Cost per month (50 PRs):**
```
50 PRs × 3 min = 150 min = $0.36
```

### Optimization: Parallel Jobs

**Without parallelization:**
```
Job 1: 20s
Job 2: 15s
Job 3: 5s
Job 4: 45s
Total: 85s × $0.24/100min = $0.0034 per PR
```

**With parallelization (what we use):**
```
Jobs 1,2,3,4 run simultaneously:
Time = max(20s, 15s, 5s, 45s) = 45s
Cost = 45s × $0.24/100min = $0.0018 per PR

💰 Saves 50% cost + 50% time!
```

---

## Dashboard: Monitoring CI Status

### GitHub PR Page

```
feature/my-feature

[Merge pull request button]

Checks:
├─ ✅ lint — passed 1 minute ago
├─ ✅ test — passed 1 minute ago
├─ ✅ smoke-test — passed 2 minutes ago
├─ ✅ check-secrets — passed 2 minutes ago
├─ ✅ lockfile-check — passed 2 minutes ago
├─ ✅ integration-test — passed 1 minute ago
├─ ✅ k8s-validate — passed 2 minutes ago
└─ ✅ docker-build — passed 30 seconds ago

[View all checks] → See detailed logs for each job
```

### GitHub Actions Tab

```
https://github.com/yourname/your-repo/actions

Recent workflow runs:
├─ feature/logging - All jobs passed        2 min ago
├─ feature/api-test - Test failed          10 min ago
│  └─ tests/test_api.py::test_healthz FAILED
├─ main - All jobs passed                  30 min ago
├─ deploy/kubernetes - Docker build failed  1 hour ago
│  └─ COPY failed: file not found
└─ ...
```

---

## Troubleshooting CI Failures

### Scenario 1: "Test Failed - But It Works Locally!"

```
CI Error:
tests/test_api.py::TestListFiles::test_returns_list_of_processed_files FAILED
  assert len(files) == 2
  AssertionError: 0 != 2

You locally: ✅ Works fine
```

**Cause:** Dependency on local files

**Solution:**
```python
# ❌ Bad: Depends on local file
def test_returns_list_of_processed_files(self, client):
    r = client.get("/api/files")
    files = r.get_json()
    assert len(files) == 2  # ← Assumes data/processed/ has 2 files

# ✅ Good: Creates own fixture
@pytest.fixture
def client(tmp_path):
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    (processed_dir / "doc1.md").write_text("Content")
    (processed_dir / "doc2.md").write_text("Content")
    # Now we control the test environment
```

---

### Scenario 2: "Secret Scan Found My API Key!"

```
check-secrets job failed:

Found verified secret: OpenAI API Key
  File: src/core/config.py
  Line: 42
  Secret: sk-proj-...
```

**What to do:**

1. **Immediately rotate the key**
   ```bash
   # In OpenAI dashboard: Revoke the exposed key
   # Create a new key
   ```

2. **Remove from git history**
   ```bash
   # Option A: Rewrite history (if not pushed to main)
   git reset --soft HEAD~1  # Undo last commit
   # Remove the secret
   git add .
   git commit -m "Remove exposed secret"

   # Option B: Use git-filter (if already pushed)
   # More complex, consult Git docs
   ```

3. **Update GitHub secret**
   ```
   GitHub Settings → Secrets and variables → Actions
   Update OPENAI_API_KEY with new key
   ```

---

### Scenario 3: "Lockfile Check Failed"

```
lockfile-check job failed:

uv lock is out of date. Run `uv lock` to update
```

**Fix:**

```bash
# Locally, update the lock file
uv lock

# Commit and push
git add uv.lock
git commit -m "Update dependencies"
git push origin feature/my-feature

# CI will pass on next run
```

---

### Scenario 4: "Docker Build Failed - Missing File"

```
docker-build job failed:

Step 7/10: COPY chroma_db/ chroma_db/
COPY failed: stat /var/lib/docker/tmp/xyz/chroma_db: no such file or directory
```

**Cause:** Dockerfile references a file that doesn't exist

**Fix:**

```dockerfile
# ❌ Bad
COPY chroma_db/ chroma_db/

# ✅ Good
# Option 1: Make it conditional
RUN [ -d chroma_db ] && echo "Found" || echo "Not found"

# Option 2: Create placeholder in CI job
# (Already done in ci.yml: mkdir -p chroma_db)
```

---

## Best Practices for CI

### 1. Keep Tests Fast

```python
# ❌ Bad: Slow test
@pytest.mark.integration
def test_everything():
    # Calls OpenAI 100 times
    for i in range(100):
        result = run_pipeline(f"query {i}")
        # ~60+ seconds

# ✅ Good: Fast test
def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    # ~0.001 seconds
```

**Why?** Slower tests = longer feedback = developers push fixes slower

---

### 2. Test Locally Before Pushing

```bash
# Before pushing, run tests locally
uv run pytest tests/ -m "not integration" -v

# Catch errors early
# Fix locally, then push
```

---

### 3. Don't Ignore CI Failures

```
❌ BAD:
Developer: "CI is broken, I'll just ignore it"

✅ GOOD:
Developer: "CI failed, let me fix it before merging"
```

---

### 4. Commit Secrets to `.gitignore`

```bash
# .gitignore (prevent accidental commits)
.env
*.key
*.secret
credentials.json
```

---

### 5. Keep Workflows Simple

```yaml
# ❌ Complex: Hard to debug
- name: Build and test and deploy and validate
  run: |
    npm install &&
    npm test &&
    docker build &&
    kubectl apply

# ✅ Simple: Easy to debug
- name: Install dependencies
  run: npm install
- name: Run tests
  run: npm test
- name: Build Docker image
  run: docker build
- name: Validate K8s
  run: kubectl apply --dry-run
```

---

## Summary

| Aspect | Details |
|---|---|
| **What is CI?** | Automated testing on every code change |
| **Platform** | GitHub Actions (GitHub's built-in CI/CD) |
| **When it runs** | Every push to main, every PR to main |
| **Time per PR** | ~2-3 minutes (parallel jobs) |
| **Jobs** | 8 jobs testing different aspects |
| **Failure = Block** | Yes, PR cannot merge if any job fails |
| **Cost** | ~$0.007 per PR (private repo) |
| **Main benefit** | Catch bugs before they reach production |

---

## Interview Talking Points

> "I implemented a **comprehensive CI pipeline with 8 automated jobs**:
>
> **Code Quality (instant feedback):**
> - Linting checks code style with ruff
> - Secret scanning prevents credential leaks
> - Dependency lockfile verification ensures reproducibility
>
> **Testing (validation):**
> - 77 unit tests verify preprocessing, retrieval, and API logic
> - Integration test validates the entire RAG pipeline with real OpenAI embeddings
> - Smoke test catches syntax errors before running full tests
>
> **Infrastructure (deployment readiness):**
> - K8s manifest validation with kubeconform
> - Docker image build check ensures deployment will work
>
> **Efficiency:**
> - All 8 jobs run in parallel (saves 50% time)
> - Feedback in ~2 minutes per PR (developers fix errors quickly)
> - Blocks PRs if any test fails (no broken code reaches production)
>
> Every developer on the team gets **immediate feedback** on code quality, and we have **confidence that merging to main means the code is production-ready**."
