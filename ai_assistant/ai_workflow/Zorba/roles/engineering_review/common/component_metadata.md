# Component metadata for focused review

Each business feature/component has a `component_name.meta` file beside its
implementation, for example `src/features/notebook_import/notebook_import.meta`.
Replace `component_name` with the actual component name. This file is a short
navigation map for engineers and reviewers, not a replacement for code, tests,
approved requirements or automated architecture checks.

## Content contract

Use a JSON object with these fields. Keep descriptions short and references
specific. Dependency direction is from this component to what it uses.

| Field | Type | Meaning |
| --- | --- | --- |
| `component` | string | Business feature/component name. |
| `description` | string | What the component is meant to do and the responsibility it owns. |
| `internal_dependencies` | array of objects | Dependencies within the project: each has `name`, repository-relative `reference` and short `purpose`, all strings. Reference the relevant public interface, component metadata or contract. |
| `external_dependencies` | array of objects | Libraries, services or external systems: each has `name`, `reference` and short `purpose`, all strings. Reference the manifest, adapter/configuration, or approved external contract. |

Both dependency arrays are present; use `[]` when there are none. Internal means
inside the project, not private implementation access. List direct material
dependencies rather than copying the full transitive graph or lockfile.

```json
{
  "component": "notebook_import",
  "description": "Extract candidate entries from notebook photos for review and send accepted entries to the ledger.",
  "internal_dependencies": [
    {
      "name": "ledger",
      "reference": "src/features/ledger/service.py",
      "purpose": "Persist accepted entries through the ledger public service."
    }
  ],
  "external_dependencies": [
    {
      "name": "vision provider",
      "reference": "src/features/notebook_import/vision_adapter.py",
      "purpose": "Extract candidate entries from images."
    }
  ]
}
```

This is an illustrative future component, not a claim those files exist.

## Reviewer use and maintenance

Read metadata only for affected components. Consult a listed dependency when a
changed behavior raises a question that dependency can answer. Do not follow all
references automatically. Compare relevant declarations with actual imports,
interfaces and check results; metadata can be stale or incomplete.

When a change alters purpose or dependencies, its metadata should change with it.
A new component's metadata is part of its review context. If metadata is missing
or stale, use targeted inspection around the changed files and record the limit.
Do not automatically block a safe review because a navigation file is absent;
block when a material ownership or dependency risk cannot be resolved. Do not
create missing feature metadata during a read-only review.

Request producers can supply `.meta` references in `change.artifact_refs`, using
the existing `artifactReference` shape. No new request field is required. Record
useful metadata references in assessment evidence and relevant verification gaps.
