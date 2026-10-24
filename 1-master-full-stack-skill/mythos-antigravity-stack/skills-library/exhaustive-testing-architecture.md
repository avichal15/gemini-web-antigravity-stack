# Skill Module: `exhaustive-testing-architecture`

- **Domain Pack**: `mythos-fullstack-engineering`
- **Description**: Design and execute Astra-grade multi-layer automated test suites, negative controls, real-engine database/RLS tests, and byte-level artifact verifiers. Invoke whenever implementing features, fixing bugs, hardening security boundaries, or preparing release candidates so every behavioral and security claim is backed by decisive executable tests.

# Exhaustive Testing Architecture

High-confidence agent engineering does not rely on happy-path smoke tests or mocked assertions that mirror the implementation's own assumptions. To achieve Astra-grade reliability, decompose every feature and bug fix into testable invariants across six complementary verification layers and require a negative control for every guard.

## 1. Extract Pure State Machines and Policies First

Never trap complex business rules inside UI components, React hooks, or platform service callbacks where they are slow or brittle to test:

- Extract deterministic state machines, routing decisions, permission matrices, retry/cooldown schedules, geometry math, and input parsers into pure functions or standalone classes before wiring them to React, DOM, or native Android/iOS bridges.
- Test the full transition matrix: initial states, valid transitions, out-of-order events, concurrent or duplicate triggers, cancellation during async work, and recovery after process death or reload.
- In Android/JVM or native modules, keep policy and wire-protocol classes free of `android.os.Binder` or framework singletons so JUnit tests can exhaustively exercise lifecycle, window, pairing, and buffer boundaries in milliseconds.

## 2. Test Real Database Engines and Privilege Boundaries Without SQL Mocks

Mocking an ORM or Supabase client proves nothing about SQL syntax, foreign-key cascades, Row Level Security (RLS), or function privileges:

- Run the complete SQL migration chain from an empty database inside an in-memory real engine (such as `@electric-sql/pglite` for PostgreSQL/Supabase or in-memory SQLite) during standard unit test runs.
- Test every role boundary explicitly (`anon`, `authenticated`, `service_role`):
  - Verify `PUBLIC` and `anon` cannot execute administrative or mutating RPCs under default grants.
  - Verify User A cannot read, update, claim, or delete User B's rows, files, call memberships, or reward ledgers.
  - Verify account deletion erases the departing user's private rows and storage metadata while preserving shared integrity and other users' records.
  - Verify rate limits, idempotency keys, and request quotas reject replay and burst abuse inside transactions.

## 3. Exercise Cryptographic, Protocol, and Input Boundaries with Adversarial Payloads

For every external input (webhooks, OAuth callbacks, deep links, file uploads, IPC intents, media decoders):

- Test with real cryptographic primitives (generating valid and invalid Ed25519/ECDSA key pairs and signatures in the test) rather than stubbing the verifier.
- Assert rejection of tampered payloads, wrong-key signatures, expired timestamps, replayed transaction IDs, unverified key servers, and key-rotation cache floods.
- Test path traversal (`../`, symlink escapes, absolute paths), oversized payloads, malformed UTF-8/JSON, null bytes, and unapproved MIME/header combinations.
- Verify that a network or storage failure rolls back or preserves retry state rather than marking an action completed or corrupting user preferences.

## 4. Prove Every Guard with a Negative Control

A test or verifier that has never been seen to fail for the target defect is a weak oracle:

- When fixing a bug, run the new regression test against the unfixed behavior (or a Deliberate fault injection) first to confirm it fails for the exact expected reason.
- For build, release, and security guards, write automated negative-control tests that invoke the guard against deliberately broken inputs (disabled minification, debug signing certificate, wrong certificate SHA-256, unapproved asset hash, missing license evidence, leaked prohibited string) and assert a non-zero exit code with the specific diagnostic message.
- For absence assertions ("no error in logs", "no prohibited symbol in DEX", "no secret in bundle"), pair the check with a positive control proving the scanner detects a seeded violation.

## 5. Verify Compiled Artifacts and Asset Bytes, Not Just Source Text

Source configurations can be bypassed by bundler defaults, transitive dependencies, or build scripts:

- Inspect the built output (APK/AAB archives, DEX bytecode tables, ELF shared library alignment, web `dist/` bundles, generated static HTML, and packaged ZIP kits).
- Verify audio, image, and binary assets by parsing their actual headers and computing SHA-256 digests (for example, checking WAV RIFF/PCM sample rates, channel counts, and exact byte-derived durations rather than trusting metadata JSON).
- Bind public manifests, download pages, and release configs to exact byte counts and SHA-256 hashes so stale or renamed artifacts fail preflight automatically.

## 6. Scale Runtime, Browser, and Device Probes to the Claim

Automated unit and artifact suites run on every edit; pair them with runtime probes matched to the environment:

- For web and UI changes, verify live rendered DOM, computed layout across desktop/mobile viewports, console/page errors, and asset responses in a real browser (`chrome-devtools-mcp` / Playwright).
- For native mobile or hardware routes, distinguish emulator checks from physical-device qualification and local API return values from recipient/acoustic ground truth.

## 7. Anti-Gaming and Guard Integrity

An agent must never pass a gate by weakening the system or the oracle:

- Never relax production flags (`minifyEnabled`, shrinking, signing certificate SHA-256, RLS policies, explicit SQL function privileges, manifest permissions, or `QaOnly` isolation) in the live workspace to turn a test green.
- Negative controls must mutate isolated temporary copies, fixtures, or parameterized inputs rather than editing live release configs in place.
- Treat any newly introduced `.skip`, `.only`, `.todo`, `@ts-ignore`, `@ts-expect-error`, `eslint-disable`, weakened threshold, or deleted assertion as a gate failure unless explicitly justified in `DECISIONS.md`.
- Keep local iteration conveniences (such as `QaOnly` receivers or debug seed helpers) strictly isolated so release artifact verifiers reject any build that retains them.

See [six-layer test patterns](references/six-layer-test-patterns.md) for concrete templates and patterns across TypeScript/Vitest, PGlite SQL, Python artifact verifiers, and JVM policy tests.

---

## Gemini Web Execution Adaptation (`exhaustive-testing-architecture`)

When executing `exhaustive-testing-architecture` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

