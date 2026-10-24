---
name: ag-handoff
description: "Records or resumes a long-running Antigravity task with project-local progress, verification evidence, active worktrees/processes, and concrete recovery steps. Use for checkpoints, handovers, or context recovery."
---

# Task checkpoint and handoff

Use the project's existing task-note convention. If none exists, keep one concise `work/handoff.md` in the active project. Reuse that task's note rather than creating a growing collection of contradictory summaries. Do not store task notes in the user's home root or modify a separate memory system unless explicitly requested.

Record the information needed to continue correctly:

- The intended outcome, accepted decisions, and remaining acceptance criteria.
- The exact checkout/worktree and branch when applicable, plus relevant uncommitted changes and ownership.
- Completed changes and actual verification results, with enough command/path information to reproduce them.
- Active native subagents or local dev servers, including their returned IDs or verified paths. Distinguish running work from completed work.
- Any verified recovery copy or reversible step, and which files it covers. Do not label an untested or partial backup a full restore point.
- The next bounded action and any blocker that requires a user decision.

Never copy credentials, tokens, private request bodies, or whole environment files into the note. Provider, endpoint, and bridge details should appear only as a scope constraint when relevant; do not inspect or test them to populate a handoff.

On resume, read the existing note and check the live status of the files/processes that matter to the next action. Reconcile drift before editing. Preserve completed work and do not rerun successful checks unless code, configuration, dependencies, or the relevant environment changed.

---

## Gemini Web Execution Adaptation (`ag-handoff`)

When executing `ag-handoff` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

