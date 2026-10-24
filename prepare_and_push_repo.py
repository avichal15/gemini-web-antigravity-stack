#!/usr/bin/env python3
"""
Prepares c:\\Users\\avich\\Downloads\\mythos\\gemini-web-antigravity-stack as a clean,
self-contained GitHub repository (https://github.com/avichal15/gemini-web-antigravity-stack)
optimized for Gemini Web (@GitHub extension, URL browsing, and sandbox execution).
Strictly read-only with respect to C:\\Users\\avich\\.gemini\\config.
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path(r"c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack")
MASTER = ROOT / "1-master-full-stack-skill" / "mythos-antigravity-stack"
REPO_SLUG = "avichal15/gemini-web-antigravity-stack"
REPO_URL = f"https://github.com/{REPO_SLUG}"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_SLUG}/main"
BLOB_BASE = f"https://github.com/{REPO_SLUG}/blob/main"


def scrub_local_keys():
    scrubbed = 0
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
                new_text = text.replace(
                    "YOUR_OMNIROUTE_API_KEY", "YOUR_OMNIROUTE_API_KEY"
                ).replace(
                    "YOUR_FREELLMAPI_API_KEY",
                    "YOUR_FREELLMAPI_API_KEY",
                )
                if new_text != text:
                    p.write_text(new_text, encoding="utf-8")
                    scrubbed += 1
            except Exception:
                pass
    print(f"Scrubbed local tokens in {scrubbed} files.")


def mirror_core_to_root():
    # Copy scripts/, memory/, playbooks/, references/ from MASTER to ROOT so root execution works out of the box
    for folder in ["scripts", "memory", "playbooks", "references"]:
        src = MASTER / folder
        dst = ROOT / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    # Copy MASTER/SKILL.md to ROOT/SKILL.md, ROOT/GEMINI.md, and ROOT/AGENTS.md
    skill_text = (MASTER / "SKILL.md").read_text(encoding="utf-8")
    (ROOT / "SKILL.md").write_text(skill_text, encoding="utf-8")
    (ROOT / "GEMINI.md").write_text(skill_text, encoding="utf-8")
    (ROOT / "AGENTS.md").write_text(skill_text, encoding="utf-8")
    print("Mirrored core runtime (SKILL.md, GEMINI.md, AGENTS.md, scripts/, memory/, playbooks/, references/) to repo root.")


def generate_skill_index_and_readme():
    ind_dir = ROOT / "3-individual-skills"
    pack_dir = ROOT / "2-domain-skill-packs"

    packs = sorted([d.name for d in pack_dir.iterdir() if d.is_dir()])
    skills = sorted([d.name for d in ind_dir.iterdir() if d.is_dir()])

    # Build SKILL_INDEX.md
    index_lines = [
        "# Mythos 5 Antigravity Stack — Complete Skill & Asset Index",
        "",
        f"Repository: `{REPO_URL}`",
        "",
        "## 1. Core Executable Engines (Root `/scripts`)",
        "",
        "| Script | Purpose | GitHub Link | Raw URL (for Gemini fetch/exec) |",
        "| :--- | :--- | :--- | :--- |",
        f"| `scripts/mythos_web_runtime.py` | PreToolUse Antibodies (`AB-001`–`AB-008`), Gravitas Read-Before-Edit & Exact-Retry Guards, PostToolUse AST/Slop/Secret verifier, `GATES.md` SHA-256 stamper | [View]({BLOB_BASE}/scripts/mythos_web_runtime.py) | `{RAW_BASE}/scripts/mythos_web_runtime.py` |",
        f"| `scripts/mythos_memory_search.py` | Hybrid Okapi BM25 + Character Trigram Cosine search across 930 records (8 antibodies, 4 episodes, 12 operator memories, 88 skills, 818 cybersecurity playbooks) | [View]({BLOB_BASE}/scripts/mythos_memory_search.py) | `{RAW_BASE}/scripts/mythos_memory_search.py` |",
        f"| `scripts/godmode_web_engine.py` | Godmode v4.0 AutoTune, Parseltongue (22 transforms), 4-Perspective Council, and Red-Team Challenge | [View]({BLOB_BASE}/scripts/godmode_web_engine.py) | `{RAW_BASE}/scripts/godmode_web_engine.py` |",
        "",
        "## 2. Memory & Playbook Catalogs (Root `/memory` & `/playbooks`)",
        "",
        "| Catalog | Records | GitHub Link | Raw URL |",
        "| :--- | :--- | :--- | :--- |",
        f"| `memory/antibodies_catalog.csv` | 8 Active PreToolUse Antibodies | [View]({BLOB_BASE}/memory/antibodies_catalog.csv) | `{RAW_BASE}/memory/antibodies_catalog.csv` |",
        f"| `memory/episodes_catalog.csv` | 4 Episodic Failure Ledgers | [View]({BLOB_BASE}/memory/episodes_catalog.csv) | `{RAW_BASE}/memory/episodes_catalog.csv` |",
        f"| `memory/operator_memories.csv` | 12 Operator & 28-Project Index Records | [View]({BLOB_BASE}/memory/operator_memories.csv) | `{RAW_BASE}/memory/operator_memories.csv` |",
        f"| `memory/skills_catalog.csv` | 88 Skills Metadata Catalog | [View]({BLOB_BASE}/memory/skills_catalog.csv) | `{RAW_BASE}/memory/skills_catalog.csv` |",
        f"| `playbooks/cybersecurity_818_catalog.csv` | 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP Playbooks | [View]({BLOB_BASE}/playbooks/cybersecurity_818_catalog.csv) | `{RAW_BASE}/playbooks/cybersecurity_818_catalog.csv` |",
        "",
        "## 3. Domain Skill Packs (`2-domain-skill-packs/`)",
        "",
        "| Domain Pack | SKILL.md Link | Raw SKILL.md URL |",
        "| :--- | :--- | :--- |",
    ]

    for p in packs:
        index_lines.append(
            f"| `{p}` | [SKILL.md]({BLOB_BASE}/2-domain-skill-packs/{p}/SKILL.md) | `{RAW_BASE}/2-domain-skill-packs/{p}/SKILL.md` |"
        )

    index_lines.extend([
        "",
        "## 4. All 88 Individual Skills (`3-individual-skills/`)",
        "",
        "| # | Skill Name | SKILL.md Link | Raw SKILL.md URL |",
        "| :--- | :--- | :--- | :--- |",
    ])

    for idx, s in enumerate(skills, 1):
        index_lines.append(
            f"| {idx} | `{s}` | [SKILL.md]({BLOB_BASE}/3-individual-skills/{s}/SKILL.md) | `{RAW_BASE}/3-individual-skills/{s}/SKILL.md` |"
        )

    (ROOT / "SKILL_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # Build comprehensive root README.md
    readme = f"""# Mythos 5 — Antigravity 2.0 Full Stack for Gemini Web

**Operator**: Avichal Goyal ([GitHub](https://github.com/avichal15) | [LinkedIn](https://www.linkedin.com/in/avichalgoyal007/))  
**Repository**: `{REPO_URL}`

This repository contains the complete **Antigravity 2.0 + Mythos 5** engineering, reasoning, memory, verification, and security stack (**88 specialized skills**, **7 domain packs**, **818 cybersecurity playbooks**, **Active Antibody Guardrails**, **Gravitas Drift/Retry Guards**, and **Godmode v4.0 Council/Challenge engines**) structured so **Gemini Web (`gemini.google.com`)** can load and execute it directly from GitHub.

---

## How to Tell Gemini Web to Use This Repository

Paste any of the prompts below directly into **Gemini Web** (works with Gemini URL browsing, `@GitHub` extension, or code import):

### Prompt 1 — General Full-Stack Execution (Recommended)
```text
Use my GitHub repository {REPO_URL} as your operating system and skill stack.
1. Read {RAW_BASE}/SKILL.md and {RAW_BASE}/SKILL_INDEX.md first.
2. Select and follow the matching skill(s) from 3-individual-skills/<skill-name>/SKILL.md (or 1-master-full-stack-skill/mythos-antigravity-stack/skills-library/<skill-name>.md).
3. Enforce the Mythos 5 Unlazy 4-Pass Protocol, Active Antibodies (memory/antibodies_catalog.csv), and No-AI-Slop rules.
Now execute this task: [YOUR TASK HERE]
```

### Prompt 2 —With `@GitHub` Extension in Gemini Web
```text
@GitHub {REPO_SLUG} Read SKILL.md and SKILL_INDEX.md, load the relevant skills and scripts from this repository, and execute: [YOUR TASK HERE]
```

---

## Instructions for Gemini (Machine-Readable Entrypoint)

When the operator instructs you to use `{REPO_URL}`, follow this exact protocol:

1. **Load Core OS Rules**: Read [`SKILL.md`]({BLOB_BASE}/SKILL.md) (also mirrored at [`GEMINI.md`]({BLOB_BASE}/GEMINI.md) and [`AGENTS.md`]({BLOB_BASE}/AGENTS.md)).
2. **Discover Relevant Skills**: Check [`SKILL_INDEX.md`]({BLOB_BASE}/SKILL_INDEX.md) or [`memory/skills_catalog.csv`]({BLOB_BASE}/memory/skills_catalog.csv) to find the exact skill(s) matching the task, then read `3-individual-skills/<skill-name>/SKILL.md`.
3. **Run the Python Verification & Memory Engines in Sandbox** (when executing code or searching memory/playbooks):
   - **Pre-Action Antibody & Drift Check**: `python scripts/mythos_web_runtime.py pre-check --command "<cmd>"`
   - **Post-Edit AST, Secret & Anti-Slop Verification**: `python scripts/mythos_web_runtime.py post-verify --file "<path>"`
   - **Completion Gate Verification**: `python scripts/mythos_web_runtime.py gate-check --gates GATES.md`
   - **Hybrid BM25 + N-Gram Search (930 Records)**: `python scripts/mythos_memory_search.py "<query>" --source all`
   - **Godmode v4.0 Council & Red-Team Challenge**:
     - `python scripts/godmode_web_engine.py council --prompt "<question>"`
     - `python scripts/godmode_web_engine.py challenge --plan "<plan>"`

---

## Repository Layout

| Path | Description |
| :--- | :--- |
| [`SKILL.md`]({BLOB_BASE}/SKILL.md) / [`GEMINI.md`]({BLOB_BASE}/GEMINI.md) / [`AGENTS.md`]({BLOB_BASE}/AGENTS.md) | Root-level Mythos 5 Apex OS & execution instructions |
| [`SKILL_INDEX.md`]({BLOB_BASE}/SKILL_INDEX.md) | Direct GitHub & Raw URLs for all 88 skills, 7 domain packs, scripts, and catalogs |
| [`ARCHITECTURE_BLUEPRINT.md`]({BLOB_BASE}/ARCHITECTURE_BLUEPRINT.md) | Complete subsystem mapping between Antigravity Desktop and Gemini Web |
| [`scripts/`]({BLOB_BASE}/scripts) | Executable Python sandbox engines (`mythos_web_runtime.py`, `mythos_memory_search.py`, `godmode_web_engine.py`) |
| [`memory/`]({BLOB_BASE}/memory) | Active antibodies (`AB-001`–`AB-008`), failure episodes, operator memories (28 workspaces), and 88-skill catalog |
| [`playbooks/`]({BLOB_BASE}/playbooks) | 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP security playbooks catalog (`cybersecurity_818_catalog.csv`) |
| [`1-master-full-stack-skill/mythos-antigravity-stack/`]({BLOB_BASE}/1-master-full-stack-skill/mythos-antigravity-stack) | Unified all-in-one master skill bundle with all 88 skills compiled in `skills-library/` |
| [`2-domain-skill-packs/`]({BLOB_BASE}/2-domain-skill-packs) | 7 modular domain skill packs (`mythos-core-os`, `mythos-fullstack-engineering`, `mythos-frontend-and-stitch`, `mythos-security-and-redteam`, `mythos-research-and-discovery`, `mythos-media-and-presentations`, `mythos-gemini-and-platform-dev`) |
| [`3-individual-skills/`]({BLOB_BASE}/3-individual-skills) | All 88 individual skills with their dedicated scripts, references, and templates |
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print("Generated root README.md and SKILL_INDEX.md.")


if __name__ == "__main__":
    scrub_local_keys()
    mirror_core_to_root()
    generate_skill_index_and_readme()
