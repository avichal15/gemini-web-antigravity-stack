#!/usr/bin/env python3
"""Multi-Channel Open-Source Tool & GitHub Repository Discovery Engine.

Searches simultaneously across:
1. GitHub Repositories (via `gh` CLI or GitHub REST API with token auto-resolution)
2. YouTube Creator Videos & Shorts (via `yt-dlp` metadata + description regex extraction for github.com/<owner>/<repo>)
3. Emits actionable Instagram Reels (`insta-manager-acceptance-bridge`) & NotebookLM Deep Research (`notebooklm` MCP) workflows.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

GITHUB_REPO_REGEX = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)

IGNORED_GH_OWNERS = {
    "sponsors",
    "orgs",
    "topics",
    "trending",
    "features",
    "marketplace",
    "explore",
    "settings",
    "notifications",
    "login",
    "join",
    "about",
    "pricing",
    "security",
}


def resolve_gh_binary() -> str | None:
    found = shutil.which("gh")
    if found:
        return found
    codex_gh = Path.home() / ".codex" / "tools" / "gh" / "bin" / "gh.exe"
    if codex_gh.is_file():
        return str(codex_gh)
    return None


def resolve_github_token() -> str | None:
    for env_key in ("GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(env_key)
        if val and val.strip():
            return val.strip()
    try:
        mcp_cfg = Path.home() / ".gemini" / "config" / "mcp_config.json"
        if mcp_cfg.is_file():
            data = json.loads(mcp_cfg.read_text(encoding="utf-8"))
            token = (
                data.get("mcpServers", {})
                .get("github-mcp-server", {})
                .get("env", {})
                .get("GITHUB_PERSONAL_ACCESS_TOKEN")
            )
            if token and token.strip():
                return token.strip()
    except Exception:
        pass
    return None


def _github_api_get(url: str, timeout: int = 15) -> dict[str, Any] | None:
    """Perform a GET request against api.github.com, automatically falling back to unauthenticated if a stored PAT is expired."""
    base_headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Antigravity-DeepDiscovery/1.0",
    }
    token = resolve_github_token()
    header_variants = []
    if token:
        header_variants.append({**base_headers, "Authorization": f"Bearer {token}"})
    header_variants.append(base_headers)

    for hdrs in header_variants:
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            continue
    return None


def clean_repo_slug(owner: str, repo: str) -> str | None:
    owner_clean = owner.strip().strip("/")
    repo_clean = re.sub(r"(\.git|[,.;:)!?\"'>\]\\]+)$", "", repo.strip().strip("/"))
    if not owner_clean or not repo_clean:
        return None
    if owner_clean.lower() in IGNORED_GH_OWNERS:
        return None
    if repo_clean.lower() in {"issues", "pulls", "releases", "actions", "wiki", "blob", "tree"}:
        return None
    return f"{owner_clean}/{repo_clean}"


def extract_github_repos_from_text(text: str) -> list[str]:
    if not text:
        return []
    seen: dict[str, str] = {}
    for match in GITHUB_REPO_REGEX.finditer(text):
        slug = clean_repo_slug(match.group(1), match.group(2))
        if slug and slug.lower() not in seen:
            seen[slug.lower()] = slug
    return list(seen.values())


def search_github_repos(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search GitHub repositories using `gh search repos` or GitHub REST API fallback."""
    gh_bin = resolve_gh_binary()
    results: list[dict[str, Any]] = []

    if gh_bin:
        try:
            proc = subprocess.run(
                [
                    gh_bin,
                    "search",
                    "repos",
                    query,
                    "--sort",
                    "stars",
                    "--limit",
                    str(limit),
                    "--json",
                    "fullName,description,stargazersCount,url,updatedAt,language",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                items = json.loads(proc.stdout)
                for item in items:
                    lang = item.get("language")
                    if isinstance(lang, dict):
                        lang = lang.get("name")
                    results.append(
                        {
                            "full_name": item.get("fullName"),
                            "url": item.get("url"),
                            "stars": int(item.get("stargazersCount") or 0),
                            "description": item.get("description") or "",
                            "language": lang or "",
                            "updated_at": item.get("updatedAt") or "",
                            "discovered_via": ["github_search"],
                        }
                    )
                if results:
                    return results
        except Exception:
            pass

    # Fallback: Direct GitHub REST API
    candidate_queries = [query]
    stripped = re.sub(r"\b(open\s*source|github|alternative|free|repo|repository)\b", " ", query, flags=re.IGNORECASE)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    if stripped and stripped.lower() != query.lower():
        candidate_queries.append(stripped)

    seen_names: set[str] = {r["full_name"].lower() for r in results if r.get("full_name")}
    for q_str in candidate_queries:
        if len(results) >= limit:
            break
        encoded_q = urllib.parse.quote(q_str)
        api_url = f"https://api.github.com/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page={limit}"
        payload = _github_api_get(api_url, timeout=15)
        if payload:
            for item in payload.get("items", []):
                fn = item.get("full_name")
                if not fn or fn.lower() in seen_names:
                    continue
                seen_names.add(fn.lower())
                results.append(
                    {
                        "full_name": fn,
                        "url": item.get("html_url"),
                        "stars": int(item.get("stargazers_count") or 0),
                        "description": item.get("description") or "",
                        "language": item.get("language") or "",
                        "updated_at": item.get("updated_at") or "",
                        "discovered_via": ["github_search"],
                    }
                )
    return results[:limit]


def fetch_github_repo_metadata(slug: str) -> dict[str, Any] | None:
    """Fetch metadata for a specific owner/repo discovered from YouTube or Instagram."""
    item = _github_api_get(f"https://api.github.com/repos/{slug}", timeout=10)
    if item and item.get("full_name"):
        return {
            "full_name": item.get("full_name") or slug,
            "url": item.get("html_url") or f"https://github.com/{slug}",
            "stars": int(item.get("stargazers_count") or 0),
            "description": item.get("description") or "",
            "language": item.get("language") or "",
            "updated_at": item.get("updated_at") or "",
        }
    return {
        "full_name": slug,
        "url": f"https://github.com/{slug}",
        "stars": 0,
        "description": "(Discovered via YouTube creator video description)",
        "language": "",
        "updated_at": "",
    }


def search_youtube_creator_repos(query: str, count: int = 6) -> dict[str, Any]:
    """Use yt-dlp to search YouTube creator videos/Shorts and extract GitHub repo links from descriptions."""
    yt_dlp_bin = shutil.which("yt-dlp")
    if not yt_dlp_bin:
        return {"videos": [], "extracted_repos": [], "error": "yt-dlp not found on PATH"}

    search_expr = f"ytsearch{count}:{query} github open source"
    videos: list[dict[str, Any]] = []
    all_repos: dict[str, list[str]] = {}

    try:
        proc = subprocess.run(
            [
                yt_dlp_bin,
                search_expr,
                "--dump-json",
                "--no-playlist",
                "--skip-download",
                "--no-warnings",
                "--quiet",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=45,
        )
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                info = json.loads(line)
            except Exception:
                continue
            title = info.get("title") or ""
            desc = info.get("description") or ""
            vid_url = info.get("webpage_url") or info.get("url") or ""
            channel = info.get("channel") or info.get("uploader") or ""
            views = int(info.get("view_count") or 0)
            repos_in_vid = extract_github_repos_from_text(f"{title}\n{desc}")
            for r in repos_in_vid:
                all_repos.setdefault(r, []).append(title)
            videos.append(
                {
                    "title": title,
                    "channel": channel,
                    "url": vid_url,
                    "views": views,
                    "github_repos_mentioned": repos_in_vid,
                    "description_snippet": re.sub(r"\s+", " ", desc).strip()[:280],
                }
            )
    except Exception as exc:
        return {"videos": videos, "extracted_repos": list(all_repos.keys()), "error": str(exc)}

    return {
        "videos": videos,
        "extracted_repos": [
            {"repo": repo, "mentioned_in_videos": titles}
            for repo, titles in all_repos.items()
        ],
    }


def search_reddit_repos(query: str, limit: int = 8) -> dict[str, Any]:
    """Search Reddit JSON feed (zero API keys) for developer threads and extract github.com/<owner>/<repo> links."""
    encoded_q = urllib.parse.quote(f"{query} github")
    url = f"https://www.reddit.com/search.json?q={encoded_q}&sort=relevance&t=year&limit={limit}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Antigravity-DeepDiscovery/2.0"}
    posts: list[dict[str, Any]] = []
    all_repos: dict[str, list[str]] = {}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        children = data.get("data", {}).get("children", [])
        for child in children:
            post = child.get("data", {})
            title = post.get("title") or ""
            selftext = post.get("selftext") or ""
            ext_url = post.get("url") or ""
            permalink = f"https://www.reddit.com{post.get('permalink', '')}"
            repos_found = extract_github_repos_from_text(f"{title}\n{selftext}\n{ext_url}")
            for r in repos_found:
                all_repos.setdefault(r, []).append(title)
            if repos_found or "github" in title.lower():
                posts.append({"title": title, "url": permalink, "github_repos_mentioned": repos_found})
    except Exception as exc:
        return {"posts": posts, "extracted_repos": [], "error": str(exc)}
    return {
        "posts": posts,
        "extracted_repos": [{"repo": r, "mentioned_in_posts": t} for r, t in all_repos.items()],
    }


def run_discovery(query: str, gh_limit: int = 10, yt_count: int = 6) -> dict[str, Any]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        gh_future = pool.submit(search_github_repos, query, gh_limit)
        yt_future = pool.submit(search_youtube_creator_repos, query, yt_count)
        rd_future = pool.submit(search_reddit_repos, query, 8)
        gh_repos = gh_future.result()
        yt_data = yt_future.result()
        rd_data = rd_future.result()

    merged_by_key: dict[str, dict[str, Any]] = {}
    for repo in gh_repos:
        fn = (repo.get("full_name") or "").strip()
        if fn:
            merged_by_key[fn.lower()] = dict(repo)

    # Enrich and merge repos extracted from YouTube video descriptions & Reddit threads
    missing_slugs: list[tuple[str, list[str], str]] = []
    for entry in yt_data.get("extracted_repos", []):
        slug = entry["repo"]
        titles = entry["mentioned_in_videos"]
        key = slug.lower()
        if key in merged_by_key:
            via = merged_by_key[key].setdefault("discovered_via", [])
            if "youtube_description" not in via:
                via.append("youtube_description")
            merged_by_key[key]["youtube_mentions"] = titles
        else:
            missing_slugs.append((slug, titles, "youtube_description"))

    for entry in rd_data.get("extracted_repos", []):
        slug = entry["repo"]
        titles = entry["mentioned_in_posts"]
        key = slug.lower()
        if key in merged_by_key:
            via = merged_by_key[key].setdefault("discovered_via", [])
            if "reddit_discussion" not in via:
                via.append("reddit_discussion")
            merged_by_key[key]["reddit_mentions"] = titles
        else:
            missing_slugs.append((slug, titles, "reddit_discussion"))

    if missing_slugs:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            meta_futures = {
                pool.submit(fetch_github_repo_metadata, slug): (slug, titles, channel_tag)
                for slug, titles, channel_tag in missing_slugs[:10]
            }
            for fut, (slug, titles, channel_tag) in meta_futures.items():
                meta = fut.result()
                if meta:
                    meta["discovered_via"] = [channel_tag]
                    meta["social_mentions"] = titles
                    merged_by_key[slug.lower()] = meta

    ranked_repos = sorted(
        merged_by_key.values(),
        key=lambda r: (
            1 if any(c in r.get("discovered_via", []) for c in ("youtube_description", "reddit_discussion")) and r.get("stars", 0) >= 50 else 0,
            int(r.get("stars") or 0),
        ),
        reverse=True,
    )

    encoded_ig = urllib.parse.quote(query)
    return {
        "query": query,
        "total_merged_repositories": len(ranked_repos),
        "ranked_repositories": ranked_repos,
        "youtube_creator_videos": yt_data.get("videos", []),
        "reddit_discussions": rd_data.get("posts", []),
        "next_channel_hooks": {
            "instagram_reels_search_url": f"https://www.instagram.com/explore/search/keyword/?q={encoded_ig}",
            "instagram_mcp_server": "insta-manager-acceptance-bridge",
            "agent_reach_cli": "C:/Users/avich/.local/bin/agent-reach.exe",
            "notebooklm_deep_research": {
                "mcp_server": "notebooklm",
                "tool": "research_start",
                "arguments": {"query": f"{query} open source github comparison", "source": "web", "mode": "deep"},
            },
        },
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="Multi-channel open-source tool & GitHub discovery engine.")
    parser.add_argument("query", help="Search query (e.g. 'capcut open source')")
    parser.add_argument("--gh-limit", type=int, default=10, help="Max GitHub search results")
    parser.add_argument("--yt-count", type=int, default=6, help="Number of YouTube creator videos to mine")
    parser.add_argument("--json", action="store_true", help="Output full JSON payload")
    args = parser.parse_args()

    res = run_discovery(args.query, gh_limit=args.gh_limit, yt_count=args.yt_count)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print(f"=== Deep Discovery Results for: {res['query']} ===")
    print(f"\nTop Ranked Repositories ({res['total_merged_repositories']}):")
    for idx, r in enumerate(res["ranked_repositories"][:12], start=1):
        via = ",".join(r.get("discovered_via", []))
        print(f"  {idx:2d}. {r['full_name']} ({r['stars']} stars) [{via}] -> {r['url']}")
        if r.get("description"):
            print(f"      {r['description'][:120]}")
    print(f"\nYouTube Creator Videos Mined ({len(res['youtube_creator_videos'])}):")
    for idx, v in enumerate(res["youtube_creator_videos"], start=1):
        repos_str = ", ".join(v.get("github_repos_mentioned") or []) or "none in description"
        print(f"  {idx:2d}. {v['title']} ({v['channel']}, {v['views']} views) -> {v['url']}")
        print(f"      Repos extracted: {repos_str}")


if __name__ == "__main__":
    main()
