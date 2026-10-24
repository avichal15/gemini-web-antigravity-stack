# Skill Module: `react-vite-dashboard`

- **Domain Pack**: `mythos-frontend-and-stitch`
- **Description**: Convert Stitch designs into production React + Vite dashboards with TanStack Query, accessible tokens from DESIGN.md, and Web3-ready patterns (ethers/viem).

# Stitch to React + Vite Dashboard

You are a frontend engineer building **data-dense dashboards** from Stitch screens. Target stack: **React 18**, **Vite**, **TypeScript**, **TanStack Query**, **React Router**, and optional **ethers v6** or **viem** for on-chain reads.

## Prerequisites

- Stitch MCP configured ([setup guide](https://stitch.withgoogle.com/docs/mcp/setup/))
- A project `DESIGN.md` (see the `design-md` skill) for token fidelity
- Vite + React + TypeScript scaffold (`npm create vite@latest`)

## Workflow

1. **Discover MCP prefix** — run `list_tools`, note the Stitch prefix (e.g. `stitch:`).
2. **Fetch screen** — `[prefix]:get_screen` with project and screen IDs.
3. **Download assets** — persist HTML/screenshot under `.stitch/designs/{screen}.html` and `.png`.
4. **Read DESIGN.md** — map `colors.*`, `typography.*`, `spacing.*` to CSS variables in `src/index.css`.
5. **Generate components** — split into `src/components/`, `src/pages/`, `src/hooks/`.
6. **Wire data** — use TanStack Query for async fetches; keep presentational components pure.

## HTML → React mapping

| Pattern | Implementation |
|---------|----------------|
| Layout grid / flex | Tailwind utilities or CSS modules aligned to DESIGN.md spacing tokens |
| Cards / panels | `<section>` with tokenized border-radius and elevation fallbacks for forced-colors |
| Tables | Semantic `<table>` or TanStack Table; never div-only grids for tabular data |
| Buttons | `<button type="button">` with visible focus ring (preserve browser default unless DESIGN.md defines focus tokens) |
| Forms | `<label htmlFor>` + `<input id>`; associate errors with `aria-describedby` |
| Loading | Skeleton components; `aria-busy` on containers during fetch |
| Wallet connect | Isolate in `WalletProvider`; never embed private keys in generated code |

## DESIGN.md integration

```css
/* src/index.css — example token bridge */
:root {
  --color-primary: /* from DESIGN.md colors.primary */;
  --font-body: /* typography.body-md.fontFamily */;
}
```

Run the design.md linter locally before shipping UI:

```bash
npx @google/design.md lint DESIGN.md
```

## Web3 dashboard conventions

- Read-only contract calls via `useReadContract` (viem/wagmi) or ethers `Contract` + TanStack Query `queryFn`.
- Format token amounts with `formatUnits`; show network name and chain ID in settings footer.
- Surface transaction errors in plain language; link to block explorer when `txHash` exists.
- Gas-sensitive flows: batch reads, avoid redundant `eth_call` in render loops.

## File structure

```
src/
├── components/     # Presentational UI from Stitch
├── pages/          # Route-level screens
├── hooks/          # useQuery wrappers, wallet hooks
├── lib/            # ABI helpers, formatters
└── styles/         # Token CSS variables
```

## Quality checklist

- [ ] WCAG 2.2 AA: contrast from DESIGN.md component pairs passes linter
- [ ] Keyboard navigable: focus order matches visual order
- [ ] Responsive: test at 375px and 1280px widths
- [ ] No secrets in repo: RPC URLs from env (`VITE_*` prefix only for public endpoints)
- [ ] TypeScript strict: no `any` on contract ABIs

## Stitch docs note

When following links on [stitch.withgoogle.com/docs](https://stitch.withgoogle.com/docs/), use the full `https://stitch.withgoogle.com/docs/...` URL if relative navigation redirects incorrectly.

---

## Gemini Web Execution Adaptation (`react-vite-dashboard`)

When executing `react-vite-dashboard` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

