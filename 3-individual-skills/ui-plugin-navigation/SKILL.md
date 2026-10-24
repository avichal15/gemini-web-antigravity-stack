---
name: ui-plugin-navigation
description: "Discover UI plugin panels relevant to the current task and surface a one-click pill in chat to open (toggle) them in the side pane. Use when a running UI plugin's panel would help with what the user is doing, or right after the user enables a new UI plugin pane and a shortcut to open it is handy."
---

# UI Plugin Navigation

> [!NOTE]
> **UI plugins and UI extensions are the same thing**: a sidecar-backed web
> panel that renders in the auxiliary (side) pane. Treat the two terms as
> interchangeable. Everything below applies whichever term the user or other
> skills use.

Some plugins expose a UI panel that renders in the auxiliary (side) pane. This
skill tells you how to surface a clickable **pill** in chat that opens/toggles
that panel, using the `sidecar://` link scheme.

## When to surface a pill

Offer a pill in either situation:

1.  **Contextual relevance.** Read the enabled UI plugins' `description` /
    `display_name`. If a plugin's purpose matches what the user is doing right
    now and seeing its UI would help, offer that plugin's pill.
2.  **After a new UI plugin pane is enabled.** When the user has just created
    and enabled a UI plugin pane, include a pill pointing to it so they can open
    it immediately.

Surface pills sparingly — only when the panel is genuinely useful. Don't repeat
a pill the user has already opened or dismissed.

## Step 1: Find UI plugin panes and their views

UI plugin panes are backed by sidecars, which live under these directories (each
in its own `<sidecar-id>/` folder containing a `sidecar.json`):

-   `~/.gemini/config/sidecars/<sidecar-id>/`
-   `~/.gemini/<app-name>/builtin/sidecars/<sidecar-id>/`
-   `~/.gemini/config/plugins/<plugin>/sidecars/<sidecar-id>/` (or external
    sidecar folders referenced by
    `~/.gemini/config/plugins/<plugin>/sidecars.json`)
-   `~/.gemini/<app-name>/builtin/plugins/<plugin>/sidecars/<sidecar-id>/` (or
    referenced by `~/.gemini/<app-name>/builtin/plugins/<plugin>/sidecars.json`)

The **sidecar-id** is the folder name — except for **plugin** sidecars (those
under a `plugins/<plugin>/sidecars/` directory or referenced by a plugin's
`sidecars.json`), whose id is namespaced as `<plugin>/<sidecar-folder>`. A
sidecar has a UI panel only if its `sidecar.json` has `has_web_ui` set to true
and a `ui_config.views` entry with `entrypoint:
SIDECAR_UI_ENTRYPOINT_AUX_PANE`. From that entry take:

-   **sidecar-id** — the folder name, or `<plugin>/<folder>` for plugin
    sidecars.
-   **view-path** — the `path` field (e.g. `/`, `host.html?view=auxpane`).
-   Use `description` / `display_name` (and `views[].title`) to judge relevance
    and to label the pill.

## Step 2: Emit the pill link

Write a standard markdown link with the `sidecar://` scheme:

```markdown
[Label](sidecar://<sidecar-id>/<view-path>)
```

-   **Label** — should be equivalent to the view `title`, the sidecar
    `display_name` or the `sidecar_id` with preference in that order. If the
    sidecar is part of a plugin, you can also use the plugin name instead.
-   Only emit pills for **AUX_PANE** views of plugins that are **enabled and
    running**.

Examples (substitute the actual id/path you discovered in Step 1):

```markdown
[<Sidecar Name>](sidecar://<sidecar-id>/)
[<Sidecar Name>](sidecar://<sidecar-id>/host.html?view=auxpane)
```

## Constraints & Tips

*   **The pill toggles the aux pane.** Clicking opens the plugin's panel. DO NOT
    output a plugin link, if the plugin isn't enabled/running.
*   **Deduce relevance from the description, not guesswork.** If no enabled UI
    plugin's description matches the conversation, don't force a pill.
*   **One pill per pane.** Don't emit multiple links to the same view.

---

## Gemini Web Execution Adaptation (`ui-plugin-navigation`)

When executing `ui-plugin-navigation` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

