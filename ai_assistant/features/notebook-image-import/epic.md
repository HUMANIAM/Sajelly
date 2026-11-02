# EP-05: Notebook Image Import

**Epic ID:** EP-05  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

Extract proposed records from images and let a user review them.

## Scope and acceptance criteria

**Owns:** Upload processing, vision-model adapter, proposed entries, and a simple review/confirm workflow. An image produces **candidates**, not trusted financial transactions.

**Done when:** A real notebook photo produces candidate entries that can be compared with the photo, corrected, accepted, or rejected individually. Only accepted entries reach the Ledger Service, with a source-image reference.

**Boundary to agree:** Candidate-record format and the approved-entry contract with [EP-04](../customers-ledger-and-safety/epic.md). Inspect real notebook samples before fixing the format.

## Architecture and requirements

**Main C3 boundary:** Image Import Handler, Vision Adapter, Ledger Service

**Requirements:** IMG-001–006, DATA-006, UX-006

**Sources:** [Problem definition](../../../docs/problem_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../docs/architecture/sajelly_C1_C2_C3/C3_backend_components.svg).

## Delivery scope

**First voice-query release:** Later.

See the [shared first milestone](../../../README.md#our-first-milestone) for the complete voice-query flow and the [working agreement](../../../README.md#how-you-can-help) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
