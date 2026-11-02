# EP-06: Deployment, Access & Diagnostics

**Epic ID:** EP-06  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

Make Sajelly accessible, authorized, persistent, and inspectable.

## Scope and acceptance criteria

**Owns:** Hosting the web app, backend, and database; HTTPS; access control; safe management of external API keys; operational logging and diagnostic traces. The app starts as a **website**, optionally installable on Android as a **Progressive Web App (PWA)**. A native Android wrapper is not required for the first release.

**Done when:** A permitted user can open Sajelly over HTTPS on an Android phone, microphone/camera permissions work, backend calls succeed, financial records survive restarts, and a failed voice turn can be investigated without exposing secrets.

**Boundary to agree:** Deployment configuration, authentication contract, and how long diagnostic audio and transcripts are retained.

## Architecture and requirements

**Main C3 boundary:** Website, backend runtime, authentication, database hosting

**Requirements:** SYS-001–003; supports SAFE-007

**Sources:** [Problem definition](../../../docs/problem_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../docs/architecture/sajelly_C1_C2_C3/C3_backend_components.svg).

## Delivery scope

**First voice-query release:** Yes (minimum).

See the [shared first milestone](../../../README.md#our-first-milestone) for the complete voice-query flow and the [working agreement](../../../README.md#how-you-can-help) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
