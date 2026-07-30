#!/usr/bin/env bash
set -e

echo "🚀 Starting Workshop Application..."
if command -v uv &> /dev/null; then
    uv run python main.py
else
    python3 main.py
fi
