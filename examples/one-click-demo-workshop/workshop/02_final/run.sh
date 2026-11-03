#!/usr/bin/env bash
set -e

echo "[INFO] Starting Workshop Application..."
if [ -x "../../.venv/bin/python" ]; then
    ../../.venv/bin/python main.py
elif [ -x ".venv/bin/python" ]; then
    .venv/bin/python main.py
else
    python3 main.py
fi
