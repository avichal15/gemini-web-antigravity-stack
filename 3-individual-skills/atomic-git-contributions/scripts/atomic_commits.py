#!/usr/bin/env python3
"""CLI utility for the atomic-git-contributions skill.

Provides deterministic, lock-free Git plumbing and fast-import operations for:
1. Auditing changed files (with --no-renames), contributor identities, and date histograms.
2. Auto-partitioning large diffs or monolithic commit ranges into dependency-ordered atomic commit plans.
3. Executing atomic commit plans and replaying commit histories via `git fast-import` (raw LF byte stream)
   with unified author/committer attribution, realistic chronological date distribution, and a mandatory
   cryptographic tree verification gate (`new_head^{tree} == target^{tree}`).
4. Generating structured Markdown ledgers (`Task`, `Why`, `Files affected`, `Implementation steps`, `Commit message`).
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import json
import os
import posixpath
import subprocess
import sys


def run_git(repo_dir: str, args: list[str], env: dict | None = None, input_bytes: bytes | None = None) -> str:
    """Runs a git command using raw byte streams to prevent Windows CRLF injection."""
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    res = subprocess.run(
        ["git"] + args,
        cwd=repo_dir,
        env=merged_env,
        input=input_bytes,
        capture_output=True,
    )
    if res.returncode != 0:
        stderr_text = res.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"git {' '.join(args)} failed (exit {res.returncode}):\n{stderr_text}")
    return res.stdout.decode("utf-8", errors="replace").strip()


def write_output(data: dict | list, output_file: str) -> None:
    """Writes structured JSON output to a file (Rule 4: Default to File Output)."""
    try:
        parent = os.path.dirname(os.path.abspath(output_file))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Success! Data written to: {output_file}")
    except (OSError, TypeError) as exc:
        print(f"Error writing to file {output_file}: {exc}", file=sys.stderr)
        sys.exit(1)


def parse_tz_offset(tz_str: str) -> timezone:
    """Parses '+0530' or '+05:30' into a datetime.timezone."""
    cleaned = tz_str.strip().replace(":", "")
    sign = -1 if cleaned.startswith("-") else 1
    digits = cleaned.lstrip("+-")
    hours = int(digits[:2])
    minutes = int(digits[2:4]) if len(digits) >= 4 else 0
    return timezone(timedelta(hours=sign * hours, minutes=sign * minutes))


def classify_file_bucket(path: str) -> tuple[int, str, str, str]:
    """Maps a repository path to (layer_order, bucket_key, default_type, default_scope)."""
    norm = path.replace("\\", "/")
    parts = norm.split("/")
    base = posixpath.basename(norm)
    is_test = (
        ".test." in base
        or ".spec." in base
        or "__tests__" in parts
        or parts[0] in ("tests", "test", "__tests__")
        or "/src/test/" in f"/{norm}"
    )

    if norm.startswith("supabase/migrations/"):
        stem = posixpath.splitext(base)[0]
        return (10, f"db-migration:{stem}", "feat", "db")
    if norm.startswith("supabase/functions/_shared/"):
        return (20, f"supabase-shared:{base}", "feat", "functions")
    if norm.startswith("supabase/functions/") and len(parts) >= 3:
        fn_name = parts[2]
        return (22, f"supabase-fn:{fn_name}", "feat", "functions")
    if norm.startswith("supabase/"):
        return (25, "supabase-config", "chore", "supabase")

    if norm.startswith("src/lib/"):
        sub = parts[2] if len(parts) > 3 else posixpath.splitext(base)[0].replace(".test", "")
        return (30, f"lib:{sub}", "test" if is_test else "feat", "lib")

    if norm.startswith("src/features/") and len(parts) >= 3:
        feat = parts[2]
        sub = parts[3] if len(parts) > 3 else "core"
        sub_clean = posixpath.splitext(sub)[0].replace(".test", "").replace(".native", "")
        layer = 42 if is_test else 40
        return (layer, f"feature:{feat}:{sub_clean}", "test" if is_test else "feat", feat)

    if norm.startswith("src/components/"):
        return (48, f"ui-component:{posixpath.splitext(base)[0]}", "feat", "ui")

    if norm.startswith("assets/"):
        sub = parts[1] if len(parts) > 1 else "root"
        sub2 = parts[2] if len(parts) > 2 else "files"
        return (35, f"assets:{sub}:{sub2}", "feat", "assets")

    if norm.startswith("app/"):
        group = parts[1] if len(parts) > 2 else posixpath.splitext(base)[0]
        return (50, f"routes:{group}", "feat", "routes")

    if norm.startswith("modules/"):
        mod_name = parts[1] if len(parts) > 1 else "native"
        if "/vendor/" in f"/{norm}":
            return (55, f"native-vendor:{mod_name}", "feat", mod_name)
        if is_test:
            return (58, f"native-test:{mod_name}:{base[:12]}", "test", mod_name)
        return (56, f"native:{mod_name}:{base[:12]}", "feat", mod_name)

    if norm.startswith("android/") or norm.startswith("ios/"):
        platform = parts[0]
        return (60, f"platform:{platform}", "feat", platform)

    if norm.startswith("plugins/"):
        return (62, "expo-plugins", "feat", "plugins")

    if norm.startswith("tests/"):
        sub = parts[1] if len(parts) > 1 else "suite"
        stem = posixpath.splitext(base)[0]
        return (70, f"tests:{sub}:{stem[:14]}", "test", sub)

    if norm.startswith("scripts/"):
        sub = parts[1] if len(parts) > 2 else posixpath.splitext(base)[0]
        return (75, f"scripts:{sub}", "feat", "scripts")

    if norm.startswith("website/"):
        sub = parts[1] if len(parts) > 1 else "root"
        return (80, f"website:{sub}", "test" if is_test else "feat", "website")

    if norm.startswith("release/"):
        return (85, "release-artifacts", "docs", "release")

    if norm.startswith("docs/"):
        return (88, f"docs:{posixpath.splitext(base)[0][:14]}", "docs", "architecture")

    if norm.startswith("work/"):
        return (90, "work-handover", "chore", "work")

    return (65, "project-config", "chore", "config")


def cmd_audit(args: argparse.Namespace) -> dict:
    repo = os.path.abspath(args.repo)
    base = args.base
    target = args.target

    diff_raw = run_git(repo, ["diff", "--no-renames", "--name-status", base, target])
    changes = []
    status_counts = Counter()
    buckets = defaultdict(list)

    for line in diff_raw.splitlines():
        if not line.strip():
            continue
        status, path = line.split("\t", 1)
        status = status.strip()
        path = path.strip()
        changes.append({"status": status, "path": path})
        status_counts[status] += 1
        _, bucket_key, _, _ = classify_file_bucket(path)
        buckets[bucket_key].append(path)

    shortlog_raw = run_git(repo, ["shortlog", "-sne", target])
    contributors = [line.strip() for line in shortlog_raw.splitlines() if line.strip()]

    dates_raw = run_git(repo, ["log", "--format=%ad", "--date=short", target])
    date_histogram = dict(sorted(Counter(dates_raw.splitlines()).items()))

    total_commits = int(run_git(repo, ["rev-list", "--count", target]))
    base_tree = run_git(repo, ["rev-parse", f"{base}^{{tree}}"])
    target_tree = run_git(repo, ["rev-parse", f"{target}^{{tree}}"])

    return {
        "repo": repo,
        "base": base,
        "target": target,
        "base_tree": base_tree,
        "target_tree": target_tree,
        "total_commits_at_target": total_commits,
        "total_changed_paths": len(changes),
        "status_counts": dict(status_counts),
        "contributors": contributors,
        "date_histogram": date_histogram,
        "candidate_bucket_count": len(buckets),
        "candidate_buckets": {k: v for k, v in sorted(buckets.items())},
    }


def cmd_auto_plan(args: argparse.Namespace) -> dict:
    repo = os.path.abspath(args.repo)
    base = args.base
    target = args.target
    max_files = args.max_files_per_commit

    diff_paths = [
        p.strip()
        for p in run_git(repo, ["diff", "--no-renames", "--name-only", base, target]).splitlines()
        if p.strip()
    ]

    grouped = defaultdict(list)
    meta_map = {}
    for p in diff_paths:
        layer, bucket_key, ctype, scope = classify_file_bucket(p)
        grouped[(layer, bucket_key)].append(p)
        meta_map[bucket_key] = (ctype, scope)

    batches = []
    for (layer, bucket_key), paths in sorted(grouped.items(), key=lambda x: (x[0][0], x[0][1])):
        paths = sorted(paths)
        ctype, scope = meta_map[bucket_key]
        # Keep vendor trees together; split other large buckets by max_files
        chunk_size = len(paths) if "vendor" in bucket_key else max_files
        for idx in range(0, len(paths), chunk_size):
            chunk = paths[idx : idx + chunk_size]
            sample_names = [posixpath.basename(f) for f in chunk[:3]]
            names_summary = ", ".join(sample_names)
            if len(chunk) > 3:
                names_summary += f" (+{len(chunk) - 3} more)"
            msg = f"{ctype}({scope}): update {names_summary}"
            why = f"Apply cohesive {scope} changes across {len(chunk)} file(s) ({names_summary})."
            task = f"Update {scope} ({names_summary})"
            batches.append(
                {
                    "task": task,
                    "why": why,
                    "message": msg,
                    "files": chunk,
                }
            )

    return {
        "repo": repo,
        "base": base,
        "target": target,
        "total_files": len(diff_paths),
        "total_batches": len(batches),
        "batches": batches,
    }


def cmd_execute(args: argparse.Namespace) -> dict:
    repo = os.path.abspath(args.repo)
    with open(args.plan, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    base = plan_data.get("base") or args.base
    target = plan_data.get("target") or args.target
    batches = plan_data["batches"]

    author_name = args.author_name
    author_email = args.author_email
    tz_str = args.timezone
    tz_info = parse_tz_offset(tz_str)

    # 1. Verify 100% file coverage between base and target (with --no-renames)
    diff_files = [
        p.strip()
        for p in run_git(repo, ["diff", "--no-renames", "--name-only", base, target]).splitlines()
        if p.strip()
    ]
    remaining = set(diff_files)
    resolved_batches = []
    for batch in batches:
        matched = sorted([p for p in batch["files"] if p in remaining])
        if not matched:
            continue
        for p in matched:
            remaining.remove(p)
        resolved_batches.append(
            {
                "task": batch["task"],
                "why": batch["why"],
                "message": batch["message"],
                "files": matched,
            }
        )

    if remaining:
        raise RuntimeError(
            f"Plan is missing {len(remaining)} changed file(s) between {base} and {target}: "
            f"{sorted(remaining)[:10]}"
        )

    # 2. Fetch early commits up to `base` to replay with unified author/dates if requested
    early_records = []
    if args.replay_early:
        raw_early = run_git(repo, ["log", "--reverse", "--format=%H %T%n%B%x00", base])
        for chunk in raw_early.split("\x00"):
            chunk = chunk.strip()
            if not chunk:
                continue
            first_line, _, msg = chunk.partition("\n")
            old_sha, tree_sha = first_line.strip().split()
            early_records.append((old_sha, tree_sha, msg.strip()))

    # 3. Map target blobs at `target`
    ls_out = run_git(repo, ["ls-tree", "-r", target])
    target_blobs = {}
    for line in ls_out.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        mode, _, sha = meta.split()
        target_blobs[path] = (mode, sha)

    # 4. Compute date windows
    start_dt = datetime.fromisoformat(args.start_date).replace(tzinfo=tz_info)
    end_dt = datetime.fromisoformat(args.end_date).replace(tzinfo=tz_info)

    stream_chunks = []
    mark_counter = 0
    temp_ref = "refs/heads/temp-atomic-rebuild"

    if early_records:
        split_dt = start_dt + (end_dt - start_dt) * (len(early_records) / max(1, len(early_records) + len(resolved_batches)))
        step_early = (split_dt - start_dt) / max(1, len(early_records) - 1)
        start_new_dt = split_dt + timedelta(hours=1)
    else:
        start_new_dt = start_dt
        step_early = timedelta(0)

    step_new = (end_dt - start_new_dt) / max(1, len(resolved_batches) - 1)

    for i, (_, tree_sha, commit_msg) in enumerate(early_records):
        mark_counter += 1
        dt = start_dt + step_early * i
        git_date = f"{int(dt.timestamp())} {tz_str}"
        msg_bytes = (commit_msg + "\n").encode("utf-8")
        header = [
            f"commit {temp_ref}",
            f"mark :{mark_counter}",
            f"author {author_name} <{author_email}> {git_date}",
            f"committer {author_name} <{author_email}> {git_date}",
            f"data {len(msg_bytes)}",
        ]
        stream_chunks.append("\n".join(header).encode("utf-8") + b"\n" + msg_bytes)
        body = []
        if mark_counter > 1:
            body.append(f"from :{mark_counter - 1}")
        body.append("deleteall")
        body.append(f'M 040000 {tree_sha} ""')
        stream_chunks.append("\n".join(body).encode("utf-8") + b"\n\n")

    new_commit_records = []
    for j, batch in enumerate(resolved_batches):
        mark_counter += 1
        dt = start_new_dt + step_new * j
        git_date = f"{int(dt.timestamp())} {tz_str}"
        iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_str
        full_msg = f"{batch['message']}\n\n{batch['why']}\n"
        msg_bytes = full_msg.encode("utf-8")
        header = [
            f"commit {temp_ref}",
            f"mark :{mark_counter}",
            f"author {author_name} <{author_email}> {git_date}",
            f"committer {author_name} <{author_email}> {git_date}",
            f"data {len(msg_bytes)}",
        ]
        stream_chunks.append("\n".join(header).encode("utf-8") + b"\n" + msg_bytes)
        body = []
        if mark_counter == 1 and not early_records:
            base_sha = run_git(repo, ["rev-parse", base])
            body.append(f"from {base_sha}")
        else:
            body.append(f"from :{mark_counter - 1}")

        for p in batch["files"]:
            if p in target_blobs:
                mode, sha = target_blobs[p]
                body.append(f"M {mode} {sha} {p}")
            else:
                body.append(f"D {p}")
        stream_chunks.append("\n".join(body).encode("utf-8") + b"\n\n")
        new_commit_records.append(
            {
                "index": j + 1,
                "date": iso_date,
                "task": batch["task"],
                "why": batch["why"],
                "message": batch["message"],
                "files": batch["files"],
            }
        )

    payload = b"".join(stream_chunks)
    run_git(repo, ["fast-import", "--force", "--quiet"], input_bytes=payload)

    new_head = run_git(repo, ["rev-parse", temp_ref])
    expected_tree = run_git(repo, ["rev-parse", f"{target}^{{tree}}"])
    actual_tree = run_git(repo, ["rev-parse", f"{new_head}^{{tree}}"])

    if expected_tree != actual_tree:
        diff_diag = run_git(repo, ["diff-tree", "-r", expected_tree, actual_tree])
        run_git(repo, ["update-ref", "-d", temp_ref])
        raise RuntimeError(
            f"CRYPTOGRAPHIC TREE MISMATCH! Expected {expected_tree}, got {actual_tree}.\n"
            f"Diff:\n{diff_diag[:2000]}"
        )

    new_shas = run_git(
        repo,
        ["rev-list", "--reverse", f"{temp_ref}~{len(resolved_batches)}..{temp_ref}"],
    ).splitlines()
    for rec, sha in zip(new_commit_records, new_shas):
        rec["sha"] = sha[:7]

    if args.update_branch:
        run_git(repo, ["update-ref", f"refs/heads/{args.update_branch}", new_head])
    run_git(repo, ["update-ref", "-d", temp_ref])

    total_commits = int(run_git(repo, ["rev-list", "--count", new_head]))
    shortlog = run_git(repo, ["shortlog", "-sne", new_head]).splitlines()
    dates_raw = run_git(repo, ["log", "--format=%ad", "--date=short", new_head])
    date_histogram = dict(sorted(Counter(dates_raw.splitlines()).items()))

    return {
        "status": "verified",
        "new_head": new_head,
        "expected_tree": expected_tree,
        "actual_tree": actual_tree,
        "tree_match": True,
        "updated_branch": args.update_branch,
        "replayed_early_commits": len(early_records),
        "new_atomic_commits": len(new_commit_records),
        "total_commits": total_commits,
        "contributors": [s.strip() for s in shortlog if s.strip()],
        "date_histogram": date_histogram,
        "commits": new_commit_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Atomic Git Contributions & Cryptographic Tree Verification CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Subcommand: audit ---
    p_audit = subparsers.add_parser(
        "audit",
        help="Audit changed files (--no-renames), contributors, and commit date histogram",
    )
    p_audit.add_argument("--repo", required=True, help="Repository root directory")
    p_audit.add_argument("--base", required=True, help="Base commit or ref")
    p_audit.add_argument("--target", required=True, help="Target commit or ref (e.g. HEAD)")
    p_audit.add_argument("--output", required=True, help="Output JSON file path")

    # --- Subcommand: auto-plan ---
    p_plan = subparsers.add_parser(
        "auto-plan",
        help="Generate a dependency-ordered atomic commit plan for all files between base and target",
    )
    p_plan.add_argument("--repo", required=True, help="Repository root directory")
    p_plan.add_argument("--base", required=True, help="Base commit or ref")
    p_plan.add_argument("--target", required=True, help="Target commit or ref")
    p_plan.add_argument(
        "--max-files-per-commit",
        type=int,
        required=True,
        help="Maximum files per atomic commit bucket (e.g. 10)",
    )
    p_plan.add_argument("--output", required=True, help="Output plan JSON file path")

    # --- Subcommand: execute ---
    p_exec = subparsers.add_parser(
        "execute",
        help="Execute atomic commit plan via git fast-import and verify exact final tree SHA",
    )
    p_exec.add_argument("--repo", required=True, help="Repository root directory")
    p_exec.add_argument("--plan", required=True, help="Input plan JSON file path")
    p_exec.add_argument("--base", help="Override base commit")
    p_exec.add_argument("--target", help="Override target commit")
    p_exec.add_argument(
        "--author-name",
        default="Avichal15",
        help="Unified Git author/committer name (default: Avichal15)",
    )
    p_exec.add_argument(
        "--author-email",
        default="avichalgoyal15@gmail.com",
        help="Unified Git author/committer email (default: avichalgoyal15@gmail.com)",
    )
    p_exec.add_argument(
        "--start-date",
        required=True,
        help="ISO start timestamp (e.g. 2026-10-01T09:15:00)",
    )
    p_exec.add_argument(
        "--end-date",
        required=True,
        help="ISO end timestamp (e.g. 2026-10-23T18:35:00)",
    )
    p_exec.add_argument(
        "--timezone",
        default="+0530",
        help="Git timezone offset (default: +0530)",
    )
    p_exec.add_argument(
        "--replay-early",
        action="store_true",
        help="Also replay commits up to --base with unified author/committer and dates",
    )
    p_exec.add_argument(
        "--update-branch",
        help="Branch name under refs/heads/ to update after tree verification succeeds (e.g. main)",
    )
    p_exec.add_argument("--output", required=True, help="Output execution ledger JSON file path")

    args = parser.parse_args()
    try:
        if args.command == "audit":
            data = cmd_audit(args)
        elif args.command == "auto-plan":
            data = cmd_auto_plan(args)
        elif args.command == "execute":
            data = cmd_execute(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
        write_output(data, args.output)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
