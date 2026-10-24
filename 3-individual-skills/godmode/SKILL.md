---
name: godmode
description: "Context-adaptive sampling parameter tuning (AutoTune), lexical encoding transforms, structured prompt templates, Dual-Gateway OmniRoute + FreeLLMAPI apex LLM execution, 4-family multi-model council synthesis (godmode_council), and adversarial red-team stress-testing (godmode_challenge)."
---

# Advanced Execution, Council & Sampling Skill for Antigravity (Dual-Gateway OmniRoute + FreeLLMAPI Edition v4.0)

This skill provides local CLI scripts and MCP tools (`godmode_*`) for lexical transformation testing, context-adaptive sampling optimization, structured prompt templates, 4-family multi-model parallel consensus deliberation (`godmode_council`), and adversarial assumption stress-testing (`godmode_challenge`) routed through local **OmniRoute** (`http://127.0.0.1:20128/v1`) and **FreeLLMAPI** (`http://127.0.0.1:3001/v1`).

## Core Capabilities

1. **Lexical Transformation Engine (`parseltongue.js` / `godmode_parseltongue`)**:
   - Character and encoding transformations (`leetspeak`, `unicode`, `zwj`, `phonetic`, `mixedcase`).
   - Use for security auditing, parser resilience testing, and input boundary analysis.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\parseltongue.js --text "query" --technique leetspeak --intensity heavy`

2. **AutoTune Sampling Engine (`autotune.js` / `godmode_autotune`)**:
   - Context-adaptive parameter optimizer across execution contexts (`code_generation`, `security_audit`, `refactoring`, `creative_architecture`, `math_reasoning`).
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\autotune.js --context security_audit`

3. **Structured Prompt Templates (`l1b3rt4s.js` / `godmode_l1b3rt4s_template`)**:
   - Prompt framing templates (`grok-420`, `gemini-reset`, `claude-inversion`) for analytical comparisons and stress-testing.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\l1b3rt4s.js --combo grok-420 --query "your query"`

4. **Dual-Gateway Apex LLM Execution (`godmode_server.js` / `godmode_llm_call`)**:
   - Routes queries through local **OmniRoute** (`http://127.0.0.1:20128/v1/chat/completions`) and **FreeLLMAPI** (`http://127.0.0.1:3001/v1/chat/completions`) with automatic failover across 14 verified `200 OK` frontier models and virtual routers:
     1. `paid-premium` (OmniRoute 13-model priority combo)
     2. `agy/claude-opus-4-6-thinking` (Anthropic Claude Opus 4.6 Thinking — AGY pool, ~3.4s)
     3. `antigravity/claude-opus-4-6-thinking` (Anthropic Claude Opus 4.6 Thinking — Antigravity pool, ~3.4s)
     4. `cx/gpt-5.6-luna-max` (OpenAI Codex GPT-5.6 Luna Max, ~1.7s)
     5. `cx/codex-auto-review-max` (OpenAI Codex Auto-Review Max, ~2.4s)
     6. `cu/auto-intelligence` (Cursor Auto-Intelligence, ~2.4s)
     7. `gweb/gemini-3.1-pro` (Google Gemini 3.1 Pro via Web, ~7.3s)
     8. `agy/claude-sonnet-4-6` (Anthropic Claude Sonnet 4.6, ~2.0s)
     9. `agy/gemini-3.8-flash-high` (Google Gemini 3.8 Flash High, ~4.8s)
     10. `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (NVIDIA Nemotron-3 Ultra 550B MoE, ~959ms)
     11. `groq/openai/gpt-oss-120b` (OpenAI GPT-OSS 120B on Groq LPU, ~1.0s)
     12. `freellmapi/auto:coding` (FreeLLMAPI composite coding router -> `cx/codex-auto-review-max` / `qwen3-coder-480b`, ~1.6s)
     13. `freellmapi/auto:smart` (FreeLLMAPI composite intelligence router across 1,622 models & 11 active providers, ~187ms–1.7s)
     14. `freellmapi/fusion` (FreeLLMAPI parallel 2-provider synthesis router)
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --prompt "Analyze target architecture" --model "paid-premium" --context "security_audit"`

5. **4-Family Multi-Model Parallel Council (`godmode_council`)**:
   - Queries 4 independent frontier model families in parallel (`agy/claude-opus-4-6-thinking` [Anthropic], `cx/gpt-5.6-luna-max` [OpenAI Codex], `agy/gemini-3.8-flash-high` [Google], and `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` [NVIDIA 550B]), anonymizes their outputs (`Response A..D`), runs blind peer critique, and synthesizes an authoritative consensus response.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --mode council --prompt "Design a zero-downtime migration strategy"`

6. **Adversarial Red-Team Challenge (`godmode_challenge`)**:
   - Subjects a proposed plan, architecture, or code diff to an adversarial red-team review (`doubt-driven-development`) using `cx/codex-auto-review-max` (OpenAI Codex Auto-Review Max, cascading to `agy/claude-opus-4-6-thinking`) to expose hidden assumptions, race conditions, and security flaws before implementation.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --mode challenge --proposal "Your proposed plan or diff" --goal "Target acceptance criteria"`

---

## Gemini Web Execution Adaptation (`godmode`)

When executing `godmode` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

