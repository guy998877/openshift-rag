"""Benchmark generator v2 — cosine-similarity neighbourhood queries.

Strategy (differs from v1):
  1. Pick a random seed document from the vectorstore.
  2. Retrieve its k nearest neighbours using cosine similarity (from stored
     embeddings — no new embedding calls needed).
  3. Pass the full neighbourhood pool (seed + k neighbours) to a *query writer*
     LLM.  It writes ONE realistic, messy user query based on 1–3 of those
     documents and returns which doc indices it drew from.
  4. Pass each flagged document + the generated query to a *validator* LLM.
     All flagged docs must pass; any failure discards the whole entry.
  5. Accepted entries are appended to the output benchmark file.

Key differences from v1:
  - Multi-document gold sets by design (reflects real retrieval difficulty).
  - Queries are intentionally noisy / typo-ridden (harder benchmark).
  - Two-stage LLM pipeline with independent validation gate.
  - Source is the live vectorstore, not raw processed Markdown files.

Usage:
    python -m eval.generate_benchmark_v2 --n 100 --k 5
    python -m eval.generate_benchmark_v2 --n 50  --k 8 --output data/ground_truth/queries_v2.json
"""

from __future__ import annotations

import argparse
import json
import random
import re
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# ── Prompts ───────────────────────────────────────────────────────────────────

QUERY_WRITER_PROMPT = """\
You are simulating a real OpenShift cluster admin or developer who is searching \
for help. They might be in a Slack thread, filing a support ticket, or typing \
into a search box — so their writing is informal, sometimes sloppy, and they \
don't always include full context.

You are given {n_docs} documentation snippets (numbered 0 to {last_idx}).
Write ONE realistic user query that could be answered using some of these documents.

Rules:
- Base the query on 1, 2, or 3 of the provided documents — your choice. \
  Never use more than 3.
- Write like a real user: informal tone, occasional typos, abbreviations, \
  incomplete sentences. Think: "whats the commad to drain a node witohut \
  evicting deamonsets" not "How do I drain a node?"
- Do NOT copy exact phrases or titles from the documents.
- The query should feel like a genuine operational problem, not a quiz question.
- Return ONLY valid JSON, no markdown fences:
{{
  "query": "<the realistic messy user query>",
  "used_indices": [<list of 1–3 integer indices you based the query on>]
}}

Documents:
{doc_blocks}"""


VALIDATOR_PROMPT = """\
You are a relevance judge for an OpenShift documentation benchmark.

User query:
  {query}

Documentation snippet:
  Title: {title}
  Topic: {topic}
  Content type: {content_type}

  {excerpt}

Does this snippet contain information that DIRECTLY helps answer the user query? \
A snippet is relevant only if it covers the specific task, command, concept, or \
error the user is describing — not just the same general topic area.

Return ONLY valid JSON, no markdown fences:
{{"relevant": true_or_false, "reason": "<one sentence>"}}"""


# ── Chroma helpers ────────────────────────────────────────────────────────────


def _all_doc_ids(collection) -> list[str]:
    result = collection.get(include=[])
    return result["ids"]


def _seed_embedding(collection, doc_id: str) -> list[float]:
    result = collection.get(ids=[doc_id], include=["embeddings"])
    return result["embeddings"][0]


def _neighbours(
    collection, embedding: list[float], k: int, exclude_id: str
) -> list[dict]:
    """Return up to k nearest docs (excluding the seed itself)."""
    result = collection.query(
        query_embeddings=[embedding],
        n_results=k + 1,  # +1 because seed will appear at rank 0
        include=["metadatas", "documents", "distances"],
    )
    docs = []
    for i, doc_id in enumerate(result["ids"][0]):
        if doc_id == exclude_id:
            continue
        docs.append(
            {
                "id": doc_id,
                "content": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i],  # lower = more similar
            }
        )
        if len(docs) == k:
            break
    return docs


def _doc_to_block(idx: int, doc: dict) -> str:
    meta = doc["metadata"]
    title = meta.get("title", meta.get("file", "unknown"))
    topic = meta.get("topic", "")
    ctype = meta.get("content_type", "")
    excerpt = doc["content"][:600].replace("\n", " ")
    return f"[{idx}] Title: {title} | Topic: {topic} | Type: {ctype}\n    {excerpt}"


# ── LLM calls ─────────────────────────────────────────────────────────────────


def _call_with_retry(llm, prompt: str, max_retries: int = 4) -> str | None:
    import re as _re

    RATE_RE = _re.compile(r"try again in (\d+(?:\.\d+)?)s", _re.IGNORECASE)
    last_exc = None
    for attempt in range(max_retries):
        try:
            resp = llm.invoke([{"role": "user", "content": prompt}])
            return resp.content.strip()
        except Exception as e:
            last_exc = e
            s = str(e)
            is_rate = "rate_limit_exceeded" in s or "RateLimitError" in type(e).__name__
            if is_rate and attempt < max_retries - 1:
                m = RATE_RE.search(s)
                wait = float(m.group(1)) + 1.0 if m else 10.0 * (2**attempt)
                time.sleep(wait)
                continue
            break
    print(f"    [warn] LLM call failed: {last_exc}")
    return None


def _parse_json(text: str) -> dict | None:
    """Strip optional markdown fences then parse JSON."""
    clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return None


def generate_query(pool: list[dict], writer_llm) -> tuple[str, list[int]] | None:
    """Ask the writer LLM to produce a query + which docs it used."""
    blocks = "\n\n".join(_doc_to_block(i, d) for i, d in enumerate(pool))
    prompt = QUERY_WRITER_PROMPT.format(
        n_docs=len(pool),
        last_idx=len(pool) - 1,
        doc_blocks=blocks,
    )
    raw = _call_with_retry(writer_llm, prompt)
    if not raw:
        return None
    parsed = _parse_json(raw)
    if not parsed:
        return None
    query = parsed.get("query", "").strip()
    indices = parsed.get("used_indices", [])
    if not query or not indices:
        return None
    # Clamp indices to valid range, deduplicate, limit to 3
    indices = list(
        dict.fromkeys(i for i in indices if isinstance(i, int) and 0 <= i < len(pool))
    )[:3]
    return query, indices


def validate_doc(query: str, doc: dict, validator_llm) -> tuple[bool, str]:
    """Return (is_relevant, reason)."""
    meta = doc["metadata"]
    title = meta.get("title", meta.get("file", "unknown"))
    topic = meta.get("topic", "")
    ctype = meta.get("content_type", "")
    excerpt = doc["content"][:800]
    prompt = VALIDATOR_PROMPT.format(
        query=query,
        title=title,
        topic=topic,
        content_type=ctype,
        excerpt=excerpt,
    )
    raw = _call_with_retry(validator_llm, prompt)
    if not raw:
        return False, "llm call failed"
    parsed = _parse_json(raw)
    if not parsed:
        return False, "unparseable response"
    return bool(parsed.get("relevant", False)), parsed.get("reason", "")


# ── Main generation loop ──────────────────────────────────────────────────────


def generate_benchmark_v2(
    chroma_dir: Path,
    collection_name: str,
    output_path: Path,
    n: int = 100,
    k: int = 5,
    writer_model: str = "gpt-4.1",
    validator_model: str = "gpt-4o-mini",
    seed: int = 42,
) -> None:
    from services.pipeline import build_vectorstore

    random.seed(seed)

    print("\nLoading vectorstore …", end=" ", flush=True)
    vs = build_vectorstore(chroma_dir, collection_name)
    collection = vs._collection
    all_ids = _all_doc_ids(collection)
    print(f"{len(all_ids)} docs")

    writer_llm = __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI(
        model=writer_model,
        temperature=0.8,
    )
    validator_llm = __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI(
        model=validator_model,
        temperature=0,
    )

    # Load existing output so we can append without duplicates
    existing: list[dict] = []
    if output_path.exists():
        existing = json.loads(output_path.read_text())
        print(f"Appending to existing {len(existing)}-entry benchmark at {output_path}")
    existing_ids = {e["id"] for e in existing}

    benchmark: list[dict] = list(existing)
    accepted = rejected = skipped = 0

    # Sample seeds (more than n to account for rejections)
    candidates = random.sample(all_ids, min(len(all_ids), n * 4))
    target_new = n

    print(
        f"Generating {target_new} new entries (k={k} neighbours, writer={writer_model}, "
        f"validator={validator_model}) …\n"
    )

    for seed_id in candidates:
        if accepted >= target_new:
            break

        # ── Step 1: build neighbourhood pool ──────────────────────────────
        try:
            emb = _seed_embedding(collection, seed_id)
            nbrs = _neighbours(collection, emb, k, exclude_id=seed_id)
        except Exception as e:
            print(f"  [skip] embedding lookup failed for {seed_id}: {e}")
            skipped += 1
            continue

        seed_meta = collection.get(ids=[seed_id], include=["metadatas", "documents"])
        seed_doc = {
            "id": seed_id,
            "content": seed_meta["documents"][0],
            "metadata": seed_meta["metadatas"][0],
            "distance": 0.0,
        }
        pool = [seed_doc] + nbrs  # index 0 = seed

        # ── Step 2: generate query ─────────────────────────────────────────
        result = generate_query(pool, writer_llm)
        if result is None:
            print(f"  [skip] query generation failed for seed {seed_id[:40]}")
            skipped += 1
            continue
        query, used_indices = result

        # ── Step 3: validate each flagged document ─────────────────────────
        used_docs = [pool[i] for i in used_indices]
        valid_docs = []
        all_passed = True
        reasons = []
        for doc in used_docs:
            ok, reason = validate_doc(query, doc, validator_llm)
            reasons.append(f"{'✓' if ok else '✗'} {doc['id'][:40]}: {reason}")
            if ok:
                valid_docs.append(doc)
            else:
                all_passed = False

        if not all_passed:
            rejected += 1
            print(f"  [reject] {seed_id[:40]}")
            for r in reasons:
                print(f"           {r}")
            continue

        # ── Step 4: build entry ────────────────────────────────────────────
        gold_ids = [d["id"] for d in valid_docs]
        # Derive a stable id from the seed stem
        entry_id = re.sub(r"[^a-z0-9_-]", "-", seed_id.lower())[:60]
        if entry_id in existing_ids:
            skipped += 1
            continue

        # Infer topic/content_type from the seed doc's metadata
        smeta = seed_doc["metadata"]
        entry = {
            "id": entry_id,
            "query": query,
            "topic": smeta.get("topic", ""),
            "content_type": smeta.get("content_type", ""),
            "gold_doc_ids": gold_ids,
            "_generation": {
                "seed_id": seed_id,
                "k_neighbours": k,
                "used_indices": used_indices,
                "writer_model": writer_model,
                "validator_model": validator_model,
            },
        }
        benchmark.append(entry)
        existing_ids.add(entry_id)
        accepted += 1

        print(
            f"  [{accepted:>3}/{target_new}] {entry_id[:45]:<45}  gold={len(gold_ids)}"
        )
        print(f"           Q: {query[:110]}")
        for r in reasons:
            print(f"           {r}")

    # ── Write output ───────────────────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(benchmark, indent=2))

    print(f"\n{'=' * 60}")
    print(f"  Accepted : {accepted}")
    print(f"  Rejected : {rejected}  (validator failed ≥1 doc)")
    print(f"  Skipped  : {skipped}   (errors / duplicates)")
    print(f"  Total in file : {len(benchmark)}")
    print(f"  Output   : {output_path}")
    print(f"{'=' * 60}")

    # Gold set size distribution
    from collections import Counter

    gold_dist = Counter(len(e["gold_doc_ids"]) for e in benchmark if "_generation" in e)
    print("\n  Gold doc count distribution (v2 entries only):")
    for n_gold, cnt in sorted(gold_dist.items()):
        print(f"    {n_gold} gold doc(s): {cnt} queries")


# ── CLI ────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m eval.generate_benchmark_v2",
        description="Generate a cosine-neighbourhood benchmark with two-stage LLM validation.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=100,
        help="Number of NEW entries to generate (default: 100)",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Neighbourhood size for cosine similarity (default: 5)",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("data/ground_truth/queries_v2.json")
    )
    parser.add_argument("--chroma-dir", type=Path, default=Path("./chroma_db"))
    parser.add_argument("--collection", default="openshift_docs_v0")
    parser.add_argument("--writer-model", default="gpt-4.1")
    parser.add_argument("--validator-model", default="gpt-4o-mini")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    generate_benchmark_v2(
        chroma_dir=args.chroma_dir,
        collection_name=args.collection,
        output_path=args.output,
        n=args.n,
        k=args.k,
        writer_model=args.writer_model,
        validator_model=args.validator_model,
        seed=args.seed,
    )


main()
