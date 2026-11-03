#!/usr/bin/env bash
# ==============================================================================
# Offline Asset Bundler Script for Emergency Network Outage
# ==============================================================================

set -e

BUNDLE_DIR="offline_assets_bundle"
echo "📦 Creating emergency offline assets bundle in '$BUNDLE_DIR'..."

mkdir -p "$BUNDLE_DIR/pip_wheels"
mkdir -p "$BUNDLE_DIR/models"
mkdir -p "$BUNDLE_DIR/gradle_cache"
mkdir -p "$BUNDLE_DIR/flutter_cache"

# 1. Download pip wheels for Python packages
if command -v uv &> /dev/null; then
    echo "⬇️ Downloading Python package wheels..."
    uv pip download -r pyproject.toml -d "$BUNDLE_DIR/pip_wheels" 2>/dev/null || true
fi

# 2. Android Gradle pre-caching (if Android stack present)
if [ -d "workshop/01_starter/app" ]; then
    echo "⬇️ Pre-caching Android Gradle dependencies..."
    (cd workshop/01_starter && ./gradlew --dry-run dependencies 2>/dev/null || true)
fi

# 3. Flutter platform pre-caching (if Flutter stack present)
if [ -f "workshop/01_starter/pubspec.yaml" ] && command -v flutter &> /dev/null; then
    echo "⬇️ Pre-caching Flutter platform engine & web artifacts..."
    flutter precache 2>/dev/null || true
    (cd workshop/01_starter && flutter pub get 2>/dev/null || true)
fi

echo "✅ Offline bundle created at '$BUNDLE_DIR'."
echo "💡 You can copy this directory to a USB flash drive for on-site distribution."

