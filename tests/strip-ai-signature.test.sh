#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SCRIPT_DIR/skills/commit-message/strip-ai-signature.sh"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

assert_equal() {
  local expected=$1
  local actual=$2
  local label=$3

  if [[ "$expected" != "$actual" ]]; then
    printf 'FAIL: %s\nExpected:\n%s\nActual:\n%s\n' "$label" "$expected" "$actual" >&2
    exit 1
  fi
}

stdin_input=$'fix: preserve message\n\nBecause the old path dropped retries.\n\nCo-Authored-By: Claude <noreply@example.com>\n'
stdin_expected=$'fix: preserve message\n\nBecause the old path dropped retries.'
stdin_actual=$(printf '%s' "$stdin_input" | "$SCRIPT")
assert_equal "$stdin_expected" "$stdin_actual" 'stdin strips AI trailer'

anchored_input=$'Co-Authored-By: GPT <noreply@example.com>\nText mentioning Co-Authored-By: Claude in the body\n'
anchored_expected='Text mentioning Co-Authored-By: Claude in the body'
anchored_actual=$(printf '%s' "$anchored_input" | "$SCRIPT")
assert_equal "$anchored_expected" "$anchored_actual" 'only trailer lines are stripped'

message_file="$TMP_DIR/message.txt"
printf '%s' "$stdin_input" > "$message_file"
"$SCRIPT" "$message_file"
file_actual=$(<"$message_file")
assert_equal "$stdin_expected" "$file_actual" 'file mode strips trailer and trailing blank lines'

if "$SCRIPT" "$TMP_DIR/missing.txt" </dev/null >/dev/null 2>&1; then
  printf 'FAIL: missing file should return an error\n' >&2
  exit 1
fi

if "$SCRIPT" first second </dev/null >/dev/null 2>&1; then
  printf 'FAIL: extra arguments should return an error\n' >&2
  exit 1
fi

printf 'PASS: strip-ai-signature behavior\n'
