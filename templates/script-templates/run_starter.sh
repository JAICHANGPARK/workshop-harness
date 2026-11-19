#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Starting Workshop Application..."

if [ -f "main.py" ]; then
    if [ -x "../../.venv/bin/python" ]; then
        ../../.venv/bin/python main.py "$@"
    elif [ -x ".venv/bin/python" ]; then
        .venv/bin/python main.py "$@"
    elif command -v uv &> /dev/null && [ -f "../../pyproject.toml" ]; then
        uv run --project ../.. python main.py "$@"
    else
        python3 main.py "$@"
    fi
elif [ -f "package.json" ]; then
    if command -v npm &> /dev/null; then
        npm start -- "$@"
    else
        echo "[FAIL] Node.js / npm is required to run this TypeScript workshop."
        exit 1
    fi
elif [ -f "go.mod" ]; then
    if command -v go &> /dev/null; then
        go run . "$@"
    else
        echo "[FAIL] Go toolchain is required to run this Go workshop."
        exit 1
    fi
elif [ -f "pubspec.yaml" ]; then
    if command -v flutter &> /dev/null; then
        flutter run -d chrome "$@"
    else
        echo "[FAIL] Flutter SDK is required to run this Flutter workshop."
        exit 1
    fi
elif [ -x "./gradlew" ]; then
    ./gradlew assembleDebug "$@"
else
    echo "[FAIL] No recognized workshop entrypoint found (main.py, package.json, go.mod, pubspec.yaml, gradlew)."
    exit 1
fi
