# Git commits — engineering history

A commit is a note to the next engineer. Explain **what changed and why** so they can follow the history from Git and the task reference.

Keep one record per task under `## Commits` in `ai_assistant/feature/pr_commits.md`. Append your record and preserve earlier entries. Fill in **Executed** after each step. A short entry is enough for a straightforward commit.

## 1. Inspect and verify

[Inspect local changes](git_guide.md#inspect-local-changes). Identify the task ID and name from the branch. Flag a missing task reference before committing.

Decide which changes belong to the task. Look for accidental deletions, secrets, generated files, and unrelated work. Run the checks that fit the change and exercise any changed user-facing behavior. Record what you inspected, what ran, the results, and any gaps.

## 2. Plan the commits

Group changes by activity and component. Give independently useful changes their own commit. Put dependencies first and keep each commit verifiable on its own.

Record the ordered groups, exact files or hunks, and complete messages. Mark which groups are ready. For exclusions, give the file or diff reference and the reason. Set aside any group that depends on a blocked change.

## 3. Commit and confirm

When authorized to commit, [stage and check](git_guide.md#stage-and-check-changes) the next ready group. [Inspect local changes](git_guide.md#inspect-local-changes) again. Confirm the staged diff matches the plan and the verification still applies. If unrelated staged work blocks an isolated commit, report it and leave it in place.

[Record and confirm the commit](git_guide.md#record-and-confirm-a-commit) using the planned message. Record the hash against its plan entry and note what remains uncommitted. Report the commits, checks, and exclusions. Work through the other ready groups in order.

## Commit record

```markdown
### <task-id-task-name>

1. **Inspect and verify**
   - **Executed** — <changes inspected, checks, results, and gaps>
2. **Plan the commits**
   - **Executed** — <ordered groups, exact files or hunks, ready or blocked>
   - **Message** — <full message for each commit>
   - **Excluded** — <file or diff reference and reason, if any>
3. **Commit and confirm**
   - **Executed** — <hash for each recorded commit and what remains>
```

## Commit message definition

```text
<activity>(<component>): <short outcome phrased as an action>

<Optional body explaining what changed and why>

Task: <task-id-task-name>
```

- **Activity** uses one of `host_fix`, `bug_fix`, `feature`, `doc`, `refactor`, `chore`, or `test`. See [Intent Clarification](../roles/intent_clarification.md#commit-activity-intentions).
- **Component** names the owning component or document area in lowercase words separated by hyphens.
- **Subject** states the outcome as an action. Keep the whole first line to 72 characters or fewer and omit the trailing period.
- **Body** explains the reason or tradeoff when the subject needs more context.
- **Task** matches the task ID and name established from the branch.

Leave a blank line between the subject, the body if present, and the task footer.

```text
bug_fix(operations): prevent duplicate writes on retry

Reuse the operation ID so a retry can return the original result
when the first write succeeds but its response is lost.

Task: APP-142-prevent-duplicate-writes
```
