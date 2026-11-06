# Backend dev container

**On this computer: VS Code → dev container.**

Install the VS Code **Dev Containers** extension. The computer holding the
checkout needs Docker with Compose, and your account must have access to Docker.

## Open on this computer

1. Open this repository's `backend/` folder in VS Code.
2. Press **Ctrl+Shift+P** and run **Dev Containers: Reopen in Container**.

There is no SSH host to select for this path.

## Open on an SSH host

For **VS Code → SSH host → dev container**, also install **Remote - SSH** on
your computer. Docker and the checkout must be on the SSH host, with Docker
accessible from your SSH account.

1. In VS Code, run **Remote-SSH: Connect to Host...** and select your SSH host.
2. Open the checkout's `backend/` folder on that host.
3. Run **Dev Containers: Reopen in Container**.

## Workspace

For either path, VS Code starts the Python 3.11 container and opens
`/workspaces/Sajelly/backend` as the `vscode` user. The whole checkout is mounted
at `/workspaces/Sajelly`, so Git and shared repository files remain available.
Edits are saved to the original checkout.

## Python environment

In the container terminal, create and activate the backend's local environment:

```bash
python -m venv .venv
. .venv/bin/activate
```

After changing the container configuration, run **Dev Containers: Rebuild Container**.

See [VS Code's SSH-to-container instructions](https://code.visualstudio.com/docs/remote/ssh#_open-a-folder-on-a-remote-ssh-host-in-a-container).
