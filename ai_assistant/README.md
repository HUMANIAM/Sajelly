# AI-assisted engineering workspace

> “Raise your words, not your voice. It is rain that raises flowers, not thunder.”
>
> — Rumi

This README is for **technical and non-technical contributors** who have cloned
Sajelly and want to set up an AI assistant for the project. The rest of this
folder preserves how people and AI assistants collaborate, how responsibilities
are divided, and how ideas become reviewable engineering work.

It is not the Sajelly application, an autonomous agent pipeline, or a replacement
for engineering judgment. Application code belongs in `frontend/` and `backend/`;
accepted project knowledge belongs in the repository-level [`docs/`](../docs/).

## What is in this folder?

```text
ai_assistant/
├── ai_workflow/
│   └── Zorba/          # Reusable roles, principles, adapters, tools, and templates
├── features/           # Sajelly-specific feature and epic workspaces
└── tmp/                # Disposable, Git-ignored experiments and handoffs
```

| Area | Use it for | Do not use it for |
| --- | --- | --- |
| [`ai_workflow/Zorba/`](ai_workflow/Zorba/) | Reusable engineering roles, team principles, collaboration contracts, diagrams, templates, and agent-runtime adapters. | Sajelly-specific requirements or implementation decisions. |
| [`features/`](features/) | Exploring and refining a Sajelly capability, preserving working context, and holding feature-level artifacts. | Treating an unreviewed draft as accepted project truth. |
| [`ai_workflow/Zorba/tools/`](ai_workflow/Zorba/tools/) | Reusable, tested utilities that help human and agent engineers work more clearly, safely, or efficiently. | Unreviewed experiments, duplicated project knowledge, or hidden automation. |
| `tmp/` | Short-lived probes, experiments, generated handoffs, and notes that can be discarded. | Durable knowledge. Promote anything important to a tracked feature, `docs/`, code, or tests. |

## How this workspace relates to the repository

Sajelly deliberately separates different kinds of knowledge:

- The repository [`README`](../README.md) is the technical contributor entry
  point and maps each kind of knowledge to its owning document.
- Repository [`docs/`](../docs/) is **project memory**: accepted requirements,
  architecture, decisions, and other durable Sajelly knowledge.
- [`features/`](features/) is **working memory**: proposals, exploration, and
  artifacts that may still change during engineering work.
- [`ai_workflow/Zorba/`](ai_workflow/Zorba/) is **engineering memory**: reusable
  roles and practices intended to improve the team across projects.
- `frontend/`, `backend/`, tests, and configuration are the actual software and
  delivery assets.

A role document such as
[`roles/architecture.md`](ai_workflow/Zorba/roles/architecture.md) defines the
Architect's responsibility and boundaries. A feature-level `architecture.md`
would describe an architecture produced for that specific feature. They are
related, but they are not interchangeable.

## Set up the AI assistant after cloning

Run all commands from the Sajelly repository root. Python 3.8 or newer is the
only requirement for the setup utility; it uses the Python standard library and
does not install packages.

The one entry point to remember is:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py
```

With no arguments, Zorba explains the available commands. Start by checking the
current laptop:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --check
```

The report separates three things:

- whether the vendor-neutral Zorba Guide and seven specialist roles are valid;
- whether Codex is installed and its project setup matches those definitions;
- whether Claude is available and which parts of its integration are still
  work in progress.

The check is read-only. It never creates or changes setup files, and
configuration readiness is not presented as proof that an assistant or
specialist actually ran.

### Set up Codex

Run:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --setup codex
```

You remain in control:

- if `.codex/agents/` is missing, Zorba asks whether to create it;
- if it already exists, Zorba asks whether to sync it;
- answering no leaves the setup unchanged.

To deliberately refresh an existing setup from the vendor-neutral Zorba
definitions, run:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --sync codex
```

If the Codex folder is missing, sync asks whether to set it up. One yes creates
the folder and generated files without asking the same question again. Sync
does not use a Codex copy as its source: it generates the adapter from
[`specialists.json`](ai_workflow/Zorba/specialists.json) and the canonical
[`roles/`](ai_workflow/Zorba/roles/) documents.

If sync finds Codex agents that are no longer in `specialists.json`, it lists
them and asks about each deletion separately. Answering no preserves that file
and leaves `--check` non-green so the unresolved drift stays visible.

Codex project-scoped custom agents live in `.codex/agents/`, as described by
the [official Codex documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

### Claude status

Claude has a thin conversational entry through repository `CLAUDE.md`, but its
specialist adapter is **work in progress**. The following commands report that
status honestly and do not create partial configuration:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --setup claude
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --sync claude
```

### Verify the conversation

After setup, open a fresh Codex CLI or IDE-extension session from the Sajelly
repository and say:

```text
Zorba, help me get started with Sajelly.
```

Zorba asks only whether you want **technical** or **non-technical** guidance,
then adapts the introduction. A CV, experience summary, or learning preference
is optional and must not block onboarding. This fresh conversation is the live
smoke test; `--check` cannot perform it for you.

## How Zorba guides contributions

Zorba defines seven specialist responsibilities:

| When you need to… | Start with… |
| --- | --- |
| Clarify a need, problem, or intended outcome | [Intent Engineer](ai_workflow/Zorba/roles/intent_clarification.md) |
| Define observable behavior and constraints | [System Analyst](ai_workflow/Zorba/roles/system_analysis.md) |
| Decide system boundaries and interactions | [Architect](ai_workflow/Zorba/roles/architecture.md) |
| Design component behavior and interfaces | [Designer](ai_workflow/Zorba/roles/design.md) |
| Build the smallest correct change | [Implementer](ai_workflow/Zorba/roles/implementation.md) |
| Produce evidence and expose quality risks | [Testing Engineer](ai_workflow/Zorba/roles/testing.md) |
| Prepare delivery, operation, and recovery | [Deployment Engineer](ai_workflow/Zorba/roles/deployment.md) |

The [Zorba Guide](ai_workflow/Zorba/roles/zorba.md) is a
contributor-facing coordination layer. It can recommend one useful specialist
contribution and return the result to the contributor. It is not an additional
technical owner.

**Current reality:** the workflow is human-coordinated. Role contracts and
Codex adapters exist, but this repository does not claim that an autonomous
engineering team or end-to-end Zorba orchestration is operational. Do not
invent a specialist result or silently continue to another role.

Experienced contributors may still invoke an available specialist directly;
Zorba does not need to stand between them and the appropriate role.

## A practical contribution pattern

For each contribution:

1. **State the outcome.** Describe the problem to solve or question to answer.
2. **Bound the work.** Name what may be read or changed and what is excluded.
3. **Choose the responsible role.** Use the smallest relevant contribution;
   do not force every role into the work.
4. **Ask for evidence.** Define the artifact, checks, or observed behavior that
   will support the result.
5. **Keep knowledge in the right place.** Preserve exploration in the feature
   workspace and move accepted knowledge into `docs/`, code, tests, or
   configuration as appropriate.
6. **Review independently.** A generated artifact, passing build, or confident
   answer is not proof that the user-facing outcome works.
7. **Leave a clear handoff.** Record actual status, changed artifacts, evidence,
   limitations, and the next decision without pretending incomplete work is
   complete.

## Team expectations

- Roles define responsibility, not rank. Human and agent engineers may
  question assumptions and propose better approaches.
- Do not widen scope across product, architecture, implementation, testing, or
  deployment boundaries without making the change explicit.
- Verify behavior in proportion to its risk. For user-facing changes, exercise
  the real user path rather than relying only on lint, type checking, or a
  build.
- Preserve important decisions and evidence so another engineer can continue
  without the original chat session.
- Use synthetic data in shared development materials. Protect customer
  records, financial information, recordings, credentials, and private data.
- Propose small, understandable changes through Git and pull requests. State
  what changed, why, how it was verified, and what remains uncertain.

The goal is not to create more ceremony. It is to help engineers contribute
with clarity, care, and enough evidence that the next person can understand and
trust the work.
