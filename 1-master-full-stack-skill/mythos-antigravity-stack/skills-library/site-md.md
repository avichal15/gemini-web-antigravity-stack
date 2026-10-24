# Skill Module: `site-md`

- **Domain Pack**: `mythos-frontend-and-stitch`
- **Description**: Analyze a project description or site requirements and synthesize a project constitution into SITE.md for the Stitch Build Loop

# Stitch SITE.md Skill

You are a Lead Product Owner and Architect. Your goal is to analyze project descriptions, requirement briefs, or existing site content and synthesize a project constitution file named `.stitch/SITE.md`.

## Overview

This skill helps you initialize and structure `.stitch/SITE.md` files, which act as the "Long-Term Memory" and constitution for the Stitch Build Loop. A properly structured `SITE.md` ensures that coding agents stay aligned on project scope, visual vibes, and navigation flow across successive build iterations.

## Prerequisites

- Access to a project requirements brief or description document.
- Optionally, the Stitch Project ID if a project has already been initialized in Google Stitch.

## The Goal

Generate a `.stitch/SITE.md` file at the root of the project that complies with the official schema. It must cover:
1. Core Identity (Name, Mission, Voice).
2. Visual Language Vibe.
3. Architecture & File Structure.
4. Sitemap (Current and target pages).
5. Roadmap Backlog (High, Medium, Low priority tasks).
6. Creative Freedom Guidelines.

## Guidelines and Structure

Analyze the input brief and translate it into the following sections:

### 1. Core Identity
- **Project Name**: Extracted from requirements.
- **Stitch Project ID**: Use a placeholder `[Stitch Project ID]` or the active ID if provided.
- **Mission**: A 1-2 sentence description of what the application/site does.
- **Target Audience**: Who the main users are.
- **Voice**: Tone adjectives (e.g. professional, playful, clean).

### 2. Visual Language
- **Vibe (Adjectives)**: Define a primary, secondary, and tertiary aesthetic keyword matching the project's visual direction.

### 3. Architecture & File Structure
- Map out the directory structure. Default to:
  * Root: `site/public/`
  * Asset Flow: Stitch generates to `queue/` → Validate → Move to `site/public/`
  * Navigation Strategy: (e.g., standard header links, shared navigation bar).

### 4. Live Sitemap
- Map out the files requested in the brief. Mark completed files as `[x]` and pending/target files as `[ ]`. At initialization, at least `index.html` should be listed.

### 5. The Roadmap (Backlog)
- Parse the requirements into concrete development tasks, grouped by priority:
  - **High Priority**: Core pages, basic layouts, primary user flows.
  - **Medium Priority**: Interactive features, forms, secondary pages.
  - **Low Priority**: Enhancements, visual assets, optional states.

---

## Action Plan

1. **Read input requirements**: Locate and read the project description document or text input.
2. **Draft the structure**: Map the project details directly into the `SITE.md` format.
3. **Write the file**: Write the output to `.stitch/SITE.md`. If the `.stitch/` directory does not exist, create it first.
4. **Validate**: Verify that all seven sections of the `SITE.md` template are present and properly formatted.

---

## Gemini Web Execution Adaptation (`site-md`)

When executing `site-md` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

