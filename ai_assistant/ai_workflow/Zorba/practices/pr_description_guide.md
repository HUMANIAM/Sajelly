# Writing a pull request description

Start with the question your reviewer needs answered. **What should change, and why?** A good PR lets someone understand the proposal, find the important changes, and judge the evidence without reading the original conversation.

Keep each PR focused on one reviewable goal. Several commits can serve that goal. Split independent work when it needs a different review.

## Read the change before describing it

[Inspect the active branch against the task's base branch](git_guide.md#inspect-a-branch-against-its-base). Use the commits and the full diff to explain what the branch changes and why it matters.

## Write in the order the reviewer reads

1. **Goal.** Name the problem and the outcome in plain language. Put the outcome in the title, and link the task or issue when there is one.
2. **Solution.** Explain how the behavior changes and why the approach fits. Cover a tradeoff, breaking change, or migration when it affects the decision.
3. **What to review.** Point the reviewer to the file or diff where they should start, and give them a specific question to check. Group related changes when that helps them navigate. Use an inline author comment when a line needs context. For example, “This operation ID stays the same across retries. Check what happens if the write succeeds but the response is lost.”
4. **Testing strategy.** Show the checks you actually ran, their results, and what remains unverified. Give the command or manual steps and link evidence when available. Report CI separately and say which revision it checked. Record a merge-result check only when that revision was actually checked.
5. **Review process.** Record who reviewed the PR, the outcome, and what remains open. At least one engineer other than the author must review it. The same rule applies to people and agents. If a requirement or design needs to change, involve its owner, update the proposal and evidence, and request another review of the affected changes.

Keep failed checks and substantive open findings visible until they are addressed. Use the authorization already given for each GitHub action, including pushing, opening the PR, publishing comments, approving, or merging.

## Copyable PR description

Scale each section to the change. A short sentence can be enough for a small fix. Keep **Testing strategy** and **Review process** even when checks or review are pending.

```markdown
# <Short title that states the outcome>

## Goal

<Problem and intended outcome. Link the task or issue when available.>

## Solution

<What changes, why the approach fits, and any compatibility impact.>

## What to review

<Where to start, what behavior or decision to check, and any relevant risk.>

## Testing strategy

- **Executed** — <command or manual steps, pass or fail result, and evidence link>
- **CI** — <status, checked revision, and run link, or not run>
- **Unverified** — <blocked checks or untested behavior, or none known>

## Review process

- **Independent review** — <pending, or reviewer, outcome, and review link>
- **Open findings** — <what still needs action, or none reported>
```
