# Codex adapter

This directory makes the vendor-neutral Zorba role contracts available as
project-scoped Codex custom agents. The Markdown documents in `../../roles/`
remain the single source of truth. These TOML files contain only the Codex
bootstrap needed to load those contracts.

## Install or refresh

From the repository root, run:

```bash
bash ai_assistant/ai_workflow/Zorba/adapters/codex/sync_agents.sh
```

This command copies the seven adapter-owned TOML files to `.codex/agents/`.
Codex discovers the project-scoped custom agents from that directory.

The sync does not delete other custom agents or change the global Codex
configuration.

After changing a Codex adapter file, run the command again. Then start a new
Codex session so agent discovery runs again.

> **Note:** This adapter requires a current Codex build with project-scoped
> custom-agent support. If Codex does not discover the files, update the Codex
> app or CLI and start a new session.

## Available agents

| Codex agent | Canonical Zorba role |
| --- | --- |
| `intent_engineer` | `roles/intent_clarification.md` |
| `system_analyst` | `roles/system_analysis.md` |
| `architect` | `roles/architecture.md` |
| `designer` | `roles/design.md` |
| `implementer` | `roles/implementation.md` |
| `testing_engineer` | `roles/testing.md` |
| `deployment_engineer` | `roles/deployment.md` |

## Invocation

Ask Codex to use one named agent for a bounded contribution:

```text
Use intent_engineer for this activity: <idea, problem, or request>
```

```text
Have system_analyst turn the accepted intent in
ai_assistant/features/<feature>/intent_clarification.md into requirements.
```

```text
Use implementer only for: <scoped implementation task>. Wait for its result and
return the handoff to me.
```

Codex custom agents are invoked through ordinary instructions like these. The
`$name` syntax invokes a Codex skill, not a custom agent. No Zorba role is
implemented as a Codex skill here, because that would duplicate the role layer
and make vendor-neutral maintenance harder.

Keep the existing Zorba workflow manual and need-driven: invoke the role that is
needed, review its result, and pass accepted artifacts onward yourself. Do not
turn the roles into a mandatory linear pipeline.

Custom agents inherit the parent Codex session's model, permissions, sandbox,
and connected tools. Set those on the parent session before invoking a role.
