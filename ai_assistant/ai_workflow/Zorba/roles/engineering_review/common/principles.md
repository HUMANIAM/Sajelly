# Engineering and Project Memory

## How to Use This Inventory

This inventory has two referenceable memory sections. **Durable lessons belong
to [Engineering Memory](#engineering-memory). Stack conventions and project
history belong to [Project Memory](#project-memory).** This classification is
part of the handover contract.

| Memory | Contains | Review authority | Reference |
| --- | --- | --- | --- |
| Engineering memory | Portable principles and reusable lessons about correctness, ownership, verification, and failure handling | Safe review defaults; apply the lesson in the target project's context | `principles.md#engineering-memory` |
| Project memory | Stack-dependent conventions, named files, product contracts, historical decisions, and source-project examples | Context and provenance; binding only when confirmed by the target project's code or explicitly adopted contract | `principles.md#project-memory` |

### Classification contract

- Classify by what a statement depends on. A lesson that remains useful after
  replacing the framework, repository layout, and product belongs to engineering
  memory. A statement that depends on those choices belongs to project memory.
- Split mixed statements: keep the portable lesson in engineering memory and
  its concrete implementation or historical evidence in project memory. Evidence
  columns below preserve provenance; they do not make source-project choices
  mandatory in another project.
- Label project memory by project and frontend/backend scope. Confirm its current
  applicability against the target repository before using it as a review rule.
  Historical source paths are not proof of current target-project behavior.
- When a project convention conflicts with a durable lesson, surface the conflict
  with evidence and request an explicit decision; do not silently promote history
  into a universal rule or silently override an adopted project contract.
- Refer to the two section anchors above when handing off memory. A reference to
  project memory must also name the project and relevant convention or contract.

Source paths below record where a lesson or convention came from. The inventory
remains usable when the original repository is unavailable; unavailable evidence
must remain explicit.

## Engineering Memory

**Contract:** preserve durable lessons that transfer across projects. Apply their
intent to the target architecture; examples illustrate failure modes rather than
mandating a framework, filename, or exact implementation.

### Universal Engineering Principles

| Principle | Review meaning | Concrete WEBAcademy evidence |
| --- | --- | --- |
| Feature ownership before technical grouping | A behavior belongs to a coherent product capability; layers then separate responsibility inside it | Backend and frontend organize feature verticals under `src/features/<feature>/` |
| One clear responsibility per layer | Transport, workflows, persistence, runtime state, and presentation must not collapse into one module | Backend `skill` separates model/schema/repo/service/route; frontend `skill` separates API/repo/service/hooks/UI |
| Small public interfaces | Consumers use the next boundary's contract rather than reaching through internal helpers | Routes call services; hooks call services; services do not expose raw transport concerns |
| Source-of-truth state outranks snapshots | Authorization and mutation decisions use canonical state, not stale render, request, cache, or transport views | Root review contract and frontend QA lessons require source-vs-snapshot analysis |
| Success requires a meaningful outcome | No code path may report success when no authorized state change or promised result occurred | Root internal-review contract explicitly challenges hidden no-op success paths |
| Start small and evolve from evidence | Begin with a cohesive file; split or abstract after independent responsibilities, stable reuse, or collaboration pressure appear | `physical_structure.md` records file-to-folder growth signals |
| Reuse follows stable ownership | Extract shared code when the responsibility is clearly cross-feature; keep uncertain reuse local | Both feature-lead guides require nearest-neighbor inspection and responsibility-first sharing |
| Duplication is a risk, not an automatic abstraction trigger | Remove duplicated rules when ownership is clear; do not generalize superficial similarity | Shared domain/repo helpers exist, while feature-local helpers remain local when reuse is unclear |
| Thin, coherent review slices | One change should deliver one explainable outcome without speculative cleanup | WEBAcademy root workflow requires thin vertical slices and coherent commit/PR outcomes |
| Verification is proportional to risk | Formatting, linting, and type checks are insufficient when behavior changes | Global verification rules require runtime or integration evidence for visible behavior |
| Tests explain behavior | Tests stay small, clearly named, feature-owned, and reuse mechanics without hiding the scenario | Backend feature test folders use `conftest.py`, `data.py`, and focused test modules |
| External dependencies require evidence | Prefer platform/stdlib and existing packages; add maintained packages only for a current need | `dependency_policy.md` records the dependency decision contract |
| Mechanical rules support human judgment | Enforce imports, cycles, types, and schema drift mechanically; keep ownership and semantic correctness with reviewers | Frontend ESLint restricts imports; `mechanical_checks.md` separates enforceable and human checks |
| Product decisions stay human-owned | Reviewers surface unresolved product or risk decisions instead of silently deciding them | Human-engineer role owns intent, tradeoffs, and merge readiness |
| Read code truth before descriptive history | Documentation must be reconciled with runtime code and tests; stale docs cannot silently override behavior | Both feature leads require nearest comparable modules and doc-drift review |

### Concrete Review Examples to Preserve as Lessons

#### Frontend stale-response example

An older request may finish after a newer query. The visible request list is a
snapshot; the latest request identity is authoritative. The reviewer should
require cancellation or request identity protection and a regression scenario
that resolves responses out of order.

#### Frontend selected-versus-visible example

An item can already be selected even when it is absent from the currently
filtered options. A decision helper that sees only visible options may allow a
false “add” success. The reviewer must compare every decision input with the
state used by the later mutation.

#### Thin frontend repository example

When the backend returns `string[]` and that is also the domain contract, the
repository may pass the values through while translating transport errors. An
invented mapping layer would add ceremony without protection.

#### Backend transaction example

A workflow that writes database state and uploads a file can partially fail.
The service owns the complete business transaction; repository helpers and an
attachment guard support rollback or compensation. A successful upload alone
must not imply a successful business operation.

#### Backend query example

Skill search ranks exact matches, then prefix matches, then other matches with
deterministic ordering and pagination. Query ordering is repository behavior;
the service should not reconstruct SQL semantics after the fact.

#### Dependency example

Adding a package requires a current need, proof that the standard platform or
an installed dependency is inadequate, and review of maintenance, license,
security, versioning, and transitive cost. Familiarity alone is not a reason to
install it.

### Reviewer ownership and human-first writing

The engineering reviewer owns its technical judgment and the report engineers
read. Validated JSON is the machine record; the deterministic renderer presents
that same judgment as Markdown. The parent routes the result and returns the
report's location rather than writing another technical assessment. Lead with
what the engineer must understand and act on; keep contract and execution
bookkeeping at the end. Clarity carries authority without inflated language.

### Artifact usability and systemic repair

A correct engineering result must remain usable outside its original chat.
Resolve saved-document links from the document's location and verify delivery
artifacts as well as their machine contracts. When a report fails, repair the
artifact and the shared workflow or tooling that allowed the failure; preserve
its technical evidence and conclusions. See the [artifact handoff rule](review_protocol.md#saved-artifact-links-and-handoff-validation).

## Project Memory

**Contract:** preserve stack conventions and project history with their scope and
provenance. The following conventions and architecture facts come from
**WEBAcademy**, not a declaration of Sajelly's current architecture. Frontend and
backend conventions apply only when the target project confirms or explicitly
adopts them. Recheck named paths, commands, frameworks, and product contracts
before treating them as current requirements.

### Frontend-Specific Rules

| Rule | Reviewer interpretation | WEBAcademy example |
| --- | --- | --- |
| Logic dependency flow | `app/page -> hooks -> service -> repo -> api`; do not skip layers without an explicit reason | `frontend/src/features/skill/*` |
| UI composition flow | Build bottom-up from primitive to interaction, domain component, section/container, then page | `src/shared/ui/DropdownList*`, `FilterRow`, cards, and grids |
| Presentation-only UI | Components render accessible behavior from typed props; they do not call API/repo/service modules | `SkillInput.tsx` composes a shared interaction component |
| Hooks own runtime state | Hooks own effects, cleanup, cancellation, loading/error/data state, and prop synchronization—not business rules | `skill/hooks.ts` uses `AbortController`, request IDs, and React lifecycle primitives |
| Services own frontend decisions | Pure selection, normalization policy, and workflows belong below hooks and above repositories | `skill/service.ts` owns add/toggle/build-option decisions |
| Repositories are thin anti-corruption boundaries | Map only real DTO/domain differences and translate transport errors; pass through when shapes already match | `skill/repo.ts` passes arrays through and classifies API errors |
| API owns transport | Request construction, credentials, payload encoding, response/error decoding, and abort signals stop at API modules | `skill/api.ts` calls shared `src/app/api.ts` |
| Contract types remain distinct | DTO, domain, and view-model meanings must not be mixed merely because shapes resemble each other | Frontend reusable-pattern guidance records DTO -> domain -> view-model flow |
| Async ordering is a correctness concern | Older responses, canceled work, unmounts, and changed props must not corrupt current UI state | Skill hook regression tests cover stale responses and prop changes |
| Accessibility is functional behavior | IDs, labels, focus, keyboard interaction, and repeated instances require explicit review | Skill input tests cover unique IDs and keyboard-safe interaction |
| Visible changes need stakeholder verification | Browser/runtime evidence and the agreed state matrix are required, not only static or compiler evidence | Frontend QA workflow requires interaction-state verification |
| Architecture rules should be linted | Import boundaries and cycle direction are suitable for mechanical enforcement | `frontend/eslint.config.js` uses restricted-import rules |

### Backend-Specific Rules

| Rule | Reviewer interpretation | WEBAcademy example |
| --- | --- | --- |
| Request flow | `route -> service -> repo -> model/database`; schemas define boundary data | `backend/src/features/skill/` |
| Routes stay thin | Routes parse protocol input, wire dependencies, select status/protocol behavior, and call services | `skill/route.py` delegates search/list work to the service |
| Services own workflows | Business rules, authorization, orchestration, transactions, presenters, and side-effect coordination belong here | Proof, request, resource, and track services coordinate multi-step operations |
| Repositories own persistence mechanics | SQL/query construction, ordering, pagination, and persistence operations stay out of routes/services | `skill/repo.py` implements ordered search and pagination |
| Models and database constraints protect persistence | Persisted shape, relationships, uniqueness, and database invariants belong at the model/migration boundary | `skill/model.py` defines normalized-name uniqueness |
| Schemas own external validation | Request/response shape and boundary normalization are distinct from persistence models | `skill/schema.py` defines query parameters |
| Transaction ownership is explicit | Composed workflows must not accidentally commit partial work; repository commit behavior must support service orchestration | Shared SQL helpers and `commit=False` patterns support one final service commit |
| Presenters are pure outward mapping | Presenter logic must not query, mutate, or perform side effects | Resource, track, user, and proof features have presenter modules |
| Ports isolate external systems | Services depend on capability contracts; adapters own provider details | `notification/ports.py` and `notification/adapters/ms_graph_adapter.py` |
| Cross-resource side effects require compensation | Database and file/external changes need explicit partial-failure handling | `attachments/commit_guard.py` coordinates upload and DB failure compensation |
| Tests mirror feature ownership | Model/schema/repo/service/route tests live under the same feature name; reusable setup has explicit scope | `src/tests/features/<feature>/` |
| Python tooling uses project isolation | Commands run through the project's own virtual environment and locked dependencies | Backend workflow requires `.venv/bin/...` tooling |

### WEBAcademy-Specific Architecture and Contracts

These items are not portable rules. They are examples or current product
contracts.

| WEBAcademy fact | Portable lesson | New-project treatment |
| --- | --- | --- |
| FastAPI + SQLModel + Pydantic | Keep transport, persistence, and validation ownership explicit | Replace with the selected Python stack while preserving boundaries |
| React + Vite + Tailwind | Separate app composition, runtime state, decisions, transport, and presentation | Replace with the selected frontend framework/toolchain |
| `skill` is the canonical reference vertical | Keep one small, complete reference feature for new contributors | Select the new project's nearest stable feature after code inspection |
| Cookie/SSO auth and `credentials: "include"` | Treat authentication transport as an explicit integration contract | Adopt only if the new backend uses cookie authentication |
| `{ error, message }` error envelope | Decode transport errors centrally and expose stable domain/UI errors upward | Replace with the new API's actual error contract |
| UUID IDs and snake_case enums | Share identifier and enum semantics across the boundary | Derive from the new backend contract |
| Multipart JSON in `payload` plus file fields | Centralize special request construction in the API boundary | Use only for matching endpoints |
| Figma is an exact source of truth | Freeze the source artifact and state matrix; verify parity before cleanup | Apply to any approved design source, but do not require Figma universally |
| `src/app/api.ts` is the shared request wrapper | Centralize stable transport mechanics | Inspect and choose the target project's actual request boundary |
| `src/features/shared/repo/sql_helpers.py` contains DB mechanics | Shared infrastructure should have a named responsibility | Reuse the target ORM/database's established mechanisms |
| `service_utils.py`, relation repos, and feature attachment modules exist | Split feature-local responsibilities only when concrete needs appear | Do not copy every optional file into a new feature |
| Exact verification commands and CI job names | CI is the command source of truth | Replace with the new project's scripts and workflow definitions |
