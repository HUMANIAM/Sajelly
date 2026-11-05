#!/usr/bin/env python3
"""Validate versioned Zorba engineering review contracts and render human reports.

No model calls, reviewed-source edits, commands, or network access. Python >=3.8 and jsonschema.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import quote, urljoin

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_BASE = "https://zorba.invalid/engineering_review/"
STACKS = {"frontend": "FE", "backend": "BE"}


def _registry() -> Registry:
    resources = []
    for path in ROOT.rglob("*.schema.json"):
        key = urljoin(SCHEMA_BASE, path.relative_to(ROOT).as_posix())
        resources.append((key, Resource.from_contents(json.loads(path.read_text(encoding="utf-8")))))
    for stack in STACKS:
        for name in ("request_schema.json", "response_schema.json"):
            path = ROOT / stack / name
            key = urljoin(SCHEMA_BASE, path.relative_to(ROOT).as_posix())
            resources.append((key, Resource.from_contents(json.loads(path.read_text(encoding="utf-8")))))
    return Registry().with_resources(resources)


def validate(kind: str, stack: str, data: dict, *, request: dict | None = None) -> None:
    if stack not in STACKS:
        raise ValueError(f"unknown specialist: {stack}")
    schema_name = "request_schema.json" if kind == "request" else "response_schema.json"
    schema = json.loads((ROOT / stack / schema_name).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, registry=_registry(), format_checker=Draft202012Validator.FORMAT_CHECKER)
    issues = sorted(validator.iter_errors(data), key=lambda e: (list(map(str, e.absolute_path)), e.message))
    if issues:
        issue = issues[0]
        where = "/".join(str(x) for x in issue.absolute_path) or "root"
        raise ValueError(f"{stack} {kind} schema invalid at {where}: {issue.message} ({len(issues)} error(s))")
    if kind == "response":
        _validate_decision(data, stack)
        if request is not None:
            validate("request", stack, request)
            for field in ("review_id", "reviewer", "contract_version"):
                if data[field] != request[field]:
                    raise ValueError(f"response {field} differs from request")
    elif kind != "request":
        raise ValueError(f"invalid contract kind: {kind}")


def _validate_decision(r: dict, stack: str) -> None:
    criteria = r["criteria"]
    ids = {item["id"] for item in criteria}
    expected = {f"U-{i:02d}" for i in range(1, 9)} | {f"{STACKS[stack]}-{i:02d}" for i in range(1, 11)}
    if ids != expected or len(criteria) != len(expected):
        raise ValueError("criteria must include exactly each universal and stack-specific ID once")
    findings = r["findings"]
    by_criterion = {c["id"]: c for c in criteria}
    finding_ids = [f["id"] for f in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise ValueError("finding identifiers must be unique")
    for item in findings:
        if not set(item["criterion_ids"]).issubset(ids):
            raise ValueError(f"finding {item['id']} cites a criterion outside {stack} scope")
    for item in criteria:
        if item["status"] == "fail" and not any(item["id"] in f["criterion_ids"] for f in findings):
            raise ValueError(f"failed criterion {item['id']} requires an evidence-backed finding")
    for finding in findings:
        if finding["severity"] in ("blocker", "required") and not any(
            by_criterion[criterion]["status"] in ("fail", "not_verified")
            for criterion in finding["criterion_ids"]
        ):
            raise ValueError(f"blocking finding {finding['id']} must correspond to failed or unverified criterion")
    for item in criteria:
        if item["status"] == "pass" and not item["evidence"]:
            raise ValueError(f"{item['id']} marked pass without evidence")
        if item["status"] in ("not_verified", "not_applicable") and not item["notes"].strip():
            raise ValueError(f"{item['id']} requires a reason")
    if any(item["status"] == "not_verified" for item in criteria) and not r["verification_assessment"]["gaps"]:
        raise ValueError("not_verified criteria require a verification gap")

    critical_bad = any(c["critical"] and c["status"] in ("fail", "not_verified") for c in criteria)
    bad_findings = any(f["severity"] in ("blocker", "required") for f in findings)
    must_block = critical_bad or bad_findings
    decision = r["decision"]
    if must_block and decision != "block":
        raise ValueError("blocking findings or critical failed/unverified criteria require block")
    if decision == "approve":
        if findings or r["verification_assessment"]["gaps"] or r["residual_risks"] or r["human_decisions_required"]:
            raise ValueError("approve cannot have open findings, gaps, residual risks, or human decisions")
        if any(c["status"] not in ("pass", "not_applicable") for c in criteria):
            raise ValueError("approve requires all applicable criteria pass")
    if decision == "approve_with_notes" and must_block:
        raise ValueError("approve_with_notes cannot hide blocking issues")
    if decision == "block" and not (must_block or findings or r["verification_assessment"]["gaps"] or r["human_decisions_required"]):
        raise ValueError("block must include a reason")


def _md(s: object) -> str:
    """Render untrusted model text as literal Markdown text, not an HTML/MD instruction."""
    value = str(s).replace("\\", "\\\\")
    for symbol in ("*", "_", "`", "[", "]", "<", ">", "#", "|"):
        value = value.replace(symbol, "\\" + symbol)
    return value.replace("\r", " ").replace("\n", " ")


def _file_reference(value: str, report_path: Path | None, project_root: Path | None) -> str:
    """Link only existing repository files; preserve unknown references as text."""
    if report_path is None or project_root is None:
        return _md(value)
    match = re.fullmatch(r"(.+?):[0-9]+(?::[0-9]+)?", value)
    path = Path(match.group(1) if match else value)
    if path.is_absolute():
        return _md(value)
    root = project_root.resolve()
    target = (root / path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return _md(value)
    if not target.is_file():
        return _md(value)
    destination = quote(os.path.relpath(target, report_path.resolve().parent), safe="/.-_")
    return f"[{_md(value)}]({destination})"


def render_response(
    r: dict, *, report_path: Path | None = None, project_root: Path | None = None,
    request: dict | None = None,
) -> str:
    """Turn the reviewer's validated judgment into the engineer's primary report."""
    stack = r["reviewer"]
    validate("response", stack, r, request=request)
    outcomes = {
        "block": "Changes needed before acceptance",
        "approve_with_notes": "No blocking findings; notes remain",
        "approve": "No findings reported",
    }
    required = [f for f in r["findings"] if f["severity"] in ("blocker", "required")]
    optional = [f for f in r["findings"] if f["severity"] in ("suggestion", "question")]
    lines = [
        f"# {stack.capitalize()} review", "",
        f"**{outcomes[r['decision']]}**", "",
        f"Required changes: {len(required)}. Suggestions and questions: {len(optional)}.", "",
    ]
    if request is not None:
        lines += ["## Change reviewed", "", _md(request["goal"]), ""]
    for heading, findings in (("Required changes", required), ("Suggestions and questions", optional)):
        lines += [f"## {heading}", ""]
        if not findings:
            lines += ["None reported.", ""]
        for finding in findings:
            lines += [
                f"### {_md(finding['title'])}", "",
                f"**{_md(finding['category'])}** · {_md(finding['severity'])} · Owner: {_md(finding['owner'])} · {_md(finding['id'])}", "",
                "**Why it matters:** " + _md(finding["risk"]), "",
                "**Where to look:**", "",
            ]
            lines += ["- " + _file_reference(path, report_path, project_root) for path in finding["paths"]] or ["- No file location supplied."]
            lines += ["", "**What the reviewer observed:**", ""]
            lines += ["- " + _md(item) for item in finding["evidence"]]
            lines += ["", "**Requested change:** " + _md(finding["required_resolution"]), "", "**How to verify the fix:**", ""]
            lines += ["- " + _md(item) for item in finding["verification_needed"]] or ["- No additional check specified."]
            lines += [""]
    lines += ["## Verification and limits", "", "**Evidence reviewed:**", ""]
    lines += ["- " + _md(item) for item in r["verification_assessment"]["evidence_reviewed"]] or ["- No verification evidence recorded."]
    gaps = r["verification_assessment"]["gaps"]
    lines += ["", "**Still unverified:**", ""]
    lines += [f"- **{_md(gap['area'])}:** {_md(gap['reason'])} Impact: {_md(gap['impact'])}" for gap in gaps] or ["- No gaps recorded."]
    lines += ["", "## Risks and decisions for the engineer", ""]
    for risk in r["residual_risks"]:
        lines += [f"- {_md(risk['risk'])} Impact: {_md(risk['impact'])} Owner: {_md(risk['owner'])}. Closure: {_md(risk['exit_condition'])}"]
    for decision in r["human_decisions_required"]:
        lines += [f"- {_md(decision['question'])} {_md(decision['context'])} Options: {' / '.join(_md(option) for option in decision['options'])}"]
    if not r["residual_risks"] and not r["human_decisions_required"]:
        lines += ["None recorded."]
    lines += ["", "## Review record", "", "The findings above are the action list. Review context and checklist details follow for traceability.", "",
              "**Reviewer context:** " + _md(r["summary"]), ""]
    if request is not None and request["change"]["diff"] is not None:
        lines += ["**Comparison:** " + _md(request["change"]["diff"]["value"]), ""]
    lines += ["| Criterion | Result | Critical | Assessment and evidence |", "| --- | --- | --- | --- |"]
    for criterion in r["criteria"]:
        detail = criterion["notes"] + (" Evidence: " + "; ".join(criterion["evidence"]) if criterion["evidence"] else "")
        lines += [f"| {_md(criterion['id'])} — {_md(criterion['name'])} | {_md(criterion['status'])} | {'yes' if criterion['critical'] else 'no'} | {_md(detail)} |"]
    metadata = r["metadata"]
    lines += ["", f"- Review: {_md(r['review_id'])}",
              f"- Reviewer: {_md(stack)} engineering reviewer",
              f"- Recorded: {_md(metadata['reviewed_at'])}",
              f"- Contract: {_md(r['contract_version'])}; decision: {_md(r['decision'])}",
              f"- Self review: {str(metadata['self_review']).lower()}",
              "- Authority: advisory; human approval separate.",
              "- Contract references: " + "; ".join(_md(ref) for ref in metadata["contract_refs"]), ""]
    return "\n".join(lines)


def write_report(path: Path, report: str) -> None:
    """Save a Markdown report atomically after checking its local navigation."""
    from artifact_links import check_report

    if path.suffix.lower() != ".md":
        raise ValueError("report output must be a .md file")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(path.parent), suffix=".md", delete=False) as output:
            temporary = Path(output.name)
            output.write(report)
        result = check_report(temporary)
        if not result["ok"]:
            raise ValueError("report link validation failed: " + "; ".join(result["errors"]))
        os.replace(str(temporary), str(path))
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and render Zorba engineering review contracts")
    parser.add_argument("action", choices=("request", "response", "render"))
    parser.add_argument("stack", choices=STACKS)
    parser.add_argument("file", type=Path)
    parser.add_argument("--request", type=Path, help="Request to correlate against for response/render")
    parser.add_argument("--output", type=Path, help="Render and atomically save the reviewer-owned Markdown report")
    parser.add_argument("--project-root", type=Path, help="Resolve source references into document-relative links when saving a report")
    args = parser.parse_args()
    if (args.output or args.project_root) and args.action != "render":
        parser.error("--output and --project-root apply only to render")
    if args.project_root and not args.output:
        parser.error("--project-root requires --output so links have a known destination")
    if args.output and not args.request:
        parser.error("saving a report requires --request for correlation validation")
    if args.project_root and not args.project_root.is_dir():
        parser.error("--project-root must be an existing repository directory")
    if args.output and args.output.resolve() in (args.file.resolve(), args.request.resolve()):
        parser.error("report output must not replace the request or response JSON")
    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
        request = json.loads(args.request.read_text(encoding="utf-8")) if args.request else None
        kind = "request" if args.action == "request" else "response"
        validate(kind, args.stack, data, request=request)
        if args.action == "render":
            report = render_response(data, report_path=args.output, project_root=args.project_root, request=request)
            if args.output:
                write_report(args.output, report)
                print(f"REPORT {args.output}")
            else:
                print(report)
        else:
            print(f"VALID {args.stack} {kind} ({data['review_id']})")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"INVALID: {exc}\n")


if __name__ == "__main__":
    main()
