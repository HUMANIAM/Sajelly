# AI assistant tool registry

> “Raise your words, not your voice. It is rain that raises flowers, not
> thunder.”
>
> — Rumi

This directory is the registry for small tools that help Sajelly’s human and
agent engineers work with greater clarity, safety, and effectiveness. Tools may
support onboarding, verification, documentation, development, testing, or other
repeatable engineering work.

Human and agent engineers are welcome to add a tool when it removes a real
friction, makes important evidence easier to obtain, or turns an error-prone
manual activity into a clear and reviewable workflow. A tool should assist
engineering judgment, not hide decisions or create an autonomous process.

## Registered tools

| Tool | Entry point | Purpose | Status | Tests |
| --- | --- | --- | --- | --- |
| Review execution planner | [`src/review_execution.py`](src/review_execution.py) via `zorba_cli.py --review-plan` | Validates configurable subject profiles and resolves model/effort assignments with risk and system-criticality floors. Exposes validated save for a future UI. | Local planning; no agent launches | Existing adapter regression suite plus recorded manual/launch verification; no new test cases |
| Review artifact link checker | [`../roles/engineering_review/tools/artifact_links.py`](../roles/engineering_review/tools/artifact_links.py) | Checks saved Markdown file links from the document location; fails on broken targets or unsupported link forms. | Local checks only; external URLs unchecked | Real review artifacts and temporary malformed-link scenarios; no new test cases |
| Review report publisher | [`../roles/engineering_review/common/skills/push_review_report.py`](../roles/engineering_review/common/skills/push_review_report.py) | Attaches an authorized reviewer report through GitHub CLI and verifies its exact read-back. | Explicit publication; no approval/merge | Local preparation checks and actual PR attachment/read-back |
| Zorba setup CLI | [`src/zorba_cli.py`](src/zorba_cli.py) | Checks the vendor-neutral Zorba definitions and manages consent-driven Codex setup. Reports Claude specialist integration honestly as work in progress. | Codex supported; Claude WIP | [`tests/test_zorba_cli.py`](tests/test_zorba_cli.py) |

## Directory contract

```text
tools/
├── README.md       # Registry, ownership rules, and usage
├── pyproject.toml  # Python version, dependencies, and test configuration
├── src/            # Reusable tool implementations and entry points
└── tests/          # Executable behavior and regression evidence
```

Keep feature-specific experiments in the relevant feature workspace or
`ai_assistant/tmp/`. Promote a script here when it has a reusable purpose, a
stable interface, an owner or maintenance boundary, and meaningful tests.

## Using the Zorba setup CLI

Run commands from the repository root. Use the shared Zorba environment (Python 3.8+) with the declared dependencies
installed. Review execution settings are validated with JSON Schema.

Show the help:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py
```

Inspect vendor-neutral, Codex, and Claude status without changing files:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --check
```

Set up or sync Codex with explicit contributor control:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --setup codex
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --sync codex
```

Claude specialist setup remains work in progress. Claude actions report that
boundary and do not create partial configuration.

When sync finds Codex agent files that are no longer listed in
`specialists.json`, it shows their names and asks about each deletion
separately. Declining keeps that file and leaves the readiness check non-green
so the remaining drift is visible.

## Development setup

The setup CLI keeps its Python and test dependencies in
[`pyproject.toml`](pyproject.toml), rather than in Sajelly application
requirements. Reviewer tools use the same Zorba environment and declare their
additional dependency in `roles/engineering_review/requirements.txt`.

From the repository root, create the Zorba-local environment and install its
development dependencies:

```console
python3 -m venv ai_assistant/ai_workflow/Zorba/.venv
ai_assistant/ai_workflow/Zorba/.venv/bin/python -m pip install 'ai_assistant/ai_workflow/Zorba/tools[dev]' -r ai_assistant/ai_workflow/Zorba/roles/engineering_review/requirements.txt
```

Run the complete test suite:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/pytest -c ai_assistant/ai_workflow/Zorba/tools/pyproject.toml
```

`project.dependencies` contains runtime dependencies shared by every tool.
`project.optional-dependencies.dev` contains test and development dependencies.
Add a dependency only when the standard library or an existing dependency does
not satisfy a real tool requirement.

### Discoverability for people and agents

The registry table is the discovery surface. A human or agent engineer should
be able to scan it and learn what a tool does, where its public entry point
lives, whether it is ready for use, and which tests demonstrate its contract.
Register a reusable tool in the table in the same change that introduces it.
Do not require someone to search `src/` to discover supported capabilities.

## Adding or changing a tool

1. Start with a concrete human or engineering need. State the behavior the
   tool should improve and what it must not do.
2. Keep the interface small and explain it through `--help`, a clear README
   registry entry, or both.
3. Keep canonical knowledge in its owning document. A tool may read or render
   that knowledge, but should not become a competing source of truth.
4. Preserve user control for file changes, external actions, credentials, or
   other meaningful side effects. Make read-only and mutating operations easy
   to distinguish.
5. Put reusable implementation in `src/` and pytest behavioral tests in
   `tests/`. Prefer the simplest test boundary that demonstrates the risk.
6. Use synthetic fixtures. Never put customer data, secrets, tokens, or private
   information in tool code, tests, examples, or generated evidence.
7. Declare runtime or development dependencies only in `pyproject.toml`.
8. Register the tool in the table above with its purpose, maturity, entry point,
   tests, and important limitations so human and agent engineers can find it.
9. Run the relevant tests and record actual results. Do not claim runtime or
   integration behavior that was not observed.

Tools follow the same review expectations as product code: changes should be
small enough to understand, errors and limitations should be explicit, and
another engineer should be able to reproduce the evidence and maintain the
result.
