#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 OUTPUT_FILE" >&2
  exit 1
fi

{
  export -p
  declare -f || true
} | sort >"$1"
