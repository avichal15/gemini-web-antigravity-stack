---
name: security-boundaries
description: "Design or review authentication, private data, uploads, files, payments/rewards, native privileges, webhooks, or other untrusted-service boundaries. Do not invoke for static presentation code alone."
---

# Security boundaries

Security follows the product's authority and data flows. A client setting, attractive UI, private Git repository or obfuscated package is not a server authorization boundary.

## Map the system

Identify assets worth protecting, untrusted inputs, actors, trust boundaries, permission scopes and external services. State where authority lives: device, client, backend, provider or OS. Ask what a malicious user could change, replay, omit, race, upload, request as another account or retain after logout. Choose controls at the boundary that actually decides the action.

Typical checks include input size/type/path validation, output encoding, server-side authorization, least-privilege database policies, bounded file operations, signed webhook verification, replay/idempotency protection, token/session lifetime, rate limits, account deletion and safe failure during outages. For an optional subsystem, failure should not disable the primary product job unless the contract requires it.

## Verify attacks, not only happy paths

- Test denied cross-account reads/writes, anonymous access and privilege escalation against the real policy engine. Distinguish local database emulation from the configured hosted service.
- Test malformed, duplicated, stale, reordered and tampered requests at API, callback and file boundaries. Check that an outage does not acknowledge an uncommitted reward or erase a user's valid progress.
- Check the committed dependency lockfile, build configuration and exact release artifact for secrets, debug flags, unsafe exported components, unnecessary permissions and asset inclusion. A text search is a lead; inspect actual bundle/package bytes for consequential release claims.
- Run negative controls for a release guard: deliberately disable the protection in a safe local test and confirm the build is rejected for the intended reason. Do not weaken a production setting just to obtain a green check.

Keep credentials, private keys, tokens, personal contacts and raw media out of source, logs, reviewer prompts and handoffs. Use small sanitized receipts and private local storage only when needed. Record asset ownership and redistribution rights separately from technical downloadability.

For a complex feature, select relevant abuse cases from the [boundary check matrix](references/boundary-checks.md). Use the real framework/provider rules for implementation details.

Client obfuscation can raise the cost of copying but cannot make a shipped app impossible to inspect or prevent a playable asset from being recorded. Keep reward/signing authority server-side and describe remaining rooted/instrumented-client limits honestly. Technical device success, user consent, provider approval, law and store policy are separate gates.

Read-only review and local fixes within the user's request can proceed. Invasive testing, new credentials/permissions, live service changes, billing, deployment or publication require explicit intent and a verified target. Do not turn a security audit into an unrelated provider or account configuration change.

---

## Gemini Web Execution Adaptation (`security-boundaries`)

When executing `security-boundaries` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

