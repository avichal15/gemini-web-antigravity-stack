---
name: stitch-manage-design-system
description: "Manage design systems in Stitch using MCP tools. Includes retrieval of assets, creating/updating design systems in Stitch, and applying them to screens."
---

# Design-System

Create a "source of truth" for your project's design language to ensure
consistency across all future screens.

> [!NOTE]
> Refer to your system prompt for instruction on handling MCP tool prefixes for
> all tools mentioned in this skill (e.g., `get_screen`,
> `create_design_system_from_design_md`, `apply_design_system`).

## 📥 Retrieval

To analyze a Stitch project, you must retrieve metadata and assets using the
Stitch MCP tools:

1. **Project lookup**: Use `list_projects` to find the target `projectId`.
2. **Screen lookup**: Use `list_screens` for that `projectId` to find
   representative screens (e.g., "Home", "Main Dashboard").
3. **Metadata fetch**: Call `get_screen` for the target screen to get
   `screenshot.downloadUrl` and `htmlCode.downloadUrl`.
4. **Asset download**: Use `read_url_content` to fetch the HTML code.

## 🧠 Synthesis from Description

If you need to extract a design system from existing screens, use the `design-md` skill (in the `stitch-utilities` plugin).

If there are no existing screens (new project), or the user provides a direct description (e.g., "dark theme, blue and purple, rounded, Inter font"):

1. Map the user's vague terms to precise values using the design mappings (see `design-md` skill in `stitch-utilities` or `generate-design` skill).
2. Select concrete hex codes, font families, and roundness values.
3. Generate the `DESIGN.md` file (refer to the `design-md` skill in `stitch-utilities` for structure).
4. Proceed to the "Create or Update Design System in Stitch" step below.

## 📝 Output Structure

The `DESIGN.md` file should follow the structure defined in the `design-md` skill (in the `stitch-utilities` plugin).

## 🚀 Create or Update Design System in Stitch

After generating `.stitch/DESIGN.md`, make sure to also create or update the
design system in Stitch.

**Two-step design system creation:**

> [!WARNING]
> **Checkpoint — User Confirmation Required.**
> Before uploading, you **MUST** pause and ask the user for
> confirmation. Present a summary of the design system you are about to create
> (display name, key colors, fonts, and roundness) and wait for explicit approval
> before proceeding. Do **NOT** upload until the user confirms.

1. **Upload `DESIGN.md`**:
   - **Option A (Recommended - Uploader Script)**: Use the modified `upload-to-stitch` Python script which natively handles `.md` files. It base64-encodes the markdown file in-process and sends it to the `/v1/projects/{projectId}/screens:batchCreate` endpoint, bypassing output token limits.
     ```bash
     python3 stitch-skills/plugins/stitch-design/skills/upload-to-stitch/scripts/upload_to_stitch.py \
       --project-id <PROJECT_ID> \
       --file-path /path/to/DESIGN.md \
       --api-key <API_KEY> \
       --generated-by <GENERATED_BY>
     ```
     Set `<GENERATED_BY>` to identify the skill or tool that produced the
     `DESIGN.md`. Use the calling skill name when invoked from another skill
     (e.g. `stitch::code-to-design`), or the agent/tool name for standalone
     use (e.g. `Gemini`, `Claude Code`). If omitted, the script defaults to
     `UserUploadedDesignMd`.

     This returns the `sourceScreen` ID and the `screenInstance` ID.
   - **Option B (Direct MCP Tool)**: If the `DESIGN.md` is small (under ~5KB), you can call the `upload_design_md` MCP tool directly, passing the base64-encoded design markdown content as `designMdBase64`.
2. **Create Design System**: Call the `create_design_system_from_design_md` tool immediately after the upload, passing the `projectId` and the `selectedScreenInstance` (containing the `id` and `sourceScreen` returned from the upload step).

Once the upload script and `create_design_system_from_design_md` have both completed,
Stitch holds the design tokens at the project level — you do NOT need to repeat
them in generation prompts.

## 🎨 Apply Design System to Screens

Use `apply_design_system` to apply a design system to existing screens.

> [!IMPORTANT]
> `selectedScreenInstances` must contain **only** `id` and `sourceScreen` — do
> NOT include position/dimension fields (`x`, `y`, `width`, `height`) or the
> request will fail with "invalid argument". Get the screen instance IDs from
> `get_project`.

```json
{
  "projectId": "...",
  "assetId": "...",
  "selectedScreenInstances": [
    {
      "id": "...",
      "sourceScreen": "projects/.../screens/..."
    }
  ]
}
```

**How to get the required IDs:**
1. Call `get_project` to retrieve `screenInstances` — each has an `id` and
   `sourceScreen`.
2. Call `list_design_systems` to retrieve the design system `name` (format:
   `assets/{assetId}`) — use the part after `assets/` as the `assetId`.
3. Filter out any instances with `type: "DESIGN_SYSTEM_INSTANCE"` — only pass
   real screens.

## 📋 Update Project Metadata

After writing `.stitch/DESIGN.md`, also create or update `.stitch/metadata.json`
to track the `projectId`, `title`, all known screens, and design system summary.
See [examples/metadata.json](examples/metadata.json) for the format.

## Schema Reference

See [reference/tool-schema.md](reference/tool-schema.md) for the full
`designSystem` object schema with all available options.

## 💡 Best Practices

Refer to the `design-md` skill (in the `stitch-utilities` plugin) for best practices on describing design elements.

---

## Gemini Web Execution Adaptation (`stitch-manage-design-system`)

When executing `stitch-manage-design-system` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

