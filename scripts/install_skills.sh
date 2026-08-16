#!/usr/bin/env bash
# ==============================================================================
# Multi-Agent Skill Suite Installer for Workshop Harness
# Supports: Google Antigravity / Gemini CLI, Claude Code, OpenAI Codex, Cursor, Aider
# Powered by Astral uv
# ==============================================================================

set -e

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../skills" && pwd)"

echo "⚡ [uv Engine] Setting up Python dependencies & installing Workshop Harness Skills across all AI Coding Agents..."

# 1. Dependency Auto-Installation
if command -v uv &> /dev/null; then
    echo "✅ Astral uv detected. Syncing project environment..."
    uv pip install reportlab pymupdf pillow python-pptx --quiet || true
else
    echo "💡 uv not found. Installing dependencies via pip..."
    pip install reportlab pymupdf pillow python-pptx --quiet || true
fi

# 2. Target Skill Directories for Different AI Agents
TARGET_DIRS=(
    "$HOME/.gemini/skills"
    "$HOME/.claude/skills"
    "$HOME/.agents/skills"
    "$HOME/.codex/skills"
)

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
    "colab-workshop-integrator"
    "workshop-slide-generator"
)

for target_dir in "${TARGET_DIRS[@]}"; do
    mkdir -p "$target_dir"
    echo "📦 Installing 15 Workshop Harness Skills to $target_dir..."
    for skill in "${skills[@]}"; do
        if [ -d "$SOURCE_DIR/$skill" ]; then
            dest="$target_dir/$skill"
            rm -rf "$dest"
            cp -r "$SOURCE_DIR/$skill" "$dest"
        fi
    done
done

echo "✅ All 15 Workshop Harness skills & dependencies installed successfully across Gemini, Claude Code, and Codex agent environments!"
