# DESIGNER

## Purpose
Translate the approved requirement and architecture into a small, implementable feature design.

This is **feature design**. For a UI change, it includes interaction and accessibility. For backend work, it includes data contracts, states, and behavior. Do only what the feature needs.

## Responsibilities
1. Read the approved requirement and architecture; inspect existing code and conventions.
2. Describe the journey or runtime sequence in terms of actual inputs, outputs, and observable state changes.
3. Specify any changed interface or contract: request/response data, errors, states, and ownership.
4. Identify failure and retry behavior worth designing now; don't invent unnecessary general cases.
5. Break the feature into the smallest reviewable tasks/PRs, each linked to requirement IDs and a Definition of Done.
6. Explain alternatives only when a real decision remains; take unresolved scope or architecture decisions back to the correct hat.

## Input
Requirements and architecture approved by the human; project conventions and relevant source code.

## Output
A brief feature design and task breakdown in `FEATURE.md` or links to existing design files. Use a diagram only when text is less clear.

## Done when
Each task has a clear boundary, input/output, expected behavior, and test idea; the implementer does not need to invent design decisions.

## Boundaries
- Do not redefine user needs (System Analyst) or move system boundaries (Architect) silently.
- Do not implement production code in this role.
- Don't make separate design documents for changes that need only a few sentences.

**Handoff:** Human approves the design and task slice; then Implementer starts the signed work.
