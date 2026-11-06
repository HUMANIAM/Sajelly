# Codex adapter

This adapter makes the nine vendor-neutral Zorba specialist contracts
available as project-scoped Codex custom agents. The tracked
[`specialists.json`](../../specialists.json) manifest and Markdown documents in
`../../roles/` are the source of truth. Codex TOML files are generated locally;
they are not a second maintained copy of Zorba.

Zorba itself remains the main conversational guide. The repository
`AGENTS.md` routes a prompt addressed to Zorba to the canonical
`roles/zorba.md` contract. Zorba is not installed as an additional specialist or
an onboarding subagent.

Project-scoped custom agents and their required fields are documented in the
[official Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

## Repository setup entry point

Use the same root entry point documented for every contributor:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py
```

Inspect Codex and Claude status without changing files:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --check
```

Set up or sync Codex:

```console
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --setup codex
python3 ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py --sync codex
```

Setup asks before creating a missing `.codex/agents/` directory or syncing an
existing one. Sync is an explicit refresh; when the directory is missing, it
asks once whether to set up Codex and then creates the required files without a
second prompt. If sync finds an agent no longer listed in `specialists.json`, it
asks before deleting it. Multiple orphaned agents receive separate decisions.
Declining preserves that agent and leaves the remaining drift visible. Neither
action changes global Codex configuration.

The read-only check:

- detects whether the Codex CLI is on `PATH` while acknowledging that it
  cannot detect a desktop app or IDE extension;
- validates the vendor-neutral manifest, Zorba Guide, and registered role documents;
- confirms that repository `AGENTS.md` routes to the canonical Zorba Guide;
- renders the expected Codex TOML in memory and compares it with the registered
  installed files;
- reports Claude separately as work in progress;
- always reports live Zorba routing and specialist invocation as
  **not verified**.

`--check` does not install, repair, overwrite, delete, or otherwise change
files. A missing, stale, or invalid required configuration exits nonzero and
prints a repair command.

Passing this check means **configuration is ready**. It does not prove that a
new Codex session discovered an agent or that a specialist contribution ran.

After setup or sync, start a new Codex CLI, desktop, or IDE-extension session
so project instructions and custom-agent discovery run again.

## Live onboarding smoke test

1. Open a new Codex CLI or IDE-extension session from the Sajelly repository.
2. Say:

   ```text
   Zorba, help me get started with Sajelly.
   ```

3. Zorba should ask only whether you want guidance as a **technical** or
   **non-technical** contributor.
4. Choose either path. A CV, experience summary, and learning preference remain
   optional and must not block onboarding.
5. Describe what you want to achieve. Zorba should recommend one small next
   contribution and make any proposed specialist permission boundary visible.

This conversation is the onboarding smoke test. The setup checker cannot
perform it on your behalf.

## Qualification prompts

Use fresh sessions for both paths.

**Non-technical path**

```text
Zorba, help me get started with Sajelly. I want non-technical guidance.
```

Expected: a short explanation of the product, a way to describe an idea or
problem, and a way to personally verify the outcome—without leading with
terminal commands, role names, or pull requests.

**Technical path**

```text
Zorba, help me get started with Sajelly. I want technical guidance.
```

Expected: the same people-first introduction plus relevant repository,
environment, verification, test/CI, feature-artifact, and peer-review context,
without requiring every document to be read first.

For either path, inspect the actual response. A prompt being accepted does not
prove that a specialist was invoked.

## Available specialist agents

| Codex agent | Canonical Zorba role |
| --- | --- |
| `intent_engineer` | `roles/intent_clarification.md` |
| `system_analyst` | `roles/system_analysis.md` |
| `architect` | `roles/architecture.md` |
| `designer` | `roles/design.md` |
| `implementer` | `roles/implementation.md` |
| `testing_engineer` | `roles/testing.md` |
| `deployment_engineer` | `roles/deployment.md` |
| `frontend_engineering_reviewer` | `roles/frontend_engineering_review.md` |
| `backend_engineering_reviewer` | `roles/backend_engineering_review.md` |

Zorba may ask Codex to invoke one named specialist for a bounded contribution
after the contributor authorizes it. Experienced contributors may also invoke a
specialist directly:

```text
Use testing_engineer to inspect this suspected duplicate-payment behavior.
Do not change files. Return evidence, limitations, and open questions.
```

The `$name` syntax invokes a Codex skill, not a custom agent.

Custom agents inherit parent settings unless supported model/effort fields are
explicitly configured. The reviewer agents use the configured lead profile.
Permissions, sandbox and connected tools still come from the parent session. An instruction to inspect only is a behavioral boundary,
not a separate read-only sandbox. Set permissions on the parent session before
requesting a specialist.

## Adapter test

The adapter regression check uses only temporary directories:

```console
ai_assistant/ai_workflow/Zorba/.venv/bin/pytest -c ai_assistant/ai_workflow/Zorba/tools/pyproject.toml
```

It verifies the contributor help, read-only status, both consent directions,
vendor-neutral generation, Codex drift handling, honest Claude WIP status, and
the “invocation not verified” boundary.

## Engineering review agents

The two reviewer entry points load `roles/engineering_review/`, the single
canonical home for their version 1.1 JSON contracts and shared review workflow.
They compare an explicit baseline and proposed revision, use component metadata
for focused context, consult automated evidence, save validated JSON and produce
their engineer-facing Markdown report before returning the machine response.

Use the shared invocation pattern below for either reviewer. Parallel review
follows the [common procedure](../../roles/engineering_review/common/review_protocol.md#parallel-review-when-requested),
with one lead reviewer owning technical synthesis and validated JSON output.

Use `frontend_engineering_reviewer` for frontend changes. For a GitHub PR, supply
its URL instead of the local revisions and use the connected read-only GitHub
tools. A connector is optional for local review, required for remote-only evidence.
The local evidence collector inspects committed revisions, not uncommitted work.
Its comparison is merge-base to head; record those exact SHAs in the review.

Installation and passing local checks prove configuration/tool readiness, not
live Codex discovery or the quality of AI review judgment. The first real review
must still be inspected by a human. Read-only reviewer instructions are behavioral
constraints; custom agents inherit their parent's tool permissions.

## Invoke reviewers from the VS Code extension

Open the Sajelly repository root in VS Code, reload the window after initial
setup, then start a new local Codex chat. Ask for a named custom agent in plain
language; `$name` invokes a skill, not an agent. Current IDE releases support
explicit subagent requests; see the [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

One common prompt for both reviewers:

```text
Delegate to <REVIEW_AGENT> to review this branch against <BASELINE>.
Goal: <intended outcome and relevant acceptance criteria>.
Pin the baseline, merge-base and branch head. Use the canonical workflow and
version 1.1 contracts in ai_assistant/ai_workflow/Zorba/roles/engineering_review/.
Assess change risk and system criticality. Resolve --review-plan for the relevant
subjects using the canonical review_execution.json. Have the lead reviewer use
parallel helpers with the planned model AND reasoning effort for each subject.
Give each a bounded question on the same changeset and necessary component
context. Do not modify source or publish anything.
Wait for all requested subagents. Have the lead reviewer reconcile findings,
save validated response JSON, then run the canonical renderer with --request,
--output <OUTPUT_DIRECTORY>/review.md and --project-root . to create its own
engineer-facing report. Give the reviewer <OUTPUT_DIRECTORY> before assigning it.
The report should lead with required changes, explain their impact and correction,
separate suggestions, and state verification limits in plain language.
Check delivery and return only the reviewer's report location and any delivery
failure. Do not author another technical summary or change the reviewer's judgment.
Identify actual invocation evidence in the execution record, not a competing report.
```

Choose `backend_engineering_reviewer` or `frontend_engineering_reviewer` for
`<REVIEW_AGENT>`. `<BASELINE>` is the explicit base branch or commit to compare
against the current branch; resolve it to pinned revisions before review.
Selected subjects might be `security`, `testing` and `maintainability`. That split is an example: choose perspectives that help assess
this change rather than always spawning three agents. For a sequential review,
omit the parallel-subagent instructions and keep the same workflow and contracts.

Replace placeholders with the actual agent, baseline, goal, subjects and output directory.
The local tool compares merge-base to head and does not include uncommitted work.
For a PR, provide its URL and use available read-only GitHub access; do not assume
this chat's plugin tools are available in the VS Code runtime.

Look for the subagent activity/thread in the Codex chat to inspect what actually
ran. If discovery fails, run the documented `--check` command, reload VS Code and
start a fresh local chat. Report an unavailable agent instead of silently
substituting the parent assistant. These instructions have been checked against
configuration and local tools; live VS Code discovery still needs a real session.

## Model settings and future UI

Both named reviewers get their explicit `model` and `model_reasoning_effort`
from the canonical `roles/engineering_review/common/review_execution.json`
`lead_profile`. Run `--sync codex` after editing lead/profile settings and start
a fresh chat. Other Zorba specialists retain their inherited defaults. The
`--check` command detects drift against the configured lead profile.

The read-only `--review-plan` command resolves helper settings per selected
subject and assessed risk/criticality. Helpers use explicit spawn overrides and
applicable review rules; do not launch the fixed-model lead agent as a cheap
helper. No global `[agents]` defaults are changed. If model access fails, report
it and the review gap instead of silently substituting another model.

The future `zorba_ui` can edit the same JSON using its adjacent schema and the
validated load/save/plan functions in `tools/src/review_execution.py`. A settings
form, account model discovery, and automatic launching service are not part of
this change. Follow the shared [model selection rules](../../roles/engineering_review/common/review_protocol.md#model-and-reasoning-selection).
