# How to Upload and Use the Antigravity Mythos 5 Stack in Gemini Web (`gemini.google.com`)

> **Desktop Isolation Guarantee**: Your live desktop Antigravity environment (`C:\Users\avich\.gemini\config\`) was accessed strictly read-only. Zero desktop hooks, skills, memories, or configs were altered. Everything inside `c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack\` is a standalone, adapted copy built specifically for **Gemini Web (`gemini.google.com`)**.

---

## 1. Why the Stack Was Adapted for Gemini Web's "Upload a Skill" Requirements

Gemini Web's **Upload a skill** dialog enforces three strict rules:
1. **`kebab-case` `name:` in `SKILL.md`**: Every skill's YAML frontmatter `name:` must strictly match `^[a-z0-9]+(-[a-z0-9]+)*$` (no `::` namespaces like `stitch::code-to-design` and no underscores like `generative_ui`). All 88 skills have been normalized to strict `kebab-case`.
2. **A `SKILL.md` file in the main (root) folder**: Every uploadable skill folder contains a single root `SKILL.md` with valid YAML frontmatter (`name` and `description`).
3. **Allowed File Extensions (`PDF, CSV, PY, TXT, and MD` + images)**:
   - Every `.mjs`, `.js`, `.ts`, `.tsx`, `.sh`, `.json`, `.yaml`, `.html`, and `.css` file across all skills has been either ported into a native executable **Python (`.py`)** script or wrapped as a clean **Markdown (`.md`)** / **CSV (`.csv`)** module.
   - `ppt-master`'s 12,193 `.svg` icons and 186 `.wav` audio files were indexed into a compact `templates/bundled_icons_and_audio_catalog.csv` while preserving all 310 `.py` scripts and 230 `.md` reference files so browser folder upload completes in ~1 second without file-type rejection.

---

## 2. Three Ways to Upload Into Gemini Web (Pick What Fits Best)

Open [gemini.google.com](https://gemini.google.com) $\rightarrow$ **Settings / Customize** $\rightarrow$ **Skills** $\rightarrow$ **Upload a skill**:

### Option A (Recommended — 1-Click Master Stack Upload)
Drag and drop **this single folder** into Gemini Web's **"Upload a skill"** dialog:
```text
c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack\1-master-full-stack-skill\mythos-antigravity-stack
```
**What this single upload gives you inside Gemini Web**:
- **Root `SKILL.md` (`name: mythos-antigravity-stack`)**: Full Mythos 5 Apex OS protocol, Anti-Hallucination rules, No-AI-Slop rules, and slash-command triggers (`/unlazy`, `/council`, `/challenge`, `/discover`, `/audit`, `/stitch`, `/ppt`, `/video`, `/learn`).
- **All 88 Adapted Skills (`skills-library/*.md`)**: Every Antigravity skill (`unlazy`, `godmode`, `gemma-reflexion`, `cybersecurity-skills`, `deep-discovery`, `agent-reach`, `cli-anything-google-vids`, `ppt-master`, `hyperframes`, all 16 Google Labs `stitch-*` skills, all 25 engineering plugin skills, Gemini API/Live/Omni skills, etc.) accessible on-demand.
- **Executable Python Verification & Hook Runtime (`scripts/mythos_web_runtime.py`)**: Runs `pre-check` (Active Antibody Guardrail + Gravitas Read-Before-Edit & Exact-Retry Fingerprint Guard), `post-verify` (Python `ast.parse`/`py_compile`, JSON validator, Anti-Placeholder check, No-AI-Slop check, Secret Redactor), `gate-check` (cryptographic `GATES.md` verifier + 6-block circuit breaker), and `learn` inside Gemini Web's Python sandbox.
- **Executable Godmode v4.0 Engine (`scripts/godmode_web_engine.py`)**: Runs `autotune`, `parseltongue` (all 22+ lexical/cipher transforms), `council` (4-Family Multi-Perspective Council: Claude Opus Systems + Codex GPT-5.6 Pragmatist + Gemini Pro Integration + Nemotron 550B Scale), and `challenge` (Red-Team Adversarial Challenge).
- **Executable Semantic Memory & Playbook Search Engine (`scripts/mythos_memory_search.py`)**: Hybrid Okapi BM25 + Subword Cosine search over `memory/antibodies_catalog.csv` (8 antibodies), `memory/episodes_catalog.csv` (failure episodes), `memory/operator_memories.csv` (operator profile + 28 owned/client workspaces), `memory/skills_catalog.csv` (88 skills), and `playbooks/cybersecurity_818_catalog.csv` (all 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP playbooks).

---

### Option B (Modular — 7 Curated Domain Skill Packs)
If you prefer having 7 distinct domain skills in your Gemini Web Skills list, drag each of the 7 folders inside:
```text
c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack\2-domain-skill-packs\
```
1. `mythos-core-os` — Core Mythos 5 OS, `unlazy`, `godmode`, `gemma-reflexion`, `doubt-driven-development`, `no-ai-slop`, `evidence-and-claims`
2. `mythos-fullstack-engineering` — 23 full-stack engineering skills (`api-and-interface-design`, `test-driven-development`, `debugging-and-error-recovery`, `performance-optimization`, `dbhub`, `graphify`, `atomic-git-contributions`, etc.)
3. `mythos-frontend-and-stitch` — 20 UI/UX & Google Labs Stitch skills (`frontend-craft`, `taste-design`, `shadcn-ui`, `react-vite-dashboard`, `stitch-loop`, `stitch-react-components`, `generative-ui`, etc.)
4. `mythos-security-and-redteam` — 6 security skills + all **818 MITRE ATT&CK / NIST / OWASP playbooks** (`cybersecurity-skills`, `security-boundaries`, `security-and-hardening`, `signal-interpreter`, `adversarial-review`, `credentials`)
5. `mythos-research-and-discovery` — 7 research & discovery skills (`deep-discovery`, `agent-reach`, `context-engineering`, `idea-refine`, `interview-me`, `documentation-and-adrs`, `notebooklm`)
6. `mythos-media-and-presentations` — 5 studio media & presentation skills (`cli-anything-google-vids`, `ppt-master`, `hyperframes`, `remotion`, `watch`)
7. `mythos-gemini-and-platform-dev` — 15 Gemini SDK & platform skills (`gemini-api-dev`, `gemini-live-api-dev`, `gemini-omni-flash-api`, `android-cli`, `workflow-skill-creator`, etc.)

---

### Option C (Granular — Upload Any of the 88 Individual Skills)
If you want to upload specific skills individually, drag any folder from:
```text
c:\Users\avich\Downloads\mythos\gemini-web-antigravity-stack\3-individual-skills\<skill-name>\
```
Every folder in `3-individual-skills/` has its own root `SKILL.md`, strict `kebab-case` `name:`, Gemini Web runtime adaptation instructions, and 100% compliant file formats.

---

## 3. How to Trigger Workflows Inside Gemini Web Chat

Once `mythos-antigravity-stack` (or the domain packs) is enabled in Gemini Web:

| What You Want to Do | What to Type in Gemini Web | What Gemini Web Executes Under the Hood |
| :--- | :--- | :--- |
| **Zero-laziness multi-part build with gates** | `/unlazy <task>` or `"Use unlazy with GATES.md to build..."` | Writes `GATES.md`, runs 4 passes, executes `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve` in Python sandbox |
| **4-Model Council architectural deliberation** | `/council <question>` | Runs `python scripts/godmode_web_engine.py council --question "..."` and synthesizes Opus + Codex + Gemini Pro + Nemotron perspectives |
| **Red-team challenge a plan or code diff** | `/challenge <plan or code>` | Runs `python scripts/godmode_web_engine.py challenge` + `doubt-driven-development` + `adversarial-review` |
| **Security audit / pentest playbook lookup** | `/audit <target>` | Searches all 818 playbooks via `python scripts/mythos_memory_search.py --source playbooks` and executes full OWASP / MITRE ATT&CK review |
| **Multi-channel open-source repo discovery** | `/discover <topic>` | Loads `deep-discovery` + `agent-reach` and searches GitHub, YouTube creator descriptions, and docs via Google Search Grounding |
| **Design UI / Stitch / React components** | `/stitch <ui brief>` or `/ui <brief>` | Loads `taste-design` + `frontend-craft` + `stitch-generate-design` and renders live interactive UI in **Gemini Canvas** |
| **Recall operator workspace or past bugs** | `"Search Mythos memory for <project/bug>"` | Runs `python scripts/mythos_memory_search.py --query "..." --source all` across your 28 workspaces, antibodies, and episodes |
| **Immunize a newly discovered mistake** | `/learn <mistake details>` | Runs `python scripts/mythos_web_runtime.py learn ...` to add a permanent antibody rule |
