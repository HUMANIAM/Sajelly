# EP-01: Web App & User Experience

**Epic ID:** EP-01  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

What the user sees, hears, and captures.

## Scope and acceptance criteria

**Owns:** A minimal Arabic-friendly web interface: sign-in, one record/stop button, audio playback and interruption, and a small camera/upload icon. The client sends audio or images to the backend; financial decisions stay on the server.

**Done when:** On an Android phone, the user can authenticate, record/stop, upload a recording, play/stop an audio reply, and choose/take a photo. These interactions can first be tested against a fake backend.

**Boundary to agree:** Audio/image upload format and the API's audio response and error behavior.

## Architecture and requirements

**Main C3 boundary:** Client → API

**Requirements:** UX-001–006, SYS-001–002

**Sources:** [Problem definition](../../../docs/problem_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../docs/architecture/sajelly_C1_C2_C3/C3_backend_components.svg).

## Delivery scope

**First voice-query release:** Yes.

See the [shared first milestone](../../../README.md#our-first-milestone) for the complete voice-query flow and the [working agreement](../../../README.md#how-you-can-help) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
