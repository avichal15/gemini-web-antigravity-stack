---
name: platform-qualification
description: "Verify or plan claims about browser, OS, OEM, hardware, device, native media, background behavior, or store support. Do not use for platform-independent domain logic."
---

# Platform qualification

Support is a matrix of exact environments and behaviors, not a single boolean. Separate a capability suggested by documentation from one observed on the target system.

## Build the matrix

For each target, record platform/browser or model, OS version, firmware/build, app version and artifact hash, permissions/role, route or peripheral, network state, foreground/background/locked state and the outcome being tested. Preserve a distinct row for each manufacturer or browser engine where its implementation can differ. Use `supported and verified`, `ready but unverified`, `setup required`, `temporarily unavailable`, `unsupported` or `unknown` in the product and report, as appropriate.

Use official version-matched API and policy sources to identify a plausible route. AOSP/framework code, a simulator, emulator or ROM image can validate that source or exercise an API shape. It cannot by itself prove an OEM modem/audio-HAL path, physical receiver audio, sensor behavior, push delivery, battery policy or store approval.

## Test the actual user path

Start with fresh identity and idle-state preflight after reconnecting or swapping a device. Verify clean setup, denied permission, primary flow, repeated actions, cancellation, interruption, process death, cold start, update, reboot, output/network changes and cleanup where relevant. Check that a failing optional feature leaves the core flow usable. For a communication/media claim, distinguish local playback, sender feedback, receiver result and continuous speech; use consenting humans and avoid raw private media capture unless separately authorized.

Retain exact evidence with timing origins and hashes. Do not reuse a stale device transport ID, old artifact result or subjective hearing report as a new automated measurement. When the device is unavailable, prepare the test and mark it pending; never invent a pass. Qualify new models one at a time, and expand the public support promise only as the matrix warrants.

---

## Gemini Web Execution Adaptation (`platform-qualification`)

When executing `platform-qualification` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

