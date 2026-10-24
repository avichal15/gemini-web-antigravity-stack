---
name: frontend-craft
description: "Design and implement a new interface or material visual redesign for an application or website, with rendered responsive and interaction checks. Do not use for a small copy or spacing edit."
---

# Frontend craft

Make the interface recognizable from its product, audience and real content. “Premium,” “modern,” or “Gen Z” alone is not a visual direction.

## Establish the art direction

1. Inspect the current screens or site, the primary user flows, real content/assets and any approved brand. Read the behavior spec as well as the visual brief. Identify which existing choices are accepted and which the user explicitly changed.
2. When references are supplied, describe the principles that make them effective: composition, typography, material, interaction, pace and clarity. Create an original visual language; do not copy the reference's artwork, layout, claims or unlicensed assets.
3. Write a compact direction before coding: one visual thesis, a small color/type/spacing system, primary screen hierarchy, one memorable interaction if appropriate, and rules for normal versus expressive moments. Choose each element for the product rather than a default template.

Question unearned repetition: identical rounded cards, generic gradients, arbitrary badges, filler icons, oversized slogans, fake statistics, meaningless technical metrics and decorative motion. These are warnings, not universal bans. A card, gradient or animation is good when it serves this brief and its interaction. A serious utility screen may need calm native conventions; a marketing page can use a more expressive scene without importing that scene into the product UI.

## Build behavior and states

- Implement the real flow, not only a screenshot. Every visible action has an outcome or an honest disabled/unavailable explanation. Use real or clearly labelled example content.
- Design loading, empty, denied, offline, error and success states with clear next actions. Keep control names and result copy consistent. Respect safe areas, text enlargement, keyboard/focus, screen readers, contrast and reduced motion.
- On mobile apps, keep essential actions reachable above system insets and preserve native call/navigation/permission conventions. Give direct manipulation a tap or keyboard alternative where feasible.
- On websites, preserve content and navigation while enhanced media loads or fails. For 3D/motion, provide a functional simple view, pause hidden work, bound resource use and keep repeated state changes from needlessly recreating the renderer.

## Inspect the rendered result

Run the actual app or site. Compare screenshots and interactions at a narrow phone width, a common phone width and a desktop/tablet size relevant to the product; add physical-device checks when the platform behavior matters. Exercise repeated switching, reverse navigation/scroll, overlays, long text, errors, keyboard and reduced motion. Inspect console/runtime errors and real control dimensions.

Critique hierarchy, legibility, copy/artwork separation, material quality, motion continuity and product truth. Fix meaningful mismatches before handoff. A passing build or static screenshot is not a visual or interaction acceptance test; a browser viewport is not physical mobile certification. Record the tested sizes and remaining devices/browsers.

For a multi-screen or animated surface, use the [visual QA matrix](references/visual-qa.md) to choose the checks that match this product.

---

## Gemini Web Execution Adaptation (`frontend-craft`)

When executing `frontend-craft` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

