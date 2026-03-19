"""Generate a 100-query benchmark from actual processed documents.

Strategy:
- Stratified sample across all topics (proportional, min 3 per topic)
- For each sampled doc, call LLM to generate 1 realistic user query
- Gold doc = the document it was generated from
- Also tag sibling docs (same topic + overlapping title prefix) as secondary gold
- Skip docs shorter than 200 chars (too sparse to generate a useful query)
"""
from __future__ import annotations

import json
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

QUERY_PROMPT = """\
You are generating a benchmark dataset for an OpenShift documentation RAG system.

Below is a documentation excerpt. Write ONE realistic question that a platform engineer, \
cluster administrator, or SRE would ask that this document directly answers. \

Rules:
- The question must be answerable using THIS document (not general knowledge)
- Write it as a natural user question (e.g. "how do I...", "what is...", "why does...")
- Be specific enough that generic answers would miss the mark
- Do NOT reference the document itself (don't say "according to this doc")
- Return ONLY the question, no explanation

Document title: {title}
Topic: {topic}
Content type: {content_type}

Document excerpt:
{excerpt}"""


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _siblings(stem: str, all_stems: list[str]) -> list[str]:
    """Find stems with a shared prefix (likely related docs)."""
    parts = stem.split("-")
    if len(parts) < 3:
        return []
    prefix = "-".join(parts[:3])
    return [s for s in all_stems if s != stem and s.startswith(prefix)]


def generate_benchmark(
    processed_dir: Path,
    docs_root: Path,
    output_path: Path,
    target: int = 100,
    model: str = "gpt-4o-mini",
    seed: int = 42,
) -> None:
    random.seed(seed)

    # Build metadata map
    from ingest import discover
    modules = discover.discover(docs_root)
    mod_map = {m.filename: m for m in modules}

    # Group docs by topic, filtering to PROCEDURE + CONCEPT only
    by_topic: dict[str, list[dict]] = defaultdict(list)
    all_md = sorted(processed_dir.glob("*.md"))
    for md_path in all_md:
        stem = md_path.stem
        mod = mod_map.get(stem + ".adoc")
        if mod is None:
            continue
        if mod.content_type not in ("PROCEDURE", "CONCEPT"):
            continue
        text = md_path.read_text(encoding="utf-8", errors="replace")
        if len(text) < 200:
            continue
        by_topic[mod.topic].append({
            "stem": stem,
            "path": md_path,
            "topic": mod.topic,
            "content_type": mod.content_type,
            "text": text,
            "title": _extract_title(text) or stem,
        })

    # Stratified sample: proportional to topic size, min 3, max 20
    total_docs = sum(len(v) for v in by_topic.values())
    selected: list[dict] = []
    for topic, docs in sorted(by_topic.items()):
        quota = max(3, min(20, round(target * len(docs) / total_docs)))
        sampled = random.sample(docs, min(quota, len(docs)))
        selected.extend(sampled)

    # Trim/extend to exactly target
    random.shuffle(selected)
    selected = selected[:target]

    all_stems = [d["stem"] for d in selected]

    print(f"Generating {len(selected)} queries with {model}...")
    llm = ChatOpenAI(model=model, temperature=0.3)

    benchmark = []
    errors = 0
    for i, doc in enumerate(selected, 1):
        excerpt = doc["text"][:1500]
        prompt = QUERY_PROMPT.format(
            title=doc["title"],
            topic=doc["topic"],
            content_type=doc["content_type"],
            excerpt=excerpt,
        )

        for attempt in range(3):
            try:
                resp = llm.invoke([{"role": "user", "content": prompt}])
                query = resp.content.strip().strip('"').strip("'")
                break
            except Exception as e:
                if attempt == 2:
                    print(f"  [WARN] failed to generate query for {doc['stem']}: {e}")
                    query = None
                    errors += 1
                else:
                    time.sleep(2)

        if not query:
            continue

        siblings = _siblings(doc["stem"], all_stems)
        entry = {
            "id": re.sub(r"[^a-z0-9_-]", "-", doc["stem"].lower())[:60],
            "query": query,
            "topic": doc["topic"],
            "content_type": doc["content_type"],
            "gold_doc_ids": [doc["stem"]] + siblings[:2],
        }
        benchmark.append(entry)

        status = f"[{i}/{len(selected)}] {doc['stem'][:45]:<45}  {doc['content_type']:<10}  {doc['topic']}"
        print(status)
        print(f"         Q: {query[:100]}")

    output_path.write_text(json.dumps(benchmark, indent=2))
    print(f"\nWrote {len(benchmark)} queries to {output_path}  ({errors} errors)")

    # Topic distribution
    from collections import Counter
    dist = Counter(e["topic"] for e in benchmark)
    print("\nTopic distribution:")
    for topic, count in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"  {topic:<40} {count}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/ground_truth/queries.json"))
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--docs-root", type=Path, default=Path("openshift-docs"))
    args = parser.parse_args()

    generate_benchmark(
        processed_dir=args.processed_dir,
        docs_root=args.docs_root,
        output_path=args.output,
        target=args.target,
        model=args.model,
        seed=args.seed,
    )
