"""RAG failure-mode analysis.

Reads grid search output and produces five analyses:
  1. Failure mode taxonomy — classify each result as retrieval miss / context
     noise / generation failure / success.
  2. Config sensitivity by failure mode — which knobs actually fix which failure.
  3. Cost-quality Pareto frontier — find the cheapest config for each quality tier.
  4. Recall@k curves — how quickly relevant docs surface as k grows, per mode.
  5. Pipeline k sensitivity — how pipeline k (3 vs 5) affects each recall@k
     threshold and whether the extra docs help or hurt faithfulness.

Usage:
    python -m eval.analysis --results-dir data/eval_results/grid_search/2025-...
    python -m eval.analysis --results-dir data/eval_results/grid_search/2025-... --csv out.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

# ── Thresholds ────────────────────────────────────────────────────────────────

RECALL_MISS_THRESHOLD = 0.0  # recall@5 == 0   → retrieval miss
NOISE_RELEVANCE_THRESHOLD = 0.50  # context_relevance < 0.5 → context noise
FAITH_THRESHOLD = 0.80  # faithfulness < 0.8 → generation failure

# ── OpenAI pricing (USD per 1M tokens, as of early 2025) ─────────────────────
# Used only for relative cost estimation.

MODEL_PRICE = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4o": {"input": 2.50, "output": 10.0},  # kept for old results
}

# Average token counts observed in the pipeline (rough estimates).
# One pipeline call = rewrite (optional) + generate + 3 judge calls.
AVG_TOKENS = {
    "rewrite_input": 300,
    "rewrite_output": 80,
    "generate_input": 2_500,  # system prompt + docs + question
    "generate_output": 350,
    "judge_input": 1_200,  # per judge call
    "judge_output": 60,
    "n_judges": 3,
}


# ── Failure mode classifier ───────────────────────────────────────────────────


def classify(r: dict) -> str:
    ret = r.get("retrieval_metrics", {})
    gen = r.get("generation_metrics", {})
    if "_error" in r:
        return "error"
    recall = ret.get("recall@5", 0)
    ctx = gen.get("context_relevance", {}).get("score")
    faith = gen.get("faithfulness", {}).get("score")
    if recall <= RECALL_MISS_THRESHOLD:
        return "retrieval_miss"
    if ctx is not None and ctx < NOISE_RELEVANCE_THRESHOLD:
        return "context_noise"
    if faith is not None and faith < FAITH_THRESHOLD:
        return "generation_failure"
    return "success"


# ── Cost estimator ────────────────────────────────────────────────────────────


def estimate_cost(model: str, do_rewrite: bool) -> float:
    """Estimated USD cost per query (pipeline + 3 judge calls with gpt-4o-mini)."""
    p = MODEL_PRICE.get(model, MODEL_PRICE["gpt-4.1"])
    judge_p = MODEL_PRICE["gpt-4o-mini"]
    t = AVG_TOKENS

    cost = t["generate_input"] * p["input"] / 1_000_000
    cost += t["generate_output"] * p["output"] / 1_000_000
    cost += t["n_judges"] * (
        t["judge_input"] * judge_p["input"] / 1_000_000
        + t["judge_output"] * judge_p["output"] / 1_000_000
    )
    if do_rewrite:
        cost += t["rewrite_input"] * p["input"] / 1_000_000
        cost += t["rewrite_output"] * p["output"] / 1_000_000
    return cost


# ── Load results ──────────────────────────────────────────────────────────────


def load_results(results_dir: Path) -> list[dict]:
    """Load all per-config metrics.json files from a grid search run dir."""
    rows = []
    for metrics_file in results_dir.glob("*/metrics.json"):
        data = json.loads(metrics_file.read_text())
        rows.append(data)
    if not rows:
        raise FileNotFoundError(f"No metrics.json files found in {results_dir}")
    return rows


def load_detailed_results(results_dir: Path) -> list[dict]:
    """Load per-query results from all run dirs (requires full results, not just metrics)."""
    rows = []
    for results_file in results_dir.glob("*/results.json"):
        cfg_data = json.loads(results_file.read_text())
        rows.extend(cfg_data)
    return rows


# ── Analysis 1: Failure mode taxonomy ─────────────────────────────────────────


def failure_taxonomy(all_results: list[dict]) -> dict:
    """
    Returns per-config and per-content-type failure mode breakdown.

    all_results: list of per-query result dicts (with 'config' field attached).
    """
    by_mode = defaultdict(lambda: defaultdict(int))  # config_label → failure → count
    by_type = defaultdict(lambda: defaultdict(int))  # content_type → failure → count
    by_topic = defaultdict(lambda: defaultdict(int))  # topic → failure → count
    totals = defaultdict(int)

    for r in all_results:
        label = _cfg_label(r["config"])
        ctype = r.get("content_type", "unknown")
        topic = r.get("topic", "unknown")
        failure = classify(r)

        by_mode[label][failure] += 1
        by_type[ctype][failure] += 1
        by_topic[topic][failure] += 1
        totals[failure] += 1

    return {
        "by_config": dict(by_mode),
        "by_content_type": dict(by_type),
        "by_topic": dict(by_topic),
        "totals": dict(totals),
    }


# ── Analysis 2: Config delta on each failure mode ────────────────────────────


def config_sensitivity(all_results: list[dict]) -> dict:
    """
    For each pipeline dimension (rerank / mode / rewrite), compute the delta in
    each failure rate when that dimension is toggled.

    Returns a dict: dimension → {failure_mode → delta (positive = fewer failures)}.
    """
    MODES_BY_DIM = {
        "rerank": [(True, False)],
        "mode": [("hybrid", "semantic"), ("hybrid", "keyword")],
        "rewrite": [(True, False)],
    }

    results_by_config: dict[str, list] = defaultdict(list)
    for r in all_results:
        key = _cfg_key(r["config"])
        results_by_config[key].append(r)

    def failure_rates(results):
        counts = defaultdict(int)
        for r in results:
            counts[classify(r)] += 1
        n = len(results) or 1
        return {
            k: counts[k] / n
            for k in [
                "retrieval_miss",
                "context_noise",
                "generation_failure",
                "success",
            ]
        }

    sensitivity = {}
    for dim, pairs in MODES_BY_DIM.items():
        sensitivity[dim] = {}
        for val_a, val_b in pairs:
            group_a = [r for r in all_results if r["config"].get(dim) == val_a]
            group_b = [r for r in all_results if r["config"].get(dim) == val_b]
            rates_a = failure_rates(group_a)
            rates_b = failure_rates(group_b)
            pair_key = f"{val_a}_vs_{val_b}"
            sensitivity[dim][pair_key] = {
                mode: round(rates_a[mode] - rates_b[mode], 4)
                for mode in ["retrieval_miss", "context_noise", "generation_failure"]
            }

    return sensitivity


# ── Analysis 3: Cost-quality Pareto frontier ──────────────────────────────────


def pareto_frontier(configs: list[dict]) -> list[dict]:
    """
    Given a list of config+aggregate rows, compute cost per query and identify
    the Pareto-optimal configs (highest composite quality for a given cost).

    Returns all configs annotated with cost + pareto flag, sorted by cost.
    """
    annotated = []
    for row in configs:
        cfg = row["config"]
        agg = row["aggregate"]
        cost = estimate_cost(cfg["model"], cfg.get("rewrite", False))
        annotated.append(
            {
                "config": cfg,
                "aggregate": agg,
                "cost_usd": round(cost, 6),
                "composite": agg.get("composite"),
            }
        )

    annotated.sort(key=lambda r: r["cost_usd"])

    # Mark Pareto-optimal: a config is dominated if a cheaper one has equal or
    # better composite quality.
    best_quality_so_far = -1.0
    for row in annotated:
        q = row["composite"] or 0
        if q > best_quality_so_far:
            best_quality_so_far = q
            row["pareto"] = True
        else:
            row["pareto"] = False

    return annotated


# ── Sensitivity by content type ───────────────────────────────────────────────


def rerank_delta_by_content_type(all_results: list[dict]) -> dict:
    """
    The core hypothesis: reranking helps PROCEDURE queries more than CONCEPT.
    Returns per-content-type composite score delta (rerank=True minus rerank=False).
    """
    by_type_rerank = defaultdict(list)  # content_type → [composite scores]
    by_type_no_rerank = defaultdict(list)

    for r in all_results:
        ctype = r.get("content_type", "unknown")
        score = _composite(r)
        if score is None:
            continue
        if r["config"].get("rerank"):
            by_type_rerank[ctype].append(score)
        else:
            by_type_no_rerank[ctype].append(score)

    result = {}
    for ctype in set(by_type_rerank) | set(by_type_no_rerank):
        with_r = by_type_rerank[ctype]
        without_r = by_type_no_rerank[ctype]
        avg_with = sum(with_r) / len(with_r) if with_r else None
        avg_without = sum(without_r) / len(without_r) if without_r else None
        delta = round(avg_with - avg_without, 4) if (avg_with and avg_without) else None
        result[ctype] = {
            "rerank_on": round(avg_with, 4) if avg_with else None,
            "rerank_off": round(avg_without, 4) if avg_without else None,
            "delta": delta,
        }
    return result


# ── Print helpers ─────────────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREY = "\033[90m"
CYAN = "\033[96m"


def _cfg_label(cfg: dict) -> str:
    return (
        f"{cfg.get('model', '?'):<12}  k={cfg.get('k', '?'):<2}  "
        f"mode={cfg.get('mode', '?'):<8}  "
        f"{'rerank' if cfg.get('rerank') else 'no-rerank':<9}  "
        f"{'rewrite' if cfg.get('rewrite') else 'no-rewrite'}"
    )


def _cfg_key(cfg: dict) -> str:
    return json.dumps(
        {k: cfg[k] for k in sorted(cfg) if k != "n_queries"}, sort_keys=True
    )


def _composite(r: dict) -> float | None:
    gen = r.get("generation_metrics", {})
    ret = r.get("retrieval_metrics", {})
    scores = [
        gen.get("answer_relevance", {}).get("score"),
        gen.get("faithfulness", {}).get("score"),
        gen.get("context_relevance", {}).get("score"),
        ret.get("recall@5"),
        ret.get("mrr"),
    ]
    valid = [s for s in scores if s is not None]
    return round(sum(valid) / len(valid), 4) if valid else None


def _fv(v: float | None, w: int = 6, sign: bool = False) -> str:
    """Format a float value for table display."""
    if v is None:
        return " n/a  ".rjust(w)
    s = f"{v:+.4f}" if sign else f"{v:.4f}"
    return s.rjust(w)


def _bar(rate: float, width: int = 20) -> str:
    filled = round(rate * width)
    return "█" * filled + "░" * (width - filled)


def print_taxonomy(taxonomy: dict) -> None:
    MODES = [
        "success",
        "retrieval_miss",
        "context_noise",
        "generation_failure",
        "error",
    ]
    COLOR = {
        "success": GREEN,
        "retrieval_miss": RED,
        "context_noise": YELLOW,
        "generation_failure": YELLOW,
        "error": GREY,
    }

    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PART 1: FAILURE MODE TAXONOMY{RESET}")
    print(f"{'=' * 70}")

    totals = taxonomy["totals"]
    grand = sum(totals.values()) or 1
    print(f"\n  Overall distribution ({grand} query results):\n")
    for mode in MODES:
        n = totals.get(mode, 0)
        rate = n / grand
        c = COLOR[mode]
        print(f"  {c}{mode:<22}{RESET}  {_bar(rate)}  {rate * 100:5.1f}%  (n={n})")

    print("\n  By content type:\n")
    for ctype, counts in taxonomy["by_content_type"].items():
        total = sum(counts.values()) or 1
        parts = [
            f"{COLOR[m]}{m}: {counts.get(m, 0) / total * 100:.0f}%{RESET}"
            for m in MODES
            if counts.get(m, 0)
        ]
        print(f"  {BOLD}{ctype:<10}{RESET}  {' | '.join(parts)}")

    print("\n  By topic (retrieval miss rate):\n")
    topic_data = [
        (topic, counts.get("retrieval_miss", 0) / (sum(counts.values()) or 1))
        for topic, counts in taxonomy["by_topic"].items()
    ]
    topic_data.sort(key=lambda x: -x[1])
    for topic, miss_rate in topic_data:
        c = RED if miss_rate > 0.3 else (YELLOW if miss_rate > 0.15 else GREEN)
        print(
            f"  {topic:<35} {c}{_bar(miss_rate, 12)}  {miss_rate * 100:4.1f}% miss{RESET}"
        )


def print_sensitivity(sensitivity: dict) -> None:
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PART 2: CONFIG SENSITIVITY BY FAILURE MODE{RESET}")
    print(
        f"  (positive delta = fewer failures with first option){RESET if False else ''}"
    )
    print(f"{'=' * 70}\n")

    for dim, pairs in sensitivity.items():
        print(f"  {BOLD}{dim.upper()}{RESET}")
        for pair_key, deltas in pairs.items():
            print(f"    {pair_key}:")
            for failure, delta in deltas.items():
                c = GREEN if delta > 0.02 else (RED if delta < -0.02 else GREY)
                sign = "+" if delta >= 0 else ""
                print(f"      {failure:<25}  {c}{sign}{delta:+.3f}{RESET}")
        print()


def print_rerank_by_type(data: dict) -> None:
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PART 2b: RERANK DELTA BY CONTENT TYPE{RESET}")
    print(f"{'=' * 70}\n")
    print(f"  {'Content type':<12} {'Rerank ON':>10} {'Rerank OFF':>11} {'Delta':>8}")
    print(f"  {'-' * 45}")
    for ctype, d in sorted(data.items()):
        delta = d["delta"]
        c = GREEN if (delta or 0) > 0.01 else (GREY if (delta or 0) >= 0 else RED)
        sign = "+" if (delta or 0) >= 0 else ""
        print(
            f"  {ctype:<12}  {str(d['rerank_on']):>9}  {str(d['rerank_off']):>10}  "
            f"{c}{sign}{delta if delta is not None else 'n/a':>7}{RESET}"
        )


# ── Analysis 4: Recall@k curves ──────────────────────────────────────────────

RECALL_KS = [1, 3, 5]


def recall_at_k_curves(all_results: list[dict]) -> dict:
    """
    For each retrieval mode and pipeline-k value, compute avg recall@1/3/5
    and MRR. Reveals the shape of the ranking curve — how quickly relevant
    docs surface as you look deeper.

    Returns:
        {
          "by_mode":    { mode → { "recall@1": ..., "recall@3": ..., ... } },
          "by_pipeline_k": { k_val → { "recall@1": ..., ... } },
          "by_mode_and_k": { (mode, k_val) → { "recall@1": ..., ... } },
        }
    """

    def _avg_ret_key(results, key):
        vals = [
            r["retrieval_metrics"].get(key)
            for r in results
            if r.get("retrieval_metrics", {}).get(key) is not None
        ]
        return round(sum(vals) / len(vals), 4) if vals else None

    def _metrics(results):
        return {
            **{f"recall@{k}": _avg_ret_key(results, f"recall@{k}") for k in RECALL_KS},
            "mrr": _avg_ret_key(results, "mrr"),
            "n": len(results),
        }

    by_mode: dict[str, list] = defaultdict(list)
    by_pk: dict[int, list] = defaultdict(list)
    by_mk: dict[tuple, list] = defaultdict(list)

    for r in all_results:
        if "_error" in r:
            continue
        mode = r["config"].get("mode", "?")
        pk = r["config"].get("k")
        by_mode[mode].append(r)
        by_pk[pk].append(r)
        by_mk[(mode, pk)].append(r)

    return {
        "by_mode": {m: _metrics(rs) for m, rs in by_mode.items()},
        "by_pipeline_k": {k: _metrics(rs) for k, rs in by_pk.items()},
        "by_mode_and_k": {f"{m}_k{k}": _metrics(rs) for (m, k), rs in by_mk.items()},
    }


# ── Analysis 5: Pipeline k sensitivity ───────────────────────────────────────


def pipeline_k_sensitivity(all_results: list[dict]) -> dict:
    """
    Compare k=3 vs k=5 across:
      - All recall@k thresholds (gain from going k=3→5 at each eval cutoff)
      - Faithfulness (do extra 2 docs add noise?)
      - Per content_type (does more context help CONCEPT more than PROCEDURE?)

    Key insight: for k=3 configs, recall@5 = recall@3 by definition (only 3
    docs retrieved). The gain in recall@5 when moving to k=5 shows whether
    ranks 4–5 actually contain the gold doc.
    """

    def _avg(results, getter):
        vals = [getter(r) for r in results if getter(r) is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    def _ret(key):
        return lambda r: r.get("retrieval_metrics", {}).get(key)

    def _gen(key):
        return lambda r: r.get("generation_metrics", {}).get(key, {}).get("score")

    def _profile(results):
        return {
            **{f"recall@{k}": _avg(results, _ret(f"recall@{k}")) for k in RECALL_KS},
            "mrr": _avg(results, _ret("mrr")),
            "faithfulness": _avg(results, _gen("faithfulness")),
            "context_relevance": _avg(results, _gen("context_relevance")),
            "n": len(results),
        }

    k3 = [r for r in all_results if r["config"].get("k") == 3 and "_error" not in r]
    k5 = [r for r in all_results if r["config"].get("k") == 5 and "_error" not in r]

    p3 = _profile(k3)
    p5 = _profile(k5)
    delta = {
        key: round((p5[key] or 0) - (p3[key] or 0), 4)
        for key in p3
        if isinstance(p3[key], float)
    }

    # Break down by content_type
    by_type: dict[str, dict] = {}
    for ctype in {r.get("content_type", "unknown") for r in all_results}:
        ct_k3 = [r for r in k3 if r.get("content_type") == ctype]
        ct_k5 = [r for r in k5 if r.get("content_type") == ctype]
        by_type[ctype] = {
            "k3": _profile(ct_k3),
            "k5": _profile(ct_k5),
            "delta_recall@5": round(
                (_profile(ct_k5).get("recall@5") or 0)
                - (_profile(ct_k3).get("recall@5") or 0),
                4,
            ),
            "delta_faithfulness": round(
                (_profile(ct_k5).get("faithfulness") or 0)
                - (_profile(ct_k3).get("faithfulness") or 0),
                4,
            ),
        }

    return {"k3": p3, "k5": p5, "delta": delta, "by_content_type": by_type}


def print_recall_curves(curves: dict) -> None:
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(
        f"{BOLD}  PART 4: RECALL@k CURVES — HOW FAST DO RELEVANT DOCS SURFACE?{RESET}"
    )
    print("  Diminishing returns shape reveals ranking quality vs. recall ceiling.")
    print(f"{'=' * 70}\n")

    # By mode (pooled across all pipeline-k values)
    print(f"  {BOLD}By retrieval mode (all pipeline-k values):{RESET}\n")
    header = f"  {'Mode':<10}  {'r@1':>6}  {'r@3':>6}  {'r@5':>6}  {'MRR':>6}  {'gain 1→3':>9}  {'gain 3→5':>9}"
    print(header)
    print(f"  {'-' * 65}")
    for mode, m in sorted(curves["by_mode"].items()):
        r1, r3, r5, mrr = (
            m.get("recall@1"),
            m.get("recall@3"),
            m.get("recall@5"),
            m.get("mrr"),
        )
        g13 = (
            round((r3 or 0) - (r1 or 0), 4)
            if r1 is not None and r3 is not None
            else None
        )
        g35 = (
            round((r5 or 0) - (r3 or 0), 4)
            if r3 is not None and r5 is not None
            else None
        )
        g13_c = GREEN if (g13 or 0) > 0.10 else (YELLOW if (g13 or 0) > 0.05 else GREY)
        g35_c = GREEN if (g35 or 0) > 0.08 else (YELLOW if (g35 or 0) > 0.03 else GREY)
        print(
            f"  {mode:<10}  {_fv(r1)}  {_fv(r3)}  {_fv(r5)}  {_fv(mrr)}"
            f"  {g13_c}{_fv(g13, sign=True)}{RESET}  {g35_c}{_fv(g35, sign=True)}{RESET}"
        )

    # By mode × pipeline-k
    print(
        f"\n  {BOLD}By mode × pipeline k (shows k=3 recall@5 ceiling effect):{RESET}\n"
    )
    header2 = (
        f"  {'Config':<16}  {'r@1':>6}  {'r@3':>6}  {'r@5':>6}  {'MRR':>6}  {'n':>5}"
    )
    print(header2)
    print(f"  {'-' * 55}")
    for label, m in sorted(curves["by_mode_and_k"].items()):
        note = f"{GREY}  [r@5=r@3]{RESET}" if "k3" in label else ""
        print(
            f"  {label:<16}  {_fv(m.get('recall@1'))}  {_fv(m.get('recall@3'))}"
            f"  {_fv(m.get('recall@5'))}  {_fv(m.get('mrr'))}  {m['n']:>5}{note}"
        )


def print_k_sensitivity(sens: dict) -> None:
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PART 5: PIPELINE k SENSITIVITY (k=3 vs k=5){RESET}")
    print("  Do the extra 2 docs (ranks 4–5) add recall or add noise?")
    print(f"{'=' * 70}\n")

    p3, p5, delta = sens["k3"], sens["k5"], sens["delta"]

    keys = [f"recall@{k}" for k in RECALL_KS] + [
        "mrr",
        "faithfulness",
        "context_relevance",
    ]
    print(f"  {'Metric':<22}  {'k=3':>8}  {'k=5':>8}  {'delta':>8}")
    print(f"  {'-' * 50}")
    for key in keys:
        v3 = p3.get(key)
        v5 = p5.get(key)
        d = delta.get(key)
        # For recall@1 and recall@3, k=3 vs k=5 should be identical (ranks 1-3 unchanged)
        # For recall@5, k=3 configs are capped at recall@3 by definition.
        # For faithfulness, a positive delta is bad (noise) or good — depends on framing.
        if key == "faithfulness":
            c = GREEN if (d or 0) >= 0 else RED
        else:
            c = GREEN if (d or 0) > 0.01 else (GREY if (d or 0) >= 0 else RED)
        sign = "+" if (d or 0) >= 0 else ""
        print(
            f"  {key:<22}  {_fv(v3):>8}  {_fv(v5):>8}  {c}{sign}{d if d is not None else 'n/a':>7}{RESET}"
        )

    print(f"\n  {BOLD}By content type — recall@5 and faithfulness delta:{RESET}\n")
    print(
        f"  {'Content type':<12}  {'Δ recall@5':>11}  {'Δ faithfulness':>15}  Interpretation"
    )
    print(f"  {'-' * 65}")
    for ctype, d in sorted(sens["by_content_type"].items()):
        dr5 = d["delta_recall@5"]
        dfth = d["delta_faithfulness"]
        dr5_c = GREEN if dr5 > 0.01 else (GREY if dr5 >= 0 else RED)
        dfth_c = GREEN if dfth >= 0 else RED
        # Interpretation: high recall gain + no faithfulness loss = clearly worth it
        if dr5 > 0.05 and dfth >= -0.02:
            interp = f"{GREEN}k=5 wins — more recall, no noise cost{RESET}"
        elif dr5 > 0.05 and dfth < -0.02:
            interp = f"{YELLOW}k=5 finds more docs but adds noise{RESET}"
        elif dr5 <= 0.02:
            interp = f"{GREY}k=3 sufficient — ranks 4-5 rarely contain gold{RESET}"
        else:
            interp = f"{YELLOW}marginal gain{RESET}"
        print(
            f"  {ctype:<12}  {dr5_c}{'+' if dr5 >= 0 else ''}{dr5:>10.4f}{RESET}"
            f"  {dfth_c}{'+' if dfth >= 0 else ''}{dfth:>14.4f}{RESET}  {interp}"
        )


def print_pareto(pareto: list[dict]) -> None:
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PART 3: COST-QUALITY PARETO FRONTIER{RESET}")
    print("  (★ = Pareto-optimal — best quality at this cost level)")
    print(f"{'=' * 70}\n")
    print(
        f"  {'★':<3} {'Model':<12} {'k':<3} {'Mode':<9} {'Rerank':<8} {'Composite':>10} {'$/query':>9}"
    )
    print(f"  {'-' * 60}")
    for row in pareto:
        cfg = row["config"]
        comp = row["composite"]
        star = f"{BOLD}{CYAN}★{RESET}" if row["pareto"] else " "
        c = GREEN if (comp or 0) >= 0.80 else (YELLOW if (comp or 0) >= 0.60 else RED)
        cost_str = f"${row['cost_usd']:.5f}"
        print(
            f"  {star:<3} {cfg.get('model', '?'):<12} {cfg.get('k', '?'):<3} "
            f"{cfg.get('mode', '?'):<9} {'on' if cfg.get('rerank') else 'off':<8} "
            f"{c}{str(comp):>10}{RESET} {cost_str:>9}"
        )


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m eval.analysis",
        description="Failure-mode anatomy of a grid search run.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        required=True,
        help="Path to a grid search output directory (contains */metrics.json).",
    )
    parser.add_argument(
        "--queries",
        type=Path,
        default=Path("./data/ground_truth/queries.json"),
        help="Path to queries.json (for content_type / topic annotation).",
    )
    parser.add_argument("--csv", type=Path, help="Optional: export Pareto data to CSV.")
    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"Error: {args.results_dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"\nLoading results from {args.results_dir} …")
    configs = load_results(args.results_dir)
    print(f"  {len(configs)} config summaries loaded")

    # Load per-query results for taxonomy analysis.
    # Grid search saves only metrics.json by default; if full results.json exist, use them.
    # Otherwise, fall back to aggregate-level analysis only.
    all_results: list[dict] = []
    for run_dir in args.results_dir.iterdir():
        full_path = run_dir / "results.json"
        if full_path.exists():
            cfg_blob = json.loads(full_path.read_text())
            all_results.extend(cfg_blob)

    # Annotate with content_type + topic from queries.json
    if all_results and args.queries.exists():
        query_meta = {q["id"]: q for q in json.loads(args.queries.read_text())}
        for r in all_results:
            meta = query_meta.get(r.get("id", ""), {})
            r.setdefault("content_type", meta.get("content_type", "unknown"))
            r.setdefault("topic", meta.get("topic", "unknown"))

    # ── Part 1 ────────────────────────────────────────────────────────────────
    if all_results:
        taxonomy = failure_taxonomy(all_results)
        print_taxonomy(taxonomy)
    else:
        print("\n[Part 1 skipped — no per-query results.json found]")
        print(
            "  Tip: modify grid_search.py to also write 'results.json' in each run_dir"
        )

    # ── Part 2 ────────────────────────────────────────────────────────────────
    if all_results:
        sensitivity = config_sensitivity(all_results)
        print_sensitivity(sensitivity)

        rerank_by_type = rerank_delta_by_content_type(all_results)
        print_rerank_by_type(rerank_by_type)

    # ── Parts 4 & 5: recall@k curves and pipeline-k sensitivity ──────────────
    if all_results:
        curves = recall_at_k_curves(all_results)
        print_recall_curves(curves)

        k_sens = pipeline_k_sensitivity(all_results)
        print_k_sensitivity(k_sens)
    else:
        print("\n[Parts 4 & 5 skipped — no per-query results.json found]")

    # ── Part 3 ────────────────────────────────────────────────────────────────
    pareto = pareto_frontier(configs)
    print_pareto(pareto)

    if args.csv and pareto:
        import csv

        with open(args.csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "model",
                    "k",
                    "mode",
                    "rerank",
                    "rewrite",
                    "composite",
                    "answer_relevance",
                    "faithfulness",
                    "context_relevance",
                    "recall@1",
                    "recall@3",
                    "recall@5",
                    "precision@1",
                    "precision@3",
                    "precision@5",
                    "mrr",
                    "cost_usd",
                    "pareto",
                ],
            )
            writer.writeheader()
            for row in pareto:
                cfg = row["config"]
                agg = row["aggregate"]
                writer.writerow(
                    {
                        "model": cfg.get("model"),
                        "k": cfg.get("k"),
                        "mode": cfg.get("mode"),
                        "rerank": cfg.get("rerank"),
                        "rewrite": cfg.get("rewrite"),
                        "composite": row["composite"],
                        "answer_relevance": agg.get("answer_relevance"),
                        "faithfulness": agg.get("faithfulness"),
                        "context_relevance": agg.get("context_relevance"),
                        "recall@1": agg.get("recall@1"),
                        "recall@3": agg.get("recall@3"),
                        "recall@5": agg.get("recall@5"),
                        "precision@1": agg.get("precision@1"),
                        "precision@3": agg.get("precision@3"),
                        "precision@5": agg.get("precision@5"),
                        "mrr": agg.get("mrr"),
                        "cost_usd": row["cost_usd"],
                        "pareto": row["pareto"],
                    }
                )
        print(f"\nPareto data exported → {args.csv}")

    print()


main()
