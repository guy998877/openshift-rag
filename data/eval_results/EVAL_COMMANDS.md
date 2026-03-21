# Evaluation Commands

## Directory Layout

```
data/
├── ground_truth/
│   └── queries.json                     # 100-query fixed benchmark (do not edit)
├── eval_results/
│   ├── EVAL_COMMANDS.md
│   ├── 2026-03-20T15-29_hybrid_k20/     # one subdir per run (auto-named)
│   │   ├── metrics.json                 # aggregate + per-query scores
│   │   └── predictions.jsonl            # per-query retrieved stems
│   └── ...
```

---

## Generate Ground Truth

Re-generate the 100-query benchmark from the processed docs (only needed if
the corpus changes significantly).

```bash
python src/eval/generate_benchmark.py \
  --output data/ground_truth/queries.json \
  --target 100 \
  --model gpt-4o-mini \
  --seed 42
```

---

## Run Retrieval Evaluation

Metrics: **recall@k**, **MRR**, **precision@k** (context precision).
No LLM calls — runs in ~40 seconds.

### Retrieval modes

| Flag | Mode | Description |
|---|---|---|
| *(default)* | `hybrid` | BM25 + vector with RRF merge |
| `--mode semantic` | `semantic` | Vector / embedding search only |
| `--mode keyword` | `keyword` | BM25 keyword search only |

Each run automatically creates a timestamped subdirectory, e.g.
`data/eval_results/2026-03-20T15-29_hybrid_k20/` containing
`metrics.json` and `predictions.jsonl`.

### Hybrid (default)

```bash
python -m eval
```

### Semantic (vector only)

```bash
python -m eval --mode semantic
```

### Keyword (BM25 only)

```bash
python -m eval --mode keyword
```

### Ablation: all three modes back-to-back

```bash
python -m eval --mode hybrid
python -m eval --mode semantic
python -m eval --mode keyword
```

### With cross-encoder reranking

Can be added to any mode:

```bash
python -m eval --mode hybrid --rerank
```

### Custom retrieval k

```bash
python -m eval --k 50
```

### Limit number of queries evaluated

Useful for quick sanity checks during development.

```bash
# First 10 queries
python -m eval --n 10

# First 10 queries, keyword mode
python -m eval --mode keyword --n 10
```

### Skip saving to disk

```bash
python -m eval --no-save
```

### Custom output directory

```bash
python -m eval --output-dir /some/other/path
```

---

## Compare Two Runs

Pass `--baseline` pointing to any previous `metrics.json` to print a
regression diff at the end. Flags any metric that moves ≥ 0.02 with
`✓ improved` / `✗ REGRESSED`.

```bash
python -m eval --baseline data/eval_results/2026-03-19T15-29_hybrid_k20/metrics.json
```

---

## Baseline Numbers (hybrid, k=20, 2026-03-19)

| Metric        | Value |
|---------------|-------|
| recall@1      | 0.697 |
| recall@5      | 0.840 |
| recall@10     | 0.888 |
| recall@20     | 0.923 |
| MRR           | 0.838 |
| any\_hit@5    | 91/100 |
| precision@5   | 0.192 |
| avg latency   | 413ms |
