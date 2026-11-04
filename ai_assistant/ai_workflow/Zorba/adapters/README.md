# Vendor adapters

Zorba's Markdown role contracts are vendor-neutral. An adapter may make those
roles discoverable to a particular agent runtime, but it must point back to the
tracked role documents instead of copying their responsibilities or output
contracts.

| Adapter | Purpose |
| --- | --- |
| [`codex/`](codex/) | Registers each Zorba role as a project-scoped Codex custom agent. |

Keep adapters thin. Changes to an engineer's purpose, ownership, collaboration,
or output belong in `../roles/`; vendor-specific file layout, registration, and
invocation guidance belong here.
