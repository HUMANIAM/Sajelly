# سجلى (Sajelly) — Epic Backlog

**Version:** 0.1 · **Status:** Proposed for team review

**Purpose:** Divide Sajelly into areas of responsibility that engineers can own. This is not a task list or an implementation plan. Each epic owner breaks the work into small, reviewable PRs after agreeing on the interfaces with the other owners.

**Sources:** `problem_definition.md`, `requirements.md`, and the agreed C3 backend diagram.

## Epics at a glance

| ID | Epic | Responsibility | Main C3 boundary | Requirements | First voice-query release? |
| --- | --- | --- | --- | --- | --- |
| EP-01 | Web App & User Experience | What the user sees, hears, and captures | Client → API | UX-001–006, SYS-001–002 | Yes |
| EP-02 | Speech Processing | Convert recorded audio to text and reply text to audio | STT/TTS Adapters → external speech services | UX-002–004, AG-001 | Yes |
| EP-03 | Conversation & Agent | Understand intent, maintain context, clarify, and request tools | API, Conversation Orchestrator, Agent Gateway, LLM Adapter, Session Store | AG-001–008 | Yes |
| EP-04 | Customers, Ledger & Safety | Maintain customer and money records; enforce rules and confirmation | Ledger Service → Ledger Store → Database | CUS-001–006, FIN-001–008, DATA-001–005, SAFE-001–008, SYS-004 | Read-only part |
| EP-05 | Notebook Image Import | Extract proposed records from images and let a user review them | Image Import Handler, Vision Adapter, Ledger Service | IMG-001–006, DATA-006, UX-006 | Later |
| EP-06 | Deployment, Access & Diagnostics | Make Sajelly accessible, authorized, persistent, and inspectable | Website, backend runtime, authentication, database hosting | SYS-001–003; supports SAFE-007 | Yes (minimum) |

## EP-01 — Web App & User Experience

**Owns:** A minimal Arabic-friendly web interface: sign-in, one record/stop button, audio playback and interruption, and a small camera/upload icon. The client sends audio or images to the backend; financial decisions stay on the server.

**Done when:** On an Android phone, the user can authenticate, record/stop, upload a recording, play/stop an audio reply, and choose/take a photo. These interactions can first be tested against a fake backend.

**Boundary to agree:** Audio/image upload format and the API's audio response and error behavior.

## EP-02 — Speech Processing

**Owns:** Backend adapters for speech-to-text (STT) and text-to-speech (TTS). Each adapter communicates with its matching external service and hides provider-specific details from the rest of Sajelly.

**Done when:** Given a sample Egyptian Arabic recording, the STT adapter returns inspectable text; given an Arabic reply, the TTS adapter returns playable audio. Both can be replaced by test doubles without external calls.

**Boundary to agree:** Accepted audio formats, transcript format, reply audio format, and error cases.

## EP-03 — Conversation & Agent

**Owns:** Backend API for voice conversations, Conversation Orchestrator, Agent Gateway/LLM Adapter, and Session Store. The agent interprets speech transcripts, asks clarifying questions, requests ledger tools, and produces short Egyptian Arabic replies. It never directly writes financial records.

**Done when:** Multi-turn conversations retain context; a known question leads to the appropriate ledger query; ambiguity leads to a follow-up question; model/tool calls and conversation turns can be inspected during testing.

**Boundary to agree:** Tool request/result contracts with EP-04 and transcript/reply contracts with EP-02.

## EP-04 — Customers, Ledger & Safety

**Owns:** Ledger Service, Ledger Store, and the financial data model. Customer records, purchases, payments, opening balances, corrections, financial queries, and calculated balances live here. Proposed changes require confirmation tied to the exact operation before committing. History is retained.

**Done when:** Tests prove that balances come from recorded history, ambiguous customers are not silently selected, unconfirmed changes never affect the ledger, confirmed changes commit once, and corrections preserve original history. The first release needs only known customers and read-only balance queries.

**Boundary to agree:** Query tools and proposal/confirmation operations available to EP-03. The ledger component owns validation and commit decisions.

## EP-05 — Notebook Image Import

**Owns:** Upload processing, vision-model adapter, proposed entries, and a simple review/confirm workflow. An image produces **candidates**, not trusted financial transactions.

**Done when:** A real notebook photo produces candidate entries that can be compared with the photo, corrected, accepted, or rejected individually. Only accepted entries reach the Ledger Service, with a source-image reference.

**Boundary to agree:** Candidate-record format and the approved-entry contract with EP-04. Inspect real notebook samples before fixing the format.

## EP-06 — Deployment, Access & Diagnostics

**Owns:** Hosting the web app, backend, and database; HTTPS; access control; safe management of external API keys; operational logging and diagnostic traces. The app starts as a **website**, optionally installable on Android as a **Progressive Web App (PWA)**. A native Android wrapper is not required for the first release.

**Done when:** A permitted user can open Sajelly over HTTPS on an Android phone, microphone/camera permissions work, backend calls succeed, financial records survive restarts, and a failed voice turn can be investigated without exposing secrets.

**Boundary to agree:** Deployment configuration, authentication contract, and how long diagnostic audio and transcripts are retained.

## First delivery — One vertical slice

**Goal:** A user asks in Egyptian Arabic how much a known customer owes and hears the correct amount.

This needs a **thin part** of EP-01, EP-02, EP-03, EP-04, and EP-06. EP-05 and financial writes in EP-04 are not needed for this first slice.

**Definition of Done:** On an Android phone, the user records and sends a short question, the model requests the correct ledger query, the stored balance is returned as spoken Arabic, ambiguous names cause clarification, playback can be stopped, and the test trace can be inspected. No financial write is enabled.

## Working agreement for friends and agents

- One owner per epic; collaborating across epics is fine.
- Agree on **inputs, outputs, and failure behavior** where epics meet before coding both sides.
- An epic owner proposes small tasks and PRs, linked to requirement IDs, with a Definition of Done.
- The implementer tests their code; a separate end-to-end verification checks the user behavior.
- Test each PR against the current integration branch before merging. The product owner accepts the result.
- Do not implement all epics at once. Start with the thin voice-query slice.
