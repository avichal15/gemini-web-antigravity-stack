# Skill Module: `migrate-workflows`

- **Domain Pack**: `mythos-gemini-and-platform-dev`
- **Description**: Automatically migrate legacy workflows to modern skills across global and workspace configurations. Scans for existing workflows, creates target SKILL.md files, and safely archives old workflow files.

# Migrate Workflows to Skills

Use this skill to autonomously migrate legacy workflow files to modern skills.

Workflows (`.agents/workflows/*.md` or `_agents/workflows/*.md`) are deprecated.
Skills (`.agents/skills/<name>/SKILL.md` or `_agents/skills/<name>/SKILL.md`)
provide all the capabilities of workflows, plus:

-   First-class slash command support (typing `/<name>` in the chat input box).
-   Semantic agent discovery (the agent can automatically invoke the skill when
    relevant).
-   Multi-file capabilities (supporting helper scripts, templates, and
    references).

--------------------------------------------------------------------------------

## Instructions for the Agent

When this skill is invoked, **you must execute the migration automatically** by
performing the following steps:

### Step 1: Discover Existing Workflows

Scan **global** and **workspace** (if applicable) configuration directories
using filesystem search tools for legacy `.md` workflow files and
`workflows.json` manifests:

1.  **Global Workflows**:

    -   `~/.gemini/config/global_workflows/*.md`
    -   `~/.gemini/config/workflows/*.md`
    -   Manifests: `~/.gemini/config/workflows.json`

2.  **Workspace Workflows** (for each open workspace root and parent
    directories):

    -   `<workspace_root>/.agents/workflows/*.md`
    -   `<workspace_root>/_agents/workflows/*.md`
    -   `<workspace_root>/.agent/workflows/*.md`
    -   `<workspace_root>/_agent/workflows/*.md`
    -   Manifests:
        `<workspace_root>/{.agents,_agents,.agent,_agent}/workflows.json`

> [!NOTE]
> **OS-Specific Path and Output Formatting:**
> - Adapt path resolution to the host OS (`%USERPROFILE%` on Windows vs. `$HOME` on macOS/Linux).
> - When presenting tables, progress, or summaries to the user, **always format paths using the host OS path separators** (e.g. `\` on Windows such as `%USERPROFILE%\.gemini\config\global_workflows\<name>.md`, `/` on macOS/Linux).

**Check each discovered workflow against existing skills:** For each workflow,
check if `<target_skill_dir>/<name>/SKILL.md` already exists to determine
whether it has already been migrated.

**Present the discovered workflows, their migration targets, and status:**

Scope     | Workflow Name | Source Path                                   | Target Skill Path                            | Status
:-------- | :------------ | :-------------------------------------------- | :------------------------------------------- | :-----
Global    | `<name>`      | `~/.gemini/config/global_workflows/<name>.md` | `~/.gemini/config/skills/<name>/SKILL.md`    | `Pending` / `Already Migrated`
Global    | `<name>`      | `~/.gemini/config/workflows/<name>.md`        | `~/.gemini/config/skills/<name>/SKILL.md`    | `Pending` / `Already Migrated`
Workspace | `<name>`      | `<workspace>/.agents/workflows/<name>.md`     | `<workspace>/.agents/skills/<name>/SKILL.md` | `Pending` / `Already Migrated`
Workspace | `<name>`      | `<workspace>/_agents/workflows/<name>.md`     | `<workspace>/_agents/skills/<name>/SKILL.md` | `Pending` / `Already Migrated`

-   If no workflow files are found (or all have already been cleaned up), inform
    the user that their workspace and global configs are already clean.
-   If all workflows are `Already Migrated`, inform the user that target
    `SKILL.md` files already exist and proceed directly to archiving/cleaning up
    the remaining legacy files without overwriting existing skills.

--------------------------------------------------------------------------------

### Step 2: Convert Each Workflow to a Skill (Idempotent Execution)

For each workflow file:

1.  **Check existing skill (Overwrite Protection)**:

    -   If `<target_dir>/<name>/SKILL.md` **already exists**, **do not overwrite
        it** (preserves any manual edits or improvements made after prior
        migrations). Skip to Step 2.4 (cleanup/archiving).
    -   If `<target_dir>/<name>/SKILL.md` **does not exist**, proceed with
        conversion.

2.  **Read and format the source workflow**:

    -   Read the source `.md` file content.
    -   Inspect existing frontmatter (if any) and markdown body.
    -   Extract the workflow's title, description, or purpose from the content.
    -   Ensure standard YAML frontmatter with `name` and `description`:

        ```markdown
        ---
        name: <name>
        description: <concise one-sentence description of what the skill does and when to use it>
        ---

        # <Title>

        <Workflow instructions and guidelines>
        ```
    -   Retain all prompt instructions, arguments, and guidelines from the
        original workflow.

3.  **Write the target skill file**:

    -   Create the directory: `<target_dir>/<name>/` (e.g.
        `<workspace>/.agents/skills/<name>/` or
        `~/.gemini/config/skills/<name>/`)
    -   Write the file: `<target_dir>/<name>/SKILL.md`

4.  **Archive the legacy workflow safely**:

    -   Rename the old `.md` workflow file to `<name>.md.bak` (e.g. using `mv
        my_workflow.md my_workflow.md.bak` on Linux/macOS, or using `Move-Item` /
        file tools on Windows). Do not permanently delete the file so that the
        original content is safely preserved as a backup.
    -   Remove migrated workflow entries from any `workflows.json` manifests.

--------------------------------------------------------------------------------

### Step 3: Verify and Confirm

1.  Confirm all target `SKILL.md` files exist and legacy workflows have been
    renamed to `.md.bak`.
2.  Inform the user of the final summary:
    -   Newly migrated skills (`SKILL.md`).
    -   Previously migrated skills skipped (preserved existing `SKILL.md`
        files).
    -   Legacy workflow files safely archived as `.md.bak`.

---

## Gemini Web Execution Adaptation (`migrate-workflows`)

When executing `migrate-workflows` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

