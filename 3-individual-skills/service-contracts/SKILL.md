---
name: service-contracts
description: "Design or change an API, database schema, migration, realtime protocol, or external-service boundary in an app or website. Skip local-only UI and pure in-memory logic."
---

# Service and data contracts

Define the boundary before connecting screens to it. A client mock, schema file and live service may be at different versions; inspect the deployed or configured target before claiming integration.

1. Read the existing callers, types, migrations, policies and error behavior. Identify the exact source and hosted versions. For unfamiliar or version-sensitive provider APIs, use the provider's current documentation and a bounded real request or local reproduction.
2. Write the contract: request/response or event schema, authentication and ownership, validation limits, versioning, ordering/deduplication, retry/idempotency, timeout and failure states. Keep core product behavior independent of optional services when the product requires it.
3. Make schema changes forward-only unless a destructive migration is explicitly authorized. Preserve existing records and data rights; test old-to-new migration against representative data and a loss-detecting negative control. Have a rollback or recovery plan before production change.
4. Place authorization at the service or database boundary. Test with at least two distinct identities plus anonymous access when relevant; a signed-in UI is not proof that cross-user reads or writes are denied. Keep privileged keys and grant decisions off the client.
5. Verify the boundary in layers: pure contract tests, local integration against the actual database/protocol, then the intended hosted environment if authorized. Record which layer ran. A successful local SQL test, mock callback or simulated ad is not hosted delivery.
6. Log only privacy-safe, actionable events with correlation IDs where useful. A network or callback failure must have an observable retry/reconciliation path and must not claim success before durable state is committed.

When the boundary handles untrusted input, accounts, private data, file storage or rewards, also use [security-boundaries](../security-boundaries/SKILL.md). Give an independent reviewer the exact contract and changed implementation for consequential migrations or protocol changes.

---

## Gemini Web Execution Adaptation (`service-contracts`)

When executing `service-contracts` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

