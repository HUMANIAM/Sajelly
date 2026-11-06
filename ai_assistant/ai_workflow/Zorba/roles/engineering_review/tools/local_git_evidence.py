#!/usr/bin/env python3
"""Read-only, bounded Git evidence for Zorba engineering reviewers.

No shell; no mutations; no network; no external diff/textconv hooks.
Emits one JSON object; any truncated output is explicitly flagged.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

MAX_BYTES = 400_000


class EvidenceError(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    env = {**os.environ, "GIT_PAGER": "cat", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    cmd = ["git", "-c", "core.pager=cat", "-c", "diff.external=", "-C", str(repo), *args]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
    if p.returncode:
        raise EvidenceError(f"git command failed ({p.returncode}): {p.stderr.decode('utf-8', 'replace')[:500].strip()}")
    return p.stdout.decode("utf-8", "replace")


def ref_sha(repo: Path, value: str) -> str:
    # Force refs to resolve to commits, then use immutable SHA for subsequent reads.
    if not value or value.startswith("-") or value.startswith(":"):
        raise EvidenceError("invalid Git revision")
    sha = git(repo, "rev-parse", "--verify", f"{value}^{{commit}}").strip()
    if len(sha) not in (40, 64) or not all(c in '0123456789abcdef' for c in sha):
        raise EvidenceError("revision did not resolve to a commit SHA")
    return sha


def safe_path(path: str) -> str:
    posix = PurePosixPath(path)
    if not path or path.startswith(("/", "-")) or "\\" in path or any(p in (".", "..", "") for p in path.split("/")):
        raise EvidenceError("file must be a normal relative repository path")
    return str(posix)


def bounded(text: str) -> dict:
    data = text.encode("utf-8")
    truncated = len(data) > MAX_BYTES
    if truncated:
        data = data[:MAX_BYTES]
    return {"text": data.decode("utf-8", "ignore"), "truncated": truncated, "total_bytes": len(text.encode("utf-8"))}


def run(args: argparse.Namespace) -> dict:
    repo = Path(args.repo).resolve(strict=True)
    if not (repo.is_dir() and git(repo, "rev-parse", "--is-inside-work-tree").strip() == 'true'):
        raise EvidenceError("not a Git worktree")
    if args.command in ("overview", "diff"):
        base = ref_sha(repo, args.base)
        head = ref_sha(repo, args.head)
        merge_base = git(repo, "merge-base", base, head).strip()
        range_arg = f"{merge_base}..{head}"
        out = {"source": "local_git", "base_sha": base, "head_sha": head,
               "merge_base_sha": merge_base, "comparison": "merge_base..head"}
        if args.command == "overview":
            files = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-status", "-z", merge_base, head)
            # git diff -z: entries use NUL separators; renames have two paths.
            parts = files.split("\0")
            entries = []
            idx = 0
            while idx < len(parts) and parts[idx]:
                status = parts[idx]; idx += 1
                old_path = parts[idx]; idx += 1
                new_path = None
                if status.startswith(("R", "C")):
                    new_path = parts[idx]; idx += 1
                entries.append({"status": status, "path": new_path or old_path,
                                **({"previous_path": old_path} if new_path else {})})
            out["changed_files"] = entries
            out["commits"] = bounded(git(repo, "log", "--format=%H %s", range_arg))
            out["worktree_status"] = bounded(git(repo, "status", "--short", "--untracked-files=no"))
        else:
            options = ["diff", "--no-ext-diff", "--no-textconv", "--no-color", merge_base, head]
            if args.path:
                options += ["--", safe_path(args.path)]
            out["patch"] = bounded(git(repo, *options))
        return out
    revision = ref_sha(repo, args.revision)
    out = {"source": "local_git", "revision_sha": revision}
    path = safe_path(args.path)
    if args.command == "file":
        # Blob at a pinned revision; no working-tree changes or exec of textconv filters.
        out["path"] = path
        out["content"] = bounded(git(repo, "show", "--no-ext-diff", "--no-textconv", f"{revision}:{path}"))
    elif args.command == "history":
        out["path"] = path
        out["history"] = bounded(git(repo, "log", "-n", "25", "--format=%H %s", revision, "--", path))
    else:
        raise EvidenceError("unsupported command")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Existing local Git checkout")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("overview", "diff"):
        p = sub.add_parser(name)
        p.add_argument("--base", required=True)
        p.add_argument("--head", default="HEAD")
        if name == "diff":
            p.add_argument("--path")
    for name in ("file", "history"):
        p = sub.add_parser(name)
        p.add_argument("--revision", default="HEAD")
        p.add_argument("--path", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args), ensure_ascii=False))
    except (EvidenceError, OSError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
