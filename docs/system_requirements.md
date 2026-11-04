# سجلى (Sajelly) — System Requirements

**Version:** 0.1  
**Status:** Ready for architecture discussion  
**Source of product intent:** [Product definition](product_definition.md)<br>
**Derived design:** [Backend architecture](../backend/docs/architecture/README.md)

## 1. Purpose

These requirements translate the
[product definition](product_definition.md) into observable, testable system
behavior. They define what Sajelly must do from a user's point of view without
repeating the product narrative or prescribing software components and
technologies.

Each requirement ID can be referenced by architecture, design, implementation,
tests, and delivery evidence. Technical structure and trade-offs belong in the
[architecture](../backend/docs/architecture/README.md).

## 2. Users and scope

- **Ledger user:** Uses voice to find customers, ask financial questions, and
  propose purchases, payments, or corrections.
- **Image contributor:** Takes or chooses photographs of existing notebook
  pages and submits them through Sajelly.
- **Import reviewer:** Compares extracted candidates with their source images,
  corrects them, and accepts or rejects them.
- **Administrator:** Manages authorized access and operational setup.

These are responsibilities, not necessarily separate people. One authorized
person may hold several roles.

A customer has **one running amount owed**, even if they bought different products. Payments reduce that amount; they are not assigned to individual products.

The first release may implement only a small part of these requirements. See [Section 12](#12-first-release-and-later-work).

## 3. Screen and voice controls — UX

- **UX-001** — Given a ledger user opens the main screen, then Sajelly shall show its name, a simple accountant symbol, one large voice button, and a small camera icon. No dashboard, customer table, or profile is needed.
- **UX-002** — When the ledger user taps the voice button while idle, Sajelly shall start recording their speech.
- **UX-003** — When the ledger user taps the voice button while recording, Sajelly shall stop recording and process what they said.
- **UX-004** — When Sajelly speaks, it shall play its answer aloud. If the ledger user presses Stop, it shall stop speaking.
- **UX-005** — The ledger user shall be able to complete normal tasks without reading, typing, or learning fixed voice commands.
- **UX-006** — The camera icon shall provide a simple way to take or choose a notebook photo, without turning the main screen into an administration screen.

## 4. Conversational assistant — AG

- **AG-001** — When the ledger user speaks, Sajelly shall understand and respond in everyday Egyptian Arabic.
- **AG-002** — When a request is incomplete, Sajelly shall ask a short, relevant question instead of guessing missing information.
- **AG-003** — When a conversation continues across several recordings, Sajelly shall remember what the current request is about.
- **AG-004** — Before proposing a financial change, Sajelly shall check the relevant existing customer and financial records.
- **AG-005** — When a customer's identity or a transaction detail is unclear, Sajelly shall ask for clarification before making a financial change.
- **AG-006** — Sajelly shall not invent names, identifying details, amounts, purchases, payments, or explanations that are absent from the available records and conversation.
- **AG-007** — When answering a question, Sajelly shall give the information requested without unnecessary detail; it shall explain further when asked.
- **AG-008** — When Sajelly cannot establish an answer from available records, it shall say so rather than provide an assumed answer.

## 5. Customers — CUS

- **CUS-001** — When registering a customer, Sajelly shall check whether a customer with the same or similar name already exists.
- **CUS-002** — When the name may be hard to distinguish later, Sajelly shall ask for more information (such as a second name or a known nickname) and briefly explain the risk of confusion.
- **CUS-003** — If the ledger user cannot provide more information and still wants to register the customer, Sajelly shall allow that registration after confirmation.
- **CUS-004** — Each registered customer shall remain a separate record, even when two customers have the same name.
- **CUS-005** — When several registered customers could match a spoken name, Sajelly shall ask which person the ledger user means before changing that person's financial records.
- **CUS-006** — Sajelly shall not silently combine two customer records or select one of several possible customers.

## 6. Purchases, payments, and balances — FIN

- **FIN-001** — When the ledger user records a purchase amount owed by a customer, Sajelly shall add that amount to the customer's outstanding balance after confirmation.
- **FIN-002** — When the ledger user records a payment from a customer, Sajelly shall reduce that customer's outstanding balance after confirmation.
- **FIN-003** — When importing an old record with only an amount owed, Sajelly shall allow that amount to be recorded as an opening balance, without inventing earlier purchases or payments.
- **FIN-004** — When a proposed payment exceeds the customer's recorded outstanding balance, Sajelly shall ask for clarification and shall not create credit or a negative debt.
- **FIN-005** — When the ledger user asks what one customer owes, Sajelly shall retrieve and speak that customer's current balance.
- **FIN-006** — When the ledger user asks who owes money, Sajelly shall read the matching customer names and amounts, continuing until the report finishes or the user presses Stop.
- **FIN-007** — When asked, Sajelly shall report the total outstanding debt across customers and payments within a stated period, based on stored records.
- **FIN-008** — When asked why a customer owes an amount, Sajelly shall explain the recorded opening balance, purchases, payments, and corrections that make up the balance.

## 7. Financial records and history — DATA

- **DATA-001** — Sajelly shall keep the customer, type, amount, and known date or details of each financial entry.
- **DATA-002** — Sajelly shall preserve opening balances, purchases, payments, and corrections as a history of entries.
- **DATA-003** — Sajelly shall calculate each outstanding balance from that history; the assistant shall not decide the balance by itself.
- **DATA-004** — When a confirmed entry is corrected, Sajelly shall preserve the original entry and record the correction so the resulting balance is traceable.
- **DATA-005** — Sajelly shall not permanently delete financial history through normal user operations.
- **DATA-006** — When an entry comes from a notebook image, Sajelly shall retain a reference to that image.

## 8. Confirmation and financial safety — SAFE

- **SAFE-001** — Before saving a financial change requested by the ledger user, Sajelly shall tell them what will change and ask for clear spoken confirmation.
- **SAFE-002** — Until the ledger user explicitly confirms, Sajelly shall not save the proposed financial change.
- **SAFE-003** — Each proposed change shall have its own ID and fixed details, so that it can be distinguished from other changes in the conversation.
- **SAFE-004** — Sajelly shall associate the ledger user's confirmation response with the exact proposed change. The assistant's claim that the user confirmed shall not, by itself, authorize saving.
- **SAFE-005** — If the ledger user rejects a change, gives an unclear answer, or changes its details, Sajelly shall not save the original proposal. A changed proposal requires a new confirmation.
- **SAFE-006** — A confirmation for one proposal shall not authorize another proposal, and repeating a confirmed request shall not create a duplicate entry.
- **SAFE-007** — The system shall retain a traceable record of which proposal was confirmed, the confirming response, and which financial entry was saved.
- **SAFE-008** — Sajelly shall enforce financial rules, including customer selection and payment limits, before saving; the assistant cannot bypass those checks.

## 9. Importing notebook photographs — IMG

- **IMG-001** — When an image contributor takes or chooses a notebook photo, Sajelly shall send it to an import reviewer.
- **IMG-002** — Sajelly shall attempt to extract customer names and financial information from an imported photo as proposed entries, not as confirmed records.
- **IMG-003** — The import reviewer shall be able to review each proposed entry separately, correct it, and accept or reject it.
- **IMG-004** — Sajelly shall store an imported financial entry only after the import reviewer confirms that entry.
- **IMG-005** — When handwriting is unreadable or its meaning is unclear, Sajelly shall show that uncertainty for review rather than invent an amount or name.
- **IMG-006** — The import process shall allow the administrator to compare the proposals against the original photo, including checking whether an entry was missed.

## 10. Access and operation — SYS

- **SYS-001** — Sajelly shall run on an Android phone and may require internet for the initial release.
- **SYS-002** — Sajelly shall offer a simple sign-in method and keep the user signed in during normal use. The exact method (Google or username/password) will be chosen during design.
- **SYS-003** — Only authorized users shall be able to access the business records. Each user shall have access appropriate to their assigned responsibilities.
- **SYS-004** — The ledger user shall be able to ask questions without giving confirmation, because reading records does not change them.

## 11. Example acceptance tests

These examples illustrate how to test requirements. A test may refer to one or more requirement IDs.

**T-001 — Ask for a balance** (`UX-002`, `UX-003`, `AG-001`, `FIN-005`, `DATA-003`)

- **Given** a known customer owes 2,000 EGP,
- **When** the ledger user asks in Egyptian Arabic how much that customer owes,
- **Then** Sajelly speaks 2,000 EGP from the records.

**T-002 — Ambiguous customer** (`CUS-005`, `AG-005`, `SAFE-008`)

- **Given** two customers share a name,
- **When** the ledger user asks to record a payment using that name,
- **Then** Sajelly asks which customer he means and saves nothing until the identity is resolved and the change is confirmed.

**T-003 — No unconfirmed change** (`SAFE-001`–`SAFE-007`)

- **Given** Sajelly proposes recording a payment,
- **When** the ledger user has not clearly confirmed that exact proposal,
- **Then** no financial entry is saved.

**T-004 — Correct an entry** (`DATA-002`, `DATA-004`, `DATA-005`)

- **Given** a payment was saved with the wrong amount,
- **When** the ledger user confirms a correction,
- **Then** the corrected balance is shown and the original entry remains in the history.

**T-005 — Import a notebook entry** (`IMG-002`–`IMG-006`)

- **Given** a photo contains handwritten records,
- **When** the import reviewer corrects and confirms one proposed entry,
- **Then** only that confirmed entry is saved with a reference to the photo.

## 12. First release and later work

**First runnable slice — Ask about existing records.** Start with a few verified
customer balances entered for testing. A ledger user shall be able to open
Sajelly on Android, use the voice button, ask in Egyptian Arabic what a customer
owes, and hear the correct answer. If a name matches several customers, Sajelly
shall ask which one the user means. The user shall be able to stop the spoken
response.

**Definition of Done:** The flow works on an Android phone; the spoken balances match the test records; an ambiguous name is not silently assigned to a customer; and Stop interrupts speech.

**Later slices:** Confirmed purchases and payments; customer registration;
corrections and history; image submission; reviewed image import. Their
requirements are defined above but are not all required for the first release.

**Out of scope for now:** General expenses, inventory, invoices, taxes, product catalogs, customer credit, offline operation, and a dashboard.

## 13. Decisions still open

- Choose the simplest sign-in method for the first version.
- Inspect real notebook photos before fixing the import data format.
- Set measurable targets for voice response time and extraction accuracy once working samples are available.

These questions do not block the first runnable slice or the architecture discussion.
