# Zorba — The Living Engineering Team

**Human and agent engineers, building software together.**

Zorba is named after **Alexis Zorba**, the character in Nikos Kazantzakis's novel *Zorba the Greek*. The name is a reminder to learn through doing, questioning, and experiencing the work—not merely following procedures.

## Why Zorba exists

Building useful software requires more than generating code. It requires understanding a need, making sound decisions, designing clear systems, testing real behavior, and preserving what we learn.

**Zorba is a reusable engineering team, not a Sajelly-specific workflow.** Product Engineers (humans) and Agent Engineers contribute as teammates: they have defined responsibilities, can challenge one another, and propose changes for peer review. The goal is to carry this engineering practice into future projects.

Each specialist engineer has a **purpose, input, responsibility, output, and ownership boundary**. Their role document is both an introduction and a reviewable contract. **Zorba Guide** is the contributor-facing coordination layer, not an additional technical decision-maker.

## Where to begin

| Read | Why |
| --- | --- |
| [`manifesto.md`](manifesto.md) | The team's shared identity, values, and commitments. |
| [`requirements.md`](requirements.md) | What Zorba as a system is expected to support. |
| [`docs/`](docs/) | Diagrams of the workflow, decomposition, collaboration, and review ideas. |
| [`roles/`](roles/) | Specialist contracts and the proposed [Zorba Guide](roles/zorba.md). |
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

**Current reality: human-coordinated.** Specialist role definitions and coding-agent adapters exist, but a complete Zorba-led specialist invocation has **not** yet been demonstrated. A Product Engineer can still invoke each specialist directly and review the resulting artifact.

**Proposed next experiment: Zorba Guide v0.1.** The conversational Guide will let a technical or non-technical contributor describe a need without choosing a role first. It recommends **one** bounded contribution, makes permissions visible, invokes that specialist only when authorized and supported by the adapter, and returns a plain-language checkpoint. This capability is **proposed**, not yet claimed operational.

```text
Contributor ⇄ Zorba Guide → one specialist contribution → Zorba Guide ⇄ Contributor
                      (authorized)             (evidence + next choice)
```

A contributor may approve the recommendation, inspect more detail, choose another specialist, say **“Pick for me”** (one permitted contribution, not autopilot), or stop. A technical contributor may also request `#analysis`, `#architecture`, or `#test`; the Guide remains the conversational interface. The next contribution is not invoked automatically.

**First pilot:** Report a suspected duplicate payment in ordinary language. Ask the Testing Engineer to investigate with explicit scope; return the actual result and next choices. If adapter invocation is unavailable, Zorba must say it did not run and provide an explicit handoff. Keep all PR review, code ownership, and safety controls unchanged.

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

This repository contains **role contracts and a proposed Zorba Guide pilot**, not proof of an autonomous engineering team. Direct specialist invocation and manual coordination remain available. The pilot adds **one authorized specialist invocation per contributor checkpoint**; general agent-to-agent orchestration and controlled execution environments remain future work.

Engineers may propose improvements to their own roles, contracts, templates, and practices through PRs. Their accumulated experience should improve the team, but new rules should follow evidence rather than ceremony.

**A useful first test:** Give Zorba an ordinary-language request, authorize one specialist investigation, and check whether the result is honest, evidence-backed, reviewable, and resumable. Do not claim a successful agent invocation until it actually runs.
