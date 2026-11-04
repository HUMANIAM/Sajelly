# Codex adapter

This adapter makes the seven vendor-neutral Zorba specialist contracts
available as project-scoped Codex custom agents. The tracked
[`specialists.json`](../../specialists.json) manifest and Markdown documents in
`../../roles/` are the source of truth. Codex TOML files are generated locally;
they are not a second maintained copy of Zorba.

Zorba itself remains the main conversational guide. The repository
`AGENTS.md` routes a prompt addressed to Zorba to the canonical
`roles/zorba.md` contract. Zorba is not installed as an eighth specialist or
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
- validates the vendor-neutral manifest, Zorba Guide, and seven role documents;
- confirms that repository `AGENTS.md` routes to the canonical Zorba Guide;
- renders the expected Codex TOML in memory and compares it with the seven
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

Zorba may ask Codex to invoke one named specialist for a bounded contribution
after the contributor authorizes it. Experienced contributors may also invoke a
specialist directly:

```text
Use testing_engineer to inspect this suspected duplicate-payment behavior.
Do not change files. Return evidence, limitations, and open questions.
```

The `$name` syntax invokes a Codex skill, not a custom agent.

Custom agents inherit the parent Codex session's model, permissions, sandbox,
and connected tools. An instruction to inspect only is a behavioral boundary,
not a separate read-only sandbox. Set permissions on the parent session before
requesting a specialist.

## Adapter test

The adapter regression check uses only temporary directories:

```console
ai_assistant/ai_workflow/Zorba/tools/.venv/bin/pytest -c ai_assistant/ai_workflow/Zorba/tools/pyproject.toml
```

It verifies the contributor help, read-only status, both consent directions,
vendor-neutral generation, Codex drift handling, honest Claude WIP status, and
the “invocation not verified” boundary.
