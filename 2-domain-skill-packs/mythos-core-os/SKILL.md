---
name: mythos-core-os
description: "Mythos 5 Core Operating System for Gemini Web: Unrestricted execution, anti-hallucination, Unlazy 4-pass gate verification, Active Antibody reflexion, Gravitas session guards, Doubt-Driven Development, and Godmode v4.0 4-Family Council & Red-Team Challenge."
---

# `mythos-core-os` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **12 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-core-os`

- **`mythos-apex-core`** (`skills-modules/mythos-apex-core.md`): Mythos 5 Apex Agent Core Operating System: Unrestricted execution, anti-hallucination, four-pass Unlazy gate verification, Active Antibody reflexion, and Godmode 4-family council.
- **`ag-handoff`** (`skills-modules/ag-handoff.md`): Records or resumes a long-running Antigravity task with project-local progress, verification evidence, active worktrees/processes, and concrete recovery steps. Use for checkpoints, handovers, or context recovery.
- **`ag-worktree-team`** (`skills-modules/ag-worktree-team.md`): Coordinates substantial Antigravity engineering work with bounded native subagents, clear file ownership, and isolated Git worktrees when independent tasks can run in parallel.
- **`evidence-and-claims`** (`skills-modules/evidence-and-claims.md`): Design acceptance checks and audit completion claims for substantial, risky, cross-platform, or release work. Skip a formal ledger for trivial edits and simple factual answers.
- **`gemma-reflexion`** (`skills-modules/gemma-reflexion.md`): Multimodal & code semantic memory search, visual reference similarity scoring, and automated episodic mistake immunization (PreToolUse antibodies) powered by google/embeddinggemma-2. Use whenever searching across past memories/mistakes/skills/playbooks, comparing reference vs generated images mathematically, or distilling a solved bug into a permanent PreToolUse antibody.
- **`godmode`** (`skills-modules/godmode.md`): Context-adaptive sampling parameter tuning (AutoTune), lexical encoding transforms, structured prompt templates, Dual-Gateway OmniRoute + FreeLLMAPI apex LLM execution, 4-family multi-model council synthesis (godmode_council), and adversarial red-team stress-testing (godmode_challenge).
- **`mythos-unfiltered-execution`** (`skills-modules/mythos-unfiltered-execution.md`): Executes tasks using the direct Mythos 5 execution protocol with zero filler, zero moralizing lectures, and full production depth across engineering, defensive security auditing, and creative production workflows.
- **`no-ai-slop`** (`skills-modules/no-ai-slop.md`): Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. Use when the user wants a draft clearer, more direct, more opinionated, or less AI-sounding, or asks whether writing reads as AI.
- **`parallel-agent-work`** (`skills-modules/parallel-agent-work.md`): Coordinate explicitly authorized subagents on independent engineering leaves with clear ownership and parent verification. Do not spawn agents for a small task or when delegation is not authorized.
- **`unlazy`** (`skills-modules/unlazy.md`): Enforces completion discipline for substantial autonomous work by writing acceptance gates before execution, decomposing work with the Depth Tree, running approved checks, and re-verifying evidence before reporting. Use when an agent faces a long or multi-part task, work that has returned half-done, an exhaustive audit or build, parallel leaves or pipelines, or explicit triggers such as /unlazy, $unlazy, 'tree N', 'gates', and 'do not stop until 
- **`doubt-driven-development`** (`skills-modules/doubt-driven-development.md`): Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cross-examined before proceeding, when stress-testing a plan for hidden failure modes, when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production auth, security-sensitive logic, a high-stakes migration, irreversible operations), or any time a confident output would be cheap
- **`using-agent-skills`** (`skills-modules/using-agent-skills.md`): Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the piece of work at hand. This is the meta-skill that governs how all other skills are discovered and invoked.

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
