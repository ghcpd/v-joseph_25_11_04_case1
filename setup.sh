#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

if [ -f ".venv/bin/activate" ]; then
  # POSIX
  source .venv/bin/activate
else
  # Windows Git Bash fallback
  source .venv/Scripts/activate
fi

python -m pip install -U pip
python -m pip install -r requirements.txt

echo "Running tests..."
pytest -q