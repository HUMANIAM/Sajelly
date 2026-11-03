# Zorba — The Living Engineering Team

**Human and agent engineers, building software together.**

Zorba is named after **Alexis Zorba**, the character in Nikos Kazantzakis's novel *Zorba the Greek*. The name is a reminder to learn through doing, questioning, and experiencing the work—not merely following procedures.

## Why Zorba exists

Building useful software requires more than generating code. It requires understanding a need, making sound decisions, designing clear systems, testing real behavior, and preserving what we learn.

**Zorba is a reusable engineering team, not a Sajelly-specific workflow.** Product Engineers (humans) and Agent Engineers contribute as teammates: they have defined responsibilities, can challenge one another, and propose changes for peer review. The goal is to carry this engineering practice into future projects.

Each engineer has a **purpose, input, responsibility, output, and ownership boundary**. Their role document is both an introduction to the engineer and a contract that teammates can understand and review.

## Where to begin

| Read | Why |
| --- | --- |
| [`manifesto.md`](manifesto.md) | The team's shared identity, values, and commitments. |
| [`requirements.md`](requirements.md) | What Zorba as a system is expected to support. |
| [`docs/`](docs/) | Diagrams of the workflow, decomposition, collaboration, and review ideas. |
| [`roles/`](roles/) | Each engineer's responsibility and documented input/output contract. |
| [`templates/`](templates/) | Shared Git commit and pull request conventions. |

## Meet the engineers

| Engineer | Main question | Typical output |
| --- | --- | --- |
| [Intent Engineer](roles/intent_clarification.md) | What are we trying to achieve, and why? | `intent_clarification.md` |
| [System Analyst](roles/system_analysis.md) | What must the system do, under which conditions, and how will we verify it? | Requirements / `system_analysis.md` |
| [Architect](roles/architecture.md) | What are the system's building blocks, responsibilities, and interactions? | `architecture.md`, diagrams, important ADRs |
| [Designer](roles/design.md) | How should the relevant components work internally? | `design.md` and detailed interface/design artifacts |
| [Implementer](roles/implementation.md) | How do we turn the agreed work into reliable software? | Code, relevant tests, and a reviewable PR |
| [Testing Engineer](roles/testing.md) | What evidence demonstrates the required behavior, and what remains unverified? | Tests, strategies, verification/QA reports as needed |
| [Deployment Engineer](roles/deployment.md) | Can we build, deliver, observe, and recover the software reliably? | Delivery assets and operational evidence as needed |

**Roles are responsibilities, not ranks or a mandatory sequence.** Any Product Engineer can approach any engineer. A bug may start with the Implementer; a new product need may start with Intent Clarification.

## How to use Zorba today

**Current state: manually coordinated.** Agent Engineers are invoked individually; they do **not** yet communicate with one another directly or run an automated orchestration workflow. The Product Engineer supplies context, reviews the result, and takes the agreed artifact to the next engineer when necessary.

For example, to explore a new Sajelly capability:

1. **Intent Engineer:** Provide the idea or problem. Review the clarified activity and desired outcome.
2. **System Analyst:** Supply the accepted intent and project context. Review the expected behaviors and acceptance conditions.
3. **Architect:** Supply the agreed requirements and current system context. Review boundaries, interactions, runtime behavior, and significant decisions.
4. **Continue only as needed:** Involve the Designer, Implementer, Tester, or Deployment Engineer according to the work's goal.

This is an **example path**, not a rule to invoke every engineer. If an artifact is unclear, return to its responsible engineer with a concrete question. Do not silently invent an answer.

### Engineering artifacts and memory

These are deliberately different spaces:

- **`ai_assistant/features/<feature>/`** — working space for ideas, discussions, refinement, and phase artifacts; it preserves the history of engineering thought.
- **Repository `docs/`** — accepted project knowledge: requirements, architecture, designs, ADRs, RFCs, and retrospectives.
- **Zorba's roles, templates, manifesto, and future playbooks/tools** — reusable **engineering memory**, designed to travel to other projects.
- **Code, tests, configuration, and data** — the actual project context and deliverables.

An engineer's `roles/architecture.md` describes **who the Architect is and its contract**. A feature's `architecture.md` describes **the architecture produced for that feature**. They serve different purposes.

Work is proposed through GitHub PRs. Draft PRs represent work in progress; changes ready for review should state the goal, solution, review focus, verification performed, and limitations. Another engineer reviews before merging.

## Decomposition without a planning agent

Work is organized as **Epic → Feature → Task**:

- **Epic:** A product capability or responsibility, defined with input from the System Analyst and Architect.
- **Feature:** A vertical slice or focused engineering work package (including bugs, investigations, testing, performance, or experiments).
- **Task:** A small, reviewable contribution toward a feature.

Every task belongs to a feature; every feature belongs to an epic. The objective is to make ownership, dependencies, and verification understandable—not to create more process.

## Current boundaries and next steps

This repository contains the **initial role and workflow design**, not proof that an autonomous engineering team is operational. We are starting with Markdown contracts, independent agent sessions, human coordination, and peer-reviewed artifacts. Agent-to-agent communication, tool integration, and controlled execution environments are future work.

Engineers may propose improvements to their own roles, contracts, templates, and practices through PRs. Their accumulated experience should improve the team, but new rules should follow evidence rather than ceremony.

**A useful first test:** Give one engineer a real, scoped activity. Check whether its input is understandable, its output can be reviewed, and another engineer could continue from the artifact without guessing essential facts.
