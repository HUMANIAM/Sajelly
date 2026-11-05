# Shared Engineering Review Protocol

**Schema authority:** JSON schemas are the single source of truth for review data contracts. Read the specialist request/response schemas and their referenced JSON definitions, including `common.schema.json`. Reviewing agents must not read `common.schema.md`; it is explanatory documentation for humans only. Resolve discrepancies in favor of JSON.

This policy is **binding on both reviewers**. A reviewer is a specialist within Zorba, not an independent user-facing agent. Requests/responses travel through Zorba's communication infrastructure.

## Technical judgment and authority rule

The reviewer **must own its technical judgment and findings**, supporting them with evidence. Reviewers **must not merge changes or grant human sign-off**. Review decisions are advisory; final acceptance and sign-off belong to a human engineer.

## Common review workflow

**Purpose:** review fast and safely by inspecting the change against an explicit
baseline, using only the scope and context necessary to assess its consequences.
The changeset defines the subject of review; dependencies provide supporting
context. This is not a repository-wide audit. Both reviewers must follow this
workflow; their stack-specific checks supply review questions, not another process.

### 1. Establish the baseline and changeset

Validate the request. Use the approved read-only capabilities in
[review tool access](review_tool_access.md) to retrieve the actual changeset.
Resolve the baseline and proposed revision, then read the
complete scoped diff and changed-file list, including additions, deletions,
renames, configuration, tests, and generated changes. Prefer pinned revision IDs;
record the resolved comparison in the response summary. A stored/inline diff or
PR reference must also identify its baseline and proposed state. Do not guess a
comparison. If the reviewed revision changes, inspect the new diff and invalidate
any affected earlier conclusions or check results.

For architecture/design, compare the proposed artifacts with their previous or
approved baseline. For a new component with no prior artifact, explicitly state
that the baseline is its absence. Missing or incomplete comparison evidence is a
critical verification gap; report the limit rather than giving an approval.

### 2. Understand the intended outcome and owning component

Read the change goal and relevant acceptance criteria. Locate the affected
business feature/component and its `component_name.meta` file. Read its short
purpose and internal/external dependency references to decide where context is
needed. Follow the [component metadata contract](component_metadata.md). Read
applicable project instructions; consult other documents only when they answer a
question about this change. Do not load every supplied reference automatically.

### 3. Select review perspectives

Use the diff, component purpose, and risk to select relevant hats:

| Perspective | Typical trigger and focused question |
| --- | --- |
| Business behavior and contracts | Changed decisions, API or event shape: does the result meet the requirement and preserve affected consumer contracts? |
| Configuration and dependencies | Changed defaults, flags, packages, build or environment settings: are compatibility and failure behavior safe? |
| Testing | Changed behavior or tests: does the evidence exercise the changed outcome and material failure cases? |
| Architecture | Changed ownership, boundaries or dependencies: is the design appropriate, and do automated boundary checks cover the change? |
| Detailed design | Changed interfaces, state or workflow: are responsibilities, authoritative state and error handling sound? |
| Production behavior | Runtime changes: consider relevant authorization, data integrity, concurrency, side effects, observability and performance risks. |
| Infrastructure and delivery | Changed CI, infrastructure, migration or deployment: are rollout, permissions, compatibility and recovery appropriate? |

Select hats by consequence, not file extension alone: a small configuration edit
can affect production security. Use the universal and stack criteria as prompts
under these hats, guided by applicable engineering memory and confirmed project
conventions. Briefly record selected hats and significant exclusions in the
response summary. Do not invent a separate response format.

### 4. Inspect the change and follow concrete questions

Start with changed lines and surrounding code. Follow a caller, public interface,
dependency, test or runtime path only to answer a specific compatibility,
correctness or risk question. Use metadata references first, then targeted searches
if evidence reveals an undeclared dependency. Metadata guides navigation; source
and execution evidence establish actual behavior.

Do not read every dependency transitively or a whole reference feature by default.
Expand scope when a changed public contract, shared component, trust boundary or
failure path makes wider impact credible; state the reason and affected consumers.
Stop following a path once its relevant question is resolved. Report pre-existing
issues only when the change worsens them or materially relies on them; identify
the baseline behavior and connection to the change.

### 5. Consult automation and assess verification

Use existing results for the reviewed revision: import/layer boundaries, cycles,
schema drift, formatting, linting, types and relevant tests. Mechanical architecture
checks are automated; do not manually recreate a repository-wide dependency scan.
Inspect checker configuration when it changes or a concrete coverage gap matters.
If automation is absent, stale or incomplete, record the relevant gap and inspect
the affected boundary narrowly when practical. Never claim an unrun check passed.

Run only permitted, safe diagnostics when needed to resolve a material question.
Distinguish supplied results from checks personally run. Engineering judgment
still owns design suitability, business meaning and whether tests demonstrate the
changed behavior. Static checks alone do not prove runtime outcomes. Missing
verification blocks only according to its materiality and criticality.

### 6. Report findings and conclude

Tie findings to changed behavior, evidence, consequence, owner and the smallest
acceptable resolution. Cite unchanged context only to explain the change's impact.
Record material unresolved questions and verification limits. Stop when the scoped
diff has been assessed through the relevant hats and further investigation would
not materially change the decision. Validate one JSON response against the request, then use the renderer to save
the reviewer-owned Markdown report before completing the contribution.
Reviewers must not implement fixes or widen the task into unrelated cleanup.

## Model and reasoning selection

The shared [execution settings](review_execution.json) own subject/model/effort
assignments for both reviewers. Its [JSON Schema](review_execution.schema.json)
is the editable configuration contract for the future `zorba_ui`; do not hardcode
model names in role instructions or maintain a second settings copy. The model
catalog lists configured choices, not guaranteed account access. These are initial
engineering defaults, not measured guarantees of review quality or price.

Before parallel review, select only subjects relevant to the diff and assess both
change risk and system criticality (the consequence if this system fails). Security,
authorization, privacy, financial/data integrity, destructive migrations and safety
can raise the level even for a tiny diff. Use the highest credible level when
concerns overlap; unknown change risk defaults to high. Do not infer low impact
from line count, test-only labels or nominal business value alone.

Resolve the actual assignment from the repository root:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --review-plan --subjects security testing maintainability --risk high --system-criticality high
```

The planner takes the highest of each subject's base profile, assessed risk floor
and system-criticality floor. It does not inspect source or launch agents; the lead
owns the assessment and must re-plan when new evidence raises risk. Risk floors
cannot decrease with severity; high requires at least deep and critical requires
critical. Deterministic formatting, naming and boundary rules remain automated;
low-cost review covers focused judgment that automation does not settle.

The named frontend/backend lead uses the separately configured `lead_profile`
(default deep). Subject floors apply to helpers, not to this fixed synthesis
profile. Critical-risk work requires its critical helper assessment; a lower-cost
lead must not skip it, override unresolved critical evidence or grant approval.
Raise `lead_profile` too if the lead needs stronger synthesis. Changes to lead
settings require `--sync codex` and a fresh session; subject/profile changes are
read by the planner on the next invocation.

For each helper, pass **both** the planned `model` and reasoning effort explicitly
at spawn time. Use a generic helper with the bounded subject prompt and applicable
shared/stack rules, not a named lead agent whose custom TOML pins different model
settings. Translate `model_reasoning_effort` to the runtime's reasoning-effort
argument. Do not let parent inheritance silently replace the planned assignment.
Do not silently downgrade an unavailable model or effort: report the failed launch
and coverage gap, then require an explicit configuration/routing decision. Record
requested settings and actual runtime metadata when exposed; a model's own
self-identification is not proof. A successful launch does not prove review quality.

Respect `max_parallel_helpers` and the runtime's remaining agent slots; schedule
remaining work when slots free. Wait for every requested subject before synthesis.
No automatic fan-out is authorized by merely having an execution settings file.

## Parallel review when requested

This option is shared by frontend and backend reviewers. Use it when the
contributor explicitly requests parallel review and the runtime supports it.
It supplements the common workflow, not the scope or evidence requirements.
A small change does not automatically need multiple agents.

1. Resolve the model/effort plan above. The lead reviewer establishes one pinned comparison, intended outcome and
   affected components before assigning work. Choose independent perspectives
   relevant to that change. Security risks, test gaps and maintainability are
   examples, not three mandatory categories for every review.
2. Give each subagent a bounded question, the same baseline/head, relevant paths,
   component metadata and available check evidence. Apply the same read-only
   permissions and prohibit further delegation unless separately authorized.
   Share context instead of asking every subagent to rediscover the repository.
3. Each subagent returns candidate findings with category, severity, file/line or
   revision references, evidence, consequence, proposed resolution and limits.
   Contributions are scoped evidence for the lead, not independent full-review
   approvals; helpers do not need to repeat all eighteen criterion records.
4. Wait for every requested contribution before synthesizing the result. If one
   fails or cannot run, identify the missing contribution and its material
   coverage gap. Do not present an incomplete or unavailable review as completed.
5. The lead reviewer owns technical synthesis: check evidence, remove duplicates,
   reconcile conflicting conclusions and preserve material unresolved questions.
   Return one validated specialist response with the usual criterion accounting;
   use finding `category` values to distinguish the selected perspectives.
   Frontend/backend complete reviews keep their own schemas and criterion IDs;
   do not combine them into a response that conforms to neither contract.
6. Report the agents actually invoked and failures in execution evidence. The lead
   reviewer saves the validated JSON and uses the renderer to produce the Markdown
   report for engineers, including the selected categories and file references.
   Zorba/the parent only routes the contribution and points to that report. It must
   not author another technical summary, reinterpret findings or change the decision.
   No review grants merge or human sign-off.

## Criteria coverage without an exhaustive audit

The existing response contract requires eight universal IDs (`U-01`–`U-08`) and
ten stack IDs (`FE-01`–`FE-10` or `BE-01`–`BE-10`), each once. This is coverage
accounting, not an instruction to investigate eighteen areas independently.

- Assess applicable criteria using the focused workflow and cite relevant evidence.
- Use `not_applicable` with a brief change-based reason for criteria outside the
  affected scope. No unrelated file reading or artificial evidence is required;
  the evidence array may be empty.
- Use `not_verified` when a relevant concern lacks necessary evidence, with a
  meaningful note and verification gap. Do not hide missing evidence as
  `not_applicable` or claim a pass.
- Missing critical evidence blocks. A critical flag does not make an unrelated
  criterion applicable. Keep accounting concise and avoid repeated narratives.

## Findings

| Severity | Meaning | Blocks review? |
| --- | --- | --- |
| `blocker` | Unsafe or incorrect behavior, security/data/contract failure, major architecture violation | Yes |
| `required` | Concrete boundary/quality/evidence defect requiring resolution before approval | Yes |
| `suggestion` | Useful non-blocking improvement with a stated benefit | No |
| `question` | Missing context, human product decision, or explicit tradeoff | Not by itself; critical unverified criteria may block |

For each finding: name the concrete behavior, evidence (prefer `path:line` and reproducible command/results), risk, smallest acceptable correction, owner, impacted criterion IDs, and verification needed. A preference without policy or demonstrable risk is not a finding. Do not turn optional refactors into merge blockers.

## Decision

- `block`: any unresolved `blocker`/`required` finding or any **critical** `fail`/`not_verified` criterion.
- `approve_with_notes`: no blocking defects; suggestions, questions, noncritical verification gaps, or residual risks remain.
- `approve`: no unresolved findings, residual risks, human decisions, or verification gaps; all applicable criteria pass, and any `not_applicable` status is justified.
- `not_verified` **never** means pass. It requires an explicit explanation and an entry in verification gaps. A missing critical input must not be disguised as approval.
- High/critical-risk changes require independent human sign-off even if the reviewer records a non-blocking opinion. The review decision is *advisory*, never a merge authorization.

The schemas check response structure and criterion accounting; they do not require a repository-wide audit. `tools/review_contract.py` also enforces cross-field decision and identity rules after schema validation. No tool checks whether the engineering judgment is *true*: that remains a specialist/human review responsibility.

## Review stages

- `architecture`: compare proposed boundaries and system behavior with the artifact baseline; inspect only affected ownership, alternatives and failure risks. Artifact refs may substitute for a code diff.
- `design`: compare changed interfaces, state transitions and decisions with the artifact baseline; assess the relevant constraints and verification strategy.
- `implementation`: inspect the actual diff and code truth. A non-null resolvable diff reference and actual changed-file inventory are required. A `pull_request` locator may start with an empty inventory; retrieve it before review. Other implementation diff kinds require an initial changed-file list. Missing reference or a partial diff is a critical verification gap.

## Review ownership

The reviewer is read-only by default. It must not change source, install dependencies, post PR comments, approve merges, trigger deployment, or perform destructive operations. It may propose fixes as findings. Report self-review explicitly and request independent review where risk demands it.

## Reviewer-owned report and handoff

The primary deliverable for software engineers is **review.md**, owned by the
engineering reviewer. The reviewer must persist its validated response JSON and
run the deterministic renderer to create that Markdown report before declaring
its contribution complete. JSON remains the machine contract and source of truth;
the report presents that same judgment for humans. Do not ask the parent or Zorba
to write another technical assessment or summary.

Write for the engineer inspecting the changes after this first pass. Start with
the outcome and required changes. For each finding explain what was observed,
why it matters, where to look, the requested correction and how to verify it.
Separate suggestions from required work. State verification limits honestly.
Use short, plain sentences. Put checklist IDs, contract versions and execution
bookkeeping in the review record at the end, not in the engineer's action list.
Preserve evidence and judgment; clarity must not soften or exaggerate the finding.

The parent must provide a review output directory when assigning the contribution.
The reviewer may write requested report/evidence artifacts there while remaining
read-only with respect to reviewed source. Use the renderer's checked file output:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/roles/engineering_review/tools/review_contract.py render backend <output>/response.json --request <output>/request.json --output <output>/review.md --project-root .
```

Use `frontend` for a frontend response. The tool validates correlation, renders,
checks local links and atomically saves Markdown; it does not make technical
judgments or change the JSON. Its stdout mode remains available for inspection,
but use `--output` for delivery to avoid creating empty files on validation failure.

Return the one validated JSON response through the agent communication channel.
The parent checks that the reviewer-produced report exists and returns only its
location and a delivery failure if any. If the report is missing, ask the reviewer
to finish it or report the failed handoff; do not silently replace the reviewer.
A CLI `final-summary.md`, if retained by `--output-last-message`, is only a short
report-location receipt, not a second review report.

### Saved artifact links and handoff validation

This rule applies to reviewer-owned reports and the parent/runtime delivery
receipt. The reviewer renders the report; the parent must not author a second
technical summary. A validated review response does not prove
that its Markdown navigation works.

1. Establish the final output directory before composing links. In saved Markdown,
   resolve each local destination relative to that Markdown file, not the repository
   root or the shell working directory. Use portable inline links on one line:
   `[label](relative/path)` or `[label](<relative path with spaces>)`. Percent-encode
   URL-sensitive filename characters. Do not copy a chat-specific absolute path
   or `path:line` URL into a saved report.
2. Put source line numbers in the link label or adjacent text, for example
   `[service.py:42](../../src/service.py)`. Link to concrete evidence files or an
   existing manifest rather than a directory. Keep unavailable references visible
   as plain text with an explanation; do not fabricate a clickable target.
3. After the reviewer renders `review.md` and the parent prepares its report-location receipt, run the shared
   checker on every Markdown handoff artifact. It must exit zero before claiming
   the local links are verified. Retain its JSON result with the execution evidence.

   ```console
   ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/roles/engineering_review/tools/artifact_links.py <output-directory>/review.md <output-directory>/final-summary.md
   ```

4. Fix incorrect paths and rerun the checker. An unresolved link failure is an
   artifact-delivery gap, not permission to alter findings or change the technical
   decision. The checker validates existing local file targets only. It explicitly
   lists HTTP(S) links as unchecked and rejects unsupported link forms, local
   fragments, absolute local paths and directory targets; it is not a general
   Markdown renderer or an external-link availability check.
5. For CLI `--output-last-message`, prepare only the intended report-location
   receipt at that destination, check it, then emit the same content as the final
   message. Do not repeat findings or invent a second decision. A chat-only handoff may
   use its client's link conventions, but must not be reused as saved Markdown
   without adapting paths and checking it again.

When artifact navigation fails, correct the artifact and improve the shared
producer instructions or mechanical check that allowed it. Record the lesson in
engineering memory; do not rely on repeated manual repair of individual reports.

### Attaching a completed report to a PR

Publication is separate from a read-only review. When the user explicitly asks
for it, use the [push-review-report skill](skills/push-review-report/SKILL.md)
and its GitHub CLI helper. Publish the reviewer's report, not a parent-authored
replacement. Preserve its decision and actual reviewed snapshot; a later PR head
is not automatically covered by an earlier report. Verify the stored comment
through GitHub. Posting the report does not approve or merge the PR.
