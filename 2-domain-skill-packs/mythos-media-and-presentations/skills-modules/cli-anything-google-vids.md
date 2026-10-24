# Skill Module: `cli-anything-google-vids`

- **Domain Pack**: `mythos-media-and-presentations`
- **Description**: Generate AI images for websites and applications using the CLI-Anything Google Vids harness (cli-anything-google-vids) with precision studio prompts and automatic Gemini watermark removal via GargantuaX/gemini-watermark-remover (gwr.mjs). Use whenever generating or replacing AI images in Antigravity.

# Google Vids + Gemini Watermark Remover AI Image Generation Skill

Use `cli-anything-google-vids` whenever generating AI images in Antigravity. This workflow pairs **HKUDS/CLI-Anything** (`https://docs.google.com/videos/u/0/` harness) with **GargantuaX/gemini-watermark-remover** (`gwr.mjs`) so every generated image uses a precision-engineered studio prompt and has its Gemini watermark mathematically removed via Reverse Alpha Blending.

## Prerequisites & Locations
- **CLI Binary**: `cli-anything-google-vids` (or `python -m cli_anything.google_vids`)
- **Harness Source**: `c:\masterplayer designs and printing\tools\CLI-Anything\google-vids\agent-harness`
- **Watermark Remover CLI**: `c:\masterplayer designs and printing\tools\gemini-watermark-remover\bin\gwr.mjs`

## 1. Forensic Reference Image Recreation (MANDATORY when a reference image exists)

Whenever replacing, upgrading, or recreating an existing product or reference image, **NEVER guess the prompt from the product title alone**. Execute this mandatory 3-step loop:

### Step A — Inspect Reference & Extract Forensic 8-Axis Prompt
1. Call `read_file` on the reference image so your own multimodal vision inspects the actual pixels.
2. Run `prompt from-image` (or pass `--reference-image` / `-r` directly to `pipeline run`) to extract the **Forensic 8-Axis Visual Specification** (`subject_and_pose`, `camera_and_framing`, `color_palette_hex`, `material_and_texture`, `printed_graphic_design`, `environment_and_props`, `lighting_and_shadows`, `negative_constraints`) via OmniRoute Vision (`agy/gemini-3.8-flash-high` / `agy/claude-sonnet-4-6`) with Gemini REST fallback:

```bash
cli-anything-google-vids --json prompt from-image "path/to/reference-image.png" \
  --title "Custom Printed Hoodie"
```

### Step B — Generate + Strip Watermark with `--reference-image` (`-r`)
```bash
cli-anything-google-vids --json pipeline run \
  --title "Custom Printed Hoodie" \
  --reference-image "path/to/reference-image.png" \
  -o "public/mp-assets/hoodie-1.webp" \
  --width 1024 --height 1024
```

### Step C — Side-by-Side Visual Verification Gate
Before claiming completion, call `read_file` on **both** the original reference image and the newly generated output image. Verify that camera angle, base hex color, garment fold/display pose, printed graphic placement, and background match the reference without hallucinated props. If any axis drifted, refine `--prompt` and regenerate.

---

## 2. End-to-End Single Image Generation (No Reference Image)

Generates a high-resolution studio image using a precision prompt, strips the Gemini watermark via `gwr.mjs remove --overwrite --json`, and converts/resizes to the target `.webp` / `.png` / `.jpg` dimensions:

```bash
cli-anything-google-vids --json pipeline run \
  --title "Custom Printed Cotton Streetwear T-Shirts" \
  --category apparel \
  -o "public/mp-assets/hero-banner-1.webp" \
  --width 1600 --height 650
```

Supported `--category` presets:
- `apparel` (T-shirts, polos, jerseys, activewear)
- `hoodies` (hoodies, sweatshirts, fleece jackets)
- `headwear` (snapback caps, trucker hats, beanies)
- `drinkware` (ceramic mugs, thermal sippers, bottles)
- `bags` (canvas totes, backpacks, drawstring bags)
- `stationery` (executive diaries, pens, lanyards, keychains)
- `awards` (optical crystal trophies, wooden plaques)
- `tech` (custom phone cases, gaming mousepads, accessories)
- `hero_banner` (16:9 widescreen hero campaign compositions)
- `review` (authentic customer unboxing/lifestyle product shots)

## 2. Preview or Customize Precision Prompts

```bash
cli-anything-google-vids --json prompt build \
  --title "Custom Embroidered Snapback Caps" \
  --category headwear \
  --brand "Masterplayer Designs and Printing" \
  --accent "#f6861f" \
  --aspect-ratio "1:1"
```

## 3. Standalone Gemini Watermark Removal (`gwr.mjs`)

To remove the Gemini watermark (`48x48` or `96x96` star mark) from any existing image file:

```bash
cli-anything-google-vids --json watermark remove \
  "path/to/watermarked-input.png" \
  -o "path/to/clean-output.png" \
  --overwrite
```

Or invoke `gwr.mjs` directly:
```bash
node "c:/masterplayer designs and printing/tools/gemini-watermark-remover/bin/gwr.mjs" remove "input.png" --output "output.png" --overwrite --json
```

## 4. Batch Generation for Storefront Catalogs

```bash
# 1. Audit catalogData.json and build a precision prompt manifest
cli-anything-google-vids --json prompt audit src/data/catalogData.json -o scratch/catalog-prompts.json

# 2. Run batch generation + watermark removal
cli-anything-google-vids --json image batch --manifest scratch/catalog-prompts.json --limit 10 --offset 0
```

## 5. Google Vids Browser Authentication (`docs.google.com/videos/u/0/`)

When authenticating or refreshing the persistent Chrome session (`~/.cli-anything-google-vids/chrome-profile` with `AutomationControlled` disabled so Google Sign-In never blocks login):

```bash
cli-anything-google-vids auth login
cli-anything-google-vids --json auth status
```

---

## Gemini Web Execution Adaptation (`cli-anything-google-vids`)

When executing `cli-anything-google-vids` inside **Gemini Web (`gemini.google.com`)**, map desktop Antigravity operations to their Gemini Web equivalents:

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

