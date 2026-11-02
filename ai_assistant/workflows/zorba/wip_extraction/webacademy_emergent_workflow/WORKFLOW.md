# Workflow

## Purpose

Move from an unclear human need to delivered, verified software through a
linear sequence of collaborating roles. Each stage reduces a different kind of
uncertainty and leaves a durable artifact for the next teammate.

## The sequence

| Stage | Role | Reads | Produces | Ready to hand off when |
| --- | --- | --- | --- | --- |
| 1 | `CLIENT` | Original human message and relevant product context | `client.md` | The human confirms that the problem, need, purpose, and important ambiguity are represented honestly. |
| 2 | `SYSTEM_ANALYSIS` | `client.md` and current system behavior | `requirements.md` | Observable requirements, non-goals, decisions, and acceptance criteria are clear enough to evaluate. |
| 3 | `ARCHITECTURE` | `client.md`, `requirements.md`, and current system architecture | `architecture.md` | Whole-system boundaries, ownership, integrations, significant risks, and technical decisions are coherent. |
| 4 | `SOFTWARE_DESIGN` | All prior artifacts and relevant code/contracts | `design.md` | APIs, modules/classes, data and state contracts, sequences, errors, and implementation slices are precise enough to build. |
| 5 | `TESTING` — strategy | All planning artifacts | `testing_strategy.md` | Requirements and risks map to practical checks at the correct test levels. |
| 6 | Human authorization | Complete planning chain and `testing_strategy.md` | Implementation authorization recorded or linked in `testing_strategy.md` | The human authorizes implementation against exact artifact revisions or returns the work for changes. |
| 7 | `IMPLEMENTATION` | All prior artifacts and current code | Code changes plus `implementation.md` | The approved behavior is implemented, developer checks ran, the diff was self-reviewed, and the exact change reference is recorded. |
| 8 | `TESTING` — QA | All prior artifacts, exact change ref, and running/testable system | Test changes plus `QA.md` | System/integration behavior was observed, results and gaps are reproducible, and the outcome is `PASS` or `BLOCK`. |
| 9 | Human review | `QA.md`, implementation, and the original need | Acceptance/rejection and any separate delivery authorization, recorded or linked in `QA.md` | The human accepts or rejects the exact delivery-candidate revision and separately states any desired delivery action. |
| 10 | `DEPLOYMENT` | Entire artifact chain, `QA.md`, exact accepted delivery-candidate ref, and authorization | Delivery/integration action plus `deployment.md` | The authorized destination contains the intended revision, checks are observed, and the result or recovery is recorded. |

The artifact chain is cumulative. A role reads the artifacts before it, but it
does not rewrite their history to make later work look correct.

## Human gates

Human judgment remains part of the engineering system:

1. The human confirms that `client.md` expresses the real need.
2. Material requirement, priority, risk, and scope decisions return to the
   human rather than being invented by an agent.
3. After the testing strategy is ready, the human authorizes implementation
   against the exact current artifact revisions. A coherent artifact chain is
   necessary, but it is not implied authorization.
4. The human reviews `QA.md` and accepts or rejects the exact tested revision.
5. Acceptance is not delivery authorization. PR creation, push, merge, release,
   cloud deployment, or another external action must be requested explicitly.

## Durable human decisions

Human gates must survive chat history:

- `client.md` records or links confirmation of the clarified need;
- `requirements.md` records or links approval of the exact requirements
  revision;
- `testing_strategy.md` records or links authorization to implement the exact
  artifact revisions;
- `QA.md` records or links human acceptance or rejection of the exact
  delivery-candidate reference and, separately, any authorized delivery action
  and destination.

An agent may quote or link an explicit human decision. It may never infer one.
If a decision changes, preserve the previous record and add the new decision
with its scope and reference.

## Artifact identity and freshness

Every artifact records:

- work-item name or ID;
- status;
- revision;
- input artifact revisions or implementation reference;
- the standard handoff.

A decision applies only to the revisions it names.

- Changing `client.md` can invalidate every later artifact.
- Changing requirements invalidates affected architecture, design, test
  strategy, implementation, and QA.
- Changing architecture invalidates affected design and downstream evidence.
- Changing the delivery candidate after QA makes the prior QA result stale;
  rerun affected verification or deliver the exact reference that passed.

When an input changes, return to the **earliest affected role**, update the
artifact chain, and rerun the affected stages. Do not patch a downstream
document to hide an upstream decision change.

## Working rules

- One active role per invocation.
- One small, complete, observable outcome per change when practical.
- Separate verified facts, proposals, human decisions, and unresolved items.
- Inspect the current project; never import another project's technical
  assumptions merely because this workflow came from there.
- Missing or inaccessible input is a blocker, not permission to guess.
- `NOT RUN` is not `PASS`; a build is not proof of runtime behavior.
- A signed plan can still be incomplete. New evidence that contradicts the
  original need returns to the appropriate earlier role.
- Relevant code changes after QA require renewed verification.
- A role may propose a better idea or workflow improvement, but may not change
  approved scope, policy, or another role's artifact silently.

## Return paths

Moving backward is normal:

- unclear need or priority -> `CLIENT`;
- unclear or conflicting behavior -> `SYSTEM_ANALYSIS`;
- system-boundary or ownership problem -> `ARCHITECTURE`;
- API, sequence, state, or detailed contract problem -> `SOFTWARE_DESIGN`;
- untestable plan -> the earliest planning role that owns the gap;
- implementation defect -> `IMPLEMENTATION`, then QA again;
- QA shows the requirement or design is wrong -> the earliest affected role;
- delivery or integration failure -> `DEPLOYMENT` diagnoses and routes the work
  back without disguising the failure.

## Completion

Work is complete only when the human can trace the delivered behavior back to
the original need, inspect how it was tested, understand remaining risk, and
know exactly what was delivered where. A new teammate must be able to resume
from repository artifacts without reconstructing a private chat.
