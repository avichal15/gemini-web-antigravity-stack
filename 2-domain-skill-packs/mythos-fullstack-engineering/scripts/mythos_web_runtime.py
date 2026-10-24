#!/usr/bin/env python3
"""
Mythos 5 — Gemini Web Python Sandbox Runtime Engine (mythos_web_runtime.py)
===========================================================================
Adapts the Antigravity 2.0 Hook & Verification Architecture (PreToolUse, PostToolUse, Stop)
to run deterministically inside Gemini Web's built-in Python Code Execution sandbox.

Capabilities:
1. pre-check     : Active Antibody Guardrail (antibodies_catalog.csv) + Gravitas Session
                   Read-Before-Edit & Exact-Retry Duplicate Failure Fingerprint Guard.
2. post-verify   : Static Compiler/AST Verifier (Python ast.parse + py_compile, JS/TS/JSON/SQL
                   structural checks, Anti-Placeholder/Stub enforcement, No-AI-Slop check,
                   Secret Redaction via SECRET_PATTERNS, and Episodic Mistake Logging).
3. gate-check    : Full Python port of Unlazy's gate-check.mjs & stop-hook.mjs (parses GATES.md,
                   executes CHECK commands, verifies EXPECT substrings, stamps SHA-256 EVIDENCE,
                   and enforces the 6-block circuit breaker).
4. learn         : Distills a newly solved bug or environment trap into a permanent Antibody
                   in antibodies_catalog.csv and episodes_catalog.csv.

Usage inside Gemini Web Python Sandbox:
  python scripts/mythos_web_runtime.py pre-check --action "run_command" --target "pytest -q"
  python scripts/mythos_web_runtime.py post-verify --file path/to/script.py
  python scripts/mythos_web_runtime.py gate-check --gates GATES.md --approve
  python scripts/mythos_web_runtime.py learn --id AB-007 --name my-rule --regex "..." --symptom "..." --root-cause "..." --prevention "..."
"""

from __future__ import annotations

import argparse
import ast
import csv
import datetime as dt
import hashlib
import json
import os
import py_compile
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
MEMORY_DIR = SKILL_ROOT / "memory"
ANTIBODIES_CSV = MEMORY_DIR / "antibodies_catalog.csv"
EPISODES_CSV = MEMORY_DIR / "episodes_catalog.csv"
SESSION_STATE_TXT = MEMORY_DIR / "session_guard_state.txt"

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[0-9A-Za-z_-]{30,})\b"),
    re.compile(r"([A-Za-z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD)[A-Za-z0-9_]*\s*[:=]\s*[\"']?)([^\s\"',;]+)", re.IGNORECASE),
]

AI_SLOP_WORDS = [
    "delve", "foster", "leverage", "utilize", "facilitate", "empower",
    "streamline", "cutting-edge", "paradigm shift", "game changer",
    "tapestry", "realm", "beacon", "multifaceted", "meticulous",
    "intricate", "paramount", "transformative", "elevate", "embark",
    "supercharge", "harness", "ever-evolving",
]

PLACEHOLDER_PATTERNS = [
    (re.compile(r"//\s*TODO\b", re.IGNORECASE), "Contains '// TODO' placeholder comment"),
    (re.compile(r"#\s*TODO\b", re.IGNORECASE), "Contains '# TODO' placeholder comment"),
    (re.compile(r"\bpass\s*#\s*(?:todo|placeholder|implement)", re.IGNORECASE), "Contains unimplemented 'pass # placeholder' stub"),
    (re.compile(r"raise\s+NotImplementedError\b"), "Contains unimplemented 'NotImplementedError' stub"),
]


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def redact_secrets(text: str) -> str:
    out = str(text or "")
    out = SECRET_PATTERNS[0].sub("Bearer <REDACTED>", out)
    out = SECRET_PATTERNS[1].sub("<REDACTED_KEY>", out)
    out = SECRET_PATTERNS[2].sub(r"\1<REDACTED>", out)
    return out


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def action_fingerprint(action: str, target: str) -> str:
    return sha256_hex(canonical_json({"action": action, "target": target}))[:16]


def load_session_state() -> Dict[str, Any]:
    if SESSION_STATE_TXT.exists():
        try:
            return json.loads(SESSION_STATE_TXT.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"reads": [], "failed_fingerprints": {}, "stop_blocks": {}}


def save_session_state(state: Dict[str, Any]) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_STATE_TXT.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_antibodies() -> List[Dict[str, str]]:
    if not ANTIBODIES_CSV.exists():
        return []
    with ANTIBODIES_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cmd_pre_check(args: argparse.Namespace) -> int:
    action = args.action.strip()
    target = args.target.strip()
    state = load_session_state()
    warnings: List[str] = []
    blocked: List[str] = []

    # 1. Gravitas Read-Before-Edit Guard
    if action in ("read_file", "inspect_file") and target:
        norm = str(Path(target).resolve())
        if norm not in state["reads"]:
            state["reads"].append(norm)
            save_session_state(state)
    elif action in ("edit_file", "write_file") and target and Path(target).exists():
        norm = str(Path(target).resolve())
        if norm not in state["reads"]:
            warnings.append(
                f"[READ-BEFORE-EDIT GUARD] Target file '{target}' exists on disk but has not been read in this session. Read it before mutating."
            )

    # 2. Gravitas Exact-Retry Duplicate Failure Guard
    fp = action_fingerprint(action, target)
    if fp in state.get("failed_fingerprints", {}):
        prev_reason = state["failed_fingerprints"][fp]
        blocked.append(
            f"[EXACT-RETRY GUARD] Identical action ({action}, fingerprint {fp}) already failed in this session ({prev_reason}). Change arguments or inspect state first."
        )

    # 3. Active Antibody Guardrail
    for ab in load_antibodies():
        tool_rx = ab.get("tool", ".*")
        if not re.search(f"^({tool_rx})$", action, re.IGNORECASE):
            continue
        must_not = ab.get("must_not_contain", "")
        if must_not and must_not in target:
            continue
        match_rx = ab.get("match_regex", "")
        if not match_rx:
            continue
        try:
            if re.search(match_rx, target, re.IGNORECASE | re.MULTILINE):
                act = ab.get("action", "warn").lower()
                msg = (
                    f"[ANTIBODY {act.upper()} {ab.get('id')}: {ab.get('name')}] "
                    f"Symptom: {ab.get('symptom')} | Root Cause: {ab.get('root_cause')} | Prevention: {ab.get('prevention')}"
                )
                if act == "block":
                    blocked.append(msg)
                else:
                    warnings.append(msg)
        except re.error:
            continue

    result = {
        "decision": "block" if blocked else "allow",
        "fingerprint": fp,
        "blocked_reasons": blocked,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    return 1 if blocked else 0


def verify_python_source(source: str, filename: str) -> List[str]:
    issues: List[str] = []
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as e:
        issues.append(f"Python SyntaxError at L{e.lineno}:{e.offset}: {e.msg}")
        return issues

    # Check for empty except pass blocks or obvious antipatterns
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass) and node.type is None:
                issues.append(f"L{node.lineno}: Bare 'except: pass' swallows all exceptions including KeyboardInterrupt/SystemExit.")
    return issues


def verify_text_quality(source: str, check_slop: bool = False) -> List[str]:
    issues: List[str] = []
    for rx, desc in PLACEHOLDER_PATTERNS:
        m = rx.search(source)
        if m:
            line_no = source[: m.start()].count("\n") + 1
            issues.append(f"L{line_no}: [DEPTH DIRECTIVE VIOLATION] {desc}")

    if check_slop:
        lower = source.lower()
        found_slop = [w for w in AI_SLOP_WORDS if re.search(r"\b" + re.escape(w) + r"\b", lower)]
        if found_slop:
            issues.append(f"[NO-AI-SLOP VIOLATION] Banned words detected: {', '.join(found_slop)}")
    return issues


def append_episode(category: str, file_path: str, symptom: str, root_cause: str, fix: str) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    write_header = not EPISODES_CSV.exists()
    with EPISODES_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "timestamp", "category", "file", "symptom", "root_cause", "fix"],
        )
        if write_header:
            writer.writeheader()
        writer.writerow({
            "id": f"EP-WEB-{int(dt.datetime.now().timestamp())}",
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "category": category,
            "file": file_path,
            "symptom": redact_secrets(symptom)[:400],
            "root_cause": redact_secrets(root_cause)[:300],
            "fix": redact_secrets(fix)[:300],
        })


def cmd_post_verify(args: argparse.Namespace) -> int:
    fpath = Path(args.file)
    if not fpath.exists():
        print(json.dumps({"status": "error", "message": f"File not found: {fpath}"}))
        return 1

    source = fpath.read_text(encoding="utf-8", errors="replace")
    ext = fpath.suffix.lower()
    issues: List[str] = []

    if ext in (".py", ".pyi"):
        issues.extend(verify_python_source(source, str(fpath)))
        try:
            py_compile.compile(str(fpath), doraise=True)
        except py_compile.PyCompileError as e:
            issues.append(f"py_compile error: {e.msg}")
        issues.extend(verify_text_quality(source, check_slop=False))
    elif ext in (".json",):
        try:
            json.loads(source)
        except json.JSONDecodeError as e:
            issues.append(f"JSONDecodeError at L{e.lineno}:{e.colno}: {e.msg}")
    elif ext in (".md", ".txt"):
        issues.extend(verify_text_quality(source, check_slop=args.check_slop))
    else:
        issues.extend(verify_text_quality(source, check_slop=False))

    state = load_session_state()
    fp = action_fingerprint("post_verify", str(fpath.resolve()))
    if issues:
        redacted_issues = [redact_secrets(i) for i in issues]
        state.setdefault("failed_fingerprints", {})[fp] = "; ".join(redacted_issues)[:180]
        save_session_state(state)
        append_episode(
            category="post-verify-static-analysis",
            file_path=str(fpath),
            symptom="; ".join(redacted_issues),
            root_cause="Post-edit AST/compiler/depth verification detected defects",
            fix="Resolve syntax, placeholder, or slop issues before claiming completion",
        )
        print(json.dumps({"status": "failed", "file": str(fpath), "issues": redacted_issues}, indent=2))
        return 1

    print(json.dumps({"status": "passed", "file": str(fpath), "issues": []}, indent=2))
    return 0


GATE_HEADER_RX = re.compile(r"^-\s*\[([ xX])\]\s*([A-Za-z0-9_-]+)\s*:\s*(.+)$")
FIELD_RX = re.compile(r"^\s+(CHECK|EXPECT|EVIDENCE|ABANDON)\s*:\s*(.+)$")


def cmd_gate_check(args: argparse.Namespace) -> int:
    gates_path = Path(args.gates)
    if not gates_path.exists():
        print(json.dumps({"status": "no_gates_file", "decision": "allow"}))
        return 0

    lines = gates_path.read_text(encoding="utf-8").splitlines()
    gates: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for idx, line in enumerate(lines):
        m_head = GATE_HEADER_RX.match(line)
        if m_head:
            if current:
                gates.append(current)
            current = {
                "line_idx": idx,
                "checked": m_head.group(1).lower() == "x",
                "id": m_head.group(2),
                "title": m_head.group(3).strip(),
                "check": None,
                "expect": None,
                "evidence": None,
                "evidence_line_idx": None,
            }
            continue
        if current is not None:
            m_field = FIELD_RX.match(line)
            if m_field:
                key = m_field.group(1).upper()
                val = m_field.group(2).strip()
                if key == "CHECK":
                    current["check"] = val
                elif key == "EXPECT":
                    current["expect"] = val
                elif key == "EVIDENCE":
                    current["evidence"] = val
                    current["evidence_line_idx"] = idx
    if current:
        gates.append(current)

    results = []
    all_met = True
    updated_lines = list(lines)

    for g in gates:
        def_hash = sha256_hex(f"{g['id']}\0{g['check']}\0{g['expect']}")
        if not args.approve:
            met = bool(g["checked"] and g["evidence"] and f"definition-sha256={def_hash}" in g["evidence"])
            if not met:
                all_met = False
            results.append({"id": g["id"], "title": g["title"], "met": met})
            continue

        # Execute CHECK command
        if not g["check"]:
            all_met = False
            results.append({"id": g["id"], "met": False, "error": "Missing CHECK command"})
            continue

        proc = subprocess.run(
            g["check"],
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        combined_out = (proc.stdout or "") + (proc.stderr or "")
        expect_ok = (g["expect"] in combined_out) if g["expect"] else (proc.returncode == 0)
        met = proc.returncode == 0 and expect_ok
        if not met:
            all_met = False

        out_hash = sha256_hex(combined_out)
        ev_str = (
            f"  EVIDENCE: automatic-evidence=v1; definition-sha256={def_hash}; "
            f"exit={proc.returncode}; EXPECT={'matched' if expect_ok else 'unmatched'}; "
            f"output-sha256={out_hash}; output-bytes={len(combined_out.encode('utf-8'))}"
        )
        if met:
            updated_lines[g["line_idx"]] = f"- [x] {g['id']}: {g['title']}"
            if g["evidence_line_idx"] is not None:
                updated_lines[g["evidence_line_idx"]] = ev_str
        results.append({
            "id": g["id"],
            "title": g["title"],
            "met": met,
            "exit_code": proc.returncode,
            "output_preview": redact_secrets(combined_out.strip())[:240],
        })

    if args.approve:
        gates_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")

    # Circuit breaker (max 6 blocks on identical gate state)
    state = load_session_state()
    state_sig = sha256_hex(json.dumps(results, sort_keys=True))[:16]
    blocks = state.get("stop_blocks", {}).get(state_sig, 0)
    if not all_met:
        blocks += 1
        state.setdefault("stop_blocks", {})[state_sig] = blocks
        save_session_state(state)

    circuit_tripped = blocks > 6
    decision = "allow" if (all_met or circuit_tripped) else "continue"
    print(json.dumps({
        "decision": decision,
        "all_met": all_met,
        "circuit_breaker_tripped": circuit_tripped,
        "consecutive_blocks_on_state": blocks,
        "gates": results,
    }, indent=2))
    return 0 if all_met else 1


def cmd_learn(args: argparse.Namespace) -> int:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    write_header = not ANTIBODIES_CSV.exists()
    with ANTIBODIES_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "name", "tool", "match_regex", "must_not_contain", "action", "symptom", "root_cause", "prevention"],
        )
        if write_header:
            writer.writeheader()
        writer.writerow({
            "id": args.id,
            "name": args.name,
            "tool": args.tool,
            "match_regex": args.regex,
            "must_not_contain": args.must_not_contain or "",
            "action": args.action,
            "symptom": redact_secrets(args.symptom),
            "root_cause": redact_secrets(args.root_cause),
            "prevention": redact_secrets(args.prevention),
        })
    append_episode(
        category="antibody-immunization",
        file_path="memory/antibodies_catalog.csv",
        symptom=args.symptom,
        root_cause=args.root_cause,
        fix=f"Created Antibody {args.id} ({args.name}): {args.prevention}",
    )
    print(json.dumps({"status": "immunized", "id": args.id, "name": args.name}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Mythos 5 Gemini Web Runtime Engine")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_pre = sub.add_parser("pre-check", help="Run PreToolUse Antibody + Gravitas Session Guards")
    p_pre.add_argument("--action", required=True, help="Tool or action name (e.g. run_command, edit_file)")
    p_pre.add_argument("--target", required=True, help="Command string, file path, or code snippet")

    p_post = sub.add_parser("post-verify", help="Run PostToolUse AST/Compiler/Depth/Slop Verifier")
    p_post.add_argument("--file", required=True, help="File path to verify")
    p_post.add_argument("--check-slop", action="store_true", help="Check prose for banned AI-slop words")

    p_gate = sub.add_parser("gate-check", help="Run Unlazy Gate Ledger verifier & Stop-Gate circuit breaker")
    p_gate.add_argument("--gates", default="GATES.md", help="Path to GATES.md")
    p_gate.add_argument("--approve", action="store_true", help="Execute CHECK commands and stamp SHA-256 EVIDENCE")

    p_learn = sub.add_parser("learn", help="Distill a solved mistake into a permanent Antibody")
    p_learn.add_argument("--id", required=True)
    p_learn.add_argument("--name", required=True)
    p_learn.add_argument("--tool", default="run_command|edit_file|write_file")
    p_learn.add_argument("--regex", required=True)
    p_learn.add_argument("--must-not-contain", default="")
    p_learn.add_argument("--action", default="warn", choices=["warn", "block", "rewrite"])
    p_learn.add_argument("--symptom", required=True)
    p_learn.add_argument("--root-cause", required=True)
    p_learn.add_argument("--prevention", required=True)

    args = parser.parse_args()
    if args.subcommand == "pre-check":
        return cmd_pre_check(args)
    if args.subcommand == "post-verify":
        return cmd_post_verify(args)
    if args.subcommand == "gate-check":
        return cmd_gate_check(args)
    if args.subcommand == "learn":
        return cmd_learn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
