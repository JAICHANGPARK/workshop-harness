#!/usr/bin/env bash
# ==============================================================================
# Install Workshop Harness Skills to Antigravity / Gemini Agent Skills Directory
# ==============================================================================

set -e

TARGET_DIR="$HOME/.gemini/skills"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../skills" && pwd)"

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
)

for skill in "${skills[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        dest="$TARGET_DIR/$skill"
        rm -rf "$dest"
        cp -r "$SOURCE_DIR/$skill" "$dest"
        echo "  - Installed skill: $skill -> $dest"
    fi
done

echo "✅ All 9 Workshop Harness skills installed successfully!"
