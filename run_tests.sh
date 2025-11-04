#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/Scripts/activate
fi

pytest test_files "$@"
