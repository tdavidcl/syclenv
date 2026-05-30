#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 BEFORE AFTER" >&2
  exit 1
fi

before="$1"
after="$2"

if ! diff -u "$before" "$after"; then
  echo "Shell environment differs between snapshots" >&2
  exit 1
fi

echo "Shell environment unchanged"
