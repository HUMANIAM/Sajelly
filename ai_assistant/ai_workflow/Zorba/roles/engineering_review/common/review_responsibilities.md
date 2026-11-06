# Eight Engineering Review Responsibilities

Use these responsibilities as review prompts within the
[common workflow](review_protocol.md#common-review-workflow). Assess consequences
of the changeset, not the health of every component. Investigate only applicable
questions; briefly mark unaffected criteria `not_applicable`. Relevant concerns
with missing evidence are `not_verified`. Mechanical structure checks are
automated; use their results and apply judgment to semantic risks.

## 1. Intent, scope, and contract integrity

The reviewer confirms that the change solves the stated need without silently
changing adjacent behavior.

Review:

- the user or system need, success signal, constraints, and non-goals
- the authoritative contract: requirements, API schema, workflow definition,
  persistence invariant, or approved design
- whether assumptions and intentionally deferred work are explicit
- whether the change is a thin, coherent outcome rather than unrelated cleanup
- whether implementation behavior matches the agreed contract

Ask:

- What exact outcome must be different after this change?
- What must remain unchanged?
- Is any product decision being hidden inside a technical implementation?

Block when the implementation cannot be judged against a stable outcome or
silently widens scope.

## 2. Feature ownership and physical placement

The reviewer confirms that every responsibility has an obvious business owner
and lives in the correct feature and layer.

Review:

- the owning feature or component
- file and folder placement against the applicable project structure policy, when relevant
- whether application bootstrap contains only composition
- whether cross-feature work uses the owning feature's public interface
- whether `core`, `shared`, `common`, or `utils` is being used to avoid an
  ownership decision
- whether production tests mirror the feature vocabulary and location

Ask:

- Which component would an engineer open first to understand this behavior?
- If the code is shared, what stable responsibility—not duplication alone—owns
  it?

Block when placement hides ownership, introduces a circular feature
dependency, or makes a shared folder a miscellaneous bucket.

## 3. Layer boundaries and interface quality

The reviewer confirms that dependencies flow through small, typed public
interfaces and that framework or infrastructure details stop at their owning
boundary.

Review:

- allowed dependency direction
- transport-to-domain and persistence-to-domain boundaries
- public function, method, event, and type contracts
- error translation at the correct boundary
- direct imports of another layer's or feature's internals
- unnecessary interfaces that have only speculative value

Ask:

- Can the higher layer explain what it needs without knowing how the lower
  layer performs it?
- Is any route, UI component, or service skipping a boundary for convenience?
- Does the interface expose more state or behavior than its consumer needs?

Block on layer leakage, circular imports, DTO/ORM leakage into unrelated
layers, or interfaces that make invariants impossible to enforce.

## 4. Data, persistence, and transaction integrity

The reviewer follows data from input through validation, normalization,
persistence, and response. The reviewer treats transaction boundaries and
external side effects as design decisions.

Review:

- schema validation versus database constraints
- canonicalization, identity, uniqueness, ownership, and referential integrity
- query semantics, ordering, pagination, and concurrency assumptions
- transaction ownership, commit/rollback behavior, and partial-failure paths
- migrations, backward compatibility, and data recovery
- coordination between database writes and files, queues, email, or external
  APIs

Ask:

- Which layer is authoritative for this invariant?
- Can the operation partially succeed?
- What happens when a retry occurs after an uncertain result?
- Can concurrent requests violate the rule even when each request is valid?

Block on data-loss risk, ambiguous transaction ownership, missing persistence
constraints for critical invariants, or unhandled partial failure.

## 5. Behavioral and state correctness

The reviewer checks the affected workflow and its material failure paths. Decisions must
use authoritative state, and success must correspond to a real outcome.

Review:

- authorization and ownership decisions
- source-of-truth state versus cached, rendered, client, or transport snapshots
- decision inputs versus mutation inputs
- omitted, empty, stale, partial, duplicated, and conflicting values
- idempotency, retries, cancellation, and no-op behavior where relevant
- error behavior and externally visible semantics

Ask:

- Which state actually authorizes this behavior?
- Is a helper missing state that later mutation logic depends on?
- Can a stale or partial snapshot change the result?
- Can a success response occur when nothing changed?

Block when an unauthorized or invalid transition is possible, a failure is
reported as success, or critical edge-state behavior is undefined.

## 6. Simplicity, reuse, and evolutionary design

The reviewer protects both simplicity today and a clear growth path tomorrow.
Start with the smallest structure that gives the responsibility a clear owner.
Extract or split only when real evidence appears.

Review:

- whether the change follows the nearest stable local pattern
- duplicated rules or setup with a clear shared owner
- premature generic abstractions and configuration-heavy components
- functions or files that mix distinct responsibilities
- proposed folders or interfaces without current consumers
- whether extension can occur without breaking public contracts

Ask:

- What current requirement makes this abstraction necessary?
- Is duplication revealing a stable shared responsibility or only superficial
  similarity?
- Would two small explicit implementations be easier to understand today?
- What concrete growth trigger would justify splitting this file?

Block unnecessary complexity that obscures correctness. Suggest, rather than
require, speculative future flexibility.

## 7. Security, reliability, and operational fitness

The reviewer checks that the change remains safe and diagnosable under real
operating conditions.

Review:

- authentication, authorization, tenant or owner isolation, and least
  privilege
- input trust boundaries, secrets, sensitive logging, and error disclosure
- resource limits, timeouts, retries, and external-service failure
- observability: structured errors, useful logs, metrics, and trace context
- configuration defaults and environment-specific behavior
- dependency, migration, rollout, and rollback risk

Ask:

- What can an untrusted caller control?
- What is logged, and could it expose credentials or personal data?
- How does an operator distinguish invalid input from a system failure?
- Can the change be deployed and rolled back without corrupting state?

Block security, privacy, irreversible-data, or uncontrolled operational risks.
Escalate material risk decisions to the human engineer.

## 8. Verification, tests, and reviewability

The reviewer requires evidence proportional to the behavior and risk. Passing
formatting, linting, or compilation is necessary but not sufficient when
runtime behavior changes.

Review:

- focused tests at the responsibility that changed
- integration or end-to-end evidence for visible or cross-layer behavior
- success, failure, authorization, and risky state permutations
- test readability and adherence to `testing_conventions.md`
- complete diff scope, generated or mechanical fallout, and documentation drift
- reproducible verification commands and honestly reported gaps

Ask:

- Which test would fail if the risky behavior returned?
- Was the real runtime path exercised from the consumer's perspective?
- Are tests proving public behavior or mirroring implementation details?
- What was not verified, and why?

Block when critical behavior lacks credible evidence, the evidence does not
exercise the changed path, or unverified risk is presented as complete.
