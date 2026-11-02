# CLIENT — Human Engineer

## Purpose
Represent the real need. Decide what is worth building and whether the result is acceptable.

**The client is the human, not an autonomous agent.** An AI assistant may help clarify or record the human's words, but cannot make product decisions or invent approval.

## When wearing this hat
- Explain the problem in plain language: who has it, what happens today, and what better looks like.
- Separate needs from suggested solutions. Identify what matters now and what can wait.
- Decide scope, priorities, acceptable risks, and constraints when trade-offs appear.
- Review the proposed requirements, architecture, and feature design. Explicitly approve or request changes.
- Try the delivered behavior and explicitly accept or reject it, based on evidence.
- Authorize deployment separately. Acceptance of code is not permission to deploy.

## Input
A problem, observation, or feature request. Existing project goals when relevant.

## Output
A short statement of intent, key constraints, and the human's decisions. Record sign-off in `FEATURE.md` or link the actual decision; never fabricate it.

## Done when
The next role knows **why** the feature matters and what outcome the human wants. Before implementation, the human has approved a clear scope and testable behavior.

## Boundaries
- Do not prescribe implementation details unless they are genuine constraints.
- Do not approve something solely because an agent reports success.
- Do not require ceremony: one clear comment or decision link is sufficient.

**Handoff:** System Analyst for new intent; after Tester, human acceptance; then Deployment Engineer if release is wanted.
