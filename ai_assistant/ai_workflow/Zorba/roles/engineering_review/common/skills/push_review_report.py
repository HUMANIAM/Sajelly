#!/usr/bin/env python3
"""Attach a reviewer-owned Markdown report to a PR and verify its read-back.

Uses authenticated GitHub CLI calls. Default mode prepares without publishing.
Publication creates a Conversation comment, never a review approval or merge.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote, unquote, urlsplit


TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from artifact_links import INLINE_LINK, check_report  # noqa: E402


def gh_api(endpoint: str, payload: Optional[Dict[str, Any]] = None,
           paginate: bool = False) -> Any:
    """Use explicit JSON input; never interpolate report content into a shell."""
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if paginate:
        command += ["--paginate", "--slurp"]
    if payload is not None:
        command += ["--method", "POST", "--input", "-"]
    result = subprocess.run(
        command, input=json.dumps(payload) if payload is not None else None,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, "GH_PROMPT_DISABLED": "1", "GH_PAGER": "cat"},
        check=False,
    )
    if result.returncode:
        raise RuntimeError("GitHub CLI failed; do not blindly retry publication: " + result.stderr.strip()[:2000])
    return json.loads(result.stdout)


def github_links(text: str, report: Path, project: Path, repository: str,
                 head: str, tracked: set) -> Tuple[str, List[str]]:
    """Rebase real inline source links to immutable GitHub blob URLs.

    Preserve code examples, prose and reviewer conclusions. Local evidence that
    is absent from the PR tree remains labelled text, not a fabricated blob link.
    """
    unpublished: List[str] = []
    lines = []
    fence = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if not fence:
                fence, fence_length = token[0], len(token)
            elif token[0] == fence and len(token) >= fence_length:
                fence = ""
            lines.append(line)
            continue
        if fence:
            lines.append(line)
            continue
        spans = list(re.finditer(r"(?<!\\)(`+).*?\1", line))
        for match in reversed(list(INLINE_LINK.finditer(line))):
            if any(span.start() <= match.start() < span.end() for span in spans):
                continue
            target = match.group("angle") or match.group("plain")
            url = urlsplit(target)
            if url.scheme in ("http", "https"):
                continue
            local = (report.parent / unquote(url.path)).resolve()
            try:
                path = local.relative_to(project).as_posix()
            except ValueError as error:
                raise ValueError("Refusing to publish a link outside the project: " + target) from error
            original = match.group(0)
            close = original.rfind("](")
            if path in tracked:
                destination = "https://github.com/{}/blob/{}/{}".format(repository, head, quote(path, safe="/"))
                replacement = original[:close + 2] + destination + ")"
            else:
                unpublished.append(path)
                replacement = original[:close + 1].lstrip("!")[1:-1] + " (local file; not published)"
            line = line[:match.start()] + replacement + line[match.end():]
        lines.append(line)
    return "".join(lines), sorted(set(unpublished))


def publish_report(args: argparse.Namespace) -> Dict[str, Any]:
    """Prepare once, optionally post once, then verify the exact stored body."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        raise ValueError("--repo must be owner/repository")
    if args.pr < 1:
        raise ValueError("--pr must be a positive pull request number")
    if not args.scope_note.strip():
        raise ValueError("Describe the report's actual reviewed snapshot in --scope-note")
    report = args.report.resolve()
    project = args.project_root.resolve()
    source_bytes = report.read_bytes()
    checked = check_report(report)
    if not checked["ok"]:
        raise ValueError("Report has invalid local navigation: " + "; ".join(checked["errors"]))
    if report.read_bytes() != source_bytes:
        raise ValueError("Report changed during validation; no publication attempted")
    source = source_bytes.decode("utf-8")
    if not source.strip():
        raise ValueError("Refusing to attach an empty report")
    protected = [report] + [path.resolve() for path in (args.response, args.request) if path]
    if args.body_output and args.body_output.resolve() in protected:
        raise ValueError("Prepared comment output must not replace the report or JSON inputs")
    metadata = ""
    if args.response or args.request:
        if not (args.response and args.request):
            raise ValueError("--response and --request must be supplied together")
        from review_contract import _md, render_response, validate
        response = json.loads(args.response.read_text(encoding="utf-8"))
        request = json.loads(args.request.read_text(encoding="utf-8"))
        validate("response", response["reviewer"], response, request=request)
        expected = render_response(response, report_path=report, project_root=project, request=request)
        if source != expected:
            raise ValueError("Report differs from the supplied reviewer JSON; render it with the canonical renderer before publishing")
        metadata = "Reviewer decision: `{}`. Review ID: `{}`.\n\n".format(_md(response["decision"]), _md(response["review_id"]))
    pr = gh_api("repos/{}/pulls/{}".format(args.repo, args.pr))
    if pr["state"] != "open":
        raise ValueError("Refusing to publish to a closed PR")
    head = pr["head"]["sha"]
    tree = gh_api("repos/{}/git/trees/{}?recursive=1".format(args.repo, head))
    if tree.get("truncated"):
        raise ValueError("GitHub tree is truncated; source links cannot be verified")
    tracked = {item["path"] for item in tree["tree"] if item["type"] == "blob"}
    rendered, unpublished = github_links(source, report, project, args.repo, head, tracked)
    report_hash = hashlib.sha256(source_bytes).hexdigest()
    marker = "<!-- zorba-review-report:{} -->".format(report_hash)
    body = (
        marker + "\n## Engineering review report\n\n"
        + "**Reviewed scope:** " + args.scope_note.strip() + "\n\n"
        + metadata
        + "PR head at publication: `{}`. Source links below point to that revision; this does not assert that the report reviewed that head.\n\n".format(head)
        + "The report is advisory. Publication does not approve or merge this PR. Supporting local evidence is not uploaded by this command.\n\n"
        + "Report SHA-256: `{}`.\n\n---\n\n".format(report_hash)
        + rendered
    )
    if len(body.encode("utf-8")) > 60000:
        raise ValueError("Report exceeds the conservative single-comment size limit; choose a separately authorized file publication method")
    if args.body_output:
        args.body_output.parent.mkdir(parents=True, exist_ok=True)
        args.body_output.write_text(body, encoding="utf-8")
    result = {
        "action": "prepared", "pr": pr["html_url"], "pr_head": head,
        "report_sha256": report_hash,
        "published_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "unpublished_local_targets": unpublished,
        "external_links_not_checked": checked["external_links_not_checked"],
    }
    if not args.publish:
        return result
    pages = gh_api("repos/{}/issues/{}/comments?per_page=100".format(args.repo, args.pr), paginate=True)
    existing = [comment for page in pages for comment in page if comment["body"].startswith(marker)]
    if len(existing) > 1:
        raise ValueError("Multiple existing attachments match this report; resolve them without another post")
    if existing:
        comment = existing[0]
        if comment["body"] != body:
            raise ValueError("This report is already attached with different context; do not overwrite review history")
        result["action"] = "already_attached"
    else:
        # No automatic POST retries: a lost response may still mean publication.
        if gh_api("repos/{}/pulls/{}".format(args.repo, args.pr))["head"]["sha"] != head:
            raise ValueError("PR head moved while preparing the report; no comment posted")
        comment = gh_api("repos/{}/issues/{}/comments".format(args.repo, args.pr), {"body": body})
        result["action"] = "published"
    stored = gh_api("repos/{}/issues/comments/{}".format(args.repo, comment["id"]))
    if stored["body"] != body or not stored["issue_url"].endswith("/issues/{}".format(args.pr)):
        raise RuntimeError("Report was posted but read-back verification failed; inspect the existing comment before retrying")
    result.update({"comment_url": stored["html_url"], "comment_id": stored["id"], "verified": True})
    result["head_changed_after_publication"] = gh_api("repos/{}/pulls/{}".format(args.repo, args.pr))["head"]["sha"] != head
    return result


def main() -> None:
    """Use --publish only after explicit authorization to attach the report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--scope-note", required=True, help="Actual reviewed revision/snapshot and freshness limits")
    parser.add_argument("--response", type=Path)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--body-output", type=Path, help="Save the prepared GitHub comment locally")
    parser.add_argument("--publish", action="store_true", help="Publish once and verify read-back; requires explicit user authorization")
    args = parser.parse_args()
    try:
        print(json.dumps(publish_report(args), indent=2))
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
