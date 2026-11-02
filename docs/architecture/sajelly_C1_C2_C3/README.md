# Sajelly — Architecture diagrams

These diagrams describe the agreed architecture without selecting a framework. They are separate, editable SVG images with PNG exports.

- **C1 — System Context:** one end user, the Sajelly software system, external speech/AI services, and persistent storage.
- **C2 — Containers:** Android application, backend server process, and ledger database. Speech/AI services are external.
- **C3 — Components:** API/Controller → Conversation Orchestrator, Agent Gateway → LLM Adapter → LLM, Orchestrator → STT/TTS Adapters → corresponding external speech services, Ledger Service → Ledger Store → Database, Session Store.

## Runtime example: ask a question

1. Android uploads recorded audio to API.
2. Orchestrator calls STT Adapter, which calls external speech-to-text.
3. Orchestrator sends text and session context to Agent Gateway, which uses LLM Adapter.
4. If a ledger query is needed, Orchestrator calls Ledger Service; Ledger Store reads persistent records. The tool result goes back to the model through the gateway.
5. Orchestrator calls TTS Adapter, which calls external text-to-speech.
6. Backend returns **audio only** to the Android user interface. Transcripts and audio traces are retained for debugging.

## Write safety

The model may propose an operation; only Ledger Service may commit it. The backend records a pending operation and ties an explicit user confirmation to the same operation before saving it. The accountant announces success only after the database commit succeeds. Financial history is append-only.

## Image import

The Android app uploads a picture through the same API. It is interpreted through the AI service; proposed records are reviewed before they become ledger entries. No separate temporary UI or user role is assumed in these architecture views.

## Notation

- Dashed blue boundary: Sajelly software system or backend process.
- Light blue: owned components.
- Purple: adapter layer within the backend.
- Green: external AI service.
- Yellow: persistent storage.
- Opposing single-headed arrows: distinct request and response paths.
- Double-headed arrow: matched request/response interaction; not two separately deployed components.

**Scope:** These are architecture views, not a complete sequence diagram or a software class design.
