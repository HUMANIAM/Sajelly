# Codex and Claude client environment investigation — 2026-11-04

## Scope

This records the investigation of the installed clients that can host Zorba.
The project owner updated the npm-installed Codex CLI and ran the diagnostics
interactively. The repository work did not change global configuration, sign
in to an account, run live onboarding, or invoke a specialist.

## Observations

| Check | Observation | Meaning |
| --- | --- | --- |
| Shell Codex path | `/home/ibrahim/.nvm/versions/node/v22.18.0/bin/codex` | The shell uses the npm-installed binary. |
| Initial shell Codex version | `codex-cli 0.111.0` | The old npm client rejected `service_tier = "default"` before authentication could be checked. |
| Current shell Codex version | `codex-cli 0.166.0` | The project owner updated the npm installation successfully. |
| Codex configuration | No active `~/.codex/config.toml`; the previous file is retained as `config.toml.bk` | Codex loads its defaults without the incompatible setting. |
| Codex authentication | `codex login status` reports `Logged in using ChatGPT` | Authentication is ready. |
| Codex diagnostics | `19 ok`, `1 idle`, `1 note`, `1 warning`, `0 fail` | Install, state databases, updates, WebSocket, and HTTP reachability pass. Only historical rollout indexing is degraded. |
| Claude version | `2.1.50 (Claude Code)` | Claude CLI is installed. |
| Claude authentication | `loggedIn: false`, `authMethod: none` | Claude cannot run a live Zorba session until the user signs in. |

The Zorba `--check` command intentionally detects configuration readiness
without treating it as proof that a fresh client loaded repository instructions
or invoked a specialist. The interactive diagnostics now establish that the
selected shell client is installed consistently, authenticated, and can reach
the active provider.

## Codex resolution

The project owner completed the repair with the documented npm update and
verified the selected executable:

```console
npm install -g @openai/codex
which -a codex
codex --version
codex login status
codex doctor --summary
```

The active configuration now uses defaults. If Fast mode is deliberately added
later, the official configuration is `service_tier = "fast"` together with
`[features] fast_mode = true`; Fast mode consumes subscription limits at a
higher rate and should not be enabled merely to silence a configuration error.

`codex doctor --summary` reports healthy state databases but warns that a few
historical rollout files are absent from the state index. With zero failures
and current sessions, authentication, and connectivity healthy, no database
repair is justified. Investigate only if conversation history is observably
missing.

The remaining Codex step is the project owner's fresh Zorba onboarding
qualification, not another setup repair.

Official references:

- [Codex CLI installation and update](https://developers.openai.com/codex/cli/#getting-started)
- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands#command-overview)
- [Codex Fast mode configuration and usage](https://learn.chatgpt.com/docs/agent-configuration/speed#fast-mode)

## Claude: proposed resolution

Authenticate in an interactive user session, then verify the result:

```console
claude auth login
claude auth status
```

Successful authentication would unblock a conversational Zorba check through
repository `CLAUDE.md`. It would not implement or qualify a Claude specialist
adapter; `--setup claude` and `--sync claude` must continue to report that
boundary as work in progress.

## Qualification boundary

No live technical or non-technical onboarding response was captured, and no
specialist was invoked. Those are contributor-experience qualifications, not
setup-script repairs. The project owner will perform the first non-technical
contributor journey and decide whether Zorba carries that contributor into a
meaningful task. Zorba remains free to adapt that journey within its canonical
role instead of producing a fixed transcript.
