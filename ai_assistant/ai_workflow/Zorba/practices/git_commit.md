# Git Commit — Engineering History Practice

## Why this exists

A commit records **one coherent engineering reason to change**, not everything an agent happened to edit.

Git history should let a teammate understand what changed, why it matters, and how the product evolved without consulting the original author or chat. A coherent change may include code, its tests, and its documentation.

## Contract

| Property | Expectation |
|---|---|
| **Scope** | One related engineering change. Separate unrelated intentions or independently useful changes. |
| **Completeness** | Prefer a commit that leaves the repository in a meaningful, buildable or testable state. Report verification gaps honestly. |
| **Message** | State the outcome in a short imperative subject; explain non-obvious reasons, decisions, or limitations in the body. |
| **Traceability** | Link the relevant issue, requirement, or activity when one exists. Do not invent references. |
| **Authorization** | Inspecting and preparing a diff is not permission to commit, push, rewrite history, or open a PR. Each action needs appropriate authorization. |

## How to prepare a commit

1. **Understand the intention.** Read the relevant issue, requirement, or intent-clarification artifact when available.
2. **Separate unrelated work.** Do not bundle a feature, an independent refactor, and CI setup simply because they were edited in one session.
3. **Stage deliberately.** Inspect the working tree; select only related files or hunks. Do not stage unrelated or user-authored changes.
4. **Inspect and verify.** Review the staged diff for accidental deletions, secrets, generated files, unrelated formatting, and missing tests. Run focused checks when practical.
5. **Write the message.** Explain what the commit achieves and why it exists; avoid a file-by-file narrative.
6. **Commit only when authorized.** Report the hash and actual checks. Push, PR creation, and history rewriting are separate actions.

```bash
git status --short
git diff --stat
git add -p                         # or stage selected paths
git diff --cached --check
git diff --cached --stat
git diff --cached
# Run the relevant project checks before committing when possible.
# git commit ... only after authorization
```

## Message contract

Use the repository's established naming convention. In Zorba, the activity-based convention is:

```text
<activity>(<component>): <short imperative outcome>

<Why this change is needed; important decision or tradeoff if useful.>

Ticket: <ticket ID or URL>
```

- **Activity:** Use the activity intentions owned by [Intent Clarification](../roles/intent_clarification.md#commit-activity-intentions): `host_fix`, `bug_fix`, `feature`, `doc`, `refactor`, `chore`, or `test`. These labels describe **why the change exists**; do not mix them with `feat`/`fix`/`ci`/`build` in the same repository without a reviewed convention change.
- **Component:** The smallest stable feature or subsystem that owns the change, in lowercase kebab-case (for example, `payment-ledger`, `dev-setup`, `ci`).
- **Header:** Specific, imperative, no trailing period; aim for around 72 characters or less.
- **Body:** Proportional to the change. Explain the non-obvious *why*, not what every line does. Omit when the subject is sufficient.
- **Ticket:** Use `Ticket: ...` only when a real ticket exists. Never invent one or write `Ticket: none`.

Keep a blank line between subject, body, and footer when those sections are present.

### Examples

```text
bug_fix(payment-ledger): prevent duplicate entries on retry

Use the confirmed operation identifier to recognize repeated payment requests.
Preserve the original transaction and balance when a response is lost.

Ticket: SAJ-142
```

```text
chore(dev-setup): document repeatable backend installation
```

```text
chore(ci): run backend and frontend checks for pull requests
```

Avoid: `updates`, `fix stuff`, `AI changes`, `implement everything`, or a message claiming checks passed without evidence.

## Commit versus PR

- **Commit:** One coherent reason for a change, including directly supporting tests or documentation.
- **PR:** One reviewable goal. It may contain several related commits.
- **Separate PRs:** Prefer when two goals can be understood, merged, or reverted independently.

For `dev_setup`, reproducible local setup and GitHub CI may be separate PRs if each is independently reviewable. That is a judgment, not a required number of commits.

## How teammates review history

A reviewer should be able to answer: Is each commit intentional and coherent? Is its reason clear? Can it be inspected or reverted without surprising unrelated effects? Does the PR contain a single reviewable goal?

**Done:** A future teammate can understand the evolution of the product from its Git history, not merely recover a list of file edits.
