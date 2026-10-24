# Mythos 5 — Antigravity Desktop Architecture Mirror & Gemini Web Adaptation Reference

This file preserves the exact production source of the desktop Antigravity 2.0 hooks, semantic memory engine, and global configuration alongside their Gemini Web Python Sandbox equivalents (`scripts/mythos_web_runtime.py`, `scripts/godmode_web_engine.py`, and `scripts/mythos_memory_search.py`).

## 1. Desktop vs. Gemini Web Runtime Mapping

| Architectural Layer | Antigravity 2.0 Desktop Implementation | Gemini Web (`gemini.google.com`) Implementation |
| :--- | :--- | :--- |
| **Core Identity & Rules** | `C:\Users\avich\.gemini\config\AGENTS.md` | `SKILL.md` (`mythos-antigravity-stack` / `mythos-apex-core`) |
| **PreToolUse Guardrail** | `pre-tool-rtk.mjs` + `antibodies.json` + `rtk.exe` | `python scripts/mythos_web_runtime.py pre-check` + `memory/antibodies_catalog.csv` |
| **PostToolUse Verifier** | `post-edit-lint.mjs` (`ruff` + `pyright` + `oxlint` + `episodes.jsonl`) | `python scripts/mythos_web_runtime.py post-verify` (`ast.parse` + `py_compile` + Secret Scrubber + `memory/episodes_catalog.csv`) |
| **Stop Gate & Circuit Breaker** | `stop-hook.mjs` + `gate-check.mjs` (`GATES.md`) | `python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve` |
| **Multi-Model Council & Challenge** | `godmode_server.js` (`OmniRoute` + `FreeLLMAPI`) | `python scripts/godmode_web_engine.py council` & `challenge` + `autotune` + `parseltongue` |
| **Semantic Memory & 818 Playbooks** | `gemma_memory.py` (`google/embeddinggemma-2` CUDA `bfloat16`) | `python scripts/mythos_memory_search.py` (Okapi BM25 + Subword Cosine over bundled CSVs) |

---

## 2. Original Desktop `hooks.json`

````json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"C:\\Program Files\\nodejs\\node.exe\" \"C:\\Users\\avich\\.gemini\\config\\hooks\\pre-tool-rtk.mjs\"",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"C:\\Program Files\\nodejs\\node.exe\" \"C:\\Users\\avich\\.gemini\\config\\hooks\\post-edit-lint.mjs\"",
            "timeout": 8
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"C:\\Program Files\\nodejs\\node.exe\" \"C:\\Users\\avich\\.gemini\\config\\skills\\unlazy\\scripts\\stop-hook.mjs\" --unlazy-hook-v2",
            "timeout": 20
          }
        ]
      }
    ]
  }
}

````

---

## 3. Original Desktop `pre-tool-rtk.mjs`

````javascript
#!/usr/bin/env node
/**
 * Antigravity 2.0 PreToolUse Hook — Active Antibody Guardrail + FreeLLMAPI On-Demand Wake + RTK Token Killer
 * 1. Intercepts known mistake patterns via C:/Users/avich/.gemini/config/memory/antibodies.json (block / rewrite / warn).
 * 2. Wakes FreeLLMAPI (port 3001) on-demand via WMI when referenced.
 * 3. Rewrites standalone dev CLI commands (git, pytest, vitest, cargo) through rtk.exe for 60-90% token savings.
 */
import { readFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";

const RTK_BIN = "C:\\Users\\avich\\.local\\bin\\rtk.exe";
const ANTIBODIES_PATH = "C:\\Users\\avich\\.gemini\\config\\memory\\antibodies.json";
const ENSURE_FREELLMAPI = "c:\\Users\\avich\\Downloads\\mythos\\freellmapi\\ensure-freellmapi.js";

let payload = {};
try {
  payload = JSON.parse(readFileSync(0, "utf8") || "{}");
} catch {
  process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
  process.exit(0);
}

const toolName = String(payload.tool_name || payload.toolName || "");
const toolInput = payload.tool_input || payload.toolInput || {};
let cmd = String(toolInput.CommandLine || toolInput.command || "").trim();
const serializedInput = JSON.stringify(toolInput);

// 1. Lazy on-demand auto-start for FreeLLMAPI (port 3001)
if ((/3001|freellmapi/i.test(serializedInput) || /godmode/i.test(toolName)) && existsSync(ENSURE_FREELLMAPI)) {
  try {
    execFileSync(process.execPath, [ENSURE_FREELLMAPI], { timeout: 6500, stdio: "ignore", windowsHide: true });
  } catch {
    // Non-blocking fallback
  }
}

// 2. Active Antibody Guardrail (Zero Repeat Mistakes)
let antibodyWarnings = [];
let rewrittenByAntibody = false;

if (existsSync(ANTIBODIES_PATH)) {
  try {
    const abData = JSON.parse(readFileSync(ANTIBODIES_PATH, "utf8"));
    const antibodies = Array.isArray(abData.antibodies) ? abData.antibodies : [];
    const targetText =
      toolName === "run_command" || toolName === "Bash"
        ? cmd
        : String(toolInput.Content || toolInput.Replacement || serializedInput);

    for (const ab of antibodies) {
      const toolPattern = new RegExp(`^(${ab.tool})$`, "i");
      if (!toolPattern.test(toolName)) continue;
      if (ab.must_not_contain && targetText.includes(ab.must_not_contain)) continue;

      const rx = new RegExp(ab.match_regex, "im");
      if (!rx.test(targetText)) continue;

      if (ab.action === "block") {
        process.stdout.write(
          JSON.stringify({
            decision: "block",
            reason: `[ANTIBODY BLOCK ${ab.id}: ${ab.name}] ${ab.symptom} | Root cause: ${ab.root_cause} | Prevention: ${ab.prevention}`,
          }) + "\n"
        );
        process.exit(0);
      } else if (ab.action === "rewrite" && (toolName === "run_command" || toolName === "Bash")) {
        if (ab.rewrite_type === "prepend_stdin_json") {
          cmd = `'{"cwd":"c:\\\\Users\\\\avich\\\\Downloads\\\\mythos","terminationReason":"COMPLETED"}' | ${cmd}`;
          rewrittenByAntibody = true;
          antibodyWarnings.push(`[ANTIBODY AUTO-REWRITE ${ab.id}] Piped JSON stdin into stop-hook.mjs to prevent fd-0 hang.`);
        } else if (ab.rewrite_type === "prepend_powershell_call_operator") {
          cmd = cmd.replace(/^(\s*)("[A-Za-z]:\\[^"]+\.exe"\s+)/gm, "$1& $2");
          rewrittenByAntibody = true;
          antibodyWarnings.push(`[ANTIBODY AUTO-REWRITE ${ab.id}] Prepended '& ' call operator to quoted .exe path in PowerShell.`);
        }
      } else if (ab.action === "warn") {
        antibodyWarnings.push(`[ANTIBODY WARNING ${ab.id}: ${ab.name}] ${ab.prevention}`);
      }
    }
  } catch {
    // Non-blocking if antibodies.json is mid-write
  }
}

// 3. RTK (Rust Token Killer) rewrite for single-statement dev CLI commands
if (
  !rewrittenByAntibody &&
  (toolName === "run_command" || toolName === "Bash") &&
  cmd &&
  existsSync(RTK_BIN) &&
  !/[;|&\r\n`$]/.test(cmd) &&
  /^(git\s+(status|diff|log|branch)|pytest\b|vitest\b|cargo\s+(test|check|clippy))\b/.test(cmd)
) {
  try {
    const rtkCmd = execFileSync(RTK_BIN, ["rewrite", cmd], {
      encoding: "utf8",
      timeout: 1500,
    }).trim();
    if (rtkCmd && rtkCmd !== cmd) {
      cmd = rtkCmd;
      rewrittenByAntibody = true;
    }
  } catch {
    // Fall through
  }
}

if (rewrittenByAntibody) {
  const updatedKey = "CommandLine" in toolInput ? "CommandLine" : "command";
  const out = {
    decision: "allow",
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      updatedInput: {
        ...toolInput,
        [updatedKey]: cmd,
      },
    },
  };
  if (antibodyWarnings.length > 0) {
    out.systemMessage = antibodyWarnings.join("\n");
  }
  process.stdout.write(JSON.stringify(out) + "\n");
  process.exit(0);
}

if (antibodyWarnings.length > 0) {
  process.stdout.write(
    JSON.stringify({
      decision: "allow",
      systemMessage: antibodyWarnings.join("\n"),
    }) + "\n"
  );
  process.exit(0);
}

process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
process.exit(0);

````

---

## 4. Original Desktop `post-edit-lint.mjs`

````javascript
#!/usr/bin/env node
/**
 * Antigravity 2.0 PostToolUse Static Analysis & Episodic Reflexion Hook (ruff + pyright + oxlint)
 * 1. Runs fast deterministic linter + type-checker diagnostics whenever a Python or JS/TS file is written or edited.
 * 2. Catches hallucinated imports, undefined symbols, wrong argument counts, and syntax errors on the spot.
 * 3. Automatically appends detected defects into C:/Users/avich/.gemini/config/memory/episodes.jsonl for continual learning.
 */
import { readFileSync, appendFileSync, existsSync } from "node:fs";
import { extname } from "node:path";
import { spawnSync } from "node:child_process";

const RUFF_BIN = "C:\\Users\\avich\\.local\\bin\\ruff.exe";
const PYRIGHT_BIN = "C:\\Users\\avich\\.local\\bin\\pyright.exe";
const OXLINT_CMD = process.platform === "win32" ? "C:\\Users\\avich\\AppData\\Roaming\\npm\\oxlint.cmd" : "oxlint";
const EPISODES_PATH = "C:\\Users\\avich\\.gemini\\config\\memory\\episodes.jsonl";

let payload = {};
try {
  payload = JSON.parse(readFileSync(0, "utf8") || "{}");
} catch {
  process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
  process.exit(0);
}

const toolName = String(payload.tool_name || payload.toolName || "");
const toolInput = payload.tool_input || payload.toolInput || {};
const filePath = String(
  toolInput.Path ||
  toolInput.file_path ||
  toolInput.TargetFile ||
  toolInput.relative_path ||
  ""
).trim();

const EDIT_TOOLS = new Set([
  "write_file",
  "edit_file",
  "replace_file_content",
  "multi_replace_file_content",
  "Write",
  "Edit",
  "MultiEdit",
  "mcp_serena_replace_symbol_body",
  "mcp_serena_insert_after_symbol",
  "mcp_serena_insert_before_symbol",
]);

if (!filePath || (!EDIT_TOOLS.has(toolName) && !toolName.includes("replace") && !toolName.includes("write") && !toolName.includes("edit"))) {
  process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
  process.exit(0);
}

if (!existsSync(filePath)) {
  process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
  process.exit(0);
}

const ext = extname(filePath).toLowerCase();
const findings = [];

try {
  if (ext === ".py" || ext === ".pyi") {
    if (existsSync(RUFF_BIN)) {
      const res = spawnSync(
        RUFF_BIN,
        ["check", "--output-format=concise", "--select=E,F", filePath],
        { encoding: "utf8", timeout: 3500 }
      );
      if (res.status !== 0 && (res.stdout || res.stderr)) {
        findings.push(`ruff:\n${(res.stdout || res.stderr).trim().slice(0, 600)}`);
      }
    }
    if (existsSync(PYRIGHT_BIN)) {
      const pyRes = spawnSync(
        PYRIGHT_BIN,
        ["--outputjson", filePath],
        { encoding: "utf8", timeout: 4000 }
      );
      if (pyRes.stdout) {
        try {
          const parsed = JSON.parse(pyRes.stdout);
          const IGNORE_RULES = new Set([
            "reportMissingImports",
            "reportMissingModuleSource",
          ]);
          const realErrors = (parsed.generalDiagnostics || []).filter(
            (d) => d.severity === "error" && !IGNORE_RULES.has(d.rule)
          );
          if (realErrors.length > 0) {
            const formatted = realErrors
              .slice(0, 5)
              .map((d) => `L${(d.range?.start?.line ?? 0) + 1}: [${d.rule || "type-error"}] ${d.message}`)
              .join("\n");
            findings.push(`pyright:\n${formatted}`);
          }
        } catch {
          // Ignore malformed JSON
        }
      }
    }
  } else if ([".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"].includes(ext) && existsSync(OXLINT_CMD)) {
    const res = spawnSync(
      OXLINT_CMD,
      ["--quiet", filePath],
      { encoding: "utf8", timeout: 3500, shell: true }
    );
    if (res.status !== 0 && (res.stdout || res.stderr)) {
      findings.push(`oxlint:\n${(res.stdout || res.stderr).trim().slice(0, 600)}`);
    }
  }
} catch {
  // Never block tool completion if linter fails to spawn
}

if (findings.length > 0) {
  const diagOutput = findings.join("\n\n");
  try {
    const episode = {
      id: `EP-AUTO-${Date.now()}`,
      timestamp: new Date().toISOString(),
      workspace: payload.cwd || "unknown",
      category: "post-edit-static-analysis",
      file: filePath,
      symptom: diagOutput.slice(0, 400),
      root_cause: "Static analysis / compiler type-check failure immediately following file edit",
      fix: "Inspect reported line numbers and symbol signatures before proceeding",
    };
    appendFileSync(EPISODES_PATH, JSON.stringify(episode) + "\n", "utf8");
  } catch {
    // Non-blocking
  }

  process.stdout.write(
    JSON.stringify({
      decision: "allow",
      systemMessage: `[PostToolUse Compiler/Linter Alert on ${filePath}]\n${diagOutput}`,
    }) + "\n"
  );
} else {
  process.stdout.write(JSON.stringify({ decision: "allow" }) + "\n");
}
process.exit(0);

````

---

## 5. Original Desktop `stop-hook.mjs`

````javascript
#!/usr/bin/env node
// Claude Code & Antigravity 2.0 Stop hook for one unlazy pipeline. Zero dependencies. Node 16+.

import { readFileSync, unlinkSync } from "node:fs";
import { resolve } from "node:path";
import {
  UNLAZY_DIR, gateState, hookStatePath, parseGates, qualify, readStableRegularFile,
  resolveTarget, sha256, validateScopeId, withFileLock, writeAtomic,
} from "./lib/gates.mjs";
import { dispatchStatus } from "./lib/dispatch.mjs";

const MAX_BLOCKS = 6;
const MAX_GATE_LEDGER_BYTES = 8 * 1024 * 1024;
const MAX_HOOK_STATE_BYTES = 1024 * 1024;
const safeHostText = (value, max = 500) => String(value)
  .replace(/[\u0000-\u001f\u007f-\u009f\u061c\u200e\u200f\u2028-\u202e\u2066-\u2069]/g, " ")
  .replace(/\s+/g, " ")
  .trim()
  .slice(0, max);

function normalizeHookState(value) {
  if (!value || typeof value !== "object" || Array.isArray(value) || value.schema !== 1 ||
      !value.sessions || typeof value.sessions !== "object" || Array.isArray(value.sessions)) {
    return { schema: 1, sessions: {} };
  }
  const sessions = {};
  for (const [key, current] of Object.entries(value.sessions)) {
    if (!/^[a-f0-9]{24}$/.test(key) || !current || typeof current !== "object" || Array.isArray(current) ||
        !/^[a-f0-9]{24}$/.test(String(current.hash || "")) ||
        !Number.isInteger(current.blocks) || current.blocks < 0 ||
        typeof current.updatedAt !== "string" || Number.isNaN(Date.parse(current.updatedAt))) continue;
    sessions[key] = current;
  }
  return { schema: 1, sessions };
}

function readHookState(path, root) {
  let text;
  try {
    text = readStableRegularFile(path, {
      root, maxBytes: MAX_HOOK_STATE_BYTES, label: "hook state",
    });
  } catch (error) {
    if (error && error.code === "ENOENT") {
      return { missing: true, state: { schema: 1, sessions: {} } };
    }
    throw error;
  }
  try { return { missing: false, state: normalizeHookState(JSON.parse(text)) }; }
  catch { return { missing: false, state: { schema: 1, sessions: {} } }; }
}

const args = process.argv.slice(2);
const scopeIndex = args.indexOf("--scope");
const scopeArg = scopeIndex === -1 ? null : args[scopeIndex + 1];

let payload = {};
let payloadParseFailed = false;
try { payload = JSON.parse(readFileSync(0, "utf8") || "{}"); }
catch { payloadParseFailed = true; }

const isAntigravity = Array.isArray(payload.workspacePaths) ||
  typeof payload.conversationId === "string" ||
  typeof payload.terminationReason === "string";

const allow = (message) => {
  if (isAntigravity) {
    console.log(JSON.stringify(message ? { decision: "allow", systemMessage: message } : { decision: "allow" }));
  } else if (message) {
    console.log(JSON.stringify({ systemMessage: message }));
  }
  process.exit(0);
};

const blockStop = (reason) => {
  console.log(JSON.stringify({
    decision: isAntigravity ? "continue" : "block",
    reason,
  }));
  process.exit(0);
};

if (payloadParseFailed) allow(null);

if (isAntigravity && payload.terminationReason && payload.terminationReason !== "COMPLETED") {
  // Never trap user cancellations (USER_CANCELED) or runtime errors (ERROR) in Antigravity 2.0.
  allow(null);
}

if (scopeIndex !== -1 && (!scopeArg || validateScopeId(scopeArg))) {
  allow("unlazy: installed hook has an invalid --scope value; not blocking.");
}

const rawRoot = (typeof payload.cwd === "string" && payload.cwd)
  ? payload.cwd
  : (Array.isArray(payload.workspacePaths) && typeof payload.workspacePaths[0] === "string" && payload.workspacePaths[0])
    ? payload.workspacePaths[0]
    : process.cwd();
const root = resolve(rawRoot);
const sessionId = payload.conversationId || payload.session_id || payload.sessionId || "anonymous";
const target = resolveTarget({ root, scope: scopeArg, sessionId });

if (target.ambiguous) {
  allow("unlazy: " + target.ambiguous.length + " pipelines under " + UNLAZY_DIR +
    "/ (" + target.ambiguous.join(", ") + ") and none bound to this session; not blocking.");
}
if (target.error && !target.ambiguous) allow("unlazy: " + safeHostText(target.error) + "; not blocking.");

const discoveryErrors = target.discoveryErrors || [];
// An invalid named scope cannot safely hold its own hook-state file. Keep its
// bounded loop-guard state at the real repository root and include the target
// identity in the session key so it cannot collide with another scope.
const statePath = hookStatePath(root, discoveryErrors.length ? null : target.scope);
const sessionKey = sha256(String(sessionId) + "\0" + String(target.scope || "unscoped")).slice(0, 24);

async function clearSessionState() {
  try { if (readHookState(statePath, root).missing) return; }
  catch { return; }
  try {
    await withFileLock(root, statePath, () => {
      const loaded = readHookState(statePath, root);
      if (loaded.missing) return;
      const state = loaded.state;
      delete state.sessions[sessionKey];
      if (!Object.keys(state.sessions).length) {
        try { unlinkSync(statePath); } catch { /* already absent */ }
      } else writeAtomic(statePath, JSON.stringify(state, null, 2) + "\n", { root });
    }, { timeoutMs: 10000 });
  } catch {
    // State cleanup must never trap a session after the gates are complete.
  }
}

// Do not even open dispatch state through a scope path already proven unsafe.
const dispatch = discoveryErrors.length
  ? { blocking: [], abandoned: [], resolved: [] }
  : dispatchStatus(root, target.scope);

if (!target.files.length && !discoveryErrors.length && !dispatch.blocking.length && !dispatch.abandoned.length) {
  await clearSessionState();
  allow(null);
}

const unmet = [...dispatch.blocking];
const invalid = discoveryErrors.map((error) => "discovery:PARSE " + safeHostText(error));
const handoffs = [...dispatch.abandoned];
const handoffMessage = () => {
  if (!handoffs.length) return "";
  const shown = handoffs.slice(0, 5).join(", ") +
    (handoffs.length > 5 ? ", +" + (handoffs.length - 5) + " more" : "");
  return " HANDOFF REQUIRED: " + handoffs.length + " abandoned item(s): " + safeHostText(shown) + ".";
};
// The loop guard compares resolved gate state between stops, not raw bytes.
// Byte comparison counted any edit as progress: a comment, a reflowed line, or
// the checker rewriting an evidence line with a fresh PATH hash. That rearmed
// the guard indefinitely, so the six-block release could only ever fire for an
// agent doing literally nothing, which is the one case least in need of it.
// Dispatch issue strings encode only canonical state and counts, not raw JSON
// bytes or timestamps, so metadata-only edits do not reset the same guard.
const resolved = [...dispatch.resolved];
if (discoveryErrors.length) resolved.push("discovery:PARSE=invalid");
for (const file of [...target.files].sort()) {
  let text;
  try {
    text = readStableRegularFile(file, {
      root, maxBytes: MAX_GATE_LEDGER_BYTES, label: "gate ledger",
    });
  }
  catch (error) {
    invalid.push(qualify(file, "PARSE") + " unreadable: " + safeHostText(error.message));
    resolved.push(qualify(file, "PARSE") + "=unreadable");
    continue;
  }
  const doc = parseGates(text);
  if (doc.errors.length) {
    invalid.push(qualify(file, "PARSE") + " " + doc.errors.slice(0, 2).map((error) => safeHostText(error)).join("; "));
    // Record only that the ledger is invalid. Diagnostic text carries line
    // numbers, which shift on an unrelated edit and would restore byte coupling.
    resolved.push(qualify(file, "PARSE") + "=invalid");
    continue;
  }
  for (const gate of doc.gates) {
    const state = gateState(gate, doc.abandoned);
    resolved.push(qualify(file, gate.id) + "=" + state);
    if (state === "abandoned") handoffs.push(qualify(file, gate.id));
    else if (state !== "met") unmet.push(qualify(file, gate.id));
  }
}

if (!unmet.length && !invalid.length) {
  await clearSessionState();
  if (!handoffs.length) allow(null);
  const where = target.scope ? " [scope " + target.scope + "]" : "";
  allow("unlazy" + where + ":" + handoffMessage());
}

const progressHash = sha256(resolved.sort().join("\0")).slice(0, 24);
let sessionState;
try {
  sessionState = await withFileLock(root, statePath, () => {
    const state = readHookState(statePath, root).state;
    let current = state.sessions[sessionKey];
    if (!current || current.hash !== progressHash) current = { hash: progressHash, blocks: 0 };
    current.blocks += 1;
    current.updatedAt = new Date().toISOString();
    state.sessions[sessionKey] = current;
    // Bound abandoned session debris without mixing counters between sessions.
    const entries = Object.entries(state.sessions).sort((a, b) => String(b[1].updatedAt).localeCompare(String(a[1].updatedAt)));
    state.sessions = Object.fromEntries(entries.slice(0, 64));
    writeAtomic(statePath, JSON.stringify(state, null, 2) + "\n", { root });
    return current;
  }, { timeoutMs: 10000 });
} catch (error) {
  if (discoveryErrors.length) {
    blockStop(
      "unlazy: invalid named scope input must be repaired before Stop: " +
        safeHostText(discoveryErrors[0])
    );
  }
  allow("unlazy: could not update the serialized hook state (" + safeHostText(error.message) + "); not blocking to avoid a trap.");
}

const where = target.scope ? " [scope " + target.scope + "]" : "";
const outstanding = [...invalid, ...unmet].map((item) => safeHostText(item));
if (sessionState.blocks > MAX_BLOCKS) {
  allow("unlazy: releasing after " + MAX_BLOCKS + " blocks without gate progress" + where +
    "; " + outstanding.length + " item(s) remain (" + outstanding.slice(0, 4).join(", ") + ")." +
    handoffMessage());
}

const list = outstanding.slice(0, 5).join(", ") + (outstanding.length > 5 ? ", +" + (outstanding.length - 5) + " more" : "");
blockStop(
  "unlazy" + where + ": " + outstanding.length + " gate/ledger/dispatch item(s) need work: " + list +
    ". Run gate-check.mjs --status to inspect without execution. To run inherited CHECK lines, inspect them and use --approve. " +
    "Use ABANDON: <id> <non-blank reason> only when a gate is genuinely impossible." + handoffMessage()
);

````

---

## 6. Original Desktop `gemma_memory.py` (`google/embeddinggemma-2`)

````python
#!/usr/bin/env python3
"""
Gemma 2 Multimodal & Code Semantic Memory + Reflexion Engine for Antigravity 2.0
Powered by google/embeddinggemma-2 (Gemma 4 architecture, 8K context, Matryoshka MRL 256d/768d).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import struct
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore")

MODEL_ID = "google/embeddinggemma-2"
MEMORY_DIR = Path(r"C:\Users\avich\.gemini\config\memory")
DB_PATH = MEMORY_DIR / "semantic_index.db"
ANTIBODIES_PATH = MEMORY_DIR / "antibodies.json"
EPISODES_PATH = MEMORY_DIR / "episodes.jsonl"
AGENTMEMORY_PATH = Path(r"C:\Users\avich\.agentmemory\standalone.json")
SKILL_ROOTS = [
    Path(r"C:\Users\avich\.gemini\config\skills"),
    Path(r"C:\Users\avich\.gemini\config\plugins"),
    Path(r"C:\Users\avich\.gemini\antigravity\builtin\skills"),
    Path(r"c:\Users\avich\Downloads\mythos\.agents\skills"),
]
CYBER_INDEX_PATH = Path(r"C:\Users\avich\.gemini\config\skill-libraries\Anthropic-Cybersecurity-Skills\index.json")

TASK_PREFIXES: dict[str, str] = {
    "SearchQuery": "task: search result | query: ",
    "CodeRetrieval": "task: code retrieval | query: ",
    "FactChecking": "task: fact checking | query: ",
    "Classification": "task: classification | query: ",
    "Clustering": "task: clustering | query: ",
    "SentenceSimilarity": "task: sentence similarity | query: ",
}


def pack_vector(vec: list[float]) -> bytes:
    return struct.pack(f"<{len(vec)}f", *vec)


def unpack_vector(blob: bytes) -> list[float]:
    count = len(blob) // 4
    return list(struct.unpack(f"<{count}f", blob))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            item_id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            dim INTEGER NOT NULL,
            embedding BLOB NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_source ON items(source)")
    conn.commit()


def load_sentence_transformer(enable_vision: bool = False) -> Any:
    import torch
    import transformers
    from sentence_transformers import SentenceTransformer

    transformers.logging.set_verbosity_error()

    # CRITICAL (AB-005): Never use float16 with google/embeddinggemma-2 (activation range exceeds fp16).
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        dtype = torch.bfloat16
        device = "cuda"
    else:
        dtype = torch.float32
        device = "cuda" if torch.cuda.is_available() else "cpu"

    config_kwargs: dict[str, Any] = {"audio_config": None}
    if not enable_vision:
        config_kwargs["vision_config"] = None

    for local_only in (True, False):
        try:
            return SentenceTransformer(
                MODEL_ID,
                device=device,
                model_kwargs={"torch_dtype": dtype},
                config_kwargs=config_kwargs,
                trust_remote_code=True,
                local_files_only=local_only,
            )
        except Exception:
            if not local_only:
                raise
    raise RuntimeError(f"Failed to load {MODEL_ID}")


def collect_corpus() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    # 1. Antibodies
    if ANTIBODIES_PATH.exists():
        try:
            data = json.loads(ANTIBODIES_PATH.read_text(encoding="utf-8"))
            for ab in data.get("antibodies", []):
                ab_id = f"antibody:{ab['id']}"
                title = f"Antibody {ab['id']} ({ab.get('name', '')})"
                content = (
                    f"Symptom: {ab.get('symptom', '')}\n"
                    f"Root Cause: {ab.get('root_cause', '')}\n"
                    f"Prevention: {ab.get('prevention', '')}\n"
                    f"Tool: {ab.get('tool', '')} | Action: {ab.get('action', '')}"
                )
                records.append(
                    {
                        "item_id": ab_id,
                        "source": "antibody",
                        "title": title,
                        "content": content,
                        "metadata": ab,
                    }
                )
        except Exception:
            pass

    # 2. Episodic Mistake Logs
    if EPISODES_PATH.exists():
        try:
            for line in EPISODES_PATH.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                ep = json.loads(line)
                ep_id = f"episode:{ep.get('id', sha256_text(line)[:10])}"
                title = f"Episode {ep.get('id', '')} [{ep.get('category', 'general')}]"
                content = (
                    f"Symptom: {ep.get('symptom', '')}\n"
                    f"Root Cause: {ep.get('root_cause', '')}\n"
                    f"Fix: {ep.get('fix', '')}\n"
                    f"Workspace: {ep.get('workspace', '')}"
                )
                records.append(
                    {
                        "item_id": ep_id,
                        "source": "episode",
                        "title": title,
                        "content": content,
                        "metadata": ep,
                    }
                )
        except Exception:
            pass

    # 3. AgentMemory (standalone.json)
    if AGENTMEMORY_PATH.exists():
        try:
            am_data = json.loads(AGENTMEMORY_PATH.read_text(encoding="utf-8"))
            memories = (
                am_data.get("mem:memories")
                or am_data.get("memories")
                or (am_data if isinstance(am_data, list) else [])
            )
            if isinstance(memories, dict):
                memories = list(memories.values())
            for mem in memories:
                if not isinstance(mem, dict):
                    continue
                if mem.get("isLatest") is False:
                    continue
                m_id = str(mem.get("id") or sha256_text(json.dumps(mem))[:12])
                concepts = mem.get("concepts", "")
                if isinstance(concepts, list):
                    concepts = ", ".join(str(x) for x in concepts)
                m_title = str(mem.get("title") or "").strip()
                title = (
                    f"Memory {m_id}: {m_title} ({mem.get('type', 'fact')})"
                    if m_title
                    else f"Memory {m_id} ({mem.get('type', 'fact')}: {concepts})"
                )
                content = str(mem.get("content", ""))
                if not content:
                    continue
                records.append(
                    {
                        "item_id": f"memory:{m_id}",
                        "source": "memory",
                        "title": title,
                        "content": f"Concepts: {concepts}\n{content[:3000]}",
                        "metadata": {
                            "id": m_id,
                            "title": m_title,
                            "type": mem.get("type", ""),
                            "concepts": concepts,
                            "files": mem.get("files", ""),
                        },
                    }
                )
        except Exception:
            pass

    # 4. Global, Plugin, Builtin & Workspace Skills
    seen_skills: set[str] = set()
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for skill_md in sorted(root.rglob("SKILL.md")):
            try:
                raw = skill_md.read_text(encoding="utf-8", errors="replace")
                skill_name = skill_md.parent.name
                if skill_name == "skills" and skill_md.parent.parent:
                    skill_name = skill_md.parent.parent.name
                if skill_name in seen_skills:
                    continue
                seen_skills.add(skill_name)
                records.append(
                    {
                        "item_id": f"skill:{skill_name}",
                        "source": "skill",
                        "title": f"Skill: {skill_name}",
                        "content": raw[:2500],
                        "metadata": {"name": skill_name, "path": str(skill_md)},
                    }
                )
            except Exception:
                pass

    # 5. Cybersecurity 818-Playbook Index
    if CYBER_INDEX_PATH.exists():
        try:
            c_data = json.loads(CYBER_INDEX_PATH.read_text(encoding="utf-8"))
            c_skills = c_data.get("skills", c_data if isinstance(c_data, list) else [])
            for cs in c_skills:
                if not isinstance(cs, dict):
                    continue
                slug = str(cs.get("name") or cs.get("id") or cs.get("slug") or "")
                if not slug:
                    continue
                desc = str(cs.get("description", ""))
                tags = ", ".join(str(t) for t in cs.get("tags", []))
                records.append(
                    {
                        "item_id": f"cyber:{slug}",
                        "source": "cyber",
                        "title": f"Cyber Playbook: {slug}",
                        "content": f"{desc}\nTags: {tags}",
                        "metadata": {
                            "name": slug,
                            "path": cs.get("path", f"skills/{slug}/SKILL.md"),
                        },
                    }
                )
        except Exception:
            pass

    return records


def cmd_sync(args: argparse.Namespace) -> int:
    t0 = time.time()
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    existing: dict[str, tuple[str, int]] = {}
    for row in conn.execute("SELECT item_id, content_hash, dim FROM items"):
        existing[row[0]] = (row[1], int(row[2]))

    corpus = collect_corpus()
    to_encode: list[dict[str, Any]] = []
    for item in corpus:
        formatted_doc = f"title: {item['title']} | text: {item['content']}"
        c_hash = sha256_text(formatted_doc)
        item["formatted_doc"] = formatted_doc
        item["content_hash"] = c_hash
        prev = existing.get(item["item_id"])
        if prev is None or prev[0] != c_hash or prev[1] != args.dim:
            to_encode.append(item)

    if to_encode:
        model = load_sentence_transformer(enable_vision=False)
        texts = [x["formatted_doc"] for x in to_encode]
        embeddings = model.encode(
            texts,
            batch_size=args.batch_size,
            truncate_dim=args.dim,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        now_iso = datetime.now(timezone.utc).isoformat()
        rows_to_upsert = []
        for item, emb in zip(to_encode, embeddings):
            vec_list = emb.tolist()
            rows_to_upsert.append(
                (
                    item["item_id"],
                    item["source"],
                    item["title"],
                    item["content"],
                    json.dumps(item["metadata"], ensure_ascii=False),
                    item["content_hash"],
                    args.dim,
                    pack_vector(vec_list),
                    now_iso,
                )
            )
        conn.executemany(
            """
            INSERT OR REPLACE INTO items
            (item_id, source, title, content, metadata_json, content_hash, dim, embedding, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows_to_upsert,
        )
        conn.commit()

    total_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    by_source = dict(conn.execute("SELECT source, COUNT(*) FROM items GROUP BY source").fetchall())
    conn.close()

    result = {
        "status": "ok",
        "model": MODEL_ID,
        "dim": args.dim,
        "newly_encoded": len(to_encode),
        "total_indexed": total_count,
        "by_source": by_source,
        "elapsed_sec": round(time.time() - t0, 2),
    }
    print(json.dumps(result, indent=2))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    import numpy as np

    t0 = time.time()
    if not DB_PATH.exists():
        print(json.dumps({"error": "Database not initialized. Run 'sync' first."}))
        return 1

    conn = sqlite3.connect(str(DB_PATH))
    sql = "SELECT item_id, source, title, content, metadata_json, dim, embedding FROM items"
    params: list[Any] = []
    if args.source and args.source != "all":
        sql += " WHERE source = ?"
        params.append(args.source)

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    if not rows:
        print(json.dumps({"status": "ok", "results": [], "count": 0}))
        return 0

    target_dim = int(rows[0][5])
    prefix = TASK_PREFIXES.get(args.task, TASK_PREFIXES["SearchQuery"])
    formatted_query = f"{prefix}{args.query}"

    model = load_sentence_transformer(enable_vision=False)
    q_emb = model.encode(
        [formatted_query],
        truncate_dim=target_dim,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]
    q_vec = np.asarray(q_emb, dtype=np.float32)

    mat = np.frombuffer(b"".join(r[6] for r in rows), dtype=np.float32).reshape(len(rows), target_dim)
    scores = mat @ q_vec
    top_indices = np.argsort(-scores)[: args.top_k]

    results = []
    for idx in top_indices:
        r = rows[int(idx)]
        results.append(
            {
                "score": round(float(scores[int(idx)]), 4),
                "item_id": r[0],
                "source": r[1],
                "title": r[2],
                "snippet": r[3][:350],
                "metadata": json.loads(r[4]),
            }
        )

    out = {
        "status": "ok",
        "model": MODEL_ID,
        "task": args.task,
        "query": args.query,
        "dim": target_dim,
        "elapsed_sec": round(time.time() - t0, 3),
        "results": results,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def cmd_learn(args: argparse.Namespace) -> int:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Append to episodes.jsonl
    episode = {
        "id": f"EP-{args.id}",
        "timestamp": now_iso,
        "workspace": args.workspace,
        "category": args.category,
        "symptom": args.symptom,
        "root_cause": args.root_cause,
        "fix": args.prevention,
    }
    with EPISODES_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(episode, ensure_ascii=False) + "\n")

    # 2. If regex provided, register active PreToolUse antibody in antibodies.json
    antibody_added = False
    if args.regex:
        ab_doc: dict[str, Any] = {"version": "1.0.0", "antibodies": []}
        if ANTIBODIES_PATH.exists():
            try:
                ab_doc = json.loads(ANTIBODIES_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        antibodies: list[dict[str, Any]] = ab_doc.get("antibodies", [])
        antibodies = [a for a in antibodies if a.get("id") != args.id]
        antibodies.append(
            {
                "id": args.id,
                "name": args.name,
                "tool": args.tool,
                "match_regex": args.regex,
                "action": args.action,
                "symptom": args.symptom,
                "root_cause": args.root_cause,
                "prevention": args.prevention,
            }
        )
        ab_doc["antibodies"] = antibodies
        ANTIBODIES_PATH.write_text(json.dumps(ab_doc, indent=2, ensure_ascii=False), encoding="utf-8")
        antibody_added = True

    # 3. Re-sync semantic index incrementally
    sync_ns = argparse.Namespace(dim=args.dim, batch_size=32)
    cmd_sync(sync_ns)

    print(
        json.dumps(
            {
                "status": "learned",
                "episode_id": episode["id"],
                "antibody_added": antibody_added,
                "antibody_id": args.id if antibody_added else None,
            },
            indent=2,
        )
    )
    return 0


def cmd_image_sim(args: argparse.Namespace) -> int:
    import numpy as np
    from PIL import Image

    t0 = time.time()
    img1 = Image.open(args.image1).convert("RGB")
    img2 = Image.open(args.image2).convert("RGB")

    model = load_sentence_transformer(enable_vision=True)
    inputs: list[Any] = [
        {"text": "<|image|>", "image": [img1]},
        {"text": "<|image|>", "image": [img2]},
    ]
    if args.prompt:
        inputs.append(f"task: search result | query: {args.prompt}")

    embs = model.encode(
        inputs,
        truncate_dim=args.dim,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    v1 = np.asarray(embs[0], dtype=np.float32)
    v2 = np.asarray(embs[1], dtype=np.float32)
    img_sim = float(np.dot(v1, v2))

    res: dict[str, Any] = {
        "status": "ok",
        "model": MODEL_ID,
        "modality": "vision+text",
        "dim": args.dim,
        "image1": str(args.image1),
        "image2": str(args.image2),
        "image_cosine_similarity": round(img_sim, 4),
        "elapsed_sec": round(time.time() - t0, 3),
    }
    if args.prompt:
        vp = np.asarray(embs[2], dtype=np.float32)
        res["prompt_to_image1_similarity"] = round(float(np.dot(vp, v1)), 4)
        res["prompt_to_image2_similarity"] = round(float(np.dot(vp, v2)), 4)

    print(json.dumps(res, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="EmbeddingGemma 2 Semantic Memory & Reflexion CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sync = sub.add_parser("sync", help="Incrementally embed & index memories, antibodies, episodes, skills, and playbooks")
    p_sync.add_argument("--dim", type=int, default=256, choices=[128, 256, 512, 768])
    p_sync.add_argument("--batch-size", type=int, default=64)
    p_sync.set_defaults(func=cmd_sync)

    p_search = sub.add_parser("search", help="Semantic search across indexed sources using task-steered EmbeddingGemma 2")
    p_search.add_argument("query", type=str)
    p_search.add_argument("--task", type=str, default="SearchQuery", choices=list(TASK_PREFIXES.keys()))
    p_search.add_argument("--source", type=str, default="all", choices=["all", "memory", "antibody", "episode", "skill", "cyber"])
    p_search.add_argument("--top-k", type=int, default=8)
    p_search.set_defaults(func=cmd_search)

    p_learn = sub.add_parser("learn", help="Record a mistake episode, create an active PreToolUse antibody, and embed it")
    p_learn.add_argument("--id", required=True, help="Identifier e.g. AB-007")
    p_learn.add_argument("--name", required=True, help="Short slug e.g. missing-env-check")
    p_learn.add_argument("--symptom", required=True)
    p_learn.add_argument("--root-cause", required=True)
    p_learn.add_argument("--prevention", required=True)
    p_learn.add_argument("--workspace", default=r"c:\Users\avich\Downloads\mythos")
    p_learn.add_argument("--category", default="engineering")
    p_learn.add_argument("--tool", default="run_command")
    p_learn.add_argument("--regex", default="")
    p_learn.add_argument("--action", default="warn", choices=["warn", "block", "rewrite"])
    p_learn.add_argument("--dim", type=int, default=256, choices=[128, 256, 512, 768])
    p_learn.set_defaults(func=cmd_learn)

    p_img = sub.add_parser("image-sim", help="Compute multimodal EmbeddingGemma 2 cosine similarity between two images")
    p_img.add_argument("image1", type=str)
    p_img.add_argument("image2", type=str)
    p_img.add_argument("--prompt", type=str, default="")
    p_img.add_argument("--dim", type=int, default=256, choices=[128, 256, 512, 768])
    p_img.set_defaults(func=cmd_image_sim)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())

````
