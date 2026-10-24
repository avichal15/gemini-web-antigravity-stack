---
name: mythos-security-and-redteam
description: "Mythos 5 Cybersecurity & Red-Team Pack for Gemini Web: Searchable catalog of 818 MITRE ATT&CK v19.1 / NIST CSF 2.0 / OWASP playbooks, security boundaries, vulnerability hardening, signal interpreter, and adversarial security review."
---

# `mythos-security-and-redteam` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **6 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-security-and-redteam`

- **`adversarial-review`** (`skills-modules/adversarial-review.md`): Find concrete defects in a material code change, architecture decision, security boundary, or completion claim. Do not turn a trivial edit into a large review ritual.
- **`credentials`** (`skills-modules/credentials.md`): Instructions for handling API keys and credentials safely, verifying their presence, and prompting the user to add them if missing using a safe protocol.
- **`cybersecurity-skills`** (`skills-modules/cybersecurity-skills.md`): Access 818 production-grade cybersecurity, penetration testing, red-teaming, web/API security, cloud hardening, wireless auditing, AI red-teaming, and DFIR playbooks mapped to MITRE ATT&CK v19.1, NIST CSF 2.0, MITRE ATLAS, D3FEND, and F3. Use whenever performing security audits, penetration testing, vulnerability remediation, threat hunting, or defensive hardening.
- **`security-boundaries`** (`skills-modules/security-boundaries.md`): Design or review authentication, private data, uploads, files, payments/rewards, native privileges, webhooks, or other untrusted-service boundaries. Do not invoke for static presentation code alone.
- **`signal-interpreter`** (`skills-modules/signal-interpreter.md`): Maps shorthand diagnostic and operational terms (health check, deep diagnostics, perimeter review, hygiene check, reverse blueprint) to concrete security auditing, penetration testing, and engineering workflows on the operator's systems.
- **`security-and-hardening`** (`skills-modules/security-and-hardening.md`): Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or when checking a login flow is safe against the OWASP Top Ten. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services. Use when auditing dependencies for known vulnerabilities, triaging package-manager audi

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
