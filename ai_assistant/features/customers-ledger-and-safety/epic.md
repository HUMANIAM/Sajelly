# EP-04: Customers, Ledger & Safety

**Epic ID:** EP-04  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

Maintain customer and money records; enforce rules and confirmation.

## Scope and acceptance criteria

**Owns:** Ledger Service, Ledger Store, and the financial data model. Customer records, purchases, payments, opening balances, corrections, financial queries, and calculated balances live here. Proposed changes require confirmation tied to the exact operation before committing. History is retained.

**Done when:** Tests prove that balances come from recorded history, ambiguous customers are not silently selected, unconfirmed changes never affect the ledger, confirmed changes commit once, and corrections preserve original history. The first release needs only known customers and read-only balance queries.

**Boundary to agree:** Query tools and proposal/confirmation operations available to [EP-03](../conversation-and-agent/epic.md). The ledger component owns validation and commit decisions.

## Architecture and requirements

**Main C3 boundary:** Ledger Service → Ledger Store → Database

**Requirements:** CUS-001–006, FIN-001–008, DATA-001–005, SAFE-001–008, SYS-004

**Sources:** [Problem definition](../../../docs/problem_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../docs/architecture/sajelly_C1_C2_C3/C3_backend_components.svg).

## Delivery scope

**First voice-query release:** Read-only part.

See the [shared first milestone](../../../README.md#our-first-milestone) for the complete voice-query flow and the [working agreement](../../../README.md#how-you-can-help) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
