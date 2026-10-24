# Skill Module: `atomic-git-contributions`

- **Domain Pack**: `mythos-fullstack-engineering`
- **Description**: Splits uncommitted changes or monolithic commit ranges into verified, dependency-ordered, fine-grained atomic Git commits with unified GitHub contributor attribution (Avichal15 <avichalgoyal15@gmail.com>), realistic chronological date distribution, pre-commit CI/test verification, and a mandatory cryptographic tree equality gate (`new_head^{tree} == target^{tree}`). Use whenever the user asks for atomic Git commits, professional commit splitting,

# Atomic Git Contributions & Verified History Splitter

## Overview

Turns large working-tree diffs or bundled/monolithic commit ranges into a clean, reviewable chain of fine-grained atomic commits while maximizing legitimate GitHub contribution visibility and enforcing 100% cryptographic tree equivalence.

Key guarantees:
1. **Pre-Commit Verification First**: Runs the repository's typecheck, lint, test suites, and secret checks before committing so CI never fails on a clean checkout.
2. **Fine-Grained Dependency Ordering**: Splits changes by architectural layer (`db/migrations` $\rightarrow$ `backend/functions` $\rightarrow$ `lib/core` $\rightarrow$ `features` $\rightarrow$ `ui/routes` $\rightarrow$ `native/modules` $\rightarrow$ `platform/plugins` $\rightarrow$ `config` $\rightarrow$ `tests` $\rightarrow$ `scripts` $\rightarrow$ `website/docs`).
3. **Unified GitHub Attribution & Date Windowing**: Ensures every commit uses `Avichal15 <avichalgoyal15@gmail.com>` for both `GIT_AUTHOR_*` and `GIT_COMMITTER_*`, and spaces commit dates evenly across the target active window (up to the current local timestamp in `+0530`, never in the future) so every commit counts toward the GitHub contribution graph.
4. **Lock-Free `git fast-import` + Cryptographic Tree Gate**: Builds 100–300+ commits in `< 2 seconds` without touching the working tree or triggering `.git/index.lock`, and verifies `git rev-parse new_head^{tree} == git rev-parse target^{tree}` before updating the branch ref.

## Dependencies

- **`git-workflow-and-versioning`** (`C:\Users\avich\.gemini\config\plugins\agent-skills\skills\git-workflow-and-versioning\SKILL.md`): Defines Conventional Commit message conventions (`feat`, `fix`, `security`, `refactor`, `test`, `docs`, `chore`), pre-commit hygiene checks, and scope separation rules.
- **`evidence-and-claims`** (`C:\Users\avich\.gemini\config\skills\evidence-and-claims\SKILL.md`): Enforces verification evidence (typecheck, lint, test execution, and tree-hash verification) before claiming completion.

## Quick Start

```powershell
# 1. Audit changed files, contributor identities, and date distribution
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" audit `
  --repo "c:\phone caller" `
  --base 9ce9c59 `
  --target HEAD `
  --output "scratch/audit.json"

# 2. Generate a candidate atomic commit plan (or craft custom semantic batches in JSON)
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" auto-plan `
  --repo "c:\phone caller" `
  --base 9ce9c59 `
  --target HEAD `
  --max-files-per-commit 10 `
  --output "scratch/plan.json"

# 3. Execute atomic commits via git fast-import and verify bit-for-bit tree match
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" execute `
  --repo "c:\phone caller" `
  --plan "scratch/plan.json" `
  --author-name "Avichal15" `
  --author-email "avichalgoyal15@gmail.com" `
  --start-date "2026-10-01T09:15:00" `
  --end-date "2026-10-23T18:35:00" `
  --timezone "+0530" `
  --replay-early `
  --update-branch main `
  --output "scratch/execution_ledger.json"
```

## Utility Scripts

The CLI utility at `scripts/atomic_commits.py` provides three subcommands. All subcommands write structured JSON to `--output` (never dumping large payloads to stdout).

### 1. `audit`

Inspects all changed paths between `--base` and `--target` using `git diff --no-renames --name-status`, lists current contributor identities (`git shortlog -sne`), and builds a daily commit histogram.

```powershell
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" audit `
  --repo "<repo_path>" `
  --base "<base_sha>" `
  --target "HEAD" `
  --output "<scratch_dir>/audit.json"
```

### 2. `auto-plan`

Partitions all changed files between `--base` and `--target` into dependency-ordered atomic commit batches capped at `--max-files-per-commit` (while keeping vendored third-party trees intact). Review and refine the `task`, `why`, and `message` fields in the generated JSON so every commit message explains the architectural *why*.

```powershell
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" auto-plan `
  --repo "<repo_path>" `
  --base "<base_sha>" `
  --target "HEAD" `
  --max-files-per-commit 8 `
  --output "<scratch_dir>/plan.json"
```

### 3. `execute`

Streams the atomic commit plan into `git fast-import` using raw LF byte buffers, optionally replaying earlier commits (`--replay-early`) with unified author/committer headers and chronological timestamps across `--start-date` .. `--end-date`. Verifies `new_head^{tree} == target^{tree}` before updating `--update-branch`.

```powershell
uv run "C:\Users\avich\.gemini\config\skills\atomic-git-contributions\scripts\atomic_commits.py" execute `
  --repo "<repo_path>" `
  --plan "<scratch_dir>/plan.json" `
  --author-name "Avichal15" `
  --author-email "avichalgoyal15@gmail.com" `
  --start-date "2026-10-01T09:15:00" `
  --end-date "2026-10-23T18:35:00" `
  --timezone "+0530" `
  --replay-early `
  --update-branch main `
  --output "<scratch_dir>/execution_ledger.json"
```

## Workflow

Follow this 5-step protocol whenever executing an atomic commit or GitHub contribution run:

### Step 1: Pre-Flight Verification & Uncommitted Work Snapshot
1. Remove any stale `.git/index.lock` or `.git/fast_import_crash_*` if no `git.exe` process is running.
2. Run the project's verification suite (`npm run typecheck`, `npm run lint`, `npm test`, or equivalent CI checks) and fix any clean-checkout defects (e.g., missing parent directories before `mkdtempSync`, unignored temp files) **before** building the atomic history.
3. If changes are currently uncommitted in the working tree, create a temporary snapshot commit on a detached or current ref (`git add -A && git commit -m "wip: snapshot"`) so `HEAD` holds the exact verified target tree (`HEAD^{tree}`), and set `--base` to `HEAD~1`.

### Step 2: Audit Diff & Existing Contribution Graph
1. Run `atomic_commits.py audit` between `--base` (the last clean atomic commit or root) and `--target` (`HEAD`).
2. Check `contributors` in `audit.json` to see if multiple identities caused GitHub to show `Contributors: 2` or omitted commits from the user's profile graph.
3. Check `date_histogram` in `audit.json` to see if commits were dated in an earlier month or bundled into giant multi-hundred-file commits.

### Step 3: Design Cohesive Atomic Commit Batches
1. Generate a baseline plan via `atomic_commits.py auto-plan` or write custom domain-specific batches in JSON following this strict dependency order:
   - **Phase 1**: Database schema & SQL migrations (1 migration per commit)
   - **Phase 2**: Backend config & Edge Functions / API routes (shared helpers first, then endpoints)
   - **Phase 3**: Core client libraries, environment validation, and cryptographic/auth adapters
   - **Phase 4**: Domain features (models/stores/hooks first, then UI components)
   - **Phase 5**: Application routes / screens
   - **Phase 6**: Native modules, vendored libraries, and platform configurations (`android/`, `ios/`, `plugins/`)
   - **Phase 7**: Project configuration, build profiles, and package manifests
   - **Phase 8**: Automated unit, integration, backend, and security test suites
   - **Phase 9**: Compliance, release, and automation scripts (`scripts/`)
   - **Phase 10**: Marketing/legal website portals, release documentation, and handover logs
2. Ensure every batch has a specific Conventional Commit message (`feat(scope): ...`, `fix(scope): ...`, `security(scope): ...`, `test(scope): ...`, `docs(scope): ...`, `chore(scope): ...`) and a clear 1-sentence `why`.

### Step 4: Execute via `git fast-import` & Verify Cryptographic Tree
1. Run `atomic_commits.py execute` with `--author-name "Avichal15"` and `--author-email "avichalgoyal15@gmail.com"`.
2. Confirm in `execution_ledger.json`:
   - `"tree_match": true` (`expected_tree == actual_tree`)
   - `"contributors"` has a single entry (`Avichal15 <avichalgoyal15@gmail.com>`)
   - `"date_histogram"` distributes commits across the desired dates without any future timestamps.
3. Push to the remote branch (`git push origin main`, or `git push --force origin main` when splitting/rewriting existing commits on a personal branch with user authorization).

### Step 5: Present Structured Atomic Commit Breakdown
Always provide a structured summary or ledger artifact containing for each commit:
- **Task**
- **Why**
- **Files affected**
- **Implementation steps**
- **Commit message**

## Rate Limiting

This skill operates exclusively on local Git object databases (`git diff`, `git ls-tree`, `git fast-import`, `git rev-parse`) and standard `git push` over HTTPS/SSH; no external REST API polling is required.

## Common Mistakes

1. **Windows Python `text=True` CRLF Injection in Git Plumbing**:
   - *Symptom*: `git update-index --index-info` silently prints `Ignoring path <file>` and produces an unchanged tree SHA on Windows.
   - *Root Cause*: Python `subprocess.run(..., text=True)` converts `\n` to `\r\n` on Windows, appending a literal `\r` to the file path in stdin.
   - *Prevention*: Always pass `input=payload.encode("utf-8")` (raw LF bytes, never `text=True`) to `git update-index` and `git fast-import`, as implemented in `scripts/atomic_commits.py`.
2. **Missing Renamed Source Paths Without `--no-renames`**:
   - *Symptom*: `git diff-tree` reports leftover old files (`A old/path/File.kt`) when reconstructing trees from `git diff --name-only`.
   - *Root Cause*: Default rename detection emits only the destination path for renamed files, leaving the old path in the base tree.
   - *Prevention*: Always pass `--no-renames` to `git diff --name-only` / `--name-status` so both the deleted old path (`D`) and added new path (`M`) are included in the atomic batch.
3. **Invalid Date Format in `git fast-import`**:
   - *Symptom*: `fatal: invalid raw date "2026-10-01T09:15:00+05:30" in ident`.
   - *Root Cause*: `git fast-import` expects raw Git epoch format `<unix_seconds> <±HHMM>` by default, not ISO-8601 strings.
   - *Prevention*: Format `fast-import` author/committer dates as `f"{int(dt.timestamp())} +0530"`.

---

## Gemini Web Execution Adaptation (`atomic-git-contributions`)

When executing `atomic-git-contributions` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

