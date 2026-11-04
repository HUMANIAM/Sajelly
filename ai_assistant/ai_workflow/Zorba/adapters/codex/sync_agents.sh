#!/usr/bin/env bash

set -euo pipefail

adapter_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repository_root="$(git -C "$adapter_dir" rev-parse --show-toplevel)"
source_dir="$adapter_dir/agents"
target_dir="${1:-$repository_root/.codex/agents}"

install -d -m 0755 "$target_dir"

for source_file in "$source_dir"/*.toml; do
  install -m 0644 "$source_file" "$target_dir/$(basename -- "$source_file")"
done

echo "Synced Zorba Codex agents to $target_dir"
