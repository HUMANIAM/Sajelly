# Testing Conventions

## Purpose

Tests are executable explanations of behavior. They must make the rule, setup,
action, and expected outcome easy to understand. Reuse should remove mechanical
noise without hiding the scenario.

## Core Rules

- Keep one behavior or business rule per test.
- Use clear names that describe outcome and condition.
- Keep setup only as large as the behavior requires.
- Prefer public behavior over implementation-detail assertions.
- Use the strongest practical boundary for the risk being tested.
- Treat test code with the same ownership, naming, and duplication standards as
  production code.
- A passing unit suite does not replace runtime or integration evidence when
  cross-layer behavior changed.

## Naming

Good Python shapes include:

```python
def test_rejects_duplicate_email_when_account_already_exists(): ...
def test_rolls_back_file_metadata_when_upload_fails(): ...
```

Good TypeScript shapes include:

```typescript
it("keeps newer results when an older request finishes last", () => {});
it("shows the authorization error without reporting success", () => {});
```

Avoid names such as `test_create`, `works`, or `handles_error`. A test name
should identify the observable rule without reading its body.

## Given, When, Then

Use short Gherkin-style comments for new or materially rewritten tests when
they make the story clearer:

```python
# Given: an existing account owns the canonical email
# When: another account is created with an equivalent email
# Then: the operation fails without inserting a row
```

Keep each comment concrete. Do not add large prose blocks that merely repeat
the code.

## Fixture and Helper Ownership

Use the narrowest reusable scope:

| Location | Responsibility |
| --- | --- |
| test-local fixture/helper | Setup used only by one test module or narrow scenario |
| `tests/features/<feature>/conftest.py` | Feature-local fixtures and default boundary mocks |
| `tests/features/<feature>/data.py` | Reusable feature sample data and builders |
| `tests/features/<feature>/test_helpers.py` | Feature-local mechanics reused across test modules |
| `tests/shared_test_helpers.py` | Stable mechanics genuinely reused across features |
| root `conftest.py` | Runtime-wide fixtures such as application, database, or authenticated client |

Fixture groups should represent a coherent capability, such as an authenticated
client or persisted catalog item. Do not create one enormous fixture that
silently builds half the application.

## Reuse Without Hiding Meaning

Extract repeated mechanics, not the important scenario.

Good reuse:

- database/session setup
- authenticated clients
- deterministic clocks or identifiers
- standard valid object builders
- repeated external-boundary mocks
- mechanical response assertions shared across a contract family

Keep visible in the test:

- the value or condition that triggers the behavior
- the action under review
- the outcome that proves the rule
- meaningful differences between cases

A helper should make the test shorter and clearer. If understanding the test
requires opening several helper files, the abstraction has hidden too much.

## Test Data

- Prefer small builders with valid defaults and explicit overrides.
- Keep feature-local data close to the feature tests.
- Use the original input object in assertions instead of retyping its literals
  when that makes the data flow clearer.
- Do not share mutable data between tests.
- Avoid random data unless the seed and failing example are reproducible.

## Mocking

- Mock external or architectural boundaries, not the unit's internal logic.
- Define reusable default feature mocks in the feature's `conftest.py` or
  equivalent setup module.
- Use inline patching only for a narrow test-specific override.
- Assert important collaboration contracts, but avoid asserting every internal
  call when the observable result is sufficient.
- Prefer a real repository with an isolated database for query semantics.
- Prefer a fake adapter when it gives clearer behavior than a deeply configured
  mock.

## Layer-Appropriate Evidence

### Python

- Model/schema tests: constraints, parsing, normalization, and serialization.
- Repository tests: queries, ordering, persistence, uniqueness, and transaction
  behavior.
- Service tests: business decisions, authorization, orchestration, and partial
  failure.
- Route/integration tests: transport contract, dependency wiring, status/error
  mapping, and persisted result.
- End-to-end tests: critical workflows across real application boundaries.

### TypeScript

- API tests: request shape, credentials, payload encoding, and error decoding.
- Repository tests: DTO/domain mapping and transport-error classification.
- Service tests: pure business decisions and workflows.
- Hook tests: loading/error/data transitions, cancellation, stale results, and
  prop/state synchronization.
- UI tests: accessible behavior and user-visible interactions.
- End-to-end tests: critical user journeys against the integrated application.

## Required Risk Scenarios

Choose relevant scenarios rather than copying a universal list:

- success with a meaningful state change
- validation or domain rejection
- unauthenticated and unauthorized access
- not-found and conflicting state
- omitted versus empty input
- stale, partial, duplicated, or reordered state
- retry, cancellation, timeout, or concurrent update
- external dependency failure
- rollback or compensation after partial work
- no-op requests that must not claim a false success

The reviewer should be able to point to the test that prevents each material
risk from recurring.

## Test Growth Rule

Start with the test next to the behavior's existing feature test module. Split
a test file when it covers multiple independent responsibilities or becomes
difficult to read as one story. Split by behavior or layer, not by arbitrary
test count.

Create shared fixtures or helpers only after repeated mechanics have a stable
owner. A little explicit repetition is preferable to an abstraction that hides
the business scenario.

## Reviewer Checklist

- Does each test name communicate the behavior and condition?
- Is there one primary rule per test?
- Can the scenario be understood without chasing helpers?
- Are repeated mechanics extracted at the narrowest correct scope?
- Are mocks placed at real boundaries?
- Do integration tests assert both the external result and important persisted
  state?
- Are risky state permutations represented?
- Was the changed runtime path exercised from the consumer's perspective?
- Are skipped or missing tests explained honestly?
