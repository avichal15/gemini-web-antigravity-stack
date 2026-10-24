---
name: mythos-media-and-presentations
description: "Mythos 5 Media, Studio Vision & Presentation Pack for Gemini Web: 8-axis forensic visual reverse-prompting (CLI-Anything Google Vids), PPT-Master presentation synthesis, HyperFrames HTML motion graphics, Remotion video walkthroughs, and video analysis."
---

# `mythos-media-and-presentations` — Mythos 5 Gemini Web Domain Skill Pack

This domain skill pack bundles **5 specialized Antigravity skills** plus the executable **Mythos 5 Gemini Web Python Sandbox Runtime** (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, `scripts/mythos_memory_search.py`).

## Bundled Skills in `mythos-media-and-presentations`

- **`cli-anything-google-vids`** (`skills-modules/cli-anything-google-vids.md`): Generate AI images for websites and applications using the CLI-Anything Google Vids harness (cli-anything-google-vids) with precision studio prompts and automatic Gemini watermark removal via GargantuaX/gemini-watermark-remover (gwr.mjs). Use whenever generating or replacing AI images in Antigravity.
- **`hyperframes`** (`skills-modules/hyperframes.md`): Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a promo, explainer, captioned clip, title card, overlay, slideshow or interactive deck, Remotion port, or any HyperFrames HTML composition. Also use it to inspect, diagnose, validate, preview, publish, or batch-render an existing HyperFrames project. Inputs may be a website URL, GitHub PR, Figma design 
- **`ppt-master`** (`skills-modules/ppt-master.md`): AI-driven presentation workflow for generating editable PPTX decks and slides, reconstructing page visuals, creating reusable Brand/Style/Layout/Deck workspaces, filling native PPTX templates, and enhancing finished PPTX files. Use when the user asks to create, generate, reconstruct, regenerate, beautify, redesign, template, fill, or enhance a presentation, PPT, PPTX, slide deck, or courseware — including adding narration or animation to one — re
- **`remotion`** (`skills-modules/remotion.md`): Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays
- **`watch`** (`skills-modules/watch.md`): Watch a video (URL or local path). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, pulls the transcript from captions (or Whisper API fallback), and hands the result to Claude so it can answer questions about what's in the video.

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
