# سجلى — Sajelly

Dear friends, welcome to Sajelly ❤️

This project starts with my father and his workshop in Egypt. He makes and sells ovens and other products. Some customers pay in full; others pay a little at a time. He keeps track of what they owe in handwritten notebooks, but he cannot read or write.

When I lived in Egypt, I helped him find the right customer, record payments, and work out what was still owed. **I want Sajelly to be the helper I used to be for him: someone he can talk to, who remembers the records and helps him find answers.**

## What we are building

Sajelly is a simple voice assistant for customer debts and payments. My father should be able to open it on his Android phone, tap a large microphone button, speak naturally in Egyptian Arabic, and hear a short, useful reply.

For example:

> «أحمد عليه كام؟» — How much does Ahmed owe?

If more than one customer could be Ahmed, Sajelly should ask which person he means. If it cannot find the answer, it should say so. Every financial answer must come from the saved records.

Over time, we want it to help with:

- Finding customers and checking their balances.
- Recording purchases and payments after explicit confirmation.
- Explaining how a balance was reached.
- Correcting mistakes while keeping the original history.
- Bringing old notebook records into the system from photographs, with each suggested entry reviewed before saving.

The main screen should stay simple: the Sajelly name, an accountant symbol, a large voice button, and a small camera option. My father should be able to use it without reading, typing, or memorizing commands.

## Where the project stands

**Sajelly is the home for the production version we intend to build. It is currently in the planning stage, with no runnable application code in this repository yet.**

We have a problem definition, system requirements, delivery epics, architecture drafts, and a UI reference. The first delivery is a website usable on an Android phone, with an optional installable PWA experience. Frameworks, providers, and deployment details still need to be agreed as implementation progresses.

There are no Sajelly installation or run commands yet. We will add them when the first working application is ready.

## Our first milestone

Start with one small, complete experience:

1. Load a few verified customer records.
2. Open Sajelly on an Android phone with internet access.
3. Record a question in Egyptian Arabic about a customer's balance.
4. Retrieve the correct balance from stored records and speak the answer.
5. Ask a follow-up question when the customer's name is ambiguous, and allow playback to be stopped.

This milestone succeeds when the full experience works on a real phone and the spoken answers match the known records. Financial writes and notebook imports come later.

## How Sajelly relates to ExpensesTracker

I am developing Sajelly inside my existing ExpensesTracker workspace because that project contains useful lessons and working examples we can reuse, including audio recording, speech processing, frontend and backend structure, and testing.

The local layout is:

```text
ExpansesTracker/       # Existing project and reference implementation
└── Sajelly/           # Production project, with its own Git repository
```

Sajelly has its own purpose, codebase, and Git history. We will bring across useful ideas and code deliberately, adapting and testing them against Sajelly's requirements. Keeping it here locally does not make the parent project a runtime dependency: friends should be able to work from a standalone Sajelly checkout as the application takes shape.

## Start exploring

| Document | What you will find |
| --- | --- |
| [Why Sajelly exists](docs/problem_definition.md) | The family story, intended experience, and product boundaries. |
| [System requirements](docs/system_requirements.md) | Expected behavior, with requirement IDs we can use in tasks and tests. |
| [Delivery epics](docs/sajelly_epics.md) | Areas of work, ownership, and the first delivery plan. |
| [Architecture draft](docs/architecture/architecture_draft.md) | Proposed components, conversation flows, and financial safeguards. |
| [Architecture diagrams](docs/architecture/sajelly_C1_C2_C3/README.md) | System context, containers, and backend components. |
| [UI reference](frontend/docs/app_ui.jpeg) | An early visual reference for the interface. |
| [Architecture presentation](docs/proposal/Sajelly_System_Architecture_Overview.pdf) | A presentation-format overview for discussion. |

The architecture documents are drafts; use the requirements and delivery epics alongside them when discussing implementation.

```text
Sajelly/
├── README.md
├── backend/           # Reserved for backend implementation; currently empty
├── frontend/
│   └── docs/          # UI reference
└── docs/              # Problem, requirements, epics, architecture, and proposals
```

## How you can help

You do not need to understand the whole system to contribute. Start by reading the problem definition, then choose a small piece of the first milestone together. The epics cover the interface, speech processing, conversation flow, customer ledger, notebook import, and deployment.

- Agree on inputs, outputs, and failure behavior before building connected pieces.
- Keep tasks and pull requests small, and link them to the relevant requirement IDs.
- Test what you build, then verify the complete user experience. For the first milestone, that includes a real Android phone.
- Share questions and challenge assumptions, especially where the experience would be confusing for my father.

Throughout the work, a few principles matter most: never guess a customer's identity or an amount; require explicit confirmation for the exact financial change being saved; preserve financial history; and keep customer records, recordings, and secrets private. Use synthetic examples in shared development materials.

Thank you for helping me build something useful for my father. A small tool that he can trust and use comfortably is the goal.
