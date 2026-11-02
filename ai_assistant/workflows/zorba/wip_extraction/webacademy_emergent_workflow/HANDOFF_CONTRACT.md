# Handoff Contract

## Purpose

A handoff is a compact contract between teammates. It gives the next role the
minimum complete context needed to begin without reconstructing a conversation
or reading unrelated noise.

Every role appends the same handoff section to its output artifact. Do not
invent a new format for each stage.

## Artifact header

Start every workflow artifact with:

```md
Work item: <name or ID>
Role: <role that owns this artifact>
Status: DRAFT | READY | BLOCKED
Revision: <number or stable revision ID>
Inputs: <artifact paths and revisions, or NONE>
```

`implementation.md`, `QA.md`, and `deployment.md` must also name the exact code,
change, build, or release reference they describe.

## Standard handoff

End every workflow artifact with:

```md
## Handoff

Status: READY | BLOCKED | NEEDS_HUMAN_DECISION
Output: <this artifact path and revision; include code ref when applicable>
Decisions: <decisions made in this stage, or NONE>
Open items: <unresolved questions or blockers, with owner; or NONE>
Risks: <material risks the next role must carry, or NONE>
Next role: <one role, or HUMAN>
Start condition: <the exact condition that permits the next role to begin>
```

## Rules

1. Keep the handoff short. Put detailed reasoning in the artifact's relevant
   section, not in the handoff.
2. Use exact artifact paths, revisions, and code references. Do not say “latest”
   when the identity matters.
3. Write `NONE` instead of leaving uncertainty hidden in a blank field.
4. `READY` means this role's responsibility is complete, not that the whole
   feature is approved or delivered.
5. `BLOCKED` and `NEEDS_HUMAN_DECISION` stop the forward flow. Name the owner
   and the smallest question or action that unblocks it.
6. A downstream role validates the handoff and inputs before starting. If they
   disagree, are stale, or are inaccessible, return to the correct owner.
7. Never replace another role's decision or evidence. Add a new revision and
   preserve traceability.
8. A chat summary may accompany a handoff but cannot replace the durable
   artifact.

## Human gate rule

When a stage stops for a human gate:

1. Set the handoff to `NEEDS_HUMAN_DECISION` and `Next role` to `HUMAN`.
2. Name the exact artifact or code revisions the decision covers.
3. After the human responds, quote or link the decision in the owning artifact
   and create a new artifact revision.
4. Set the handoff to `READY` and name the next engineering role only when the
   decision permits forward progress.

Never replace a pending decision with an agent interpretation.

## Receiving checklist

Before accepting a handoff, the next teammate checks:

- Is this the role I was asked to perform?
- Are all named inputs accessible and at the recorded revisions?
- Is the start condition satisfied?
- Are human decisions explicit rather than inferred?
- Do open items or risks prevent this stage from starting honestly?

If any answer blocks the work, update the handoff status and return it to the
responsible role instead of guessing.

## Workflow feedback, only when needed

Self-improvement belongs after the normal handoff and must not distract from it:

```md
## Workflow feedback

Observed friction: <specific repeated or material problem>
Evidence: <where it occurred>
Smallest proposed improvement: <proposal>
Expected benefit: <what becomes safer, clearer, or faster>
```

This is a proposal for team discussion, not permission for the agent to alter
the workflow silently.
