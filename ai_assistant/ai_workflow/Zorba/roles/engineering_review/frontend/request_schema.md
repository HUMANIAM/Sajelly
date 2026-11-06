# Frontend Review Request Contract

**Machine contract:** [`request_schema.json`](request_schema.json) (JSON Schema 2020-12, version 1.1).\
**Sample:** [`examples/request.json`](examples/request.json).\
Validate before invoking the reviewer. JSON is used between Zorba and specialists; this Markdown describes its meaning to engineers.

## Required fields

| Field | Meaning |
| --- | --- |
| `contract_version` | Exactly `1.1`; version contract changes rather than silently changing payload meaning. |
| `review_id`, `reviewer` | Stable review correlation; `reviewer` must equal `frontend`. |
| `stage` | `architecture`, `design`, or `implementation`. |
| `goal`, `requirements` | Why this change exists and what behavior must be achieved; at least one requirement. |
| `non_goals`, `assumptions` | Explicit things *not* changed and assumptions requiring verification. |
| `source_of_truth_refs` | Authoritative relevant requirements/approved decisions. A reference may have `available:false`; absence must be handled honestly. |
| `change.changed_files`, `.diff`, `.artifact_refs` | Reviewed scope. Implementation requires a non-null diff reference. A `pull_request` locator may omit the initial file inventory because the reviewer retrieves it; other diff kinds require at least one changed file. Design stages may use artifact refs. |
| `project_context` | Actual repo root, README, physical structure or equivalent, architecture refs, nearest stable examples. |
| `frontend_context` | Stack-specific actual tech and applicable API/runtime/design or persistence context. |
| `risk` | Assessed change risk and areas; reviewer must independently verify and adjust conclusions. |
| `verification` | Recorded commands/status/evidence; report whether commands ran, failed, were blocked, or not run. |
| `known_gaps` | Known missing information, unresolved tests, and limits on review. |

## Reference behavior

An `artifactReference` includes `kind` (`path`, `url`, `inline`, `git_ref`, `command_output`), `location`, `purpose`, and `available`. A claimed location is **not** proof of accessibility or successful review. Inspect references needed to assess the change; report a gap when a necessary reference is unavailable. Do not load every reference automatically. A `diff` may identify a `git_range`, file, inline text, or pull request; the host must be able to resolve it.

The requester must not label an unavailable or partial diff as complete. Missing context is not filled in by imagination. The receiving reviewer validates its own domain input; Zorba transports the message and preserves correlation.

## Project adaptation

The source material came from WebAcademy. Use the **target repository's** applicable policies and affected component metadata before applying frontend/backend pattern examples; consult architecture references only where relevant to the change. Do not require a given framework, filename, authentication mechanism, transaction tool, or layer count unless the target repo owns that rule.

## Output

The reviewer saves its validated JSON and produces `review.md` using the canonical renderer and [`response_template.md`](response_template.md) before completing. It then returns the one validated JSON object through the agent channel. The parent only delivers the report location; see the shared [report contract](../common/review_protocol.md#reviewer-owned-report-and-handoff).

## Focused comparison and component context

Resolve and record the baseline and proposed revision before reviewing. For an
artifact change, identify the prior/approved version, or explicitly state an absent
baseline for a new component. A file, inline diff or PR must identify the comparison
as well as the changed content. Supply affected `component_name.meta` files through
`change.artifact_refs` to explain purpose and direct internal/external dependencies.
Those references guide targeted inspection; they are not a mandatory reading list.
See the [common workflow](../common/review_protocol.md#common-review-workflow).

## Git evidence access

For GitHub, use a `pull_request` locator such as `owner/repo#123`. Resolve its
base/head SHAs and retrieve the actual file inventory and diff using approved
read-only tools. For local Git, use the bundled `tools/local_git_evidence.py`.
See [review tool access](../common/review_tool_access.md). A tool manifest documents
expected capabilities; it does not grant access or install a connector.
