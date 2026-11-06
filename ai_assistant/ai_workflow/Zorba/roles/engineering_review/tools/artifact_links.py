#!/usr/bin/env python3
"""Check inline links in saved review Markdown without accessing the network.

Review artifacts use [label](relative/path) or [label](<relative path>).
Reference-style links, local fragments, directories and absolute local paths
are rejected rather than presented as verified. Code examples are ignored.
This checks artifact navigation, not general Markdown syntax or review truth.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import unquote, urlsplit


INLINE_LINK = re.compile(
    r"(?<!\\)!?\[(?:\\.|[^\]\\\n])*\]"
    r"\((?:<(?P<angle>[^>\n]+)>|(?P<plain>(?:\\.|[^()\s])+))\)"
)
LINK_SYNTAX = re.compile(r"(?<!\\)\[[^\n]*?\](?:\(|\[)|^\s*\[[^\]]+\]:|<a\s", re.I)


def check_report(path: Path) -> Dict[str, Any]:
    """Resolve supported local links from the saved document's own directory."""
    errors: List[str] = []
    external: List[str] = []
    local_count = 0
    fence = ""
    fence_length = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if not fence:
                fence, fence_length = token[0], len(token)
            elif token[0] == fence and len(token) >= fence_length:
                fence = ""
            continue
        if fence:
            continue
        # Ignore links inside code spans without changing a real destination
        # containing backticks or stripping code formatting from its label.
        spans = list(re.finditer(r"(?<!\\)(`+).*?\1", line))
        matches = [
            match for match in INLINE_LINK.finditer(line)
            if not any(span.start() <= match.start() < span.end() for span in spans)
        ]
        remaining = line
        for match in reversed(matches):
            remaining = remaining[:match.start()] + " " * (match.end() - match.start()) + remaining[match.end():]
        remaining = re.sub(r"(?<!\\)(`+).*?\1", "", remaining)
        if LINK_SYNTAX.search(remaining):
            errors.append("line {}: unsupported link syntax; use inline links with encoded destinations or angle brackets".format(line_number))
        for match in matches:
            target = match.group("angle") or match.group("plain")
            try:
                url = urlsplit(target)
                if url.scheme in ("https", "http") and url.netloc:
                    external.append(target)
                    continue
                if url.scheme or url.netloc:
                    raise ValueError("unsupported URI scheme or network path")
                destination = unquote(url.path)
                if not destination or Path(destination).is_absolute() or "\\" in destination:
                    raise ValueError("use a file path relative to this Markdown document")
                if re.search(r":\d+(?::\d+)?$", destination):
                    raise ValueError("put source line numbers in the label, not the filename")
                if url.fragment or url.query:
                    raise ValueError("local fragments/queries are not checked; link the file and put location details in the label")
                resolved = (path.parent / destination).resolve()
                if not resolved.is_file():
                    raise ValueError("target is missing or is a directory: {}".format(resolved))
                local_count += 1
            except (OSError, ValueError) as error:
                errors.append("line {}: {}: {}".format(line_number, target, error))
    return {
        "report": str(path), "ok": not errors,
        "local_files_checked": local_count,
        "external_links_not_checked": external,
        "errors": errors,
    }


def main() -> None:
    """Print a machine-readable validation result and fail on broken links."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path, help="Saved Markdown reports and summaries")
    args = parser.parse_args()
    results = []
    for path in args.reports:
        try:
            results.append(check_report(path.resolve()))
        except (OSError, UnicodeError) as error:
            results.append({"report": str(path), "ok": False, "errors": [str(error)]})
    ok = all(result["ok"] for result in results)
    print(json.dumps({"ok": ok, "reports": results}, indent=2))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
