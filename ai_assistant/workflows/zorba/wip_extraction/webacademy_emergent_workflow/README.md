# Emergent AI Engineering Workflow

This folder defines a small, portable workflow for humans and AI agents building
software together. An agent is a teammate: it thinks, asks, challenges, and
contributes ideas while owning one clear responsibility at a time.

The workflow is **opt-in**. It does not replace a repository's existing rules,
architecture, or source of truth merely because this folder is present. A human
chooses to use it for a work item.

## Repository placement and sharing

The intended long-term placement is a personal workflow namespace:

```text
ai_assistant/
  workflow/
    <workflow-owner>/
```

Other teammates may add sibling namespaces, compare approaches, or adopt one
role at a time. The namespace identifies who maintains that workflow; it does
not give that person or workflow automatic authority over the repository.

Each role is deliberately small and shareable. An engineer may reuse a single
role without importing the whole workflow, provided its input, output, and
handoff are mapped clearly to the local process.

## Start here

For a new chat or agent:

1. Read the current project's instructions and relevant source of truth.
2. Read [TEAM_PRINCIPLES.md](TEAM_PRINCIPLES.md).
3. Read [WORKFLOW.md](WORKFLOW.md).
4. Read [HANDOFF_CONTRACT.md](HANDOFF_CONTRACT.md).
5. Read only the role file for the stage you were asked to perform.
6. Read that role's input artifacts and confirm they are current.
7. State your active role, complete only that responsibility, write its output,
   add the standard handoff, and stop.

Do not silently continue into the next role. A person or a newly invoked agent
receives the handoff and decides when the next stage begins.

## Flow and artifacts

```text
unclear human need
  -> CLIENT              -> client.md
  -> SYSTEM_ANALYSIS     -> requirements.md
  -> ARCHITECTURE        -> architecture.md
  -> SOFTWARE_DESIGN     -> design.md
  -> TESTING (strategy)  -> testing_strategy.md
  -> human implementation authorization
  -> IMPLEMENTATION      -> code changes + implementation.md
  -> TESTING (QA)        -> system/integration tests + QA.md
  -> human QA review and acceptance/rejection
  -> DEPLOYMENT          -> PR/push/integration/release + deployment.md
```

`TESTING` is intentionally invoked twice. Before implementation it defines how
the behavior will be proved. After implementation it independently exercises
the completed system and explains what changed and how it was tested.

## Role invocation

No CLI or agent framework is required. Plain instructions are enough:

```text
Use the CLIENT role for <work-item>. Produce client.md and stop at handoff.
Use SYSTEM_ANALYSIS for <work-item> from client.md.
Use TESTING in strategy mode for <work-item>.
Use TESTING in QA mode against implementation ref <ref>.
Use DEPLOYMENT for the human-authorized action <action and destination>.
```

An invocation selects a responsibility; it does not grant permission to merge,
push, publish, deploy, spend money, use credentials, or make a human decision.
Those actions require their normal explicit authorization.

## Contents

- `TEAM_PRINCIPLES.md` — how humans and agents work together.
- `WORKFLOW.md` — stages, gates, artifacts, and return paths.
- `HANDOFF_CONTRACT.md` — one concise handoff shape used by every role.
- `roles/` — one responsibility per role.

Projects may store the generated artifacts wherever their conventions require.
Use existing issue trackers or specifications when they already provide the
same durable information; do not create duplicate paperwork.

This V1 deliberately contains no orchestration, tools, playbooks, or template
library. Let real work show what deserves to be added.
