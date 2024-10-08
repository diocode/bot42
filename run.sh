#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi
