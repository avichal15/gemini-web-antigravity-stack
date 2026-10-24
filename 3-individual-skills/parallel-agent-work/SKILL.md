---
name: parallel-agent-work
description: "Coordinate explicitly authorized subagents on independent engineering leaves with clear ownership and parent verification. Do not spawn agents for a small task or when delegation is not authorized."
---

# Parallel agent work

More agents help only when their work can be bounded and integrated. The driver remains responsible for the user's whole request, the live checkout and the final claim.

## Before dispatch

Inventory every independently required outcome and the shared files/interfaces. Split into coherent leaves with observable acceptance, dependencies and **one writer per file**. Assign shared integration files, credentials, remote services and physical devices to the driver unless a different owner is explicitly authorized. Use isolated worktrees when the host supports them and separate checkouts improve safety; ownership notes alone do not sandbox a filesystem.

Give each child the exact target path, relevant current instructions, brief/contract, allowed files and actions, known failures, expected output and stop condition. Do not assume a child inherited the main conversation. A reviewer should receive a stable artifact and enough context to challenge it, without the author's preferred conclusion.

## Integrate

Track each return as implemented, verified, blocked or incomplete. Inspect the changed diff and the actual test evidence; rerun the child's decisive checks in the target checkout. Run interface and end-to-end checks once the leaves join. A leaf's “done” message, test output from another branch or rate-limited partial return is not integration success.

When a child stops or a lease changes owner, record the exact file set and handoff before anyone else edits it. Release ownership after parent review. Keep a single device driver to avoid conflicting taps/settings and preserve user choices after QA. Close or account for active agents, servers and temporary files at handoff.

If delegation is unavailable, disallowed or would add coordination cost, work solo. The same outcome inventory and evidence discipline still apply.

---

## Gemini Web Execution Adaptation (`parallel-agent-work`)

When executing `parallel-agent-work` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

