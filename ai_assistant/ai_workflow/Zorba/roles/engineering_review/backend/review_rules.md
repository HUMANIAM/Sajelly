# Backend Engineering Review Criteria

Follow the [common review workflow](../common/review_protocol.md#common-review-workflow).
These criteria are a catalogue of questions to apply to the changeset, not a
repository-wide audit. Select relevant questions using changed behavior, risk,
affected `component_name.meta` files and the target project's confirmed contracts.
Consult engineering/project memory only where it informs the change. Mechanical
boundary and dependency checks use automated evidence; judgment evaluates whether
the affected architecture is appropriate. WEBAcademy patterns below are conditional
examples, not universal filenames or mandatory layers.

## Backend Review Criteria

### `BE-01` Application composition

- Bootstrap creates and configures the application, middleware, lifecycle,
  providers, and public route registration.
- Feature rules and raw queries do not accumulate in bootstrap code.
- Startup/shutdown work is ordered, failure-aware, and testable.

### `BE-02` Feature ownership and dependency flow

- The owning feature is obvious.
- Runtime flow is route/handler -> service -> repo -> model/database.
- Lower layers do not import higher layers.
- Cross-feature work uses explicit public services or ports, not repository or
  model internals.
- Shared packages have a stable named responsibility.

### `BE-03` Models, migrations, and persistence invariants

- Models own persisted shape, relationships, and database constraints.
- Critical invariants are protected at the database boundary when applicable.
- Migrations preserve or deliberately transform existing data.
- Forward, rollback, compatibility, and deployment-order risks are explicit.

### `BE-04` Schemas and transport contracts

- Schemas own external shape, parsing, serialization, and boundary validation.
- Schema and model responsibilities are not collapsed for convenience.
- Optionality, enums, identifiers, versioning, error envelopes, and upload or
  event payloads are explicit.
- Consumer compatibility is reviewed from the actual contract.

### `BE-05` Repository semantics

- Repositories own SQL/query and persistence mechanics only.
- Filtering, ordering, pagination, locking, uniqueness, and not-found behavior
  are deterministic.
- Commit/flush behavior supports the service-owned transaction boundary.
- Repositories do not contain authorization, workflow, HTTP, or presentation
  decisions.

### `BE-06` Services and transactions

- Services own business rules, authorization/ownership checks, orchestration,
  and the complete business transaction.
- Decision inputs use authoritative persisted/domain state.
- Partial failure, retry, idempotency, concurrency, and no-op behavior are
  explicit where material.
- Presenter coordination is pure and side effects occur in a safe order.

### `BE-07` Routes and error mapping

- Routes/controllers remain thin protocol boundaries.
- Dependency wiring and authentication guards are explicit.
- Domain/application failures map consistently to external status and error
  contracts.
- Routes do not query or mutate persistence directly.
- Authorization is not weakened by test or development conveniences.

### `BE-08` Ports, adapters, and side effects

- External capabilities are isolated behind ports when substitution, provider
  detail, or failure behavior justifies the seam.
- Adapters own vendor/protocol mechanics, timeouts, and provider errors.
- Database plus file/message/email/external operations have rollback,
  compensation, or an explicitly accepted consistency model.
- Logs and errors do not leak secrets or sensitive data.

### `BE-09` Backend verification

- Models/schemas prove constraints and validation.
- Repository tests prove real query and persistence semantics.
- Service tests prove rules, authorization, orchestration, and failure paths.
- Route/integration tests prove transport, dependencies, errors, and persisted
  outcomes.
- Critical workflows receive runtime or end-to-end evidence proportional to
  risk.

### `BE-10` Dependency and environment discipline

- New packages satisfy `dependency_policy.md`.
- Python standard-library and installed capabilities were considered first.
- Tooling runs in the project-local environment.
- Dependency, migration, and architecture configuration changes are explicit
  and reviewable.
- Mechanical checks enforce real import and contract rules without unexplained
  exceptions.

## Conditional application

Do not force React, Vite, FastAPI, SQLModel, Figma, an ORM, or the WEBAcademy `skill` feature on an unrelated project. For an unaffected criterion, use `not_applicable` with a concise changeset-based reason; no unrelated investigation is required. If evidence is missing, use `not_verified`, not `pass`.
