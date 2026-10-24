#!/usr/bin/env python3
"""
Mythos 5 — Gemini Web Semantic Memory & Playbook Search Engine (mythos_memory_search.py)
========================================================================================
Zero-dependency Hybrid Search Engine (Okapi BM25 + Character Trigram & Token Cosine Similarity)
for Gemini Web's offline Python sandbox. Searches across all 5 bundled knowledge bases:
  1. antibodies : Active PreToolUse & PostToolUse mistake-immunization antibodies
  2. episodes   : Past failure episodes, root causes, and verified fixes
  3. memories   : Operator profile (Avichal Goyal), preferences, and 28 owned/client workspaces
  4. skills     : All 88 Antigravity skills adapted for Gemini Web
  5. playbooks  : All 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP cybersecurity playbooks

Usage inside Gemini Web Python Sandbox:
  python scripts/mythos_memory_search.py --query "zero downtime database migration" --source skills
  python scripts/mythos_memory_search.py --query "jwt authentication bypass" --source playbooks --top-k 5
  python scripts/mythos_memory_search.py --query "trugifting solutions" --source memories
  python scripts/mythos_memory_search.py --query "powershell spawn hang" --source all
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
MEMORY_DIR = SKILL_ROOT / "memory"
PLAYBOOKS_DIR = SKILL_ROOT / "playbooks"

SOURCES_MAP = {
    "antibodies": MEMORY_DIR / "antibodies_catalog.csv",
    "episodes": MEMORY_DIR / "episodes_catalog.csv",
    "memories": MEMORY_DIR / "operator_memories.csv",
    "skills": MEMORY_DIR / "skills_catalog.csv",
    "playbooks": PLAYBOOKS_DIR / "cybersecurity_818_catalog.csv",
}

TOKEN_RX = re.compile(r"[a-z0-9_+-]{2,}")


def tokenize(text: str) -> List[str]:
    lower = text.lower()
    words = TOKEN_RX.findall(lower)
    # Add character 3-grams for fuzzy/subword semantic recall (analogous to subword embeddings)
    compact = re.sub(r"\s+", " ", lower)
    trigrams = [f"#{compact[i:i+3]}" for i in range(max(0, len(compact) - 2)) if len(compact[i:i+3].strip()) == 3]
    return words + trigrams[:120]


def load_records(source_filter: str) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    targets = SOURCES_MAP.keys() if source_filter == "all" else [source_filter]
    for src in targets:
        path = SOURCES_MAP.get(src)
        if not path or not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text_blob = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
                records.append({
                    "source": src,
                    "id": row.get("id") or row.get("name") or row.get("skill_id") or "",
                    "title": row.get("name") or row.get("title") or row.get("category") or row.get("id") or "",
                    "row": row,
                    "text": text_blob,
                })
    return records


def hybrid_search(query: str, records: List[Dict[str, Any]], top_k: int = 8) -> List[Dict[str, Any]]:
    if not records:
        return []
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    q_counts = Counter(q_tokens)
    q_norm = math.sqrt(sum(v * v for v in q_counts.values())) or 1.0

    doc_tokens = [tokenize(r["text"]) for r in records]
    doc_lens = [len(dt) for dt in doc_tokens]
    avg_dl = (sum(doc_lens) / len(doc_lens)) if doc_lens else 1.0

    df: Counter = Counter()
    for dt in doc_tokens:
        for tok in set(dt):
            df[tok] += 1

    N = len(records)
    k1 = 1.5
    b = 0.75
    scored: List[Tuple[float, Dict[str, Any]]] = []

    for idx, r in enumerate(records):
        dt = doc_tokens[idx]
        if not dt:
            continue
        d_counts = Counter(dt)
        dl = doc_lens[idx]

        # 1. Okapi BM25 score
        bm25 = 0.0
        for tok, qf in q_counts.items():
            if not tok.startswith("#") and tok in d_counts:
                tf = d_counts[tok]
                idf = math.log(1.0 + (N - df[tok] + 0.5) / (df[tok] + 0.5))
                bm25 += idf * ((tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (dl / avg_dl))))

        # 2. Subword + Token Cosine Similarity
        dot = sum(q_counts[t] * d_counts[t] for t in q_counts if t in d_counts)
        d_norm = math.sqrt(sum(v * v for v in d_counts.values())) or 1.0
        cosine = dot / (q_norm * d_norm)

        # Combine BM25 + Cosine
        combined = (0.65 * (bm25 / (bm25 + 4.0))) + (0.35 * cosine)
        if combined > 0.01:
            scored.append((round(combined, 4), r))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "score": score,
            "source": item["source"],
            "id": item["id"],
            "title": item["title"],
            "details": item["row"],
        }
        for score, item in scored[:top_k]
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Mythos 5 Gemini Web Hybrid Semantic Search")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument(
        "--source",
        default="all",
        choices=["all", "antibodies", "episodes", "memories", "skills", "playbooks"],
        help="Knowledge base to search",
    )
    parser.add_argument("--top-k", type=int, default=8, help="Number of results to return")
    args = parser.parse_args()

    records = load_records(args.source)
    hits = hybrid_search(args.query, records, top_k=args.top_k)
    print(json.dumps({
        "query": args.query,
        "source": args.source,
        "total_indexed_in_scope": len(records),
        "results": hits,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
