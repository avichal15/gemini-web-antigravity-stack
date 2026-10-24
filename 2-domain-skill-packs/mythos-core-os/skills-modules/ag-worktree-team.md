# Skill Module: `ag-worktree-team`

- **Domain Pack**: `mythos-core-os`
- **Description**: Coordinates substantial Antigravity engineering work with bounded native subagents, clear file ownership, and isolated Git worktrees when independent tasks can run in parallel.

# Worktree coordination

Choose parallel work only when independent scopes improve delivery or review. A small change can stay with one agent.

Read the active project instructions and current Git status before dividing work. Identify the implementation owner, the acceptance criteria, and any shared files that require serial changes. Use Antigravity's native workspace options through the tool schema actually available: inherit an existing workspace for read-only research, or use an isolated branch/worktree for independent implementation when the project is a Git repository. Do not manufacture tool arguments or assume a non-Git folder supports worktrees.

Use built-in `research` for focused codebase discovery. Use `ag-reviewer` for an independent review of a stable diff and `ag-verifier` for acceptance checks. Give each agent the actual project path, allowed files/actions, requirements, known failures, and an explicit completion condition. Subagents start with separate context, so do not assume they know the main conversation.

The added specialists use `model: inherit`. Keep the user's selected provider, endpoints, credentials, and bridge configuration intact. Do not introduce per-agent API routing or credential-backed probes as part of coordination.

Keep one owner per writable file. When work runs in isolated worktrees, record the returned locations and review the diffs before integrating them. Do not overwrite unrelated edits or use destructive Git resets. Start reviewers after the relevant implementation is stable; run the final integration check in the actual target checkout.

Read the agents' evidence, resolve conflicting findings, and report the integrated result rather than forwarding success claims unchecked. Local coordination does not authorize commits, pushes, deployment, or external messages. For long tasks, use `ag-handoff` to preserve completed work and the next integration step.

## Synchronized Peer-to-Peer Mesh Protocol (`send_message`)

Subagents do not know each other's `conversationId` at spawn time unless the Coordinator tells them. Whenever spawning two or more subagents that need to coordinate (e.g., frontend + backend workers, or `ag-reviewer` + `ag-verifier`), execute the **Peer Directory Handshake**:

1. **Spawn Subagents**: Call `invoke_subagent` for each participant and record every returned `conversationId` alongside the Coordinator's own `conversationId`.
2. **Broadcast Peer Directory**: Immediately call `send_message` to each spawned subagent with the complete directory of active `conversationId`s and roles:
   - `Coordinator (Main Agent): <main_conversation_id>`
   - `Peer <Role A>: <subagent_a_conversation_id>`
   - `Peer <Role B>: <subagent_b_conversation_id>`
3. **Direct Peer-to-Peer Sync**: Instruct subagents to use `send_message(Recipient=<peer_conversation_id>, Message=...)` to negotiate API contracts, share reproduction results, challenge hypotheses, or unblock dependencies directly with each other, and to message the Coordinator (`<main_conversation_id>`) once synchronized.
4. **Reactive Wakeup**: Do not poll in loops. End the turn after dispatching messages; Antigravity automatically wakes up whichever agent receives a `send_message` payload.

---

## Gemini Web Execution Adaptation (`ag-worktree-team`)

When executing `ag-worktree-team` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

