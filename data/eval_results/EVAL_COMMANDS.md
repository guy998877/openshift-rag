# Evaluation Commands

## Directory Layout

```
data/
├── ground_truth/
│   └── queries.json          # 100-query fixed benchmark (do not edit)
├── eval_results/             # all run outputs land here
│   ├── baseline_hybrid.json  # hybrid k=20 baseline (reference)
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

### Hybrid (default)

```bash
python -m eval \
  --output data/eval_results/hybrid_k20.json
```

### Semantic (vector only)

```bash
python -m eval \
  --mode semantic \
  --output data/eval_results/semantic_k20.json \
  --baseline data/eval_results/baseline_hybrid.json
```

### Keyword (BM25 only)

```bash
python -m eval \
  --mode keyword \
  --output data/eval_results/keyword_k20.json \
  --baseline data/eval_results/baseline_hybrid.json
```

### Ablation: all three modes back-to-back

```bash
python -m eval --mode hybrid  --output data/eval_results/hybrid_k20.json
python -m eval --mode semantic --output data/eval_results/semantic_k20.json --baseline data/eval_results/hybrid_k20.json
python -m eval --mode keyword  --output data/eval_results/keyword_k20.json  --baseline data/eval_results/hybrid_k20.json
```

### With cross-encoder reranking

Can be added to any mode:

```bash
python -m eval \
  --mode hybrid \
  --rerank \
  --output data/eval_results/hybrid_rerank_k20.json \
  --baseline data/eval_results/baseline_hybrid.json
```

### Custom k

```bash
python -m eval \
  --k 50 \
  --output data/eval_results/hybrid_k50.json \
  --baseline data/eval_results/baseline_hybrid.json
```

---

## Compare Two Runs

Pass `--baseline` to any run to print a regression diff at the end.
Flags any metric that moves ≥ 0.02 with `✓ improved` / `✗ REGRESSED`.

```bash
python -m eval \
  --output data/eval_results/my_run.json \
  --baseline data/eval_results/baseline_hybrid.json
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
