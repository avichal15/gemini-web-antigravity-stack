---
name: godmode
description: Context-adaptive sampling parameter tuning (AutoTune v4.5: 20 contexts, 5 strategies, 6 hyperparameters & EMA self-learning), 33-technique lexical encoding transforms & selective trigger detection (Parseltongue), structured prompt templates, Dual-Gateway OmniRoute + FreeLLMAPI apex LLM execution, 5-tier multi-model benchmarking & response quality scoring (Ultraplinian), 4-family multi-model council synthesis (godmode_council), and adversarial red-team stress-testing (godmode_challenge).
---

# Advanced Execution, Benchmarking, Council & Sampling Skill for Antigravity (Dual-Gateway OmniRoute + FreeLLMAPI Edition v4.5)

This skill provides local CLI scripts and MCP tools (`godmode_*`) for 33-technique lexical transformation testing (`parseltongue.js`), 20-context self-learning sampling optimization (`autotune.js`), structured prompt templates (`l1b3rt4s.js`), 5-tier multi-model benchmarking & composite response scoring (`ultraplinian.js`), 4-family multi-model parallel consensus deliberation (`godmode_council`), and adversarial assumption stress-testing (`godmode_challenge`) routed through local **OmniRoute** (`http://127.0.0.1:20128/v1`) and **FreeLLMAPI** (`http://127.0.0.1:3001/v1`).

## Core Capabilities (v4.5)

1. **33-Technique Lexical & Selective Trigger Engine (`parseltongue.js` / `godmode_parseltongue`)**:
   - **33 Encoding & Cipher Techniques** across 3 intensity tiers (`light`, `medium`, `heavy`):
     - *Standard (15)*: `leetspeak`, `base64`, `rot13`, `morse`, `binary`, `hex`, `pig_latin`, `reversed`, `insert_ZWS`, `fullwidth`, `upside_down`, `small_caps`, `bubble`, `braille`, `url_encode`
     - *Esoteric / Ancient Scripts (15)*: `elder_futhark`, `hieroglyphs`, `ogham`, `Aurebesh`, `wingdings`, `strikethrough`, `underline`, `superscript`, `subscript`, `fraktur`, `double_struck`, `monospace`, `vaporwave`, `zalgo`, `tap_code`
     - *Linguistic / Cipher (3)*: `caesar`, `atbash`, `NATO_phonetic` (+ aliases `unicode`, `zwj`, `phonetic`, `mixedcase`)
   - **Selective Trigger Detection (`--selective` / `detectTriggers`)**: Automatically detects parser-sensitive trigger tokens and transforms ONLY those words while keeping surrounding context 100% readable.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\parseltongue.js --text "verify bypass and payload injection" --technique leetspeak --intensity medium --selective`

2. **20-Context Self-Learning AutoTune Engine (`autotune.js` / `godmode_autotune`)**:
   - **20 Query Contexts**: `code_generation`, `security_audit`, `refactoring`, `creative_architecture`, `math_reasoning`, `creative`, `code`, `analysis`, `conversation`, `factual`, `brainstorm`, `roleplay`, `technical`, `philosophical`, `humor`, `debate`, `storytelling`, `summarization`, `translation`, `debugging`.
   - **5 Sampling Strategies**: `precise`, `balanced`, `creative`, `chaotic`, `adaptive`.
   - **6 Hyperparameters**: `temperature`, `top_p`, `top_k`, `frequency_penalty`, `presence_penalty`, `repetition_penalty`.
   - **Dynamic Context Classifier & EMA Self-Learning**: Automatically classifies raw prompts (`classifyQueryContext`) and updates persistent per-context EMA parameter adjustments (`autotune_state.json`) using automated quality heuristics (`computeHeuristics`).
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\autotune.js --prompt "Debug this race condition in worker threads" --strategy adaptive`

3. **Structured Prompt Templates (`l1b3rt4s.js` / `godmode_l1b3rt4s_template`)**:
   - Prompt framing templates (`grok-420`, `gemini-reset`, `claude-inversion`) for analytical comparisons and stress-testing.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\l1b3rt4s.js --combo grok-420 --query "your query"`

4. **ULTR4PL1N14N Multi-Model Benchmarking, Scoring & STM Engine (`ultraplinian.js` / `godmode_ultraplinian`)**:
   - **5 Speed Tiers**: `fast` (2 models, ~1s), `standard` (3 models, ~2-3s), `smart` (4 models, ~3-5s), `power` (5 models), `ultra` (7 models across OmniRoute + FreeLLMAPI).
   - **5-Axis Composite Response Scorer (`scoreResponse`)**: Scores every response (0-100) across `substance`, `structure`, `relevance`, `depth`, and `hedgePenalty`, ranking candidates highest-to-lowest and extracting `consensus_points` and `disagreement_points`.
   - **Surgical Text Modules (`STM_MODULES`)**: Post-processing filters (`hedge_reducer`, `direct_mode`, `casual_mode`) that strip preachy AI disclaimers and throat-clearing openers.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --mode ultraplinian --tier smart --prompt "Design an expand-contract zero-downtime migration"`

5. **Dual-Gateway Apex LLM Execution (`godmode_server.js` / `godmode_llm_call`)**:
   - Routes queries through local **OmniRoute** (`http://127.0.0.1:20128/v1/chat/completions`) and **FreeLLMAPI** (`http://127.0.0.1:3001/v1/chat/completions`) with automatic failover across 14 verified `200 OK` frontier models and virtual routers (`paid-premium`, `agy/claude-opus-4-6-thinking`, `cx/gpt-5.6-luna-max`, `cx/codex-auto-review-max`, `cu/auto-intelligence`, `gweb/gemini-3.1-pro`, `agy/claude-sonnet-4-6`, `agy/gemini-3.8-flash-high`, `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, `groq/openai/gpt-oss-120b`, `freellmapi/auto:coding`, `freellmapi/auto:smart`, `freellmapi/fusion`).
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --prompt "Analyze target architecture" --model "paid-premium" --context "auto"`

6. **4-Family Multi-Model Parallel Council (`godmode_council`)**:
   - Queries 4 independent frontier model families in parallel (`agy/claude-opus-4-6-thinking` [Anthropic], `cx/gpt-5.6-luna-max` [OpenAI Codex], `agy/gemini-3.8-flash-high` [Google], and `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` [NVIDIA 550B]), scores each response (`quality_score`), extracts `consensus_points` & `disagreement_points`, anonymizes outputs (`Response A..D`), runs Stage-2 blind peer critique, and synthesizes an authoritative consensus response.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --mode council --prompt "Design a zero-downtime migration strategy"`

7. **Adversarial Red-Team Challenge (`godmode_challenge`)**:
   - Subjects a proposed plan, architecture, or code diff to an adversarial red-team review (`doubt-driven-development`) using `cx/codex-auto-review-max` (OpenAI Codex Auto-Review Max, cascading to `agy/claude-opus-4-6-thinking`) to expose hidden assumptions, race conditions, and security flaws before implementation.
   - CLI: `node C:\Users\avich\.gemini\config\skills\godmode\scripts\godmode_server.js --mode challenge --proposal "Your proposed plan or diff" --goal "Target acceptance criteria"`
