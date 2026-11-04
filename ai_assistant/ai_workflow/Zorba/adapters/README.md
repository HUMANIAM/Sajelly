# Vendor adapters

Zorba's Markdown role contracts are vendor-neutral. An adapter may make those
roles discoverable to a particular agent runtime, but it must point back to the
tracked role documents instead of copying their responsibilities or output
contracts.

| Adapter | Purpose |
| --- | --- |
| [`codex/`](codex/) | Documents the generated project-scoped Codex adapter. Setup and verification use `../tools/src/zorba_cli.py`. |
| Claude | Work in progress. No specialist adapter is generated yet. |

Keep adapters thin. Changes to an engineer's purpose, ownership, collaboration,
or output belong in `../roles/`; vendor-specific file layout, registration, and
invocation guidance belong here.

The vendor-neutral [`specialists.json`](../specialists.json) manifest names the
seven specialists and their canonical role documents. The contributor setup
CLI generates vendor files from that manifest; sync must not treat a generated
Codex or Claude file as canonical Zorba knowledge.

## Conversational entry points

Zorba remains the main conversational guide rather than another specialist
agent. Thin project instructions route an ordinary-language request to the
canonical [Zorba role](../roles/zorba.md):

| Client | Entry configuration | Specialist adapter |
| --- | --- | --- |
| Codex CLI or IDE extension | Repository `AGENTS.md` | Implemented in [`codex/`](codex/) |
| Claude CLI or IDE extension | Repository `CLAUDE.md` | Not implemented or qualified |

In either supported client, the intended smoke-test request is:

```text
Zorba, help me get started with Sajelly.
```

The entry instructions only tell the active assistant to adopt Zorba's
canonical contract. They are not copies of the role and do not prove that the
client loaded them. Run the client-specific smoke test in a fresh session and
report the observed response.

Codex specialist configuration must not be presented as Claude configuration.
Until a Claude specialist adapter is deliberately designed and qualified,
Claude may provide Zorba onboarding through `CLAUDE.md` but specialist
invocation remains unavailable or unverified and must be reported that way.
