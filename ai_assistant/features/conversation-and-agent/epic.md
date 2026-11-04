# EP-03: Conversation & Agent

**Epic ID:** EP-03  
**Version:** 0.1  
**Status:** Proposed for team review

## Purpose

Understand intent, maintain context, clarify, and request tools.

## Scope and acceptance criteria

**Owns:** Backend API for voice conversations, Conversation Orchestrator, Agent Gateway/LLM Adapter, and Session Store. The agent interprets speech transcripts, asks clarifying questions, requests ledger tools, and produces short Egyptian Arabic replies. It never directly writes financial records.

**Done when:** Multi-turn conversations retain context; a known question leads to the appropriate ledger query; ambiguity leads to a follow-up question; model/tool calls and conversation turns can be inspected during testing.

**Boundary to agree:** Tool request/result contracts with [EP-04](../customers-ledger-and-safety/epic.md) and transcript/reply contracts with [EP-02](../speech-processing/epic.md).

## Architecture and requirements

**Main C3 boundary:** API, Conversation Orchestrator, Agent Gateway, LLM Adapter, Session Store

**Requirements:** AG-001–008

**Sources:** [Product definition](../../../docs/product_definition.md), [system requirements](../../../docs/system_requirements.md), and [C3 backend diagram](../../../backend/docs/architecture/diagrams/C3_components.svg).

## Delivery scope

**First voice-query release:** Yes.

See the [first runnable slice](../../../docs/system_requirements.md#12-first-release-and-later-work) for the complete voice-query flow and the [contribution expectations](../../../README.md#contribution-expectations) for ownership and verification.

## Future Jira planning

This document defines one future Jira epic. Tasks will be created from it later, after the relevant interfaces and acceptance criteria are agreed.
