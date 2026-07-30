#!/usr/bin/env bash
# ==============================================================================
# Offline Asset Bundler Script for Emergency Network Outage
# ==============================================================================

set -e

BUNDLE_DIR="offline_assets_bundle"
echo "📦 Creating emergency offline assets bundle in '$BUNDLE_DIR'..."

mkdir -p "$BUNDLE_DIR/pip_wheels"
mkdir -p "$BUNDLE_DIR/models"

# 1. Download pip wheels for Python packages
if command -v uv &> /dev/null; then
    echo "⬇️ Downloading Python package wheels..."
    uv pip download -r pyproject.toml -d "$BUNDLE_DIR/pip_wheels" || true
fi

echo "✅ Offline bundle created at '$BUNDLE_DIR'."
echo "💡 You can copy this directory to a USB flash drive for on-site distribution."
