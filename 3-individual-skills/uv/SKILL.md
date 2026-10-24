---
name: uv
description: "Checks whether the uv Python package manager is installed and installs it if missing. Ensures uv is on PATH. Use when another skill requires uv as a prerequisite."
---

# uv (Python Package Manager)

`uv` is a fast Python package manager used by Science Skills to run their Python
CLI scripts. Many skills depend on `uv` being installed and on
PATH.

Ensure `uv` is available before running any skill that depends on it.

## Setup

1.  Check if `uv` is already available: `uv --version` (or `& uv --version` in
    PowerShell). If this succeeds, `uv` is ready — skip the remaining steps.
2.  Check whether `uv` is installed at its default location but not on PATH:

    -   **Unix/macOS**: `"$HOME/.local/bin/uv" --version`
    -   **Windows (PowerShell)**: `& "$HOME\.local\bin\uv.exe" --version`

    If either succeeds, skip to step 4.

3.  If uv is not installed do these steps in order:

    
    (a) Tell the user that uv is a tool for creating a consistent and reliable
        Python environment used for running the Science Skills, and that you
        need to install it now.

    (b) Install `uv`:

        -   **Unix/macOS**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
        -   **Windows (PowerShell)**: `powershell -ExecutionPolicy ByPass -c
            "irm https://astral.sh/uv/install.ps1 | iex"`

    

4.  Add `uv` to PATH and verify (run as a single command):

    -   **Unix/macOS**: `export PATH="$HOME/.local/bin:$PATH" && uv --version`
    -   **Windows (PowerShell)**: `$env:PATH = "$HOME\.local\bin;" + $env:PATH;
        uv --version`

After setup, bare `uv` commands should work without repeating the export.

---

## Gemini Web Execution Adaptation (`uv`)

When executing `uv` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

