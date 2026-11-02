# AI-assisted Engineering Workflow — V1

**Purpose:** help a human engineer and optional AI assistants take a real problem into small, reviewable, tested software. Start manual and linear. Learn from actual work before adding process.

## The hats

**Client (Human Engineer) → System Analyst → Architect → Designer → Implementer → Tester → Deployment Engineer**

The **human** owns product choices, risk appetite, scope, acceptance, and permission to release. Each hat can be invoked independently. Moving backward is normal when evidence changes a decision; no automatic agent team or orchestrator is required.

| Hat | Main output | Boundary |
|---|---|---|
| Client | Human intent and approvals | Makes product and acceptance decisions |
| System Analyst | Testable requirements | What/why, not how |
| Architect | System boundaries and contracts | Structure, not implementation |
| Designer | Feature design and small tasks | Detailed behavior within architecture |
| Implementer | Code, unit/integration tests, PR | Only signed scope |
| Tester | Independent behavior evidence | Does not fix or approve on behalf of human |
| Deployment Engineer | Authorized release and smoke test | Does not deploy without explicit permission |

## Use one hat at a time

Open the relevant `roles/<ROLE>.md` and say, for example: **"Act as Architect for feature X using its approved requirements."** There is no required CLI, magic phrase, agent framework, or automatic handoff. A person may wear more than one hat, but should explicitly distinguish creation from independent checking.

The previous four `$feature` expressions can remain as **optional labels** for work, not installed commands:

| Existing shorthand | V1 meaning |
|---|---|
| `$feature --plan --analysis --design <feature_name>$` | Client/Analyst/Architect/Designer work, **one hat at a time**, with human decisions at meaningful boundaries; stop before implementation sign-off |
| `$feature --impl --full <feature_name>$` | Implementer finishes the approved task and developer tests; never means full workflow completion |
| `$feature --verify <feature_name>$` | Tester independently checks the approved behavior and records actual evidence |
| `$feature --qa <feature_name>$` | Human's final review of scope, behavior, evidence, and risks; request help from the appropriate hat if needed |

**Deployment is separately authorized**, not part of `--impl --full` or `--qa`. The four expressions are workflow notation only until someone deliberately wires them to real tooling.

## Minimum durable state

Reuse existing project artifacts (problem definition, requirements IDs, architecture diagrams, issue tracker). Don't duplicate them for every feature. Only two short files per active feature are suggested; an existing issue tracker can replace them if it provides the same information:

- **`FEATURE.md`** — original request/link, agreed outcome and scope, requirement IDs, affected boundaries, small tasks, acceptance checks, human design/sign-off evidence, status, and next hat.
- **`EVIDENCE.md`** — code/PR ref, exact executed checks with results, tester outcome, human acceptance, deployment result if any, remaining risk, and resume point.

A project-level **`LESSONS.md`** is optional: write short lessons backed by repeated evidence, not rules from one bad day. Avoid a mandatory pack of templates.

### Minimal feature status

`idea → requirements → architecture → design → signed → implementing → verifying → awaiting_acceptance → accepted → deployed`.

A feature can be `blocked` at any point. Record **why** and the **next owner**. Skip unnecessary design documents or deployment when they add no value, but never skip actual human approval for changed scope, or evidence for safety-critical behavior.

## Rules that protect speed and trust

1. **A signed contract is the implementation boundary.** Record explicit human approval; no agent claims it on the human's behalf.
2. **One small PR, one testable outcome** when possible. Derive tasks from requirements and architecture, not arbitrary file boundaries.
3. **Tests are executable evidence.** Developer writes unit/integration tests; Tester independently tests agreed observable behavior.
4. **No silent scope drift.** Reopen the correct hat and obtain human approval if behavior or architecture materially changes.
5. **Failures are visible.** `NOT RUN` is not `PASS`; report observed results, paths/commands, and limitations.
6. **Resume without guessing.** Read the two feature files and current code, state what is done and what is next. Revalidate stale evidence after relevant changes.
7. **No forced complexity.** Specialists and orchestration remain out of V1.

## When to add more process (only with recurring evidence)

- Repeated boundary defects → a focused reviewer or contract test for that boundary.
- Frequent incompatible passing PRs → merged-result CI or shared integration checks.
- Repeated lost context between sessions → a smaller standardized status/resume note.
- Repeated release failures → a deployment checklist and recovery rehearsal.
- Manual handoffs repeatedly cause delays or mistakes → *then* consider automation/orchestration.

Prefer the smallest corrective change and record whether it helped.

## V1 Definition of Done

Take **one feature** from human need to a small PR, reproduce at least one meaningful runtime check, complete independent verification, record human acceptance, and (only if requested) verify a deployment. Another engineer can resume from the repository without reconstructing a chat.

**Package contents:** the seven named role files in `roles/` and this guide. Each file is self-contained; no hidden agent platform is required.
