# Codex task — Zorba onboarding and setup verification

**Project:** Sajelly · **Feature:** `ai_assistant/features/dev_setup/`
**Status:** Proposed first qualification experiment; not evidence of implemented functionality.

## Why this work exists

Zorba is a **human-first conversational collaboration layer** between a contributor's intention and the Living Engineering Team. It helps technical and non-technical people contribute meaningful changes without hiding engineering responsibility, tests, or peer review. Zorba coordinates relevant specialist engineers; it does not own their technical decisions.

I want to test Zorba as a **first-time contributor**, starting with the request: *“Zorba, help me get started with Sajelly so I can contribute.”* This is also the first practical qualification of the Codex adapter.

## Scope — build the smallest real end-to-end slice

### A. Make Codex setup verifiable

Inspect the existing `ai_assistant/ai_workflow/Zorba/adapters/codex/sync_agents.sh` and adapter README before changing anything. Today the script copies seven TOML configurations into `.codex/agents/`; it does not verify that Codex can invoke them.

Add a **read-only `--check` (or `--doctor`) mode** without changing the current no-argument installation behavior. Report clear results:

```text
Zorba — Codex Setup

[PASS] Codex CLI detected
[PASS] Seven specialist agent configurations installed and in sync
[PASS] Canonical role documents found
[PASS] Installed agent TOML files parse correctly
[NOT VERIFIED] Live specialist invocation (requires a new Codex session)

Configuration ready.
Next: Start a new Codex session and run the Zorba onboarding smoke test.
```

Show `FAIL` or `WARN` instead of `PASS` where a check is missing or inconclusive. Give a useful repair instruction. Verify actual configured names and canonical role references, not just file count. Prefer standard tools already available in the project; don't add a framework. A `--check` must not install, overwrite, delete, or modify files. Exit nonzero for a failed required check. Keep existing agent configurations and unrelated files untouched.

**Important:** Installed TOML and valid syntax are *configuration evidence*, not proof of runtime agent discovery or successful delegation. The smoke test must establish those separately.

### B. Let Zorba onboard the contributor

**Onboarding belongs to Zorba, not a new onboarding agent.** Inspect the canonical `roles/zorba.md`, Zorba `README.md`, manifesto, requirements, Sajelly `README.md`, and existing Codex adapter. Add only the **minimum Codex entry point** necessary to invoke Zorba as the conversational Guide, if none exists; keep Codex-specific syntax outside the vendor-neutral role contract. Do not copy or redefine Zorba's role text in adapter files.

The **only required newcomer information** is:

> Would you like guidance as a **technical** or **non-technical** contributor?

This selects **how Zorba explains and presents evidence**, not what the person is allowed to propose or how seriously their contributions are treated. Both can raise ideas, bugs, improvements, or questions and collaborate with the same engineers.

- **Non-technical path:** Explain what Sajelly does, how to describe an idea or problem, how Zorba helps, and **how the contributor can personally verify the result**. Do not lead with terminal commands, PR details, agent names, or engineering artifacts unless requested.
- **Technical path:** Offer the same human-first introduction, plus relevant repository structure, Python backend / TypeScript frontend context, setup/verification commands, test and CI conventions, feature artifacts, and peer-reviewed PR workflow. Don't require reading all docs upfront.
- **Optional personalization for either path:** Invite a CV or brief experience summary and ask how the contributor prefers to learn, **but never require either**. Explain that this only helps tailor guidance. Avoid requesting or storing unnecessary personal information. Never commit a raw CV or sensitive profile to Git, send it to an external service, or persist an extracted profile without explicit consent.

After the introduction, ask what the contributor wants to achieve and recommend **one small next contribution**. If specialist invocation is available, Zorba may propose one bounded handoff, make permissions visible, wait for authorization, report the actual result and evidence, then stop at the contributor checkpoint. If invocation is unavailable, state this plainly and offer the smallest manual alternative. No fake delegation, no automatic full lifecycle, no unauthorized writes, pushes, merges, privileged commands, or deployments.

Keep onboarding conversational and short. Do not add a mandatory form, a separate onboarding agent, a workflow database, or a large new onboarding framework.

## Existing architecture and boundaries

- `ai_assistant/ai_workflow/Zorba/roles/` — canonical identity and contracts (Intent, Analyst, Architect, Designer, Implementer, Testing, Deployment, and Zorba Guide).
- `ai_assistant/ai_workflow/Zorba/adapters/codex/` — Codex-specific invocation and setup; **not** the source of role identity.
- `ai_assistant/features/<feature>/` — ongoing engineering exploration and activity artifacts.
- `docs/` — accepted Sajelly project knowledge; source code, tests, and configuration are the executable context.
- GitHub — PRs, CI, and independent review. No engineer self-approves or merges their own work.
- Work follows the problem, not a mandatory role pipeline. Zorba's current pilot authorizes at most **one bounded specialist invocation per contributor checkpoint**, not ongoing autopilot.

## Qualification tests (run and report actual results)

| Scenario | Expected observable result |
| --- | --- |
| Fresh or incorrect setup | The check fails honestly, explains what is missing, and does not modify files. |
| Installed configuration | The check distinguishes installed/valid TOML from **runtime invocation not verified**. |
| New non-technical contributor | Zorba asks only the mandatory technical/non-technical distinction, explains Sajelly in accessible language, and offers a way to contribute and personally verify outcomes. |
| New technical contributor | Zorba offers relevant setup, repository, test, CI, and review context without overwhelming the user. |
| No CV or learning preference provided | Onboarding continues normally; neither is a blocker. |
| One authorized specialist request | Zorba either demonstrates a **real invocation and return**, or reports an unavailable capability honestly. No automatic second specialist. |

**Definition of Done:** A new contributor can determine whether Codex is configured, reach Zorba (or receive a truthful blocker), understand how to contribute at their preferred level, and choose a meaningful next action. Separately report what was actually automated, what was manually simulated, and what remains unverified.

## What to deliver

1. Minimal script/adapter/onboarding changes, using existing paths and practices.
2. A short newcomer-facing README section: setup → `--check` → start Zorba → first request → smoke-test outcome.
3. Tests or reproducible checks, with **actual** commands, observed outputs, and failures.
4. A small experiment record under `ai_assistant/features/dev_setup/`: **Expectation → Observation → Cause (if known) → Proposed improvement**.
5. A concise handoff naming modified files, decisions, limitations, and the next test.

Use the repository's existing `practices/git_commit.md` and `practices/gh_pr/` when available. **Do not commit, push, open a PR, or change shared history without explicit authorization.** Present a small reviewable diff first. Do not silently modify canonical Zorba requirements to make an experiment appear compliant; propose any required contract changes for review.

**Start by inspecting the current files and reporting the smallest implementation plan. Then implement and run the verification within the permissions already granted.**
