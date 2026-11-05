---
name: push-review-report
description: Attach an existing engineer-facing review report to a GitHub PR using gh and verify the published content. Use when asked to publish or attach a completed review, not while conducting a read-only review.
---

# Publish the reviewer's report

The engineering reviewer owns the report. Publish its Markdown without rewriting
findings or submitting an approval. Publication requires explicit user
authorization; preparing or running a review does not authorize posting it.

Use [push_review_report.py](../push_review_report.py) with the shared Zorba
environment. Supply the repository, existing PR number, report and an honest
scope note identifying what was reviewed. A report of an earlier working-tree
snapshot must not be presented as a review of the final PR head. If available,
pass both response and request JSON for correlation validation.

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/python ai_assistant/ai_workflow/Zorba/roles/engineering_review/common/skills/push_review_report.py --repo OWNER/REPO --pr NUMBER --report PATH_TO_REVIEW_MD --project-root . --scope-note "Actual reviewed revision or snapshot and its freshness limits" --body-output /tmp/review-comment.md
```

This prepares the report without publishing. Inspect the prepared body. Once the
user has authorized this PR/report publication, rerun the same command with
`--publish`. Existing authorization for the same action remains sufficient.

The helper posts the full Markdown as a PR Conversation comment, not a file
upload or a GitHub approval. It rebases existing source links to the pinned PR
head after checking its tree. Local-only evidence becomes labelled text; it is
not uploaded. The scope note distinguishes that source-link revision from the
snapshot actually reviewed. External URLs remain unchecked.

Verify success using the returned comment URL and `verified` result: the helper
fetches the comment by ID and compares its exact body and target PR. An identical
report/context is reused rather than posted twice. If a POST or read-back fails,
inspect existing comments before any retry; a failed response may still mean the
comment was created. Do not overwrite review history, merge, approve, rerun CI or
change source as part of attaching a report.

For a new PR, prepare and verify code and description first, commit only relevant
changes, push an explicit head branch, and use `gh pr create --body-file` according
to the project's [PR practice](../../../../../practices/gh_pr/practice.md).
Existing blocking findings belong visibly in the description and attached report;
use a draft when the proposal is not ready for acceptance. Monitor actual CI and
report absent checks or failures honestly.
