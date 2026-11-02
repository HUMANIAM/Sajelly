# EP-02: Speech Processing

**Epic ID:** EP-02  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

Convert recorded audio to text and reply text to audio.

## Scope and acceptance criteria

**Owns:** Backend adapters for speech-to-text (STT) and text-to-speech (TTS). Each adapter communicates with its matching external service and hides provider-specific details from the rest of Sajelly.

**Done when:** Given a sample Egyptian Arabic recording, the STT adapter returns inspectable text; given an Arabic reply, the TTS adapter returns playable audio. Both can be replaced by test doubles without external calls.

**Boundary to agree:** Accepted audio formats, transcript format, reply audio format, and error cases.

## Architecture and requirements

**Main C3 boundary:** STT/TTS Adapters → external speech services

**Requirements:** UX-002–004, AG-001

**Sources:** [Problem definition](../../../docs/problem_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../docs/architecture/sajelly_C1_C2_C3/C3_backend_components.svg).

## Delivery scope

**First voice-query release:** Yes.

See the [shared first milestone](../../../README.md#our-first-milestone) for the complete voice-query flow and the [working agreement](../../../README.md#how-you-can-help) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
