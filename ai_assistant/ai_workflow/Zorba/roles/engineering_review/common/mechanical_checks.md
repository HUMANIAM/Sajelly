# Mechanical Architecture Checks

## Principle

Mechanical checks protect rules that a tool can determine consistently. They
do not replace engineering review. The reviewer still owns semantic questions:
correct feature ownership, sound abstractions, authoritative state, transaction
meaning, and whether tests prove the real behavior.

Introduce checks in this order:

1. Freeze the real project structure and allowed dependency directions.
2. Start checks in report-only mode and inventory existing violations.
3. Create a narrow baseline for legacy violations rather than weakening rules.
4. Make new violations blocking.
5. Remove baseline entries as touched code is corrected.

Do not enable a large ruleset whose failures the team routinely ignores.

## Reviewer use

Consume existing automated results for the baseline/proposed revision and the
changed scope. Do not repeat a repository-wide import, cycle or structure audit.
Inspect a checker or its exceptions when changed, or when a concrete risk exposes
a coverage gap. If relevant automation is missing, report the gap and inspect the
affected boundary narrowly where practical; never assume the checker exists.
The tool suggestions and adoption steps below are guidance for project maintainers,
not setup work for a read-only reviewer. Apply human judgment questions only where
the change makes them relevant.

## Python Checks

### Import and component boundaries

Use `import-linter`, an AST-based architecture test, or an equivalent tool to
enforce contracts such as:

- `route` may import `service` and `schema`, but not feature `repo` or `model`
- `service` may import repositories, ports, schemas, and pure domain code, but
  not routes
- `repo` may import models and shared persistence helpers, but not services or
  routes
- `model` may not import repo, service, or route
- `features/shared` may not import a concrete feature
- Feature A may not import Feature B's repository or model internals
- composition/bootstrap may import all public feature entry points

Prefer contracts based on module roles and public packages over fragile checks
for individual filenames.

### Type and quality checks

- Run `mypy` or `pyright` for typed public interfaces.
- Run `ruff` for linting, import hygiene, and selected correctness rules.
- Run a formatter check rather than rewriting files in CI.
- Detect circular imports with import-linter or a dependency-graph check.
- Validate migrations against the selected migration tool.
- Run security/dependency checks appropriate to the deployment risk.

### Targeted structural tests

Small repository-specific checks can verify:

- every mounted route belongs to a feature module
- feature names follow one convention
- tests mirror production feature names
- generated directories are not manually modified
- legacy architecture allowlists do not gain entries

Avoid brittle rules such as a universal maximum file length. A long cohesive
file can be healthier than several arbitrary fragments.

## TypeScript Checks

### Import and layer boundaries

Use ESLint `no-restricted-imports`, `eslint-plugin-boundaries`,
`dependency-cruiser`, or equivalent rules to enforce:

- UI cannot import feature API, repository, or service modules
- hooks cannot import repository or API modules
- services cannot import UI or hooks
- repositories cannot import UI, hooks, or services
- shared modules cannot import concrete features
- internal imports use the selected project alias consistently
- feature-to-feature imports use approved public entry points only

Use `dependency-cruiser` or `madge` to detect dependency cycles and produce a
reviewable graph when needed.

### Type and quality checks

- Run `tsc --noEmit` for type contracts.
- Run ESLint with architecture rules enabled.
- Run formatter checks.
- Detect unused exports and accidental dependency additions when the project
  benefits from those checks.
- Validate generated API clients or contract types against their source.

## Cross-Application Contract Checks

When Python and TypeScript communicate through HTTP or events:

- choose one authoritative contract source
- generate or validate TypeScript DTOs from that source when practical
- fail CI when generated artifacts drift
- test error envelopes, authentication behavior, enums, identifiers, optional
  fields, and multipart/event payloads at the contract boundary
- prohibit backend DTO assumptions in shared frontend UI

Contract checks should detect incompatibility without requiring every service
test to duplicate the full transport schema.

## Pull-Request and Ownership Checks

Recommended repository controls:

- `CODEOWNERS` requires the engineering reviewer or engineering-review team for
  production source, migrations, public contracts, architecture configuration,
  CI, and `physical_structure.md`.
- Branch protection requires the engineering-review approval and green checks.
- A PR template includes the eight-responsibility assessment, runtime evidence,
  unverified areas, and architecture deviations.
- Changed-path logic runs only the relevant focused suites plus mandatory
  contract/boundary checks.
- Any edit to a boundary rule requires the same review as an architecture
  change; disabling the checker is not a shortcut.

## Suggested CI Shape

```text
format-check
    |
lint-and-boundaries
    |
typecheck
    |
focused-unit-and-integration-tests
    |
cross-application-contract-tests
    |
build/package
    |
risk-selected-runtime-or-e2e-tests
```

Independent jobs may run in parallel. Branch protection should require every
job relevant to the changed scope.

## What Must Remain Human Review

Tools cannot reliably decide:

- whether the correct feature owns a responsibility
- whether an abstraction is justified by real variation
- whether the source of truth is correct
- whether a transaction boundary matches the business operation
- whether success represents a meaningful state change
- whether a test scenario proves the important risk
- whether a breaking contract change is acceptable to users

The engineering reviewer must address the questions relevant to the change even
when mechanical checks pass; unrelated areas do not require investigation.

## Adoption Checklist for the New Codebase

- Map the real module graph before writing rules.
- Select one boundary tool per language unless another tool fills a distinct
  gap.
- Encode the smallest high-value dependency rules first.
- Capture existing violations in a reviewed, non-growing baseline.
- Add clear failure messages explaining the allowed destination.
- Run checks locally with the same command used in CI.
- Assign ownership for maintaining checker configuration.
- Review false positives by changing either the design or the documented rule;
  do not add unexplained exceptions.
