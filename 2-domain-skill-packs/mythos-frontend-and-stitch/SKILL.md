---
name: mythos-frontend-and-stitch
description: "Mythos 5 Frontend Craft & Google Labs Stitch Design Pack for Gemini Web: All 16 official Stitch skills, DESIGN.md synthesis, shadcn/ui, React+Vite dashboards, Generative UI, Taste Design, and Canvas/Browser verification."
---

# `mythos-frontend-and-stitch` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **21 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-frontend-and-stitch`

- **`ag-browser-check`** (`skills-modules/ag-browser-check.md`): Verifies a local web app's requested UI behavior in Antigravity using browser observations, interaction checks, and relevant responsive evidence. Use for rendered frontend acceptance or UI regressions.
- **`agent-browser`** (`skills-modules/agent-browser.md`): Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to 'open a website', 'fill out a form', 'click a button', 'take a screenshot', 'scrape data from a page', 'test this web app', 'login to a site', 'automate browser actions', or any task r
- **`frontend-craft`** (`skills-modules/frontend-craft.md`): Design and implement a new interface or material visual redesign for an application or website, with rendered responsive and interaction checks. Do not use for a small copy or spacing edit.
- **`stitch-code-to-design`** (`skills-modules/stitch-code-to-design.md`): Convert frontend code (Vite, React, Angular, Vue, etc.) to a Stitch Design by chaining static HTML extraction, design system extraction, and file upload. **ALWAYS** use this skill when the user's intent is to move existing web apps or React/Angular/Vue components into Stitch (e.g., requests to 'save', 'migrate', or 'upload'). You must use this skill even for simple 'save' operations, as it is the only way to ensure the design system is extracted 
- **`design-md`** (`skills-modules/design-md.md`): Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files
- **`enhance-prompt`** (`skills-modules/enhance-prompt.md`): Transforms vague UI ideas into polished, Stitch-optimized prompts. Enhances specificity, adds UI/UX keywords, injects design system context, and structures output for better generation results.
- **`stitch-extract-design-md`** (`skills-modules/stitch-extract-design-md.md`): Extract a comprehensive design system (DESIGN.md) directly from frontend source code — React, Vue, Svelte, Angular, plain HTML/CSS, or any web framework. Analyzes component files, stylesheets, Tailwind configs, theme definitions, and design tokens to produce a rich, Stitch-compatible design system document. Use this skill whenever the user wants to reverse-engineer a design system from an existing codebase, audit the visual language of a project,
- **`stitch-extract-static-html`** (`skills-modules/stitch-extract-static-html.md`): Extract self-contained static HTML from a built web application or React components by inlining CSS and images. Use this skill whenever you need to capture a specific UI state, share a static version of a page, or prepare assets for Stitch upload, even if the user just asks to 'save the HTML' or 'mock the view'.
- **`stitch-generate-design`** (`skills-modules/stitch-generate-design.md`): Generate new screens from text prompts or images, edit existing screens with prompts and design system tokens, and generate design variants using Stitch MCP. Includes prompt enhancement pipeline, design mappings, professional UI/UX terminology, design tokens and theme system capabilities.
- **`stitch-loop`** (`skills-modules/stitch-loop.md`): Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern
- **`stitch-manage-design-system`** (`skills-modules/stitch-manage-design-system.md`): Manage design systems in Stitch using MCP tools. Includes retrieval of assets, creating/updating design systems in Stitch, and applying them to screens.
- **`stitch-react-components`** (`skills-modules/stitch-react-components.md`): Converts Stitch designs into modular Vite and React components, or syncs/updates existing React components to align with the latest Stitch designs, using system-level networking and AST-based validation.
- **`stitch-react-native`** (`skills-modules/stitch-react-native.md`): Convert Stitch HTML designs to React Native components, or syncs/updates existing native components to align with the latest Stitch designs, using StyleSheet.
- **`react-vite-dashboard`** (`skills-modules/react-vite-dashboard.md`): Convert Stitch designs into production React + Vite dashboards with TanStack Query, accessible tokens from DESIGN.md, and Web3-ready patterns (ethers/viem).
- **`shadcn-ui`** (`skills-modules/shadcn-ui.md`): Expert guidance for integrating and building applications with shadcn/ui components, including component discovery, installation, customization, and best practices.
- **`site-md`** (`skills-modules/site-md.md`): Analyze a project description or site requirements and synthesize a project constitution into SITE.md for the Stitch Build Loop
- **`taste-design`** (`skills-modules/taste-design.md`): Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typography, calibrated color, asymmetric layouts, perpetual micro-motion, and hardware-accelerated performance.
- **`stitch-upload-to-stitch`** (`skills-modules/stitch-upload-to-stitch.md`): Upload local assets (images, mockups, extracted HTML, design markdown) to a Stitch project. ALWAYS use this skill when you need to upload visual assets, HTML pages, or design docs to Stitch, particularly when direct MCP tool calls fail or truncate due to base64 token limits.
- **`browser-testing-with-devtools`** (`skills-modules/browser-testing-with-devtools.md`): Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data. Requires the chrome-devtools MCP server to be configured.
- **`frontend-ui-engineering`** (`skills-modules/frontend-ui-engineering.md`): Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output needs to look and feel production-quality rather than AI-generated.
- **`generative-ui`** (`skills-modules/generative-ui.md`): How to render rich interactive HTML widgets inline in the chat or as standalone artifacts. Use this skill when you want to show the user diagrams, data visualizations, interactive controls, educational walkthroughs, or any rich visual content beyond plain text and markdown.

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
