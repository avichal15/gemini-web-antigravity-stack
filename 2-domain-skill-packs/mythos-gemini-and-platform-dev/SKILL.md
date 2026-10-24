---
name: mythos-gemini-and-platform-dev
description: "Mythos 5 Gemini SDK, Live API, Omni Video & Platform Engineering Pack for Gemini Web: Gemini API Dev, Gemini 3.8 Live API streaming, Gemini Omni 1.1 Flash video generation, Android CLI, Antigravity customizations, and workflow automation."
---

# `mythos-gemini-and-platform-dev` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **15 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-gemini-and-platform-dev`

- **`platform-qualification`** (`skills-modules/platform-qualification.md`): Verify or plan claims about browser, OS, OEM, hardware, device, native media, background behavior, or store support. Do not use for platform-independent domain logic.
- **`uv`** (`skills-modules/uv.md`): Checks whether the uv Python package manager is installed and installs it if missing. Ensures uv is on PATH. Use when another skill requires uv as a prerequisite.
- **`workflow-skill-creator`** (`skills-modules/workflow-skill-creator.md`): Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a skill, or when they say 'make this a skill', 'create a skill from what we just did', 'package this workflow' or similar. Do not use for creating skills from scratch without an existing workflow (use a generic skill-creator for that).
- **`gemini-api-dev`** (`skills-modules/gemini-api-dev.md`): Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, speech generation (TTS), voice design, voice replication, streaming responses, background research tasks, function calling, structured output, or migrating from the old generateContent API. Covers SDK usage and best practices for Gemini models and agents in Python and TypeScript.
- **`gemini-live-api-dev`** (`skills-modules/gemini-live-api-dev.md`): Use this skill when building real-time, bidirectional streaming applications with the Gemini Live API, or migrating legacy Live models (2.0/2.5/3.1) to Gemini 3.8 Live. Covers WebSocket-based audio/video/text streaming, voice activity detection (VAD), background reasoning (extended thinking), asynchronous function calling, session management, ephemeral tokens, live transcription, and live translation. SDKs covered - google-genai (Python), @google
- **`gemini-omni-flash-api`** (`skills-modules/gemini-omni-flash-api.md`): Use this skill for generative video editing, text-to-video, image-referenced video generation, first-frame-to-video, first-and-last-frame transitions, and video extensions using Gemini Omni 1.1 Flash (gemini-omni-1.1-flash) via the official google-genai SDK. Includes workflows for pre-processing/optimizing high-resolution or long source videos with ffmpeg, stripping audio for full sound regeneration, and handling turn-by-turn video editing and pa
- **`android-cli`** (`skills-modules/android-cli.md`): Provides instructions for installing and using the `android` CLI. The `android` command-line tool is a critical tool for Android development and helps you create new Android projects, run Android apps on devices, manage and interact with Android virtual devices (including screenshots and UI inspection), manage Android SDK components, look up official Android documentation, and discover and install official Android skills.
- **`agy-customizations`** (`skills-modules/agy-customizations.md`): Comprehensive guide and reference for the Antigravity Customization System. Use to explain how customizations work, their loading priority, discovery mechanisms, and to guide the creation of skills, rules, plugins, hooks, and MCP servers.
- **`antigravity-guide`** (`skills-modules/antigravity-guide.md`): Provides a comprehensive guide, quick reference, and sitemap for Google Antigravity (AGY), including the Antigravity CLI (agy), Antigravity 2.0, Antigravity IDE, Python SDK, slash commands, keybindings, and customizations (skills, rules, MCP, sidecars). Activate this skill when the user asks questions about how to use, configure, or customize Antigravity, AGY, the agy CLI, the Antigravity IDE, or Antigravity 2.0.
- **`automation`** (`skills-modules/automation.md`): Interactive guide to design and create a scheduled background automation. Use this skill when the user wants to create an automated or recurring scheduled task (e.g. 'summarize my emails every morning', 'every Monday send me a to-do list'). Also triggered by the /automation slash command.
- **`migrate-workflows`** (`skills-modules/migrate-workflows.md`): Automatically migrate legacy workflows to modern skills across global and workspace configurations. Scans for existing workflows, creates target SKILL.md files, and safely archives old workflow files.
- **`permissioned-github`** (`skills-modules/permissioned-github.md`): Guidelines for interacting with GitHub and request permissions from the user when commands fail due to restrictions in the agent environment.
- **`plugin`** (`skills-modules/plugin.md`): How to manage and create plugins — namespaced bundles of skills, agents, rules, MCP servers and hooks that install, enable and disable as a single unit. Use this skill when the user wants to enable, disable, install or uninstall a plugin, when they want to create a new plugin, or when a new customization should be packaged into a plugin rather than left loose. Also triggered by the /plugin slash command. Don't use for the underlying customization
- **`run-workflow`** (`skills-modules/run-workflow.md`): How to write and run a dynamic workflow script with the `run_workflow` tool: a Python script that orchestrates many agents with `agent`, `parallel`, `pipeline`, and `phase`. Use when a task splits into many independent or staged pieces of agent work (fan out over files, modules, bugs, or review angles, then aggregate), or when the user asks for a workflow. Don't use for a single delegated task (use a subagent) or for legacy workflow files (see mi
- **`ui-plugin-navigation`** (`skills-modules/ui-plugin-navigation.md`): Discover UI plugin panels relevant to the current task and surface a one-click pill in chat to open (toggle) them in the side pane. Use when a running UI plugin's panel would help with what the user is doing, or right after the user enables a new UI plugin pane and a shortcut to open it is handy.

## How Gemini Web Executes This Pack

1. **Select Relevant Module**: When the user's request matches any skill above, read `skills-modules/<skill-name>.md` and follow its workflow end-to-end.
2. **Run Pre-Action & Post-Action Verification in Python Sandbox**:
   - Before executing complex actions: `python scripts/mythos_web_runtime.py pre-check --action "<action>" --target "<target>"`
   - After generating code or artifacts: `python scripts/mythos_web_runtime.py post-verify --file "<path>"`
   - For multi-step deliverables: write `GATES.md` and run `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve`
3. **Search Bundled Memory & Playbooks**:
   - Run `python scripts/mythos_memory_search.py --query "<keywords>" --source all`
4. **Run Godmode 4-Family Council & Red-Team Challenge**:
   - Run `python scripts/godmode_web_engine.py council --question "<question>"`
   - Run `python scripts/godmode_web_engine.py challenge --target "<file_or_plan>"`
