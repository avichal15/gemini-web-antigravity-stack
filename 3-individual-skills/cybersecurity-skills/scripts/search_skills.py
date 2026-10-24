#!/usr/bin/env python3
"""Fast BM25/keyword search across all 818 skills in Anthropic-Cybersecurity-Skills."""

import argparse
import json
import pathlib
import re
import sys

LIBRARY_ROOT = pathlib.Path(r"C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills")
INDEX_PATH = LIBRARY_ROOT / "index.json"


def load_skills():
    if INDEX_PATH.exists():
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8", errors="replace"))
        if isinstance(data, dict) and "skills" in data:
            return data["skills"]
        if isinstance(data, list):
            return data
    skills = []
    skills_dir = LIBRARY_ROOT / "skills"
    if skills_dir.exists():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            skills.append({"name": skill_md.parent.name, "path": str(skill_md)})
    return skills


def score_skill(item: dict, terms: list[str]) -> int:
    name = str(item.get("name") or item.get("id") or "").lower()
    subdomain = str(item.get("subdomain") or item.get("domain") or "").lower()
    desc = str(item.get("description") or "").lower()
    tags = " ".join(str(t).lower() for t in (item.get("tags") or []))
    attack = " ".join(str(t).lower() for t in (item.get("mitre_attack") or []))
    blob = f"{name} {subdomain} {tags} {attack} {desc}"

    score = 0
    for term in terms:
        if term in name:
            score += 10
        if term in tags or term in subdomain or term in attack:
            score += 6
        if term in desc:
            score += 3
        elif term in blob:
            score += 1
    return score


def main():
    parser = argparse.ArgumentParser(description="Search 818 Anthropic Cybersecurity Skills")
    parser.add_argument("query", help="Search keywords, domain, or MITRE ATT&CK ID")
    parser.add_argument("--limit", type=int, default=10, help="Max results to return")
    args = parser.parse_args()

    terms = [t.lower() for t in re.split(r"\s+", args.query.strip()) if t]
    skills = load_skills()
    scored = []
    for s in skills:
        sc = score_skill(s, terms)
        if sc > 0:
            scored.append((sc, s))

    scored.sort(key=lambda x: (-x[0], str(x[1].get("name", ""))))
    top = scored[: args.limit]

    results = []
    for sc, s in top:
        name = s.get("name") or s.get("id")
        skill_path = LIBRARY_ROOT / "skills" / str(name) / "SKILL.md"
        results.append(
            {
                "score": sc,
                "name": name,
                "subdomain": s.get("subdomain") or s.get("domain"),
                "description": s.get("description"),
                "mitre_attack": s.get("mitre_attack", []),
                "nist_csf": s.get("nist_csf", []),
                "skill_md_path": str(skill_path),
            }
        )

    print(json.dumps({"query": args.query, "total_indexed": len(skills), "matches": len(scored), "results": results}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
