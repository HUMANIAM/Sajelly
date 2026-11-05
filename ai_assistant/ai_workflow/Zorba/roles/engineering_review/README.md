# Engineering review agents

`roles/engineering_review/` is the single canonical home for version 1.1 review
instructions, contracts, examples, tools and tests. Zorba's Codex frontend and
backend review agents use this directory. It incorporates the agreed focused review workflow,
engineering/project memory, component metadata and JSON-only contract authority.

## Layout

```text
engineering_review/
  README.md
  common/       # Shared workflow, policies, memory and schemas
  frontend/     # Frontend role, checks, contracts and examples
  backend/      # Backend role, checks, contracts and examples
  tools/        # Contract rendering, Git evidence and artifact link validation
  tests/        # Existing contract and Git evidence acceptance suites
```

The top-level `roles/frontend_engineering_review.md` and
`roles/backend_engineering_review.md` are thin adapter entry points. They refer
here and do not maintain another copy of reviewer policy. Edit reviewer policy
and contracts only in this directory.

## Entry points and connections

```text
specialists.json
  -> roles/frontend_engineering_review.md or roles/backend_engineering_review.md
  -> this bundle's frontend/role.md or backend/role.md
  -> common/review_protocol.md (one workflow)
  -> relevant common responsibilities and stack review_rules.md
  -> JSON request/response schemas (machine contract)
  -> tools/review_contract.py (validation and human report rendering)
```

`common/review_tool_access.md` and `common/reviewer_tools.json` describe evidence
capabilities. `tools/local_git_evidence.py` supplies actual read-only local Git
access; remote PRs use approved connected GitHub tools. The manifest does not
install tools or grant permissions. `common/common.schema.md` is for humans
only; reviewers must not read it. JSON schemas are the contract source of truth.

## Common way of working

Follow the [shared workflow](common/review_protocol.md#common-review-workflow):
resolve the baseline/proposed revisions, inspect the complete changeset, select
relevant hats, use affected [component metadata](common/component_metadata.md)
to locate necessary context, consult automated checks, then report findings.
Review fast and safely with enough scope and context; do not audit the whole
repository. The eighteen criterion rows provide concise coverage accounting,
not eighteen independent investigations. Unaffected areas are `not_applicable`;
material evidence gaps are `not_verified`. Reviewers own technical judgment but
cannot merge or grant human sign-off.

For explicitly requested parallel reviews, both specialists use the same
[parallel review procedure](common/review_protocol.md#parallel-review-when-requested):
assign relevant perspectives, wait for all contributions, and have the lead
reviewer reconcile one validated result and its engineer-facing Markdown report. The parent only
returns the reviewer-produced report location. The split into security, test gaps and maintainability is an example,
not a required agent roster.

## Setup and verification

Run from the repository root, using Python 3.8+ and the shared Zorba environment:

```bash
python3 -m venv ai_assistant/ai_workflow/Zorba/.venv
ai_assistant/ai_workflow/Zorba/.venv/bin/python -m pip install 'ai_assistant/ai_workflow/Zorba/tools[dev]' -r ai_assistant/ai_workflow/Zorba/roles/engineering_review/requirements.txt
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --sync codex
```

Start a fresh Codex session after sync. See the
[Codex adapter](../../adapters/codex/README.md#engineering-review-agents)
for invocation prompts and permission boundaries, including
[VS Code instructions](../../adapters/codex/README.md#invoke-reviewers-from-the-vs-code-extension). No custom model or global
Codex configuration is required.

For bundle commands, change into this directory:

```bash
../../.venv/bin/python tools/review_contract.py request backend backend/examples/request.json
../../.venv/bin/python tools/review_contract.py response backend backend/examples/response_block.json --request backend/examples/request.json
../../.venv/bin/python tools/review_contract.py render frontend frontend/examples/response_approve.json --request frontend/examples/request.json
../../.venv/bin/python -m unittest discover -s tests -v
../../.venv/bin/python tools/local_git_evidence.py --repo /path/to/checkout overview --base BASE_SHA --head HEAD_SHA
../../.venv/bin/python tools/local_git_evidence.py --repo /path/to/checkout diff --base BASE_SHA --head HEAD_SHA
```

Local evidence compares **merge-base to head**, reports both requested base and
effective merge-base, caps returned content, and marks truncation. It reads
committed revisions; it does not inspect uncommitted changes, PR discussions or
remote CI. Do not treat missing capabilities as successfully verified evidence.
The examples are synthetic. Passing tests proves contracts and tools, not AI
judgment or live Codex invocation. Reviews remain advisory and human-owned.

## Configurable subjects and reasoning

[review_execution.json](common/review_execution.json) is the single editable
source for profiles and subjects. The planner raises helper assignments to the
higher change-risk/system-criticality floor. At low risk in a low-criticality
system, the initial base assignments are:

| Subject | Model | Reasoning |
| --- | --- | --- |
| Maintainability and local clarity | `gpt-6-luna` | `medium` |
| Test gaps; configuration and dependencies | `gpt-6.1-sol` | `medium` |
| Architecture/design; security/privacy; production/data; infrastructure | `gpt-6.1-sol` | `high` |
| Safety and critical impact | `gpt-6-astra` | `high` |

The lead defaults to `gpt-6.1-sol`/`high` for synthesis, configured independently.
High risk raises every selected helper to at least Sol/high; critical risk raises
helpers to Astra/high. See [model selection rules](common/review_protocol.md#model-and-reasoning-selection)
for risk assessment, launch requirements and unavailable-model handling. The table
is explanatory; the editable JSON is authoritative.

`zorba_ui` is not implemented here. Its future settings form can use
[review_execution.schema.json](common/review_execution.schema.json) and the
`load_settings`, `validate_settings`, `save_settings`, and `review_plan` functions
in [review_execution.py](../../tools/src/review_execution.py). Save validates before
atomic replacement; the UI must manage user authorization and concurrent edits.
The model catalog is configurable but does not discover account availability.
The planner never launches agents or changes global Codex configuration.

From the repository root:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --review-plan --subjects testing security --risk high --system-criticality high
```

Profile names express review depth. Changing their models requires human
calibration on representative changes; a high label cannot guarantee capability.
The initial choices follow [official Codex guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
about narrow versus demanding work. Validate quality with real reviewed examples
before treating these defaults as a proven risk policy.

## Verify delivered report links

Validate saved navigation separately from review JSON. From the repository root:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/roles/engineering_review/tools/artifact_links.py ai_assistant/tmp/engineering_review_evaluation/final-summary.md ai_assistant/tmp/engineering_review_evaluation/001/review.md
```

[artifact_links.py](tools/artifact_links.py) resolves inline local links relative
to each Markdown file and exits nonzero for broken or unsupported links. External
HTTP(S) links are listed as unchecked; no network calls are made. This validates
navigation, not review truth. Both reviewers and the parent handoff follow the
[shared delivery rule](common/review_protocol.md#saved-artifact-links-and-handoff-validation).

## Primary deliverable for engineers

The reviewer owns `review.md`, rendered from validated JSON. It leads with required
changes, separates suggestions, explains evidence and verification limits, and
keeps checklist bookkeeping at the end. Zorba/the parent returns the report's
location; it does not write another technical summary. See the shared
[report contract](common/review_protocol.md#reviewer-owned-report-and-handoff).

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/roles/engineering_review/tools/review_contract.py render backend <output>/response.json --request <output>/request.json --output <output>/review.md --project-root .
```

The renderer's checked output mode constructs document-relative source links only
for existing files inside the project. It leaves unknown references as text and
preserves the original JSON. The parent provides the output directory before
assigning the review.

## Attach the report to a PR

Use the shared [push-review-report skill](common/skills/push-review-report/SKILL.md)
only when publication is authorized. Its helper at
[common/skills/push_review_report.py](common/skills/push_review_report.py) posts
the full reviewer-owned Markdown as a PR Conversation comment, converts source
links to verified files at the pinned head, and fetches the comment back to
verify its exact body. It requires an honest scope note and never grants approval.
Local evidence is not uploaded; unavailable remote targets are labelled as such.
