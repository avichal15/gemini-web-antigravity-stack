# Skill Module: `cybersecurity-skills`

- **Domain Pack**: `mythos-security-and-redteam`
- **Description**: Access 818 production-grade cybersecurity, penetration testing, red-teaming, web/API security, cloud hardening, wireless auditing, AI red-teaming, and DFIR playbooks mapped to MITRE ATT&CK v19.1, NIST CSF 2.0, MITRE ATLAS, D3FEND, and F3. Use whenever performing security audits, penetration testing, vulnerability remediation, threat hunting, or defensive hardening.

# Anthropic Cybersecurity Skills Router (818 Playbooks · 34 Domains)

This skill routes on-demand to the **818 structured cybersecurity skills** stored locally at:
`C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills`

By routing through `index.json` instead of loading all 818 folders into the global `<skills>` prompt, you get sub-second access to every practitioner playbook with **zero idle context token cost**.

---

## 1. Fast Skill Discovery (`search_skills.py`)

Before starting a security audit, penetration test, red-team assessment, or hardening workflow, search the 818-skill index by keyword, domain, MITRE ATT&CK technique (`T1XXX`), or OWASP category:

```powershell
python "C:\Users\avich\.gemini\config\skills\cybersecurity-skills\scripts\search_skills.py" "<query>" --limit 10
```

### Example Queries
- **Web & API Security**: `python "C:\Users\avich\.gemini\config\skills\cybersecurity-skills\scripts\search_skills.py" "jwt auth bypass graphql idor"`
- **Wireless & Network Auditing**: `python "C:\Users\avich\.gemini\config\skills\cybersecurity-skills\scripts\search_skills.py" "wireless wpa bluetooth network"`
- **Cloud & Container Hardening**: `python "C:\Users\avich\.gemini\config\skills\cybersecurity-skills\scripts\search_skills.py" "aws iam kubernetes rbac"`
- **AI & LLM Red-Teaming**: `python "C:\Users\avich\.gemini\config\skills\cybersecurity-skills\scripts\search_skills.py" "prompt injection mcp garak"`

---

## 2. Loading a Matched Playbook

Once `search_skills.py` returns the matching skill IDs, read the top 1–3 `SKILL.md` files directly via `read_file`:

```text
C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills\skills\<skill-name>\SKILL.md
```

If the skill includes deep references or helper scripts, inspect:
- `C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills\skills\<skill-name>\references\`
- `C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills\skills\<skill-name>\scripts\`

---

## Gemini Web Execution Adaptation (`cybersecurity-skills`)

When executing `cybersecurity-skills` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

