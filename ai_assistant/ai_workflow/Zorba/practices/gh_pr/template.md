<!--
PR description template — scale it to the change.
A small fix may need only Goal, Solution, Affected packages,
What to review, Testing strategy, and Review process.
Remove sections that are not relevant, but always keep
Testing strategy and Review process.
Do not claim tests, CI, reviews, or approvals that have not happened.
-->

# <Short PR title>

## Goal

<!-- Why is this change needed? What problem does it solve? -->

Issue: <!-- Link to the real issue or ticket if available; otherwise omit. -->

## Solution

<!-- Describe how this solves the problem, not each edited file.
Explain important behavior, interface, or architecture changes.
Add a diagram only if it improves understanding. -->

## ⚠️ Breaking changes

<!-- Omit when none. What breaks, who is affected, and what must change? -->

## Affected packages

| Package / area | What changed | Why |
|---|---|---|
| `<area>` | `<change>` | `<reason>` |

## What to review

<!-- Guide reviewers to the important files, contracts, risks, and decisions.
Mention what can be safely skipped. Add relevant diff links if useful.
Optional: add focused inline comments on non-obvious changed lines. -->

## Testing strategy

<!-- Keep this section. Report actual commands, results and evidence.
Distinguish passed / failed / blocked / not run.
Link CI, relevant test artifacts or logs when available.
Explain untested cases and limitations. -->

- **Executed:** `<command>` — `<actual result>`
- **CI:** `<link and actual status, or not run>`
- **Not verified / limitations:** `<details, or none known>`

## Notes

<!-- Optional: additional context, known limitations, follow-up work. -->

## Review process

<!-- Keep this section. Mark checked only after the review actually occurred.
The author preparing the PR does not count as independent approval. -->

- [ ] Code reviewed
- [ ] Tests reviewed
- [ ] Documentation reviewed
