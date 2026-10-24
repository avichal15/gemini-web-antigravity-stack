---
name: gemma-reflexion
description: "Multimodal & code semantic memory search, visual reference similarity scoring, and automated episodic mistake immunization (PreToolUse antibodies) powered by google/embeddinggemma-2. Use whenever searching across past memories/mistakes/skills/playbooks, comparing reference vs generated images mathematically, or distilling a solved bug into a permanent PreToolUse antibody."
---

# EmbeddingGemma 2 Semantic Memory & Reflexion (`gemma-reflexion`)

Powered by **`google/embeddinggemma-2`** (Gemma 4 architecture, 8,192-token context, Matryoshka MRL 256d/768d vectors, CUDA `bfloat16`) running locally at `C:\Users\avich\.gemini\config\memory\gemma_memory.py` (`C:\Users\avich\.local\bin\gemma-memory.cmd`).

## Core Capabilities

1. **Unified Semantic Search (`gemma-memory search`)**:
   - Searches across 5 indexed local knowledge sources simultaneously in `<15ms` once encoded:
     - `antibody`: Active `PreToolUse` mistake-prevention rules (`C:\Users\avich\.gemini\config\memory\antibodies.json`)
     - `episode`: Historical bug/failure/fix episodes (`C:\Users\avich\.gemini\config\memory\episodes.jsonl`)
     - `memory`: Long-term architectural & operator memories (`C:\Users\avich\.agentmemory\standalone.json`)
     - `skill`: All 65+ installed Antigravity skills (`C:\Users\avich\.gemini\config\skills\*\SKILL.md`)
     - `cyber`: All 818 MITRE ATT&CK / NIST / OWASP playbooks (`Anthropic-Cybersecurity-Skills`)
   - Supports task-steered instruction prefixes: `SearchQuery`, `CodeRetrieval`, `FactChecking`, `Classification`, `SentenceSimilarity`.

   ```powershell
   C:\Users\avich\.local\bin\gemma-memory.cmd search "windows child process hang on port 3001" --task SearchQuery --source all --top-k 5
   C:\Users\avich\.local\bin\gemma-memory.cmd search "graphql jwt authentication bypass" --task CodeRetrieval --source cyber --top-k 5
   ```

2. **Continual Mistake Learning & PreToolUse Antibody Creation (`gemma-memory learn`)**:
   - Whenever you diagnose and fix a non-trivial bug, tool hang, CLI syntax trap, or environment quirk, distill it into an active antibody so [`pre-tool-rtk.mjs`](file:///C:/Users/avich/.gemini/config/hooks/pre-tool-rtk.mjs) automatically intercepts (`warn`, `rewrite`, or `block`) any future attempt to repeat the mistake:

   ```powershell
   C:\Users\avich\.local\bin\gemma-memory.cmd learn `
     --id "AB-007" `
     --name "example-pattern" `
     --tool "run_command" `
     --regex "some-bad-flag" `
     --action "warn" `
     --symptom "Command fails with error X" `
     --root-cause "Flag Y is deprecated in v4" `
     --prevention "Use --new-flag instead"
   ```

3. **Multimodal Reference-vs-Output Image Similarity (`gemma-memory image-sim`)**:
   - Uses `google/embeddinggemma-2`'s 170M vision encoder (`<|image|>`) alongside the 8-axis visual check in `cli-anything-google-vids` to compute the cosine similarity between a reference image and a generated output image:

   ```powershell
   C:\Users\avich\.local\bin\gemma-memory.cmd image-sim "path/to/ref.png" "path/to/generated.png" --prompt "studio product photo"
   ```

4. **Incremental Corpus Sync (`gemma-memory sync`)**:
   - SHA-256 content-hashed batch indexing (`batch_size=64`, `truncate_dim=256`). Only newly added or modified records are encoded:

   ```powershell
   C:\Users\avich\.local\bin\gemma-memory.cmd sync --dim 256
   ```

## Precision Rule (AB-005)
Never pass `torch.float16` to `google/embeddinggemma-2` (its activation range exceeds `fp16` dynamic range and produces `NaN`). Always use `torch.bfloat16` on CUDA or `torch.float32` on CPU (handled automatically by `gemma_memory.py`).

---

## Gemini Web Execution Adaptation (`gemma-reflexion`)

When executing `gemma-reflexion` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

