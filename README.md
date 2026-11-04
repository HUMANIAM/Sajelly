<h1 align="center">Sajelly</h1>

<p align="center"><strong>Technical entry point for contributors</strong></p>

Welcome to Sajelly ❤️

This README helps engineers understand the repository, find the authoritative
documents for their work, and begin contributing without duplicating knowledge.

Sajelly (Arabic: **سجلى**, meaning “record for me”) is a people-first product.
Its purpose, users, experience, capabilities, and product boundaries are owned
by the [product definition](docs/product_definition.md).

## Project status

**Sajelly is currently in planning and system design. There is no runnable
application in this repository yet.**

The repository contains the product definition, system requirements,
architecture drafts, delivery epics, engineering workflow, and an early UI
reference. Installation, development, testing, and deployment commands will be
added with the first implementation.

## Documentation map

Each document owns a different kind of knowledge. Follow its links when broader
context is needed; do not copy that context into another document.

| Document | Owns | Primary readers |
| --- | --- | --- |
| [Product definition](docs/product_definition.md) | Product purpose, users, value, intended experience, capabilities, principles, and scope. | Everyone; especially product, intent, and analysis contributors. |
| [System requirements](docs/system_requirements.md) | Testable system behavior, constraints, requirement IDs, and acceptance examples. | Analysts, designers, implementers, and testers. |
| [Backend architecture](backend/docs/architecture/README.md) | System boundaries, components, responsibilities, interactions, and technical trade-offs. | Architects, designers, implementers, testers, and deployment engineers. |
| [Architecture diagrams](backend/docs/architecture/README.md#3-the-system-in-four-views-c4) | Visual system context, containers, and backend components. | Technical contributors who need a structural overview. |
| [Feature workspaces](ai_assistant/features/) | Epic boundaries, working artifacts, and feature-specific exploration. | Epic owners and contributing specialists. |
| [AI-assisted engineering workspace](ai_assistant/README.md) | How human and agent engineers collaborate and where their artifacts belong. | All human and agent contributors. |
| [Zorba engineering team](ai_assistant/ai_workflow/Zorba/README.md) | Reusable engineering roles, collaboration contracts, and adapters. | Contributors using or improving the engineering workflow. |

The links describe a dependency of knowledge, not a mandatory work sequence:

~~~text
Product definition
        ↓ informs
System requirements
        ↓ constrain
Architecture
        ↓ guides
Design, implementation, testing, and deployment
~~~

A specialist should read as far upstream or downstream as the task requires.
For example, an Implementer may begin with a feature and architecture decision,
then follow a requirement link to understand expected behavior and a product
definition link to understand the user outcome. The Implementer should not copy
those documents into an implementation note.

## Recommended reading paths

### New contributor

1. Read the [product definition](docs/product_definition.md).
2. Read the [system requirements](docs/system_requirements.md).
3. Review the [backend architecture](backend/docs/architecture/README.md) and
   its [diagrams](backend/docs/architecture/README.md#3-the-system-in-four-views-c4).
4. Choose the relevant [delivery epic](ai_assistant/features/).
5. Read the [engineering workspace guide](ai_assistant/README.md) before
   creating feature artifacts or invoking a Zorba specialist.

### Product or requirements work

Start with the product definition and system requirements. Preserve product
intent in the product definition; put observable, testable behavior in the
requirements. Link the two instead of maintaining parallel descriptions.

### Architecture or design work

Start with the requirement IDs in scope, then read the product definition when
the user outcome or product boundary affects a decision. Record system-level
decisions in architecture documents and detailed component decisions in the
relevant feature workspace.

### Implementation or testing work

Begin with the assigned feature, applicable requirement IDs, and accepted
architecture or design. Follow source links when context is missing. Code and
tests are the implementation evidence; do not create Markdown copies of them.

### Deployment work

Read the runtime architecture, operational requirements, and the features being
released. Keep environment, delivery, observability, and recovery decisions in
their owning deployment artifacts.

## Delivery epics

| Epic | Responsibility |
| --- | --- |
| [EP-01: Web App & User Experience](ai_assistant/features/web-app-and-user-experience/epic.md) | Accessible client experience and user interaction. |
| [EP-02: Speech Processing](ai_assistant/features/speech-processing/epic.md) | Speech-to-text and text-to-speech integration. |
| [EP-03: Conversation & Agent](ai_assistant/features/conversation-and-agent/epic.md) | Intent, conversation context, and ledger-tool coordination. |
| [EP-04: Customers, Ledger & Safety](ai_assistant/features/customers-ledger-and-safety/epic.md) | Customer records, financial history, validation, and confirmation safeguards. |
| [EP-05: Notebook Image Import](ai_assistant/features/notebook-image-import/epic.md) | Image extraction and review-before-save workflow. |
| [EP-06: Deployment, Access & Diagnostics](ai_assistant/features/deployment-access-and-diagnostics/epic.md) | Hosting, access, persistence, observability, and operational safety. |

The first runnable slice and its acceptance criteria are defined in the
[system requirements](docs/system_requirements.md#12-first-release-and-later-work).
Epics describe ownership and delivery boundaries; they do not redefine the
product or system requirements.

## Repository layout

~~~text
Sajelly/
├── README.md                 # Technical contributor entry point
├── ai_assistant/
│   ├── README.md             # Human and agent collaboration guide
│   ├── ai_workflow/Zorba/    # Reusable engineering team
│   └── features/             # Sajelly delivery epics and working artifacts
├── backend/                  # Reserved for backend implementation
├── frontend/
│   └── docs/                 # Early UI reference
└── docs/
    ├── product_definition.md
    ├── system_requirements.md
    └── architecture/
~~~

Sajelly is maintained as an independent Git repository inside a larger local
ExpensesTracker workspace. ExpensesTracker may provide reference patterns, but
it is not a runtime dependency. Any reused code must be adapted and verified
against Sajelly's own product definition, requirements, and architecture.

## Contribution expectations

- Keep each change small, reviewable, and connected to a product outcome or
  requirement.
- Update knowledge in the document that owns it; link from related documents.
- Agree on inputs, outputs, and failure behavior where components meet.
- Add focused tests with implementation and independently verify meaningful
  user behavior.
- Report what was actually verified, including limitations and unknowns.
- Challenge assumptions that make the product confusing, unsafe, inaccessible,
  or difficult to operate.
- Use synthetic data in shared development materials. Never commit customer
  records, recordings, credentials, or other private information.

See the [AI-assisted engineering workspace](ai_assistant/README.md) for the full
collaboration model and the [Zorba team guide](ai_assistant/ai_workflow/Zorba/README.md)
for specialist responsibilities.
