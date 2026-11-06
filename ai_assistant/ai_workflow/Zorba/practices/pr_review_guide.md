# Reviewing a pull request

The human reviewer starts with the **PR description** to understand the proposed change and the **review report** to see what the reviewing agent checked and where to look next.

## Review the changes

1. Read the PR description or task and [inspect the changes against the base branch](git_guide.md#inspect-a-branch-against-its-base). Record the commit you reviewed.
2. Read the code around the diff. Use your engineering judgment to decide which behavior, failure cases, and tests need attention. Run the checks that help answer those questions and record the results.
3. Write the report in `feature/review.md`. Put the summary first, followed by the findings. Give each finding a file and line so the author can see it in context. Explain when the issue occurs, what happens, and how to address it if you have a suggestion.

## Write the report

```markdown
# Review report

Reviewed commit — <commit ID>

## Summary

<What you looked at, what the checks showed, and what you could not verify.
Point the human reviewer to the most important issue or open question.>

## Findings

### `src/operations.py:49` — A retry can create a duplicate

If the first write succeeds but its response is lost, retrying creates a
second record. Reuse the original operation ID to recognize the retry.
```

Use a short paragraph in the summary for an issue that affects the whole change. If you found no issues, say so and keep any limits on what you checked visible.

## Publish when asked

Use the summary as the overall PR review. Post each finding as an inline comment on the change it concerns. Check the reviewed commit before posting so the comments still point to the right lines. A review with no inline findings can still have a summary.
