# Zorba onboarding qualification — 2026-11-04

**Status:** The setup and synchronization contract is implemented and passes
its automated qualification. The current Codex project configuration is in
sync. Live contributor onboarding and specialist invocation remain deliberately
unverified and are owned by the project owner's first non-technical journey.

This record separates configuration readiness, automated contract evidence,
client-environment readiness, and contributor-experience qualification. Passing
one category does not imply that another passed.

## 1. Read-only setup verification

**Expectation:** `--check` validates vendor-neutral Zorba, reports Codex and
Claude separately, distinguishes a missing setup from an invalid one, exits
nonzero for required drift, and never changes files.

**Observation:** Passed. Temporary-repository tests cover missing and ready
Codex setups and compare file snapshots before and after the check. The current
checkout reports:

```text
[PASS] Vendor-neutral Zorba defines the Guide and 7 canonical specialists
[PASS] AGENTS.md routes Zorba to the canonical Guide
[PASS] Codex matches vendor-neutral Zorba (7 specialists)
[PASS] CLAUDE.md routes Zorba to the canonical Guide
[WIP] Claude specialist setup and sync are not implemented yet
[NOT VERIFIED] Client loading and specialist invocation require a fresh live session
```

**Limitation:** Executable detection does not prove that a client can parse its
global configuration, authenticate, load repository instructions, or run a
specialist. The output keeps that boundary explicit.

## 2. Codex setup and synchronization

**Expectation:** Codex files are rendered from `specialists.json` and canonical
role documents. Setup and sync preserve contributor control. If an installed
agent is no longer in the manifest, sync asks before deleting it.

**Observation:** Passed. The CLI now:

- asks before creating a missing `.codex/agents/` directory;
- asks before syncing an existing setup when `--setup codex` finds drift;
- lets `--sync codex` transition into setup with one creation confirmation;
- lists orphaned TOML files and asks about each deletion separately;
- deletes confirmed orphans and preserves declined ones;
- leaves readiness non-green when an orphan is preserved, making the remaining
  drift visible;
- derives team size dynamically rather than embedding a seven-agent invariant;
- renders TOML-safe strings and validates them with `tomllib` or `tomli`.

The actual project setup was synchronized from the current seven-entry manifest.
No orphaned project agent existed, so the real sync deleted nothing.

## 3. Tool project and contributor documentation

**Expectation:** Reusable Zorba code has one dependency definition, a
reproducible pytest workflow, and a registry that lets a person or agent find
and extend supported tools.

**Observation:** Passed. Zorba's Python tooling now lives under
`ai_assistant/ai_workflow/Zorba/tools/` with:

- `pyproject.toml` as the only runtime and development dependency definition;
- a tool-local `.venv` workflow;
- pytest configuration and behavioral tests;
- a registry table with entry points, purpose, status, and tests;
- guidance for adding discoverable tools without duplicating canonical
  knowledge.

The documented pytest command completed with **23 passed**.

## 4. Technical and non-technical onboarding contract

**Expectation:** An ordinary-language request reaches the canonical Zorba Guide.
Zorba asks only whether the contributor wants technical or non-technical
guidance. CV, experience, and learning preferences are optional.

**Observation:** Static contract validation passed. `AGENTS.md` and `CLAUDE.md`
point to the same canonical Guide, and the Guide contains both contributor
paths without introducing an onboarding agent, database, or orchestration
framework.

**Qualification boundary:** Capturing prescribed technical and non-technical
responses is not an artifact-improvement task. The meaningful test is whether
Zorba can carry an actual newcomer into a useful contribution and create the
right artifacts for that person's background. The project owner will perform
that first non-technical journey. Zorba's team retains freedom to adapt the
onboarding rather than follow a fixed transcript.

## 5. Client environment investigation

**Codex observation:** Resolved. The project owner updated the selected npm
installation from `codex-cli 0.111.0` to `0.166.0`. The incompatible active
`config.toml` is absent and retained as `config.toml.bk`. `codex login status`
reports ChatGPT authentication, and `codex doctor --summary` reports `19 ok`,
`0 fail`, healthy databases, and working WebSocket and HTTP connectivity.

The remaining diagnostic warning says some historical rollout files are absent
from the state index. It does not block a new session and does not justify a
database repair while current state remains healthy.

**Claude observation:** Claude Code `2.1.50` is installed, but `claude auth
status` reports `loggedIn: false` and `authMethod: none`.

The cause, completed resolution, remaining limitation, and official Codex
references are recorded in
[`client_environment_investigation.md`](client_environment_investigation.md).
The repository changes did not alter global configuration or authentication.

## 6. Live specialist qualification

No specialist contribution was run. The project owner explicitly reserved this
verification and will act as Sajelly's first non-technical contributor. Setup
readiness therefore must not be reported as proof of specialist discovery or
invocation.

## Reproducible local checks

Run from the repository root:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --check
ai_assistant/ai_workflow/Zorba/tools/.venv/bin/pytest -c ai_assistant/ai_workflow/Zorba/tools/pyproject.toml
bash ai_assistant/ai_workflow/Zorba/tests/test_onboarding_contract.sh
```

## Remaining owner-controlled qualification

After the selected client environment is repaired, the project owner will:

1. start a fresh session and say, “Zorba, help me get started with Sajelly”;
2. choose non-technical guidance without supplying a CV or learning profile;
3. judge whether Zorba leads to a meaningful task and creates suitable
   contributor-specific artifacts;
4. decide whether and when to authorize any specialist contribution.

These are intentionally not automated or claimed as completed here.
