# Skill Module: `deep-discovery`

- **Domain Pack**: `mythos-research-and-discovery`
- **Description**: Multi-channel open-source tool, repository, and workflow discovery across GitHub, YouTube creator videos/Shorts (via yt-dlp description & transcript mining), Instagram Reels (via insta-manager-acceptance-bridge + watch skill), Scrapling stealth web extraction, and NotebookLM Deep Research. Use whenever searching for an existing open-source alternative (e.g. 'CapCut open source'), CLI harness, MCP server, or reference implementation before buildin

# Deep Discovery — Multi-Channel Solution & Repository Finder

Plain Google/web search often surfaces SEO listicles instead of the actual open-source repositories, CLI harnesses, and workflows creators showcase on **YouTube**, **Instagram Reels**, **GitHub**, and **NotebookLM Deep Research**.

Whenever a task can be solved or accelerated by an existing open-source tool, CLI harness (`CLI-Anything`), or GitHub repository — **run this 4-channel discovery protocol before writing custom code from scratch**.

---

## 1. Automated Multi-Channel CLI Sweep (`discover.py`)

Run the bundled `discover.py` script to simultaneously query **GitHub Search** (`gh` CLI / REST API) and **YouTube Creator Videos/Shorts** (`yt-dlp` metadata + full video description mining for `github.com/<owner>/<repo>` links):

```powershell
python "C:\Users\avich\.gemini\config\skills\deep-discovery\scripts\discover.py" "capcut open source" --yt-count 6 --gh-limit 10 --json
```

What `discover.py` executes automatically:
1. **GitHub Direct & Breakout Search**: Queries `gh search repos` (or GitHub API with token fallback from `mcp_config.json`) across both all-time star leaders and modern breakouts, ranking by stars and activity.
2. **YouTube Creator & Shorts Description Mining**: Uses `yt-dlp` to pull top creator videos/Shorts matching `<query> github open source`, parses every video description for `https://github.com/<owner>/<repo>` URLs, and cross-enriches any discovered GitHub repos that didn't appear in standard keyword search.
3. **Deduplicated Ranked Output**: Merges and ranks repositories found across both GitHub and YouTube creator descriptions, flagging repos discovered via creator videos (`discovered_via: ["youtube", "github"]`).

---

## 2. Instagram Reels Discovery Channel (`insta-manager-acceptance-bridge` + `watch`)

Many niche open-source tools, UI libraries, and AI workflows go viral on Instagram Reels before ranking on Google. When searching for visual tools, video editors, design generators, or AI workflows on Instagram:

1. **Search via `insta-manager-acceptance-bridge` MCP**:
   - Call `instagram_navigate` to `https://www.instagram.com/explore/search/keyword/?q=<url_encoded_query>` (or use `instagram_click` + `instagram_type` on the search input).
   - Call `instagram_find_elements` or `instagram_screenshot` to collect the top Reel URLs (`https://www.instagram.com/reel/...`).
2. **Extract Repo Name via `watch` Skill (`yt-dlp` + `ffmpeg` + Whisper/Captions)**:
   - Pass any high-signal Reel URL to the `watch` skill (`C:\Users\avich\.gemini\config\skills\watch\SKILL.md`) to extract the spoken transcript and key video frames showing the GitHub repo name or terminal command.
   - Resolve the extracted repository name on GitHub via `gh search repos` or `github-mcp-server`.

---

## 3. NotebookLM Deep Research Channel (`notebooklm` MCP)

When you need Gemini Notebook-grade multi-source synthesis (comparing architectures, evaluating competing open-source stacks, or synthesizing deep documentation):

1. Call `notebook_create(title="Deep Discovery: <Topic>")` via the `notebooklm` MCP server.
2. Call `research_start(notebook_id=..., query="<Topic> open source architecture comparison", source="web", mode="deep")`.
3. Poll `research_status` until completed, call `research_import` to ingest the discovered web sources, and call `chat_ask` to extract the synthesized comparison with source citations.

---

## 4. Stealth Web & Reddit/HN Extraction (`scrapling` MCP)

When Google snippets are truncated or pages block standard fetchers (Cloudflare, Reddit threads, Hacker News discussions, ProductHunt alternatives):
- Use the `scrapling` MCP server (`get`, `fetch`, `stealthy_fetch`) to pull clean Markdown directly from the target page without bot-detection blocks.

---

## Gemini Web Execution Adaptation (`deep-discovery`)

When executing `deep-discovery` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

