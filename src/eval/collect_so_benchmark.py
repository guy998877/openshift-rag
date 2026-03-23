"""Collect real user questions from Stack Overflow to build an OpenShift benchmark.

Fetches questions tagged [openshift] from the Stack Exchange public API (no key needed),
filters for quality, then writes a queries.json compatible with the existing eval pipeline.

Since these are real questions (no gold docs), retrieval metrics won't apply —
use this benchmark with the LLM-as-judge generation eval only.

Usage:
    python -m eval.collect_so_benchmark --output data/ground_truth/so_queries.json
    python -m eval.collect_so_benchmark --output data/ground_truth/so_queries.json --max 200 --min-score 2
"""
from __future__ import annotations

import argparse
import html
import json
import re
import time
from pathlib import Path

import os

import requests
from dotenv import load_dotenv

load_dotenv()

# ── Stack Exchange API ─────────────────────────────────────────────────────────

SO_API_BASE = "https://api.stackexchange.com/2.3"

# Tags that map to OpenShift topic areas (used to classify questions)
TAG_TO_TOPIC: dict[str, str] = {
    "openshift":              "general",
    "openshift-4":            "general",
    "openshift-origin":       "general",
    "okd":                    "general",
    "kubernetes":             "general",
    "microshift":             "microshift",
    "crc":                    "general",
    "openshift-operator":     "operators",
    "operator-sdk":           "operators",
    "olm":                    "operators",
    "openshift-router":       "networking",
    "openshift-networking":   "networking",
    "route":                  "networking",
    "ingress":                "networking",
    "networkpolicy":          "networking",
    "openshift-pipeline":     "cicd",
    "tekton":                 "cicd",
    "jenkins":                "cicd",
    "openshift-builds":       "cicd",
    "openshift-deployment":   "workloads",
    "deploymentconfig":       "workloads",
    "pod":                    "workloads",
    "openshift-rbac":         "authentication",
    "rbac":                   "authentication",
    "openshift-authentication": "authentication",
    "serviceaccount":         "authentication",
    "openshift-registry":     "registry",
    "image-registry":         "registry",
    "openshift-storage":      "storage",
    "persistent-volume":      "storage",
    "openshift-monitoring":   "monitoring",
    "prometheus":             "monitoring",
    "openshift-logging":      "logging",
    "elasticsearch":          "logging",
    "openshift-install":      "installing",
    "openshift-upgrade":      "upgrading",
    "cni":                    "networking",
    "ovn":                    "networking",
    "rosa":                   "rosa",
    "openshift-dedicated":    "osd",
}

UNWANTED_PATTERNS = re.compile(
    r"(pastebin|gist\.github|i\.imgur|stackoverflow\.com/questions/\d+|"
    r"please help|any help|thanks in advance)",
    re.IGNORECASE,
)


def _infer_topic(tags: list[str]) -> str:
    """Return the most specific topic for a question's tag list."""
    for tag in tags:
        if tag in TAG_TO_TOPIC:
            topic = TAG_TO_TOPIC[tag]
            if topic != "general":
                return topic
    return "general"


def _clean_title(title: str) -> str:
    """Decode HTML entities and strip trailing punctuation clutter."""
    title = html.unescape(title).strip()
    # Normalise question mark at end
    if not title.endswith("?"):
        title = title.rstrip(".!") + "?"
    return title


def _is_quality(q: dict, min_score: int) -> bool:
    """Return True if the question meets quality bar."""
    if q.get("score", 0) < min_score:
        return False
    if not q.get("is_answered", False):
        return False
    if q.get("closed_reason"):
        return False
    title = q.get("title", "")
    if UNWANTED_PATTERNS.search(title):
        return False
    if len(title) < 20:
        return False
    return True


def fetch_so_questions(
    tags: list[str],
    min_score: int,
    max_questions: int,
    api_key: str | None,
) -> list[dict]:
    """Fetch questions from the Stack Exchange API with pagination."""
    collected: list[dict] = []
    seen_ids: set[int] = set()
    page = 1
    backoff = 1.0

    params: dict = {
        "site":     "stackoverflow",
        "tagged":   ";".join(tags),
        "order":    "desc",
        "sort":     "votes",
        "pagesize": 100,
    }
    if api_key:
        params["key"] = api_key

    print(f"Fetching Stack Overflow questions tagged: {tags}")

    while len(collected) < max_questions:
        params["page"] = page
        try:
            resp = requests.get(f"{SO_API_BASE}/questions", params=params, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [ERROR] API request failed: {e}")
            break

        data = resp.json()

        # Respect backoff directive from the API
        if data.get("backoff"):
            wait = int(data["backoff"]) + 1
            print(f"  [BACKOFF] API asked us to wait {wait}s")
            time.sleep(wait)

        items = data.get("items", [])
        if not items:
            break

        for q in items:
            qid = q["question_id"]
            if qid in seen_ids:
                continue
            seen_ids.add(qid)
            if _is_quality(q, min_score):
                collected.append(q)
                if len(collected) >= max_questions:
                    break

        has_more = data.get("has_more", False)
        quota_remaining = data.get("quota_remaining", 0)
        print(
            f"  page={page}  fetched={len(items)}  accepted={len(collected)}  "
            f"quota_remaining={quota_remaining}"
        )

        if not has_more or quota_remaining <= 5:
            break

        page += 1
        # Polite delay — the API allows ~30 requests/s without a key
        time.sleep(backoff)

    return collected


def build_benchmark(questions: list[dict]) -> list[dict]:
    """Convert raw SO API question objects into benchmark query entries."""
    benchmark = []
    for q in questions:
        tags = [t.lower() for t in q.get("tags", [])]
        topic = _infer_topic(tags)
        title = _clean_title(q.get("title", ""))
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower())[:60].strip("-")
        qid = f"so-{q['question_id']}"

        entry = {
            "id":            qid,
            "query":         title,
            "topic":         topic,
            "content_type":  "REAL_USER",
            "gold_doc_ids":  [],          # no gold docs — use generation eval only
            "source": {
                "site":       "stackoverflow",
                "question_id": q["question_id"],
                "score":      q.get("score", 0),
                "tags":       tags,
            },
        }
        benchmark.append(entry)

    return benchmark


def collect(
    output_path: Path,
    max_questions: int = 150,
    min_score: int = 1,
    tags: list[str] | None = None,
    api_key: str | None = None,
) -> None:
    if tags is None:
        tags = ["openshift"]

    raw = fetch_so_questions(
        tags=tags,
        min_score=min_score,
        max_questions=max_questions,
        api_key=api_key,
    )

    print(f"\nPassed quality filter: {len(raw)} questions")

    benchmark = build_benchmark(raw)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(benchmark, indent=2))
    print(f"Wrote {len(benchmark)} entries → {output_path}")

    # Topic distribution
    from collections import Counter
    dist = Counter(e["topic"] for e in benchmark)
    print("\nTopic distribution:")
    for topic, count in sorted(dist.items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 40)
        print(f"  {topic:<30} {bar}  {count}")


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python -m eval.collect_so_benchmark",
        description="Collect OpenShift questions from Stack Overflow as a real-user benchmark.",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("data/ground_truth/so_queries.json"),
        help="Output path for the queries JSON file.",
    )
    parser.add_argument(
        "--max", type=int, default=150,
        dest="max_questions",
        help="Maximum number of questions to collect (default: 150).",
    )
    parser.add_argument(
        "--min-score", type=int, default=1,
        help="Minimum Stack Overflow score to include (default: 1).",
    )
    parser.add_argument(
        "--tags", nargs="+", default=["openshift"],
        help="Stack Overflow tags to search (default: openshift).",
    )
    parser.add_argument(
        "--api-key", default=None,
        help="Stack Exchange API key (falls back to SO_API_KEY env var).",
    )
    args = parser.parse_args()

    collect(
        output_path=args.output,
        max_questions=args.max_questions,
        min_score=args.min_score,
        tags=args.tags,
        api_key=args.api_key or os.getenv("SO_API_KEY"),
    )
