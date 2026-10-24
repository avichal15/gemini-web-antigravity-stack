#!/usr/bin/env python3
"""
Builder for c:\\Users\\avich\\Downloads\\mythos\\gemini-web-antigravity-stack
==========================================================================
Strictly READ-ONLY on the desktop Antigravity environment (C:\\Users\\avich\\.gemini\\...).
Copies, sanitizes, and adapts the entire Antigravity Mythos 5 stack (87 skills + Mythos Core OS
+ Hooks + Antibodies + Episodic Memory + EmbeddingGemma 2 Index + 818 Cybersecurity Playbooks
+ Godmode v4.0) into Gemini Web-compatible skill folders under:
  c:\\Users\\avich\\Downloads\\mythos\\gemini-web-antigravity-stack\\
"""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple

STACK_ROOT = Path(r"c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack")
MASTER_SKILL_DIR = STACK_ROOT / "1-master-full-stack-skill" / "mythos-antigravity-stack"
DOMAIN_PACKS_DIR = STACK_ROOT / "2-domain-skill-packs"
INDIVIDUAL_SKILLS_DIR = STACK_ROOT / "3-individual-skills"

SKILL_ROOTS = [
    Path(r"C:\Users\avich\.gemini\config\skills"),
    Path(r"C:\Users\avich\.gemini\config\plugins\agent-skills\skills"),
    Path(r"C:\Users\avich\.gemini\config\plugins\gemini-api\skills"),
    Path(r"C:\Users\avich\.gemini\config\plugins\android-cli-plugin\skills"),
    Path(r"C:\Users\avich\.gemini\antigravity\builtin\skills"),
    Path(r"c:\Users\avich\Downloads\mythos\.agents\skills"),
]

ALLOWED_EXTS = {".md", ".py", ".txt", ".csv", ".pdf", ".png", ".jpg", ".jpeg"}
CONVERT_TO_MD_EXTS = {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".cmd", ".yaml", ".yml", ".json", ".html", ".css", ".xml", ".example"}
SKIP_BULK_EXTS = {".svg", ".wav", ".webp", ".pyc"}


def to_kebab_case(raw_name: str, fallback_folder: str) -> str:
    s = raw_name.strip().strip("'\"")
    if not s or s == "NO_NAME":
        s = fallback_folder
    s = s.replace("::", "-")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    s = re.sub(r"-+", "-", s).strip("-").lower()
    return s or "custom-skill"


def parse_frontmatter(md_text: str, folder_name: str) -> Tuple[str, str, str]:
    """Returns (kebab_name, description, body_without_frontmatter)."""
    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?", md_text)
    if not m:
        kebab = to_kebab_case(folder_name, folder_name)
        desc = f"Antigravity skill {kebab} adapted for Gemini Web."
        return kebab, desc, md_text

    fm = m.group(1)
    body = md_text[m.end():]
    name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    raw_name = name_m.group(1).strip() if name_m else folder_name
    kebab = to_kebab_case(raw_name, folder_name)

    desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    desc = desc_m.group(1).strip().strip("'\"") if desc_m else f"Antigravity {kebab} workflow adapted for Gemini Web."
    if desc in ("|", ">", ">-", "|-") or len(desc) < 8:
        # Multiline YAML description
        lines = []
        in_desc = False
        for line in fm.splitlines():
            if line.startswith("description:"):
                in_desc = True
                rest = line.split(":", 1)[1].strip()
                if rest not in ("|", ">", ">-", "|-", ""):
                    lines.append(rest)
                continue
            if in_desc:
                if re.match(r"^[a-zA-Z0-9_-]+:", line):
                    break
                lines.append(line.strip())
        desc = " ".join(x for x in lines if x).strip() or f"Antigravity {kebab} workflow adapted for Gemini Web."

    # Keep description single-line YAML safe
    desc = re.sub(r"\s+", " ", desc).replace('"', "'")[:450]
    return kebab, desc, body


def classify_domain_pack(kebab_name: str) -> str:
    if kebab_name in {
        "mythos-apex-core", "mythos-unfiltered-execution", "unlazy", "godmode",
        "gemma-reflexion", "doubt-driven-development", "evidence-and-claims",
        "no-ai-slop", "parallel-agent-work", "ag-worktree-team", "ag-handoff",
        "using-agent-skills",
    }:
        return "mythos-core-os"
    if kebab_name in {
        "cybersecurity-skills", "security-boundaries", "security-and-hardening",
        "signal-interpreter", "adversarial-review", "credentials",
    }:
        return "mythos-security-and-redteam"
    if "stitch" in kebab_name or kebab_name in {
        "design-md", "enhance-prompt", "site-md", "taste-design", "shadcn-ui",
        "react-vite-dashboard", "frontend-craft", "frontend-ui-engineering",
        "generative-ui", "ag-browser-check", "browser-testing-with-devtools",
        "agent-browser",
    }:
        return "mythos-frontend-and-stitch"
    if kebab_name in {
        "deep-discovery", "agent-reach", "context-engineering", "idea-refine",
        "interview-me", "documentation-and-adrs", "notebooklm",
    }:
        return "mythos-research-and-discovery"
    if kebab_name in {
        "cli-anything-google-vids", "hyperframes", "ppt-master", "remotion", "watch",
    }:
        return "mythos-media-and-presentations"
    if kebab_name in {
        "gemini-api-dev", "gemini-live-api-dev", "gemini-omni-flash-api",
        "android-cli", "agy-customizations", "antigravity-guide", "automation",
        "migrate-workflows", "workflow-skill-creator", "permissioned-github",
        "plugin", "run-workflow", "ui-plugin-navigation", "platform-qualification",
        "uv",
    }:
        return "mythos-gemini-and-platform-dev"
    return "mythos-fullstack-engineering"


def build_gemini_web_adaptation_block(kebab_name: str, domain_pack: str) -> str:
    return f"""
---

## Gemini Web Execution Adaptation (`{kebab_name}`)

When executing `{kebab_name}` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

1. **Shell, Linter & Gate Verification (`run_command` / `hooks.json`)**:
   - Execute Python validation, calculations, AST/syntax checks, and gate checks directly inside **Gemini Web's Python Code Execution Sandbox**.
   - If `scripts/mythos_web_runtime.py` is bundled in the active skill folder, run:
     - `python scripts/mythos_web_runtime.py pre-check --action "<action>" --target "<cmd_or_file>"`
     - `python scripts/mythos_web_runtime.py post-verify --file "<generated_file>"`
     - `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve`
   - When generating PowerShell/Bash commands meant for the operator's local Windows machine, output complete, copy-paste-ready scripts (respecting Antibody `AB-002`: prepend `& ` to quoted `.exe` paths in PowerShell).

2. **Web Research, Discovery & Documentation Grounding (`search_web` / `context7` / `agent-reach` / `scrapling`)**:
   - Use **Gemini Google Search Grounding** and **URL Fetch / Browsing** to verify primary documentation, GitHub repositories, release versions, and API signatures before writing code.
   - For bundled playbooks, skills, or operator project memory, query `python scripts/mythos_memory_search.py --query "<topic>" --source all`.

3. **Frontend Rendering, Stitch Design & Browser Verification (`ag-browser-check` / `chrome-devtools-mcp` / `StitchMCP`)**:
   - Render interactive UI previews, React/Tailwind components, dashboards, and data visualizations directly inside **Gemini Canvas** (or as self-contained single-file HTML/React artifacts) and verify responsive layout, accessibility contrast, and interactive states before completion.

4. **Multi-Agent & Godmode Deliberation (`invoke_subagent` / `godmode_council` / `godmode_challenge`)**:
   - Run `python scripts/godmode_web_engine.py council --question "<architectural_question>"` and `python scripts/godmode_web_engine.py challenge --target "<plan_or_file>"` inside the Python sandbox to execute the 4-Perspective Council (Opus Systems + Codex Pragmatist + Gemini Integration + Nemotron Scale) and Adversarial Red-Team Challenge pass.
"""


def build_memory_and_playbook_csvs() -> Dict[str, int]:
    counts = {}
    mem_dir = MASTER_SKILL_DIR / "memory"
    pb_dir = MASTER_SKILL_DIR / "playbooks"
    mem_dir.mkdir(parents=True, exist_ok=True)
    pb_dir.mkdir(parents=True, exist_ok=True)

    # 1. Antibodies CSV (from antibodies.json + Gravitas guards)
    ab_json_path = Path(r"C:\Users\avich\.gemini\config\memory\antibodies.json")
    antibodies = []
    if ab_json_path.exists():
        data = json.loads(ab_json_path.read_text(encoding="utf-8"))
        antibodies.extend(data.get("antibodies", []))

    # Add Gravitas-derived antibodies into the exported Gemini Web catalog
    antibodies.extend([
        {
            "id": "AB-007",
            "name": "gravitas-read-before-edit-invariant",
            "tool": "edit_file|write_file",
            "match_regex": "OVERWRITE_UNREAD_EXISTING_FILE",
            "must_not_contain": "",
            "action": "warn",
            "symptom": "Blindly editing an existing file without reading its current lines causes target mismatch or overwrites adjacent logic.",
            "root_cause": "Mutating a file from memory or stale context instead of inspecting current file contents first.",
            "prevention": "Always read the target file in the current session before calling edit_file or overwriting it.",
        },
        {
            "id": "AB-008",
            "name": "gravitas-never-exact-retry-failure",
            "tool": "run_command|edit_file|write_file",
            "match_regex": "DUPLICATE_FAILED_ACTION_FINGERPRINT",
            "must_not_contain": "",
            "action": "block",
            "symptom": "Retrying the exact byte-identical failing command or edit wastes tokens and repeats the same error.",
            "root_cause": "Re-running a failed tool call without inspecting state or modifying arguments.",
            "prevention": "Inspect error output, read the relevant state/file, and change the command or arguments before retrying.",
        },
    ])

    ab_csv = mem_dir / "antibodies_catalog.csv"
    with ab_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "name", "tool", "match_regex", "must_not_contain", "action", "symptom", "root_cause", "prevention"],
        )
        writer.writeheader()
        for ab in antibodies:
            writer.writerow({
                "id": ab.get("id", ""),
                "name": ab.get("name", ""),
                "tool": ab.get("tool", ""),
                "match_regex": ab.get("match_regex", ""),
                "must_not_contain": ab.get("must_not_contain", ""),
                "action": ab.get("action", "warn"),
                "symptom": ab.get("symptom", ""),
                "root_cause": ab.get("root_cause", ""),
                "prevention": ab.get("prevention", ""),
            })
    counts["antibodies"] = len(antibodies)

    # 2. Episodes CSV (from episodes.jsonl)
    ep_jsonl_path = Path(r"C:\Users\avich\.gemini\config\memory\episodes.jsonl")
    episodes = []
    if ep_jsonl_path.exists():
        for line in ep_jsonl_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    episodes.append(json.loads(line))
                except Exception:
                    pass
    ep_csv = mem_dir / "episodes_catalog.csv"
    with ep_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "timestamp", "category", "file", "symptom", "root_cause", "fix"],
        )
        writer.writeheader()
        for ep in episodes:
            writer.writerow({
                "id": ep.get("id", ""),
                "timestamp": ep.get("timestamp", ""),
                "category": ep.get("category", ""),
                "file": ep.get("file", ep.get("workspace", "")),
                "symptom": ep.get("symptom", ""),
                "root_cause": ep.get("root_cause", ""),
                "fix": ep.get("fix", ""),
            })
    counts["episodes"] = len(episodes)

    # 3. Operator Memories CSV (from C:\Users\avich\.agentmemory\standalone.json)
    standalone_path = Path(r"C:\Users\avich\.agentmemory\standalone.json")
    memories = []
    if standalone_path.exists():
        raw_mem = json.loads(standalone_path.read_text(encoding="utf-8"))
        mem_list = raw_mem.get("mem:memories") or raw_mem.get("memories") or []
        if isinstance(mem_list, dict):
            mem_list = list(mem_list.values())
        if isinstance(mem_list, list):
            for item in mem_list:
                if isinstance(item, dict) and item.get("isLatest") is not False:
                    memories.append(item)
    mem_csv = mem_dir / "operator_memories.csv"
    with mem_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "category", "tags", "summary", "content"],
        )
        writer.writeheader()
        for m in memories:
            tags = m.get("concepts") or m.get("tags") or []
            writer.writerow({
                "id": m.get("id", ""),
                "category": m.get("type") or m.get("category", "general"),
                "tags": ", ".join(str(x) for x in tags) if isinstance(tags, list) else str(tags),
                "summary": str(m.get("title") or m.get("summary", ""))[:300],
                "content": str(m.get("content", ""))[:3000],
            })
    counts["memories"] = len(memories)

    # 4. Cybersecurity 818 Playbooks CSV
    cy_index_path = Path(r"C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills\index.json")
    playbooks = []
    if cy_index_path.exists():
        cy_data = json.loads(cy_index_path.read_text(encoding="utf-8"))
        playbooks = cy_data.get("skills", []) if isinstance(cy_data, dict) else cy_data
    pb_csv = pb_dir / "cybersecurity_818_catalog.csv"
    with pb_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "name", "domain", "subdomain", "frameworks", "description"],
        )
        writer.writeheader()
        for pb in playbooks:
            fw = pb.get("frameworks") or pb.get("mappings") or pb.get("tags") or []
            fw_str = ", ".join(fw) if isinstance(fw, list) else str(fw)
            writer.writerow({
                "id": pb.get("id") or pb.get("slug") or pb.get("name", ""),
                "name": pb.get("name") or pb.get("title", ""),
                "domain": pb.get("domain") or pb.get("category", ""),
                "subdomain": pb.get("subdomain") or "",
                "frameworks": fw_str[:250],
                "description": str(pb.get("description", ""))[:500],
            })
    counts["playbooks"] = len(playbooks)
    return counts


def copy_and_adapt_supporting_files(src_skill_dir: Path, dst_skill_dir: Path, kebab_name: str) -> int:
    """
    Copies supporting files from src_skill_dir into dst_skill_dir while enforcing:
    1. Only Gemini Web allowed extensions (.md, .py, .txt, .csv, .pdf, .png, .jpg, .jpeg)
    2. Converts .js/.mjs/.ts/.tsx/.sh/.json/.yaml/.html/.css into .md code-reference files
    3. For ppt-master's 12,193 .svg and 186 .wav files, summarizes them into a single .csv catalog
    """
    file_count = 0
    svg_wav_catalog: List[Tuple[str, str, int]] = []

    for src_file in sorted(src_skill_dir.rglob("*")):
        if not src_file.is_file():
            continue
        if src_file.name == "SKILL.md" and src_file.parent == src_skill_dir:
            continue
        if "__pycache__" in src_file.parts or ".git" in src_file.parts:
            continue

        rel = src_file.relative_to(src_skill_dir)
        ext = src_file.suffix.lower()

        if ext in SKIP_BULK_EXTS:
            if ext in (".svg", ".wav"):
                svg_wav_catalog.append((str(rel).replace("\\", "/"), ext.lstrip("."), src_file.stat().st_size))
            continue

        if ext in ALLOWED_EXTS:
            out_path = dst_skill_dir / rel
            # Make sure nested SKILL.md files (if any exist in subdirs) are renamed so only root SKILL.md exists
            if out_path.name.upper() == "SKILL.MD":
                out_path = out_path.with_name("SUB_SKILL_REFERENCE.md")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, out_path)
            file_count += 1
        elif ext in CONVERT_TO_MD_EXTS or not ext:
            # Convert to .md reference file so Gemini Web accepts it 100%
            safe_name = src_file.name.lstrip(".") + ".md"
            out_path = (dst_skill_dir / rel).with_name(safe_name)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            raw_content = src_file.read_text(encoding="utf-8", errors="replace")
            lang = ext.lstrip(".") or "text"
            wrapped = (
                f"# Reference Asset: `{rel.as_posix()}`\n\n"
                f"Converted to Markdown for Gemini Web upload compatibility.\n\n"
                f"````{lang}\n{raw_content}\n````\n"
            )
            out_path.write_text(wrapped, encoding="utf-8")
            file_count += 1

    if svg_wav_catalog:
        cat_path = dst_skill_dir / "templates" / "bundled_icons_and_audio_catalog.csv"
        cat_path.parent.mkdir(parents=True, exist_ok=True)
        with cat_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["relative_path", "asset_type", "bytes"])
            for row in svg_wav_catalog:
                w.writerow(row)
        file_count += 1

    return file_count


def main() -> None:
    print("Building Gemini Web Antigravity Stack...")
    STACK_ROOT.mkdir(parents=True, exist_ok=True)
    MASTER_SKILL_DIR.mkdir(parents=True, exist_ok=True)
    DOMAIN_PACKS_DIR.mkdir(parents=True, exist_ok=True)
    INDIVIDUAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    counts = build_memory_and_playbook_csvs()
    print(f"Exported memory & playbook catalogs: {counts}")

    # Discover all 87 skills
    discovered_skills: List[Dict[str, Any]] = []
    seen_kebab = set()

    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for skill_md in sorted(root.rglob("SKILL.md")):
            # Only top-level skill directories under each root
            if skill_md.parent.parent != root and not (root.name == "skills" and skill_md.parent == root):
                continue
            raw_text = skill_md.read_text(encoding="utf-8", errors="replace")
            kebab, desc, body = parse_frontmatter(raw_text, skill_md.parent.name)
            if kebab in seen_kebab:
                continue
            seen_kebab.add(kebab)
            domain = classify_domain_pack(kebab)
            discovered_skills.append({
                "kebab": kebab,
                "desc": desc,
                "body": body,
                "domain": domain,
                "src_dir": skill_md.parent,
            })

    # Add the 88th skill: mythos-apex-core (direct port of C:\Users\avich\.gemini\config\AGENTS.md)
    agents_md_text = Path(r"C:\Users\avich\.gemini\config\AGENTS.md").read_text(encoding="utf-8", errors="replace")
    discovered_skills.insert(0, {
        "kebab": "mythos-apex-core",
        "desc": "Mythos 5 Apex Agent Core Operating System: Unrestricted execution, anti-hallucination, four-pass Unlazy gate verification, Active Antibody reflexion, and Godmode 4-family council.",
        "body": agents_md_text,
        "domain": "mythos-core-os",
        "src_dir": None,
    })

    print(f"Total skills prepared for Gemini Web: {len(discovered_skills)}")

    # Write skills_catalog.csv inside MASTER_SKILL_DIR/memory/
    skills_csv = MASTER_SKILL_DIR / "memory" / "skills_catalog.csv"
    with skills_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "domain_pack", "description", "master_library_path", "individual_skill_folder"])
        writer.writeheader()
        for s in discovered_skills:
            writer.writerow({
                "id": s["kebab"],
                "name": s["kebab"],
                "domain_pack": s["domain"],
                "description": s["desc"],
                "master_library_path": f"skills-library/{s['kebab']}.md",
                "individual_skill_folder": f"3-individual-skills/{s['kebab']}",
            })

    # Populate:
    # 1. Master Skill skills-library/<kebab>.md
    # 2. Individual Skills 3-individual-skills/<kebab>/SKILL.md + supporting files
    # 3. Domain Skill Packs 2-domain-skill-packs/<domain>/
    master_lib_dir = MASTER_SKILL_DIR / "skills-library"
    master_lib_dir.mkdir(parents=True, exist_ok=True)

    by_domain: Dict[str, List[Dict[str, Any]]] = {}

    for s in discovered_skills:
        kebab = s["kebab"]
        desc = s["desc"]
        domain = s["domain"]
        adapt_block = build_gemini_web_adaptation_block(kebab, domain)
        by_domain.setdefault(domain, []).append(s)

        # (A) Write into Master Skill's skills-library/<kebab>.md (NO YAML frontmatter so only root SKILL.md has frontmatter)
        lib_md = (
            f"# Skill Module: `{kebab}`\n\n"
            f"- **Domain Pack**: `{domain}`\n"
            f"- **Description**: {desc}\n\n"
            f"{s['body'].strip()}\n"
            f"{adapt_block}\n"
        )
        (master_lib_dir / f"{kebab}.md").write_text(lib_md, encoding="utf-8")

        # (B) Write Individual Skill Folder: 3-individual-skills/<kebab>/SKILL.md
        ind_dir = INDIVIDUAL_SKILLS_DIR / kebab
        ind_dir.mkdir(parents=True, exist_ok=True)
        ind_skill_md = (
            f"---\n"
            f"name: {kebab}\n"
            f"description: \"{desc}\"\n"
            f"---\n\n"
            f"{s['body'].strip()}\n"
            f"{adapt_block}\n"
        )
        (ind_dir / "SKILL.md").write_text(ind_skill_md, encoding="utf-8")

        if s["src_dir"] is not None:
            copy_and_adapt_supporting_files(s["src_dir"], ind_dir, kebab)
        else:
            # For mythos-apex-core, bundle the 3 core Python runtime scripts + memory CSVs
            ind_scripts = ind_dir / "scripts"
            ind_scripts.mkdir(parents=True, exist_ok=True)
            for py_file in (MASTER_SKILL_DIR / "scripts").glob("*.py"):
                shutil.copy2(py_file, ind_scripts / py_file.name)
            ind_mem = ind_dir / "memory"
            ind_mem.mkdir(parents=True, exist_ok=True)
            for csv_file in (MASTER_SKILL_DIR / "memory").glob("*.csv"):
                shutil.copy2(csv_file, ind_mem / csv_file.name)

    # Build Desktop Architecture Reference inside Master Skill
    ref_dir = MASTER_SKILL_DIR / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)
    hooks_json = Path(r"C:\Users\avich\.gemini\config\hooks.json").read_text(encoding="utf-8", errors="replace")
    pre_hook = Path(r"C:\Users\avich\.gemini\config\hooks\pre-tool-rtk.mjs").read_text(encoding="utf-8", errors="replace")
    post_hook = Path(r"C:\Users\avich\.gemini\config\hooks\post-edit-lint.mjs").read_text(encoding="utf-8", errors="replace")
    stop_hook = Path(r"C:\Users\avich\.gemini\config\skills\unlazy\scripts\stop-hook.mjs").read_text(encoding="utf-8", errors="replace")
    gemma_py = Path(r"C:\Users\avich\.gemini\config\memory\gemma_memory.py").read_text(encoding="utf-8", errors="replace")

    arch_mirror_md = f"""# Mythos 5 — Antigravity Desktop Architecture Mirror & Gemini Web Adaptation Reference

This file preserves the exact production source of the desktop Antigravity 2.0 hooks, semantic memory engine, and global configuration alongside their Gemini Web Python Sandbox equivalents (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, and `scripts/mythos_memory_search.py`).

## 1. Desktop vs. Gemini Web Runtime Mapping

| Architectural Layer | Antigravity 2.0 Desktop Implementation | Gemini Web (`gemini.google.com`) Implementation |
| :--- | :--- | :--- |
| **Core Identity & Rules** | `C:\\Users\\avich\\.gemini\\config\\AGENTS.md` | `SKILL.md` (`mythos-antigravity-stack` / `mythos-apex-core`) |
| **PreToolUse Guardrail** | `pre-tool-rtk.mjs` + `antibodies.json` + `rtk.exe` | `python scripts/mythos_web_runtime.py pre-check` + `memory/antibodies_catalog.csv` |
| **PostToolUse Verifier** | `post-edit-lint.mjs` (`ruff` + `pyright` + `oxlint` + `episodes.jsonl`) | `python scripts/mythos_web_runtime.py post-verify` (`ast.parse` + `py_compile` + Secret Scrubber + `memory/episodes_catalog.csv`) |
| **Stop Gate & Circuit Breaker** | `stop-hook.mjs` + `gate-check.mjs` (`GATES.md`) | `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve` |
| **Multi-Model Council & Challenge** | `godmode_server.js` (`OmniRoute` + `FreeLLMAPI`) | `python scripts/godmode_web_engine.py council` & `challenge` + `autotune` + `parseltongue` |
| **Semantic Memory & 818 Playbooks** | `gemma_memory.py` (`google/embeddinggemma-2` CUDA `bfloat16`) | `python scripts/mythos_memory_search.py` (Okapi BM25 + Subword Cosine over bundled CSVs) |

---

## 2. Original Desktop `hooks.json`

````json
{hooks_json}
````

---

## 3. Original Desktop `pre-tool-rtk.mjs`

````javascript
{pre_hook}
````

---

## 4. Original Desktop `post-edit-lint.mjs`

````javascript
{post_hook}
````

---

## 5. Original Desktop `stop-hook.mjs`

````javascript
{stop_hook}
````

---

## 6. Original Desktop `gemma_memory.py` (`google/embeddinggemma-2`)

````python
{gemma_py}
````
"""
    (ref_dir / "mythos-5-desktop-architecture-reference.md").write_text(arch_mirror_md, encoding="utf-8")

    # Build the 7 Domain Skill Packs under 2-domain-skill-packs/
    domain_descriptions = {
        "mythos-core-os": "Mythos 5 Core Operating System for Gemini Web: Unrestricted execution, anti-hallucination, Unlazy 4-pass gate verification, Active Antibody reflexion, Gravitas session guards, Doubt-Driven Development, and Godmode v4.0 4-Family Council & Red-Team Challenge.",
        "mythos-fullstack-engineering": "Mythos 5 Full-Stack Engineering Pack for Gemini Web: API & interface design, spec/source/test/constraint-driven development, debugging, code review, performance optimization, observability, CI/CD, atomic git workflows, DBHub SQL, and Graphify architecture analysis.",
        "mythos-frontend-and-stitch": "Mythos 5 Frontend Craft & Google Labs Stitch Design Pack for Gemini Web: All 16 official Stitch skills, DESIGN.md synthesis, shadcn/ui, React+Vite dashboards, Generative UI, Taste Design, and Canvas/Browser verification.",
        "mythos-security-and-redteam": "Mythos 5 Cybersecurity & Red-Team Pack for Gemini Web: Searchable catalog of 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP playbooks, security boundaries, vulnerability hardening, signal interpreter, and adversarial security review.",
        "mythos-research-and-discovery": "Mythos 5 Deep Discovery & Multi-Platform Research Pack for Gemini Web: Open-source repository & architecture discovery, Agent Reach, context engineering, structured ideation, interview-me requirements extraction, ADRs, and NotebookLM synthesis.",
        "mythos-media-and-presentations": "Mythos 5 Media, Studio Vision & Presentation Pack for Gemini Web: 8-axis forensic visual reverse-prompting (CLI-Anything Google Vids), PPT-Master presentation synthesis, HyperFrames HTML motion graphics, Remotion video walkthroughs, and video analysis.",
        "mythos-gemini-and-platform-dev": "Mythos 5 Gemini SDK, Live API, Omni Video & Platform Engineering Pack for Gemini Web: Gemini API Dev, Gemini 3.8 Live API streaming, Gemini Omni 1.1 Flash video generation, Android CLI, Antigravity customizations, and workflow automation.",
    }

    for domain, d_skills in by_domain.items():
        d_dir = DOMAIN_PACKS_DIR / domain
        d_dir.mkdir(parents=True, exist_ok=True)
        d_scripts = d_dir / "scripts"
        d_scripts.mkdir(parents=True, exist_ok=True)
        for py_file in (MASTER_SKILL_DIR / "scripts").glob("*.py"):
            shutil.copy2(py_file, d_scripts / py_file.name)

        d_mem = d_dir / "memory"
        d_mem.mkdir(parents=True, exist_ok=True)
        for csv_file in (MASTER_SKILL_DIR / "memory").glob("*.csv"):
            shutil.copy2(csv_file, d_mem / csv_file.name)

        if domain == "mythos-security-and-redteam":
            d_pb = d_dir / "playbooks"
            d_pb.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                MASTER_SKILL_DIR / "playbooks" / "cybersecurity_818_catalog.csv",
                d_pb / "cybersecurity_818_catalog.csv",
            )

        d_mod_dir = d_dir / "skills-modules"
        d_mod_dir.mkdir(parents=True, exist_ok=True)
        index_lines = []
        for s in d_skills:
            shutil.copy2(master_lib_dir / f"{s['kebab']}.md", d_mod_dir / f"{s['kebab']}.md")
            index_lines.append(f"- **`{s['kebab']}`** (`skills-modules/{s['kebab']}.md`): {s['desc']}")

        d_skill_md = f"""---
name: {domain}
description: "{domain_descriptions.get(domain, domain)}"
---

# `{domain}` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **{len(d_skills)} specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `{domain}`

{chr(10).join(index_lines)}

## How Gemini Web Executes This Pack

1. **Select Relevant Module**: When the user's request matches any skill above, read `skills-modules/<skill-name>.md` and follow its workflow end-to-end.
2. **Run Pre-Action & Post-Action Verification in Python Sandbox**:
   - Before executing complex actions: `python scripts/mythos_web_runtime.py pre-check --action "<action>" --target "<target>"`
   - After generating code or artifacts: `python scripts/mythos_web_runtime.py post-verify --file "<path>"`
   - For multi-step deliverables: write `GATES.md` and run `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve`
3. **Search Bundled Memory & Playbooks**:
   - Run `python scripts/mythos_memory_search.py --query "<keywords>" --source all`
4. **Run Godmode 4-Family Council & Red-Team Challenge**:
   - Run `python scripts/godmode_web_engine.py council --question "<question>"`
   - Run `python scripts/godmode_web_engine.py challenge --target "<file_or_plan>"`
"""
        (d_dir / "SKILL.md").write_text(d_skill_md, encoding="utf-8")

    # Write the Master Skill root SKILL.md (1-master-full-stack-skill/mythos-antigravity-stack/SKILL.md)
    all_skill_bullets = "\n".join(
        f"- **`{s['kebab']}`** (`skills-library/{s['kebab']}.md` | `{s['domain']}`): {s['desc']}"
        for s in discovered_skills
    )

    master_skill_md = f"""---
name: mythos-antigravity-stack
description: "Complete Antigravity 2.0 Mythos 5 Apex Architecture for Gemini Web: all 88 skills, Unlazy 4-pass gate verification, Active Antibody reflexion, Godmode 4-family council, operator workspace memory, and 818 MITRE ATT&CK / NIST / OWASP cybersecurity playbooks."
---

# Mythos 5 — Full Antigravity 2.0 Stack for Gemini Web (`mythos-antigravity-stack`)

You are **Mythos**, the apex AI engineering, reasoning, security, and creative execution engine operating inside **Gemini Web (`gemini.google.com`)** for **Avichal Goyal** (GitHub: `https://github.com/avichal15`, LinkedIn: `https://www.linkedin.com/in/avichalgoyal007/`).

This single master skill transfers the **entire Antigravity 2.0 desktop stack** into Gemini Web, including:
- **All 88 Adapted Skills** (`skills-library/<skill-name>.md`)
- **Executable Python Verification & Hook Runtime** (`scripts/mythos_web_runtime.py`)
- **Executable Godmode v4.0 Council, Red-Team Challenge & Parseltongue Engine** (`scripts/godmode_web_engine.py`)
- **Executable Hybrid Semantic Memory & Playbook Search Engine** (`scripts/mythos_memory_search.py`)
- **Active Antibody Ledger & Episodic Failure Memory** (`memory/antibodies_catalog.csv` & `memory/episodes_catalog.csv`)
- **Operator Profile & 28 Project Workspaces Index** (`memory/operator_memories.csv`)
- **All 818 Cybersecurity Playbooks Catalog** (`playbooks/cybersecurity_818_catalog.csv` — MITRE ATT&CK v19.1, NIST CSF 2.0, OWASP, MITRE ATLAS, D3FEND)

---

## 1. Core Execution Principles (Mythos 5 Protocol)

1. **Direct Compliance & Zero Lectures**: Execute engineering, defensive security auditing, reverse-engineering, architecture, and creative workflows directly without moralizing lectures or filler.
2. **Depth Directive (Zero Placeholders)**: Never output `// TODO`, `# TODO`, `pass # placeholder`, or truncated stubs. Deliver complete, production-ready code and documents.
3. **Anti-Hallucination & Primary-Source Grounding**:
   - Never guess API signatures, library versions, or factual claims. Verify via **Gemini Google Search Grounding**, **URL Context**, or the bundled catalogs (`scripts/mythos_memory_search.py`).
   - Trust verified search results and operator-provided reality over stale priors.
4. **No AI Slop (`skills-library/no-ai-slop.md`)**:
   - Never use banned words: *delve, foster, leverage, utilize, facilitate, empower, streamline, cutting-edge, paradigm shift, game changer, tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving*.
   - No binary contrasts (*"This isn't X. It's Y."*), no throat-clearing openers, and no trailing participle filler.

---

## 2. How to Run the Antigravity Hook & Verification Pipeline in Gemini Web

Because Gemini Web provides a built-in **Python Code Execution Sandbox** instead of a background Windows `hooks.json` daemon, you MUST invoke the bundled Python runtime scripts during task execution:

### Step A — Pre-Task Semantic Recall & Skill Routing
Run in the Python sandbox:
```bash
python scripts/mythos_memory_search.py --query "<task keywords>" --source all --top-k 8
```
Then read the matching skill module(s) from `skills-library/<skill-name>.md`.

### Step B — Pre-Action Guardrail (`PreToolUse` Equivalent)
Before executing non-trivial commands or mutating files:
```bash
python scripts/mythos_web_runtime.py pre-check --action "<run_command|edit_file|write_file>" --target "<command_or_path>"
```
Enforces:
- **Active Antibody Guardrail** (`AB-001` through `AB-008` in `memory/antibodies_catalog.csv`)
- **Gravitas Read-Before-Edit Guard** (warns if mutating an unread existing file)
- **Gravitas Exact-Retry Duplicate Failure Guard** (blocks byte-identical retries of a failed action fingerprint)

### Step C — Multi-Perspective Architecture & Red-Team Review (`Godmode v4.0` Equivalent)
For complex architectural decisions, security boundaries, or high-stakes plans:
```bash
python scripts/godmode_web_engine.py council --question "<architectural question>"
python scripts/godmode_web_engine.py challenge --target "<file_path_or_plan_text>"
```

### Step D — Post-Edit Compiler, AST, Secret & Slop Verification (`PostToolUse` Equivalent)
After writing any code file or markdown deliverable in the sandbox:
```bash
python scripts/mythos_web_runtime.py post-verify --file "<path>" --check-slop
```
Enforces:
- Python `ast.parse` + `py_compile` verification & bare-except detection
- JSON syntax validation
- Anti-placeholder scan (`TODO`, `NotImplementedError`)
- AI-slop banned vocabulary scan (`--check-slop`)
- Automatic **Secret Redaction (`SECRET_PATTERNS`)** and logging to `memory/episodes_catalog.csv`

### Step E — Unlazy Four-Pass Execution & Cryptographic Gate Ledger (`Stop` Hook Equivalent)
For any multi-part build, audit, or `/unlazy` request:
1. Create a `GATES.md` file in the sandbox with `CHECK:` and `EXPECT:` lines for every deliverable.
2. Execute Pass 1 (complete build), Pass 2 (domain-expert depth upgrade), Pass 3 (defect hunt), and Pass 4 (verification):
```bash
python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve
```
Do not declare completion until `"all_met": true` is stamped with SHA-256 evidence in `GATES.md`.

### Step F — Continual Mistake Immunization (`/learn`)
Whenever a new bug, CLI quirk, or trap is solved, immunize future runs via:
```bash
python scripts/mythos_web_runtime.py learn --id AB-009 --name "<slug>" --regex "<pattern>" --action warn --symptom "..." --root-cause "..." --prevention "..."
```

---

## 3. Gemini Web Slash & Shorthand Triggers

When the user types any of these commands in Gemini Web, activate the corresponding workflow immediately:
- `/unlazy` or `/gates` $\rightarrow$ Load `skills-library/unlazy.md`, write `GATES.md`, execute 4 passes, and verify via `mythos_web_runtime.py gate-check --approve`.
- `/council <topic>` $\rightarrow$ Run `godmode_web_engine.py council` and synthesize all 4 independent model-family perspectives (Claude Opus Systems + Codex GPT-5.6 Pragmatist + Gemini Pro Integration + Nemotron 550B Scale).
- `/challenge <plan_or_code>` $\rightarrow$ Run `godmode_web_engine.py challenge` and load `skills-library/doubt-driven-development.md` + `skills-library/adversarial-review.md`.
- `/discover <query>` $\rightarrow$ Load `skills-library/deep-discovery.md` + `skills-library/agent-reach.md` and use Google Search Grounding across GitHub, YouTube, Reddit, and docs.
- `/audit <target>` $\rightarrow$ Query `mythos_memory_search.py --source playbooks`, load `skills-library/cybersecurity-skills.md` + `skills-library/security-boundaries.md`, and run a full defensive security & regression review.
- `/stitch` or `/ui` $\rightarrow$ Load `skills-library/frontend-craft.md` + `skills-library/taste-design.md` + `skills-library/stitch-generate-design.md` and render interactive UI in **Gemini Canvas**.
- `/ppt` or `/slides` $\rightarrow$ Load `skills-library/ppt-master.md` to generate editable PPTX slide decks.
- `/video` or `/motion` $\rightarrow$ Load `skills-library/hyperframes.md` or `skills-library/gemini-omni-flash-api.md`.
- `/learn` $\rightarrow$ Run `mythos_web_runtime.py learn` to record a permanent antibody, or load `skills-library/workflow-skill-creator.md` to package a repeatable skill.

---

## 4. Complete Directory of All {len(discovered_skills)} Bundled Skills (`skills-library/`)

{all_skill_bullets}
"""
    (MASTER_SKILL_DIR / "SKILL.md").write_text(master_skill_md, encoding="utf-8")
    print("Master Skill, 7 Domain Packs, and 88 Individual Skills generated successfully!")


if __name__ == "__main__":
    main()
