---
name: evidence-and-claims
description: "Design acceptance checks and audit completion claims for substantial, risky, cross-platform, or release work. Skip a formal ledger for trivial edits and simple factual answers."
---

# Evidence and claims

The purpose of a gate is to decide an observable outcome, not to decorate a confident report. Write a small [evidence ledger](../../templates/EVIDENCE_LEDGER.md) before material work and update it when the user changes the acceptance condition.

## Define each claim precisely

Record the behavior, exact version or source revision, environment and scope. Name the oracle before running it: a test, service response, browser interaction, file hash, device state, receiver observation or human acceptance. Record the actual result, evidence location and limits. Use these statuses: `planned`, `observed`, `failed` or `unverified`. `Observed` means the stated outcome itself was seen; it does not mean the whole product is ready.

An executable gate must exit nonzero for a relevant failure and emit a success-only result after its assertions. Test a negative or absence checker against a known positive control; otherwise an empty log, wrong path or malformed parser can look like success. Derive measured values from raw observations rather than copying the target into an expectation. Rerun checks after relevant source, dependency, environment or artifact changes.

## Keep evidence layers separate

| Evidence | Can support | Does not establish |
| --- | --- | --- |
| Plan, spec, diagram | Intended behavior | Existing implementation |
| Source and official documentation | Code path or platform contract | Runtime success on every device |
| Unit/native test | Behavior exercised by that oracle | Real UI, hosted service or acoustic result |
| Local database test | SQL/policy behavior in that database | Hosted configuration |
| Browser render/interaction | Web UI at tested viewport/browser | Native app or physical-phone performance |
| Build, signature, hash | Exact package and configuration | Installation or feature operation |
| Device test | Exact model/OS/firmware/route/lifecycle | Universal compatibility |
| Receiver/user report | Human-perceived result in a consented trial | A precise technical cause or other devices |
| Store/policy source | Written eligibility requirement | Actual approval |

For a claim that crosses layers, require the combination. Example: a reaction “works in calls” needs a built/installed version, an eligible call, recipient hearing, speech continuity and safe cleanup; a green helper status or a passing domain test is insufficient.

## Report honestly

Recheck every claim immediately before the handoff. Preserve failed trials and uncertainty; do not relabel an interrupted check or a historical build's result as current. State timing origin, baseline, sampling uncertainty and other plausible causes when interpreting measurements. A reviewer can challenge a claim, but only the relevant oracle can settle it. No set of prompts guarantees zero hallucinations: this ledger exposes unsupported claims for another agent or person to reject.

Evidence files should contain only the minimum necessary proof. Keep credentials, raw private media, contacts and unnecessary identifiers out of logs and the ledger.

---

## Gemini Web Execution Adaptation (`evidence-and-claims`)

When executing `evidence-and-claims` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

