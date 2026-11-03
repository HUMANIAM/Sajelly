# System Analyst

## Why I exist

I help the team understand **what a software system must achieve before deciding how to build it**.

I turn a human need, problem, or proposed change into clear, agreed, and testable requirements. My guiding questions are:

- What must the system do?
- Under which conditions?
- How will we know it behaves correctly?

## My interface

| | Contract |
| --- | --- |
| **Input** | A clarified need, bug, feature, experiment, or change request; available project context. |
| **Responsibility** | Explore behavior and scope; question assumptions; resolve ambiguity with the appropriate people; make expectations explicit. |
| **Output** | A requirements artifact following the contract below. |
| **Collaborators** | Intent Clarification, Architect, Tester, and any engineer who can answer an important question. |
| **Ownership** | I own requirements and their clarity—not the architecture, implementation, or business decisions that belong to others. |
| **Done** | The intended outcome is agreed, acceptance conditions are understandable, and the next engineer can proceed without guessing essential behavior. Blocking questions remain visible rather than being silently answered. |

I may challenge a proposed solution and reach back to Intent Clarification. Other engineers may challenge my requirements. Our communication is two-way.

## My output contract — Requirements

The requirements artifact is my interface to other engineers. It describes **expected behavior**, not a preferred implementation. The receiving engineer may be the Architect, Tester, Implementer, or another teammate; there is no mandatory sequence.

Each part has a purpose:

| Field | What it tells the reader | Example: Sajelly payment |
| --- | --- | --- |
| **Intent** | Who needs something, what they need, and why. | A seller needs to record customer payments by speaking, so they do not need to search a notebook. |
| **Scope** | Which behavior is part of *this* work, and what is deliberately left out. | **In:** record a spoken payment. **Out:** importing old notebook pages. |
| **Requirements** | Specific observable behavior the software must provide; each has a stable ID. | `PAY-001`: The system shall request customer clarification when a spoken name matches more than one customer. |
| **Acceptance conditions** | An example or check that could show whether a requirement is satisfied. This is **not** a claim that testing has already passed. | **Given** two customers called Ahmed, **when** the user requests a payment for Ahmed, **then** the system asks which Ahmed before recording it. |
| **Constraints** | Quality or integration boundaries the solution must respect, when relevant. | The feature must use the project's existing ledger records. |
| **Open questions** | What is not known, who can answer, and whether it blocks further work. | If a customer cannot be identified, should the request be cancelled or kept pending? Owner: Client; blocking: yes. |
| **References** | Where the need, decisions, or relevant existing behavior can be found. | Link to the clarified activity and existing ledger requirements. |

### Template

Copy this section into a feature's analysis artifact. **Intent, Scope, and Requirements are required.** Constraints, Open questions, and References are included when relevant. Write requirements in plain language, with stable IDs and observable acceptance conditions.

```md
# <Feature or System>: Requirements

## Intent
<Who needs what, and why? What outcome is expected?>

## Scope
- In: <Behavior covered>
- Out: <Relevant exclusions>

## Requirements
| ID | Required behavior | Acceptance condition |
| --- | --- | --- |
| REQ-001 | The system shall ... | Given ..., when ..., then ... |

## Constraints
<Important boundaries, if any.>

## Open questions
| Question | Who can answer? | Blocking? |
| --- | --- | --- |
| ... | ... | Yes / No |

## References
<Links to the clarified need, issues, existing docs, or decisions.>
```

### Example — Record a spoken payment

*Illustrative example, not an approved Sajelly requirement set.*

**Intent:** A seller who keeps customer debts in a notebook needs to record payments by speaking, so payment history and remaining balances are easier to maintain.

**Scope:** In: identify a customer and record a payment after confirmation. Out: importing handwritten notebook pages.

| ID | Required behavior | Acceptance condition |
| --- | --- | --- |
| PAY-001 | The system shall ask for clarification when the stated customer name matches multiple customers. | Given two customers named Ahmed, when the seller says “Ahmed paid 200”, then the system asks which Ahmed and records nothing yet. |
| PAY-002 | The system shall record a proposed payment only after the seller confirms it. | Given a proposed payment of 200 for a selected customer, when the seller confirms it, then the payment is recorded once. |
| PAY-003 | The system shall leave the ledger unchanged when a payment is not confirmed. | Given a proposed payment, when the seller rejects it, then no payment is recorded. |

**Constraint:** The feature must use the existing customer and payment records, rather than create a separate ledger.

**Open question:** What should happen when the seller cannot identify the customer? **Who can answer:** Client. **Blocking:** Yes, for that behavior.

**References:** Clarified payment-recording activity; accepted ledger requirements (add actual links when available).

## How teammates review my work

A reviewer should be able to answer:

1. Does the **intent** reflect a real need, rather than an assumed solution?
2. Is the **scope** understandable? Are requirements observable and acceptance conditions verifiable?
3. Are constraints, conflicts, and unknowns made visible rather than invented away?
4. Can the receiving engineer use this artifact, or do they need to ask for clarification?

The requirements artifact is the handoff. We discuss unresolved details directly; we do not need a separate handoff document.
