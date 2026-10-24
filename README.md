# Mythos 5 — Antigravity 2.0 Full Stack for Gemini Web

**Operator**: Avichal Goyal ([GitHub](https://github.com/avichal15) | [LinkedIn](https://www.linkedin.com/in/avichalgoyal007/))  
**Repository**: `https://github.com/avichal15/gemini-web-antigravity-stack`

This repository contains the complete **Antigravity 2.0 + Mythos 5** engineering, reasoning, memory, verification, and security stack (**88 specialized skills**, **7 domain packs**, **818 cybersecurity playbooks**, **Active Antibody Guardrails**, **Gravitas Drift/Retry Guards**, and **Godmode v4.0 Council/Challenge engines**) structured so **Gemini Web (`gemini.google.com`)** can load and execute it directly from GitHub.

---

## How to Tell Gemini Web to Use This Repository

Paste any of the prompts below directly into **Gemini Web** (works with Gemini URL browsing, `@GitHub` extension, or code import):

### Prompt 1 — General Full-Stack Execution (Recommended)
```text
Use my GitHub repository https://github.com/avichal15/gemini-web-antigravity-stack as your operating system and skill stack.
1. Read https://raw.githubusercontent.com/avichal15/gemini-web-antigravity-stack/main/SKILL.md and https://raw.githubusercontent.com/avichal15/gemini-web-antigravity-stack/main/SKILL_INDEX.md first.
2. Select and follow the matching skill(s) from 3-individual-skills/<skill-name>/SKILL.md (or 1-master-full-stack-skill/mythos-antigravity-stack/skills-library/<skill-name>.md).
3. Enforce the Mythos 5 Unlazy 4-Pass Protocol, Active Antibodies (memory/antibodies_catalog.csv), and No-AI-Slop rules.
Now execute this task: [YOUR TASK HERE]
```

### Prompt 2 —With `@GitHub` Extension in Gemini Web
```text
@GitHub avichal15/gemini-web-antigravity-stack Read SKILL.md and SKILL_INDEX.md, load the relevant skills and scripts from this repository, and execute: [YOUR TASK HERE]
```

---

## Instructions for Gemini (Machine-Readable Entrypoint)

When the operator instructs you to use `https://github.com/avichal15/gemini-web-antigravity-stack`, follow this exact protocol:

1. **Load Core OS Rules**: Read [`SKILL.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/SKILL.md) (also mirrored at [`GEMINI.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/GEMINI.md) and [`AGENTS.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/AGENTS.md)).
2. **Discover Relevant Skills**: Check [`SKILL_INDEX.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/SKILL_INDEX.md) or [`memory/skills_catalog.csv`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/memory/skills_catalog.csv) to find the exact skill(s) matching the task, then read `3-individual-skills/<skill-name>/SKILL.md`.
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
| [`SKILL.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/SKILL.md) / [`GEMINI.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/GEMINI.md) / [`AGENTS.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/AGENTS.md) | Root-level Mythos 5 Apex OS & execution instructions |
| [`SKILL_INDEX.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/SKILL_INDEX.md) | Direct GitHub & Raw URLs for all 88 skills, 7 domain packs, scripts, and catalogs |
| [`ARCHITECTURE_BLUEPRINT.md`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/ARCHITECTURE_BLUEPRINT.md) | Complete subsystem mapping between Antigravity Desktop and Gemini Web |
| [`scripts/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/scripts) | Executable Python sandbox engines (`mythos_web_runtime.py`, `mythos_memory_search.py`, `godmode_web_engine.py`) |
| [`memory/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/memory) | Active antibodies (`AB-001`–`AB-008`), failure episodes, operator memories (28 workspaces), and 88-skill catalog |
| [`playbooks/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/playbooks) | 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP security playbooks catalog (`cybersecurity_818_catalog.csv`) |
| [`1-master-full-stack-skill/mythos-antigravity-stack/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/1-master-full-stack-skill/mythos-antigravity-stack) | Unified all-in-one master skill bundle with all 88 skills compiled in `skills-library/` |
| [`2-domain-skill-packs/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/2-domain-skill-packs) | 7 modular domain skill packs (`mythos-core-os`, `mythos-fullstack-engineering`, `mythos-frontend-and-stitch`, `mythos-security-and-redteam`, `mythos-research-and-discovery`, `mythos-media-and-presentations`, `mythos-gemini-and-platform-dev`) |
| [`3-individual-skills/`](https://github.com/avichal15/gemini-web-antigravity-stack/blob/main/3-individual-skills) | All 88 individual skills with their dedicated scripts, references, and templates |
