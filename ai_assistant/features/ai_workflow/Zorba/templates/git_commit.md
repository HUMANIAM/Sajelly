# Git Commit Message

A commit records one coherent engineering outcome and preserves its intention
in repository history. It is not a list of changed files.

Before writing the message, read the relevant intent-clarification artifact
when one exists. Choose `activity` from the definitions owned by
[Intent Clarification](../roles/intent_clarification.md#commit-activity-intentions).

## Format

```text
<activity>(<component>): <commit header>

<commit body>

Ticket: <ticket ID or URL>
```

## Contract

- **Activity:** Use one standard activity intention from Intent Clarification:
  `host_fix`, `bug_fix`, `feature`, `doc`, `refactor`, `chore`, or `test`.
  It describes why the committed change exists.
- **Component:** Name the smallest stable component, feature, or subsystem that
  owns the complete staged change. Use lowercase kebab-case.
- **Header:** State the outcome in the imperative mood. Keep it concise and
  specific, and do not end it with a period.
- **Body:** Explain why the change is needed, what outcome it creates, and any
  important decisions, trade-offs, limitations, evidence, or follow-up work.
  Keep it proportional to the change rather than narrating every edited file.
- **Ticket:** End with `Ticket: <ticket ID or URL>` when a ticket exists. Omit
  the footer when there is no ticket; never invent one or write `Ticket: none`.

Separate the header, body, and ticket footer with one blank line. If the staged
diff contains independent intentions or components, split it into coherent
commits before writing the messages.

## Example

```text
bug_fix(payment-ledger): prevent duplicate payments on retry

Use the stable payment identifier to make ledger recording idempotent. Preserve
one balance change when the confirmation request is repeated and add regression
evidence for sequential retries.

Ticket: SAJ-142
```
