# Shared engineering review schema

**Audience: humans only.** Reviewing agents must not read this file. JSON schemas are the single source of truth for review data contracts; this document explains them and adds no contract rules. If the two disagree, follow JSON.

Human reference for [common.schema.json](common.schema.json), the machine-readable JSON Schema Draft 2020-12 definition library used by frontend and backend review contracts.

## How validation works

JSON values have types: object, array, string, number, integer, boolean, and null. This schema explicitly constrains every shared record and field. The JSON schema is the validation authority; this document explains its meaning.

This schema keeps shared review data consistent across frontend and backend reviewers. It defines common records, such as evidence references, risks, and findings. Each specialist’s request and response schemas use these definitions to validate a complete review message.

Every definition below is an object and rejects unknown properties (`additionalProperties: false`). Required fields must be present. Optional fields may be omitted; omission is different from null. Only `verificationRecord.evidence_ref` accepts null. Arrays may be empty unless a minimum is stated. String lengths count characters; a nonempty string is not necessarily nonblank. Enum values are exact and case-sensitive.

## Definitions

### artifactReference

Points reviewers to one artifact that provides context or evidence.

The producer is responsible for stating what the artifact is, where to find it, why it matters, and whether it was available when the review request was assembled. Setting `available` to false preserves a known-but-missing dependency instead of silently omitting it.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `kind` | string | Yes | Allowed: `path`, `url`, `inline`, `git_ref`, `command_output` | How to interpret `location`: `path` is a repository or filesystem path, `url` is a web address, `inline` is content embedded by the containing document, `git_ref` identifies Git state, and `command_output` identifies captured command results. |
| `location` | string | Yes | Minimum characters: 1 | Locator for the artifact, formatted according to `kind`. It must be specific enough for a reviewer to retrieve or identify the same evidence. |
| `purpose` | string | Yes | Minimum characters: 1 | Short explanation of what review question this artifact helps answer; do not merely repeat its filename or location. |
| `available` | boolean | Yes | Type only | Whether the artifact was accessible when this reference was produced. `false` signals an evidence gap that the reviewer must account for. |

### diffReference

Identifies the exact baseline-to-proposed changeset in scope. Resolve and record both revisions before review; do not infer an unstated comparison. File, inline and pull-request references must identify their comparison as well as changed content.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `kind` | string | Yes | Allowed: `git_range`, `file`, `inline`, `pull_request` | How `value` identifies the change set: `git_range` is a revision comparison, `file` points to a stored diff, `inline` embeds the diff in the containing document, and `pull_request` identifies a reviewable PR. |
| `value` | string | Yes | Minimum characters: 1 | Concrete comparison reference according to kind: prefer a pinned baseline..proposed Git range. Stored or inline diffs and pull requests must identify their baseline and proposed state. The schema validates a nonempty string; the reviewer must verify comparison identity and accessibility. |

### changedFile

Declares one file that the change author considers part of the review scope.

This record helps reviewers reconcile the claimed scope with the actual diff and route files to the appropriate architectural layers. Notes should explain exceptional cases such as generated files, cross-layer responsibilities, or renames.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `path` | string | Yes | Minimum characters: 1 | Repository-relative path to the file after the change; for deleted files, use the former path. |
| `status` | string | Yes | Allowed: `added`, `modified`, `deleted`, `renamed` | File operation represented by the diff: newly created, edited in place, removed, or moved/renamed. |
| `claimed_layers` | array of string | Yes | Unique items; Each item: at least 1 character(s) | Architectural or application layers affected by this file, using project-defined layer names. Multiple values are allowed for cross-layer changes; an empty array means no layer was claimed. |
| `notes` | string | No | Type only | Optional reviewer context that cannot be inferred from the path, status, or claimed layers. |

### verificationRecord

Records one check performed against the proposed change.

The person or automation producing the record is responsible for naming the reproducible command or procedure, reporting its true outcome, and summarizing useful evidence. A blocked or skipped check remains visible rather than being presented as a pass.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `command` | string | Yes | Minimum characters: 1 | Exact command or clearly named manual procedure used for the check, written so another engineer can reproduce it. |
| `status` | string | Yes | Allowed: `passed`, `failed`, `not_run`, `blocked` | Observed outcome: `passed` or `failed` when executed, `not_run` when intentionally omitted, and `blocked` when execution was attempted but could not proceed. |
| `summary` | string | Yes | Minimum characters: 1 | Human-readable result, including the relevant behavior observed and, for `failed`, `not_run`, or `blocked`, the reason and impact. |
| `evidence_ref` | artifactReference object or null | No | Referenced artifactReference constraints apply when non-null | Reference to logs, screenshots, reports, or other detailed evidence. Use null when no separate artifact exists; the summary must still be meaningful. |

### risk

Communicates the engineering risk carried by a proposed change.

The assessor is responsible for selecting the highest credible impact level, naming every materially exposed area, and explaining the evidence behind that judgment. This assessment should guide review depth and verification effort rather than restating change size.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `level` | string | Yes | Allowed: `low`, `medium`, `high`, `critical` | Highest credible consequence if the change is wrong: `low` is limited and easily reversible, `medium` has meaningful but contained impact, `high` can seriously affect users or systems, and `critical` threatens safety, security, data integrity, or service continuity. |
| `areas` | array of string | Yes | Unique items; Each item: `architecture`, `contract`, `state`, `accessibility`, `authentication`, `authorization`, `security`, `privacy`, `persistence`, `migration`, `transaction`, `concurrency`, `external_side_effect`, `performance`, `dependency`, `operations`, `user_experience` | Distinct technical or product concerns that could be affected. Include all material areas; use an empty array only when no predefined area applies. |
| `rationale` | string | Yes | Minimum characters: 1 | Evidence-based explanation connecting the proposed change to the selected level and affected areas, including important mitigations or uncertainty. |

### criterionAssessment

Reports the review result for one criterion from the engineering-review checklist.

The reviewer is responsible for evaluating the criterion independently, attaching concrete evidence, and explaining failures, exclusions, or verification gaps. `critical` is copied from the governing checklist so consumers can determine whether the result blocks approval.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `id` | string | Yes | Pattern: `^(U&#124;FE&#124;BE)-[0-9]{2}$` | Stable checklist identifier: `U` for universal/shared criteria, `FE` for frontend criteria, or `BE` for backend criteria, followed by two digits. |
| `name` | string | Yes | Minimum characters: 1 | Canonical human-readable criterion name from the governing checklist, not a review-specific conclusion. |
| `status` | string | Yes | Allowed: `pass`, `fail`, `not_applicable`, `not_verified` | Conclusion: `pass` or `fail` when assessed, `not_applicable` when the criterion does not govern this change, and `not_verified` when applicability is known but evidence is insufficient. |
| `critical` | boolean | Yes | Type only | Whether an unmet criterion must block approval according to the governing checklist; this is not a reviewer preference. |
| `evidence` | array of string | Yes | Unique items; Each item: at least 1 character(s) | Concrete observations, commands, paths, or artifact references supporting the status. Use an empty array only when no evidence exists and explain why in `notes`. |
| `notes` | string | Yes | Minimum characters: 1 | Reasoning that connects the evidence to the status. For `fail`, `not_applicable`, or `not_verified`, explicitly explain the defect, exclusion, or missing evidence. |

### finding

Describes one actionable result of the engineering review.

The reviewer is responsible for making the finding independently understandable: identify the problem or question, show evidence, explain the risk, assign an owner, define the required resolution, and state how closure will be verified. Findings should not depend on private reviewer context.

| Field | JSON type | Required | Machine constraints | Meaning |
| --- | --- | --- | --- | --- |
| `id` | string | Yes | Minimum characters: 1 | Stable identifier unique within this review, used to discuss and track the finding through resolution. |
| `severity` | string | Yes | Allowed: `blocker`, `required`, `suggestion`, `question` | Expected handling: `blocker` and `required` require a blocking decision until resolved; `suggestion` is an optional improvement, and `question` requests clarification or a decision. |
| `category` | string | Yes | Minimum characters: 1 | Concise classification used to group findings, such as correctness, security, accessibility, testing, or maintainability. |
| `title` | string | Yes | Minimum characters: 1 | Short statement of the concrete issue or question, written to remain meaningful outside the full review report. |
| `owner` | string | Yes | Allowed: `frontend`, `backend`, `shared`, `human` | Accountable resolution owner: frontend, backend, both through `shared`, or a human decision-maker when engineering work alone cannot close it. |
| `paths` | array of string | Yes | Unique items; Each item: at least 1 character(s) | Repository-relative paths where the issue exists or resolution is expected. Use an empty array only for findings with no meaningful file location. |
| `evidence` | array of string | Yes | Minimum items: 1; Each item: at least 1 character(s) | One or more specific, reproducible observations supporting the finding, such as path and line references, observed behavior, or command output. |
| `risk` | string | Yes | Minimum characters: 1 | User, system, operational, or maintenance consequence of leaving the finding unresolved. |
| `required_resolution` | string | Yes | Minimum characters: 1 | Observable code change, documentation update, or human decision required for closure; describe the outcome rather than prescribing unnecessary implementation details. |
| `verification_needed` | array of string | Yes | Each item: at least 1 character(s) | Commands, tests, inspections, or stakeholder checks that should provide evidence of resolution. An empty array means no additional verification was identified. |
| `criterion_ids` | array of string | Yes | Minimum items: 1; Unique items; Each item matches `^(U&#124;FE&#124;BE)-[0-9]{2}$` | One or more checklist criterion IDs that this finding causes to fail, leaves unverified, or otherwise materially affects. |

## Validation beyond shared field types

The specialist request and response schemas add stage requirements and exact criterion coverage. The [contract validator](../tools/review_contract.py) also checks decision consistency, unique finding IDs, criterion ownership, evidence requirements, and request–response identity. Both `blocker` and `required` findings require a `block` decision. These checks do not establish whether a finding is factually correct or whether an artifact is accessible.

Markdown descriptions are documentation annotations, not validation rules. Machines follow `type`, `$ref`, `required`, `enum`, patterns, and collection constraints in the JSON schemas; reviewing agents must not read this Markdown.
