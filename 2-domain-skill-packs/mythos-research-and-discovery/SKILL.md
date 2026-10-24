---
name: mythos-research-and-discovery
description: "Mythos 5 Deep Discovery & Multi-Platform Research Pack for Gemini Web: Open-source repository & architecture discovery, Agent Reach, context engineering, structured ideation, interview-me requirements extraction, ADRs, and NotebookLM synthesis."
---

# `mythos-research-and-discovery` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **7 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-research-and-discovery`

- **`agent-reach`** (`skills-modules/agent-reach.md`): MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X / 看看大家怎么评价 X / X 上有什么讨论 / research this topic。 Also MUST USE when user mentions any platform or shares any URL/链接: 小红书/xiaohongshu/xhs, Twitter/推特/X, B站/bilibili, Reddit, Facebook, Instagram, V2EX, LinkedIn/领英/Boss直聘/招聘/求职/jobs, YouTube, GitHub code search, 小宇宙播客, 雪球/股票行情, RSS feeds, or any web URL. 16 platforms, multi-ba
- **`deep-discovery`** (`skills-modules/deep-discovery.md`): Multi-channel open-source tool, repository, and workflow discovery across GitHub, YouTube creator videos/Shorts (via yt-dlp description & transcript mining), Instagram Reels (via insta-manager-acceptance-bridge + watch skill), Scrapling stealth web extraction, and NotebookLM Deep Research. Use whenever searching for an existing open-source alternative (e.g. 'CapCut open source'), CLI harness, MCP server, or reference implementation before buildin
- **`context-engineering`** (`skills-modules/context-engineering.md`): Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project.
- **`documentation-and-adrs`** (`skills-modules/documentation-and-adrs.md`): Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design choice, when changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.
- **`idea-refine`** (`skills-modules/idea-refine.md`): Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on 'ideate', 'refine this idea', or 'stress-test my plan'.
- **`interview-me`** (`skills-modules/interview-me.md`): Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified ('build me X' without 'for whom' or 'why now'), when the user explicitly invokes ('interview me', 'grill me', 'are we sure?', 'stress-test my thinking'), or when you catch yourself silently filling in ambiguous requirements bef
- **`notebooklm`** (`skills-modules/notebooklm.md`): Complete API for Google NotebookLM - full programmatic access including features not in the web UI. Create notebooks, add sources, generate all artifact types, download in multiple formats. Activates on explicit /notebooklm or intent like 'create a podcast about X

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
