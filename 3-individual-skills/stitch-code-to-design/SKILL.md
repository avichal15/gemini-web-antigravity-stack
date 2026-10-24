---
name: stitch-code-to-design
description: "Convert frontend code (Vite, React, Angular, Vue, etc.) to a Stitch Design by chaining static HTML extraction, design system extraction, and file upload. **ALWAYS** use this skill when the user's intent is to move existing web apps or React/Angular/Vue components into Stitch (e.g., requests to 'save', 'migrate', or 'upload'). You must use this skill even for simple 'save' operations, as it is the only way to ensure the design system is extracted "
---

# Code to Design

Transform your existing frontend code (React + Vite, Next.js, Angular, Vue, etc.) into a Stitch Design so you can iterate and improve it using Stitch.

This skill orchestrates three other skills in sequence:
1. `extract-static-html`: Extract a single self-contained HTML file from your build output or running dev server (e.g., Vite dev server or Angular CLI `ng serve`).
2. `extract-design-md`: Analyze the source code (including Angular `angular.json`, external `.html` templates, theme files, and components) to create a design system (DESIGN.md).
3. `upload-to-stitch`: Upload that HTML file and the design system to your Stitch project.

## Workflow

Follow these steps to convert your existing code.

### Prerequisites

- A running local dev server (e.g. `npm run dev`, `ng serve`) OR a built web application directory containing `index.html` and assets.
- Target Stitch `projectId` (use `list_projects` if unknown).

### Steps

#### 1. Extract Self-Contained HTML

Delegate to the `extract-static-html` skill to generate a standalone HTML file.
Read [skills/extract-static-html/SKILL.md](../extract-static-html/SKILL.md) for detailed instructions and script usage.

Expected output: A single file like `/path/to/extracted/standalone.html`.

#### 2. Verify HTML (Optional — User-Driven)

After extraction, inform the user of the output file path so they can manually
verify in a browser if desired. **Do not block on verification** — proceed
directly to Step 3.

If the user reports issues after reviewing, fix them before continuing.

#### 3. Extract Design System (File)

Delegate to the `extract-design-md` skill to analyze the project's source files
(components, stylesheets, theme configs) and produce a design system. Read
[skills/extract-design-md/SKILL.md](../extract-design-md/SKILL.md) for the
full analysis workflow.

Write `.stitch/DESIGN.md` following the `extract-design-md` skill's output
structure.

#### 4. Upload DESIGN.md and Create Design System in Stitch

Delegate to the `manage-design-system` skill to upload the `DESIGN.md` and
create the design system in Stitch. Read
[skills/manage-design-system/SKILL.md](../manage-design-system/SKILL.md) for
the full workflow (upload script usage, `create_design_system_from_design_md`
call, and required schemas). Pass
`--generated-by 'stitch::code-to-design'` when uploading.

#### 5. Upload HTML to Stitch

Use the same `upload-to-stitch` skill's script to upload the extracted HTML file.
Read [skills/upload-to-stitch/SKILL.md](../upload-to-stitch/SKILL.md) for detailed instructions and script usage.

You will need:
- The path to the standalone HTML file generated in Step 1.
- Your Stitch API Key (same key used in Step 4).
- The target `projectId`.
- The `--generated-by` argument set to `'stitch::extract-static-html'`.
- The `--title` argument set to the **route path** of the page (e.g., `'/dashboard'`, `'/settings/profile'`, `'/inbox'`) so that the screen name/title in Stitch clearly identifies its route in the application.

---

## Gemini Web Execution Adaptation (`stitch-code-to-design`)

When executing `stitch-code-to-design` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

