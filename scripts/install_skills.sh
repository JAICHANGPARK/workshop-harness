#!/usr/bin/env bash
# ==============================================================================
# Install Workshop Harness Skills to Antigravity / Gemini Agent Skills Directory
# Powered by Astral uv
# ==============================================================================

set -e

TARGET_DIR="$HOME/.gemini/skills"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../skills" && pwd)"

echo "⚡ [uv Engine] Setting up Python dependencies & installing Workshop Harness Skills..."

# Check if uv is installed, if not auto-install or use pip fallback
if command -v uv &> /dev/null; then
    echo "✅ Astral uv detected. Syncing project environment..."
    uv pip install reportlab pymupdf pillow --quiet || true
else
    echo "💡 uv not found. Installing Astral uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh || true
    pip install reportlab pymupdf pillow --quiet || true
fi

echo "📦 Installing Workshop Harness Skills to $TARGET_DIR..."

mkdir -p "$TARGET_DIR"

skills=(
    "workshop-scaffolder"
    "prerequisite-checker"
    "hands-on-curriculum-builder"
    "pdf-handout-generator"
    "workshop-troubleshooter"
    "cross-architecture-checker"
    "workshop-runbook-generator"
    "live-debug-assistant"
    "workshop-faq-generator"
    "workshop-tester"
    "workshop-web-researcher"
    "workshop-persona-loop-evaluator"
    "open-codelabs-integrator"
)

for skill in "${skills[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        dest="$TARGET_DIR/$skill"
        rm -rf "$dest"
        cp -r "$SOURCE_DIR/$skill" "$dest"
        echo "  - Installed skill: $skill -> $dest"
    fi
done

echo "✅ All 13 Workshop Harness skills & dependencies installed successfully via uv!"
