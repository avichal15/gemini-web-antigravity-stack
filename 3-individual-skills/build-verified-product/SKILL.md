---
name: build-verified-product
description: "Build a new application, website, or substantial end-to-end feature from the brief through implementation and verified handoff. Do not use for a tiny edit or read-only explanation."
---

# Build a verified product

Use the user's actual product goal as the contract. A request to build does not authorize a different architecture, a remote deployment, a commit, a paid integration or a physical-device change.

## Establish the current truth

1. Identify the target checkout and inspect its status, applicable instructions, entrypoints, dependency versions, tests and working services. Read relevant files before editing. Preserve unrelated user work.
2. Identify the product's users, primary jobs, required flows, non-goals, platform targets, data/privacy obligations and release channel. If a consequential choice is missing, ask once while continuing independent work. Use [the brief form](../../templates/PROJECT_BRIEF.md) when the request is broad.
3. Rank authorities: current user direction, current project instructions/decisions, current source and tests, dated handoff, older specifications and examples. Resolve a material conflict explicitly and record what was superseded. A planned module in an architecture diagram is not an implemented module.
4. Probe the hardest technical assumption early. Use version-matched official documentation for unfamiliar APIs and an executable or physical proof where the outcome depends on a provider, browser, OS or hardware. State the exact uncertainty instead of inventing an integration.

## Build in complete slices

- Choose one coherent product architecture and define interfaces at platform, service and data boundaries. Keep a native adapter or backend service behind a contract rather than coupling every screen to it.
- Split work into small vertical behaviors a user can complete. For each slice, implement the real state/service path, loading/empty/error/unavailable states, and a recovery action. Fake people, fake success, nonfunctional buttons and mock results presented as live are defects.
- Run the narrowest meaningful check after each slice, then integrate. Expand checks when a changed boundary or failed result justifies it. Do not mandate a commit; commit, push and publish only when the user's instructions authorize them.
- On a failure, read the complete error and identify whether source, test oracle, dependency, tool, provider or task context caused it. Use a small harmless probe when provider health is uncertain; do not change credentials or routing because one task failed. Change the suspected cause, then rerun the decisive check. Do not loop unchanged commands or wait for the user when other authorized work can advance.
- Protect stable product behavior while changing adjacent features. A failed optional subsystem should leave the primary job usable.

Load [exhaustive-testing-architecture](../exhaustive-testing-architecture/SKILL.md) to design multi-layer tests and negative controls alongside implementation, [frontend-craft](../frontend-craft/SKILL.md) when UI is created or reshaped, [service-contracts](../service-contracts/SKILL.md) for API/data/realtime boundaries, [security-boundaries](../security-boundaries/SKILL.md) at trust boundaries, and [platform-qualification](../platform-qualification/SKILL.md) for device/browser/OS support. Load [parallel-agent-work](../parallel-agent-work/SKILL.md) only when delegation is authorized and genuinely useful.

## Accept and hand off

- Use [evidence-and-claims](../evidence-and-claims/SKILL.md) to map each required outcome to a check that can fail. For material changes, use [adversarial-review](../adversarial-review/SKILL.md) before calling the result complete.
- Verify at the layer of the claim: unit/integration, rendered browser or app, exact artifact, physical device/recipient, hosted service and distribution policy as applicable. Passing one layer never silently satisfies another.
- For a release claim, inspect clean install and update paths, production configuration and signing, migrations and recovery, privacy/asset rights, dependency risk, accessibility, performance, crash/health visibility and the supported platform matrix. Keep the status below release-ready while a required gate is open. Deployment and publication need explicit user intent and the verified destination.
- Reconcile the final brief against the delivered product. Report changed files, actual commands/results, observed interactions, unresolved outcomes and the next bounded action. For work that spans sessions, maintain one current [handoff](../../templates/HANDOFF.md) with exact version, ownership and process state.

---

## Gemini Web Execution Adaptation (`build-verified-product`)

When executing `build-verified-product` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

