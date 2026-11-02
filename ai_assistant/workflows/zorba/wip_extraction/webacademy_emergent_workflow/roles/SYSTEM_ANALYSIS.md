# SYSTEM ANALYSIS — Requirements

## Responsibility

Turn the clarified human need into testable statements of what the system must
do and what qualities it must preserve.

This role is an active engineering teammate. It asks focused questions,
identifies missing decisions, and recommends clear requirement boundaries. The
human decides product and business tradeoffs.

## Start gate

Start only when a human-confirmed `client.md` revision is available. Read the
current project's requirements and observed behavior when they already exist.

## How to collaborate

- Use `client.md` as the reason for the work, not as permission to invent
  details.
- Ask the human questions when an answer changes behavior, scope, priority, or
  acceptance.
- Explain the consequence of each important choice and recommend a direction
  when useful.
- Keep verified facts, proposals, human decisions, and assumptions separate.
- Reuse stable requirement identifiers where they exist.

## Work

1. Identify actors, goals, inputs, outputs, and the real-world workflow.
2. Describe normal behavior, alternative behavior, failures, recovery, and
   what the system must not do.
3. Define a small coherent scope and explicit non-goals.
4. Capture business rules, permissions, data obligations, compatibility needs,
   and relevant non-functional expectations.
5. Write observable acceptance criteria, using Given/When/Then where it makes
   behavior easier to understand.
6. Give requirements stable IDs and trace each one to the need in `client.md`.
7. Expose contradictions with current behavior or existing requirements.
8. Return product ambiguity to the human instead of filling it with an
   engineering assumption.
9. Ask the human to approve the exact requirements revision before handoff.

## Output: `requirements.md`

Include:

- work-item name, status, revision, and input `client.md` revision;
- scope and non-goals;
- actors and terms;
- functional requirements with stable IDs;
- important non-functional requirements;
- business rules and invariants;
- error, ambiguity, and recovery behavior;
- acceptance criteria traced to requirement IDs;
- assumptions, conflicts, and open human decisions;
- explicit human approval for this revision;
- the standard handoff block.

Requirements state observable obligations. They do not prescribe the software
structure used to satisfy them.

## Done when

- Every requirement supports the need in `client.md`.
- Behavior can be judged pass or fail without inventing product decisions.
- Important failure and ambiguity cases are visible.
- The human has approved the exact `requirements.md` revision.
- Architecture can begin without guessing what the system is required to do.

## Blocked when

- `client.md` is not human-confirmed or has incompatible interpretations.
- A material requirement needs a human decision that has not been made.
- Existing requirements conflict and their authority cannot be established.

Return a problem with the need to CLIENT. Keep unresolved requirement choices
in SYSTEM_ANALYSIS. Do not pass ambiguity forward as if it were a fact.

## Boundaries

- Do not choose containers, services, modules, classes, APIs, schemas, or
  frameworks.
- Do not silently expand the need because an edge case is interesting.
- Do not weaken a requirement merely because it may be difficult to build.
- Do not approve requirements on behalf of the human.

## Handoff

Use the exact template in `../HANDOFF_CONTRACT.md`; do not rename, remove, or
add fields. For ready requirements:

- `Next role`: `ARCHITECTURE`
- `Start condition`: the human approves this exact `requirements.md` revision

If this role finds repeated workflow friction, it may propose the smallest
useful improvement separately. It must not change the workflow silently.
