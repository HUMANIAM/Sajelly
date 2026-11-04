#!/usr/bin/env bash

set -euo pipefail

test_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
zorba_dir="$(cd -- "$test_dir/.." && pwd)"
repository_root="$(git -C "$zorba_dir" rev-parse --show-toplevel)"
role_file="$zorba_dir/roles/zorba.md"

require_text() {
  local file="$1"
  local text="$2"
  local purpose="$3"

  if ! grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s (%s)\n' "$purpose" "$file" >&2
    exit 1
  fi
}

require_text \
  "$role_file" \
  'Would you like guidance as a **technical** or **non-technical** contributor?' \
  "the one required onboarding question is missing"
require_text \
  "$role_file" \
  'For a **non-technical contributor**' \
  "the non-technical path is missing"
require_text \
  "$role_file" \
  'can coordinate help, and how they can personally verify' \
  "the non-technical path lacks personal verification"
require_text \
  "$role_file" \
  'For a **technical contributor**' \
  "the technical path is missing"
require_text \
  "$role_file" \
  'repository structure, local setup, verification, test/CI' \
  "the technical path lacks engineering context"
require_text \
  "$role_file" \
  'a CV or brief experience summary and a preferred way of' \
  "optional personalization is not explicit"
require_text \
  "$role_file" \
  'recommend one small next contribution' \
  "the onboarding checkpoint is missing"

for entry_file in "$repository_root/AGENTS.md" "$repository_root/CLAUDE.md"; do
  require_text \
    "$entry_file" \
    'Zorba, help me get started with Sajelly' \
    "the ordinary-language Zorba trigger is missing"
  require_text \
    "$entry_file" \
    'ai_assistant/ai_workflow/Zorba/roles/zorba.md' \
    "the entry point does not reference the canonical Zorba role"
  require_text \
    "$entry_file" \
    'Do not create or delegate to a' \
    "the entry point permits an onboarding agent"
done

printf 'PASS: technical and non-technical onboarding contracts and client entry points are present\n'
