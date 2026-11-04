# سجلى (Sajelly) — Product Definition

**Version:** 0.2<br>
**Status:** Proposed product baseline<br>
**Document owner:** Product purpose, users, value, experience, capabilities, and scope<br>
**Derived requirements:** [System requirements](system_requirements.md)

This document defines **why Sajelly exists and what product it should become**.
It does not define testable system behavior or technical design. Those details
belong in the linked requirements and architecture documents.

## 1. Product summary

**Sajelly** means **“record for me.”** It is a people-first, voice-enabled
customer ledger for individuals and small businesses that need a simpler way to
manage purchases, payments, and money owed.

Sajelly lets people work with their records through natural conversation. It
begins with Egyptian Arabic and an Android-friendly web experience, with a
simple path for bringing existing handwritten records into the system.

The product is not intended to replace a full accounting platform. It focuses
on a smaller promise: help people record customer activity, retrieve trustworthy
answers, and remain in control of every financial change.

## 2. The problem

Many small businesses manage customer balances in handwritten notebooks.
Finding a customer, calculating what remains unpaid, and preserving corrections
can be slow and error-prone. Conventional financial software may also assume
that users are comfortable reading dense screens, typing, navigating menus, or
learning accounting terminology.

People need a way to:

- Ask about customer balances in familiar spoken language.
- Record purchases and payments without filling in complex forms.
- Distinguish customers who have similar names.
- Understand how a balance was calculated.
- Correct mistakes without losing the earlier record.
- Bring existing notebook records into a digital ledger carefully.

The product must reduce interaction difficulty without weakening accuracy,
privacy, traceability, or human control.

## 3. People the product serves

Sajelly is designed around responsibilities rather than one specific family or
business:

- **Ledger user:** Uses voice to find customers, ask financial questions, and
  propose purchases, payments, or corrections.
- **Image contributor:** Photographs or uploads existing notebook pages.
- **Import reviewer:** Compares extracted candidates with the source image,
  corrects them, and decides which entries may be accepted.
- **Administrator:** Manages authorized access and operational setup.

One person may hold several of these responsibilities. Access should be limited
to the responsibilities each person is authorized to perform.

The primary experience serves people who prefer speaking, have difficulty
reading or typing, or need a faster and more natural interface. The design
should remain useful to any authorized person managing a simple customer ledger.

## 4. Intended experience

The main experience should feel like speaking with a careful assistant:

1. The user opens Sajelly on an Android phone.
2. They tap one prominent voice control and speak naturally in Egyptian Arabic.
3. Sajelly answers directly from the stored records or asks one short,
   relevant question when the request is unclear.
4. If the request would change financial data, Sajelly explains the exact
   proposed change and waits for explicit confirmation.
5. The user can stop a spoken response at any time.

The main interface should avoid dashboards, dense tables, and required typing.
Administrative and import-review work may use additional views, but it should
not complicate the primary voice experience.

Example:

> «أحمد عليه كام؟»
>
> How much does Ahmed owe?

If several customers could be Ahmed, Sajelly asks which customer the user means.
If the records cannot support an answer, Sajelly says so instead of guessing.

## 5. Product capabilities

### Conversational access

- Understand and respond in everyday Egyptian Arabic.
- Preserve enough context for a short, multi-turn task.
- Ask focused clarification questions instead of inventing missing details.
- Return concise spoken answers and allow playback to be stopped.

### Customer ledger

- Keep distinct customer records, including customers with similar names.
- Record opening balances, purchases, payments, and corrections.
- Calculate balances from financial history rather than model-generated values.
- Explain the entries that make up a balance.
- Report individual balances and useful summaries of money owed or paid.

### Safe financial changes

- Present the exact proposed change before writing financial data.
- Require explicit confirmation tied to that proposal.
- Prevent one confirmation from authorizing a different or duplicate change.
- Preserve original entries when a correction is recorded.

### Notebook import

- Accept photographs of existing notebook pages.
- Extract candidate customers and financial entries without treating them as
  trusted records.
- Let an authorized reviewer compare, correct, accept, or reject each candidate.
- Preserve a reference to the source image for accepted entries.
- Expose unreadable content and possible omissions instead of guessing.

### Access and operation

- Provide an Android-friendly web experience, optionally installable as a PWA.
- Keep normal sign-in simple while restricting records to authorized people.
- Preserve the diagnostic evidence needed to investigate failed interactions
  without exposing private information.

Exact, testable behavior for these capabilities belongs in the
[system requirements](system_requirements.md).

## 6. Product principles

1. **People first:** Technology should adapt to people without removing their
   understanding, dignity, or control.
2. **Accessible by design:** Common tasks should not require typing, memorizing
   commands, or navigating a complex interface.
3. **No guessing:** Customer identity, amounts, and financial explanations must
   come from records or explicit clarification.
4. **Confirmation before change:** Every financial write must be authorized for
   the exact operation being saved.
5. **Traceable history:** Balances, corrections, and imports must remain
   understandable from preserved evidence.
6. **Honest limitations:** Missing, ambiguous, or unverified information must be
   visible to the user.
7. **Privacy and safety:** Financial records, recordings, source images,
   credentials, and diagnostic data must be protected.

## 7. First product release

The first release proves one complete, useful path: an authorized user asks in
Egyptian Arabic how much a known customer owes and hears the correct amount from
verified records.

It includes voice capture, speech processing, conversational clarification,
read-only ledger access, spoken output, basic authorization, persistence, and
diagnostic traceability. It does not include financial writes or notebook
imports.

The exact acceptance conditions and requirement IDs are defined in
[System Requirements §12](system_requirements.md#12-first-release-and-later-work).

## 8. Later product slices

After the first read-only path works reliably, Sajelly can add:

- Confirmed purchases and payments.
- Customer registration and identity clarification.
- Corrections with preserved history.
- Notebook image submission and reviewed import.
- Broader reporting grounded in stored financial records.

Each slice should be delivered and verified independently.

## 9. Current non-goals

The current product scope does not include:

- General expense tracking.
- Inventory or product catalog management.
- Invoicing and tax accounting.
- Customer credit or negative debt balances.
- A full accounting dashboard.
- Offline operation in the initial release.
- Autonomous financial decisions or unconfirmed writes.

These boundaries keep Sajelly focused on an accessible and trustworthy customer
ledger. A future proposal may change them through product review; implementation
or architecture work must not expand them silently.

## 10. Product success

Sajelly succeeds when authorized people can use it comfortably, understand and
trust its answers, remain in control of financial changes, and recover the
history behind every balance. Producing a fluent answer is not enough if the
answer is unsupported, the interaction is inaccessible, or the user cannot
verify what happened.
