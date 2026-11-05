# Source Assessment — WEBAcademy Handover

**Input:** `engineering_reviewer_agent.zip` (15 Markdown/JSON source documents, under `engineering_reviewer_agent/`, including four JSON Schemas). This assessment addresses the **handover artifacts**, not the underlying WebAcademy source code or actual PRs. None of those project files were supplied or executed.

## What is strong and retained

| Source | Evidence and reusable decision | Output |
| --- | --- | --- |
| `principles_inventory.md` | Explicitly separates universal engineering values, frontend/backend rules, and WebAcademy-only examples. Contains concrete stale-response, snapshot/selected-state, transaction and dependency lessons. | `common/principles.md` preserved as the shared historical source. |
| `review_responsibilities.md` | Eight defensible universal review concerns, including source-of-truth state, meaningful success, data/transaction integrity, and verification against risk. | `common/review_responsibilities.md` retained; both specialists use U-01–U-08. |
| `frontend_reviewer_agent.md` | Ten focused frontend criteria for composition, layers, API/DTOs, repository, services, hooks, UI/a11y, design behavior, verification, toolchain. | `frontend/role.md` and `frontend/review_rules.md`. |
| `backend_reviewer_agent.md` | Ten focused backend criteria for schemas/models/repo/service/transaction/route/adapters/migrations/tests. | `backend/role.md` and `backend/review_rules.md`. |
| `physical_structure.md` | Clear difference between runtime call flow and dependency direction; growth by use case rather than arbitrary file size. | `common/project_adaptation.md` distilled as **examples**, not binding target-repo layout. |
| `testing_conventions.md`, `mechanical_checks.md`, `dependency_policy.md` | Behavioral/Given-When-Then test quality; import-boundary checks; controlled dependency introduction. | Reused once under `common/`. |
| `handover_to_chatgpt.md`, `README.md` | Separate specialists, read-only behavior, schema-first output, proportional evidence and explicit human sign-off. | Shared `review_protocol.md`, specialist roles, CLI, acceptance tests. |
| `contracts/*` | Reasonably detailed JSON Schema 2020-12 contracts already exist and allow architecture/design stages without a code diff. | Preserved the established fields, adapted relative references and added specialist response wrappers. The active contracts are version `1.1`, allowing a PR locator to resolve its changed-file inventory through evidence tools. |

## Weak points found in the source and actions taken

1. **Criterion coverage was not enforceable by schema.** The original response schema required `minItems:18`, which permitted duplicate IDs with missing criteria. Each new specialist response schema requires exactly one of its eight universal and ten stack-specific IDs, with no extras.
2. **Decisions depended on prompt obedience.** Original text forbade approval with blocking findings but the response JSON structure did not enforce it. `tools/review_contract.py` rejects inconsistent decisions, repeated finding IDs, out-of-scope criterion citations, undocumented unverified criteria, and claims of passing criteria without any cited evidence.
3. **Request–response correlation was not checked mechanically.** The CLI checks matching `review_id`, `reviewer`, and `contract_version` when given the original request.
4. **A physical-structure file was assumed to exist.** In the new request schema, `physical_structure_ref` may be `null`. A reviewer must derive candidate boundaries from the actual code and disclose uncertainty; it must not impose WebAcademy's file layout by default.
5. **Human report generation was specified but not implemented.** Each specialist now owns a `response_template.md`; the deterministic renderer produces a Markdown report only from validated JSON.
6. **No executable acceptance suite was included.** Added positive and negative contract tests for approval, blocking, missing evidence, cross-stack ownership, wrong IDs, missing diffs, duplicate criteria, and renderer escaping.
7. **Shared instructions could drift between two copied agents.** Universal criteria and policy now live in `common/`; per-stack `role.md` references the shared source and contains only role responsibilities and workflow.

## Deliberate constraints

- No live agent invocation is bundled. This package defines reviewer behavior and testable boundaries; it is not a hosted model, runner, or CI bot.
- The examples are **synthetic**; successful schema validation is not proof that any real code has been reviewed. The example artifacts, hashes, timestamps, and line numbers are placeholders explicitly labeled synthetic.
- No project-specific architecture law is assumed until a target repository's README, structure, code, and approved decisions are inspected.
- No automatic changes, comments, or approval actions are allowed during ordinary review.
- The validator checks **shape and cross-field consistency**, not whether a review finding is factually correct. Semantic quality and reviewer calibration require evaluation against labeled real code changes.
- Source fields remain close to the original version 1.0 handover. The active version 1.1 explicitly supports PR evidence discovery; future material changes must also be versioned.

## Recommended next field experiment

Pick one **known-good** frontend diff and one known-bad backend diff from WebAcademy (or vice versa). Fill both request objects with actual resolvable repository context. Run each reviewer with the matching role, review rules, and common policy. Save the structured responses, validate them, render reports, and compare findings with an independent human review. Record false positives, missed defects, and extra review time before modifying review instructions.

**DoD for this package:** two separated review roles; common rules shared exactly once; request and response schemas; human templates; examples; runnable positive and negative contract tests; documented limits. Semantic reviewer capability is **not yet verified**.

## Review execution configuration verification — 2026-11-05

Model and reasoning assignments are editable in `common/review_execution.json`,
validated against its adjacent schema plus reference/risk-floor invariants. The
existing setup adapter renders the lead settings; `--review-plan` resolves helper
settings without launching agents. The future `zorba_ui` can use the validated
load/save/plan functions; no UI or model-availability service is implemented.

Live bounded subagent calls in this session were accepted and completed:

| Invocation/task ID | Requested model | Requested effort | Observed check |
| --- | --- | --- | --- |
| `/root/model_routing_advice` | `gpt-6-luna` | `medium` | Low-risk/low-criticality maintainability resolves to lightweight. |
| `/root/standard_review_verification` | `gpt-6.1-sol` | `medium` | Testing/configuration resolve to standard at medium impact. |
| `/root/deep_review_verification` | `gpt-6.1-sol` | `high` | Architecture/production resolve to deep; all 128 subject assignments across 16 risk/criticality combinations respect configured floors. |
| `/root/critical_review_verification` | `gpt-6-astra` | `high` | Critical helpers resolve to Astra/high; invalid pairs, disabled subjects and weakened critical floors reject. |

These are actual launch requests and returned contributions, not installed
configuration alone. The launcher did not expose independent serving-model
metadata. They establish scoped launch/planner behavior, not review efficacy or
fresh VS Code custom-agent discovery. No new test cases were introduced.
