# GitHub Pull Request — Engineering Review Practice

## Why this exists

A PR is an **engineering proposal**, not just a delivery of generated code. It should make review easier by explaining the goal, significant decisions, behavior, verification, and risks.

**One PR = one reviewable goal.** Multiple coherent commits may serve that goal; unrelated goals belong in separate PRs when practical.

## Contract

| Property | Expectation |
|---|---|
| **Scope** | One understandable change with necessary code, tests, and documentation. |
| **History** | Intentional, coherent commits following [`git_commit.md`](../git_commit.md). |
| **Description** | Use [`template.md`](template.md) proportionally: goal, solution, affected areas, review focus, and actual testing evidence. |
| **Review guidance** | Tell reviewers where to start, what deserves attention, and what can be skipped. Explain non-obvious design tradeoffs. |
| **Evidence** | Separate tests actually run, CI status, missing tests, and unverified behavior. Green CI does not prove correctness. |
| **Review** | At least one engineer other than the author reviews the proposal; an agent and a human follow the same independent-review rule. |
| **Authorization** | Preparing content is not permission to push, open, comment on, approve, or merge a PR. Use the appropriate authorization for each action. |

## How to prepare a PR

1. **State the goal.** Identify the problem and intended result; link the issue or activity if available.
2. **Check the boundary.** Inspect the full PR diff against the target branch, not just the last commit. Split independent goals when review would otherwise be difficult.
3. **Make the history readable.** Review the commit sequence and staged/uncommitted changes. Don't rewrite shared history without explicit authorization.
4. **Verify the change.** Run relevant focused tests and integration checks. Record commands, results, CI status, and what was not tested. Do not claim the eventual merge commit passed unless checked.
5. **Guide the reviewer.** Identify important files, contracts, behavioral changes, and risks. Use diagrams only when they improve understanding.
6. **Prepare the description.** Start with [`template.md`](template.md). Remove irrelevant optional sections. Always retain **Testing strategy** and **Review process**.
7. **Request independent review.** Resolve comments with evidence, preserve meaningful discussions, and update the description when the proposal changes.

Useful local checks:

```bash
git status --short
git log --oneline <base>..HEAD
git diff --stat <base>...HEAD
git diff --check <base>...HEAD
git diff <base>...HEAD
```

`<base>` means the target branch or an appropriate merge base; do not assume an outdated base proves integration readiness.

## Inline review notes on the diff

Optional **author comments attached to relevant changed lines** can shorten review when they explain something that the diff alone does not reveal:

- Why a non-obvious algorithm or contract changed.
- Which failure case or race the reviewer should inspect.
- An important compatibility or migration consequence.

Example:

> This payment ID is stable across retries. Please review the case where the first write succeeds but its response is lost.

Do **not** comment on every line, restate obvious code, or use comments to replace clear source code and the PR description. Draft the comments first; publishing them through GitHub is a separate authorized action.

## When review reveals a problem

- Request clarification or involve the relevant role owner if a requirement, architecture, or design contract needs changing.
- Revise the implementation and its verification; explain any meaningful change of direction.
- A failing check or unresolved substantive review comment is not an approved result.
- Neither the author nor Zorba may substitute a self-check for independent review or self-approve a PR.

## How teammates review the PR

Can the reviewer quickly understand the purpose, inspect the important diff, reproduce the stated checks, identify unverified risks, and decide whether the proposed change is acceptable?

**Done:** The PR tells a coherent engineering story with evidence and allows an independent engineer to review it without reconstructing the original chat.
