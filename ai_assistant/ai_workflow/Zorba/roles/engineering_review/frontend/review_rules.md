# Frontend Engineering Review Criteria

Follow the [common review workflow](../common/review_protocol.md#common-review-workflow).
These criteria are a catalogue of questions to apply to the changeset, not a
repository-wide audit. Select relevant questions using changed behavior, risk,
affected `component_name.meta` files and the target project's confirmed contracts.
Consult engineering/project memory only where it informs the change. Mechanical
boundary and dependency checks use automated evidence; judgment evaluates whether
the affected architecture is appropriate. WEBAcademy patterns below are conditional
examples, not universal filenames or mandatory layers.

## Frontend Review Criteria

### `FE-01` Application composition

- Entry points only mount or compose the application.
- App shell owns global providers, routes, and top-level boundaries.
- Feature workflows do not accumulate in app or page modules.
- URL and navigation behavior match the application's routing contract.

### `FE-02` Feature ownership and dependency flow

- The owning feature is obvious.
- The default flow is page/container -> hook -> service -> repo -> API.
- Consumers use public contracts rather than deep feature internals.
- Shared modules do not import concrete features.
- Cross-feature dependencies are deliberate and acyclic.

### `FE-03` Transport and API contract

- API modules own request construction, authentication transport, DTOs,
  response decoding, and transport errors.
- Payload, optionality, enum, ID, error, and upload semantics match the actual
  backend contract.
- UI, hooks, and services do not call raw transport directly.
- Contract uncertainty is surfaced rather than guessed.

### `FE-04` Repository boundary

- Repositories insulate services from DTOs and transport failures.
- Mapping exists only for a real semantic or shape difference.
- Identity/pass-through mapping is accepted when contracts already match.
- Pure domain rules do not migrate into repository code.

### `FE-05` Service decisions

- Services own pure business decisions and frontend workflows.
- Services do not import React, UI, or lifecycle concerns.
- Decision helpers receive every authoritative state input required by later
  mutation logic.
- No service reports success without the promised meaningful outcome.

### `FE-06` Hooks and runtime state

- Hooks own UI runtime state, effects, cleanup, cancellation, and service
  orchestration.
- Loading/error/data transitions are deterministic.
- Stale responses cannot overwrite newer state.
- Controlled or externally seeded state stays synchronized.
- Hooks do not contain business policy or call repos/API directly.

### `FE-07` UI composition and accessibility

- Presentation components receive typed values and callbacks.
- Shared UI owns generic rendering, accessibility, and interaction mechanics.
- Domain rules remain in the feature layers.
- Components grow bottom-up rather than becoming page-sized reuse units.
- Labels, IDs, focus, keyboard input, semantics, overflow, and repeated
  instances behave correctly.

### `FE-08` Design and visible behavior

- An approved design/source artifact is treated according to the target
  project's authority rules.
- The exact target state/variant and allowed deviations are explicit.
- Refactoring does not conceal whether parity was first achieved.
- Evidence covers the interaction-state matrix, not only one screenshot.
- If no external design contract exists, review against the stated product and
  design-system contract rather than inventing one.

### `FE-09` Frontend verification

- Pure API/repo/service rules have focused tests where requested by project
  policy.
- Hooks and UI are tested at the interaction boundary.
- Critical visible flows have browser or end-to-end evidence appropriate to
  risk.
- Success, validation, authorization, failure, stale, empty, and partial states
  are covered when relevant.
- Build/type/lint success is not presented as runtime proof.

### `FE-10` Dependency and toolchain discipline

- New packages satisfy `dependency_policy.md`.
- Existing platform and installed capabilities were considered first.
- Framework, build, lint, and generated-code changes are scoped and reviewed.
- Architecture checks protect real boundaries without creating unexplained
  exceptions.

## Conditional application

Do not force React, Vite, FastAPI, SQLModel, Figma, an ORM, or the WEBAcademy `skill` feature on an unrelated project. For an unaffected criterion, use `not_applicable` with a concise changeset-based reason; no unrelated investigation is required. If evidence is missing, use `not_verified`, not `pass`.
