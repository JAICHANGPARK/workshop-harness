#!/usr/bin/env bash
# ==============================================================================
# Offline Asset Bundler Script for Emergency Network Outage
# ==============================================================================

set -euo pipefail

BUNDLE_DIR="offline_assets_bundle"
echo "Creating emergency offline assets bundle in '$BUNDLE_DIR'..."

mkdir -p "$BUNDLE_DIR/pip_wheels"
mkdir -p "$BUNDLE_DIR/models"
mkdir -p "$BUNDLE_DIR/gradle_cache"
mkdir -p "$BUNDLE_DIR/flutter_cache"

# 1. Export lockfile via uv pip compile and download Python wheels via pip download
if [ -f "pyproject.toml" ]; then
    REQ_FILE="$BUNDLE_DIR/requirements.lock"
    if command -v uv &> /dev/null; then
        echo "[1/5] Compiling lockfile via uv pip compile..."
        if uv pip compile pyproject.toml -o "$REQ_FILE" --quiet 2>/dev/null; then
            echo "      Generated $REQ_FILE"
        else
            echo "[WARN] uv pip compile failed; falling back to pyproject.toml direct download."
            REQ_FILE=""
        fi
    else
        REQ_FILE=""
    fi

    if command -v python3 &> /dev/null && python3 -m pip --version &> /dev/null; then
        echo "[2/5] Downloading Python wheels into $BUNDLE_DIR/pip_wheels..."
        if [ -n "$REQ_FILE" ] && [ -f "$REQ_FILE" ]; then
            python3 -m pip download -r "$REQ_FILE" -d "$BUNDLE_DIR/pip_wheels" || echo "[WARN] Some wheels could not be downloaded."
        else
            python3 -m pip download . -d "$BUNDLE_DIR/pip_wheels" || echo "[WARN] Some wheels could not be downloaded."
        fi
    else
        echo "[WARN] python3 -m pip not found; skipping wheel pre-download."
    fi
fi

# 2. Android Gradle pre-caching (if Android stack present)
if [ -d "workshop/01_starter/app" ] && [ -x "workshop/01_starter/gradlew" ]; then
    echo "[3/5] Pre-caching Android Gradle dependencies..."
    (cd workshop/01_starter && ./gradlew --dry-run dependencies || echo "[WARN] Gradle pre-cache returned non-zero.")
fi

# 3. Flutter platform pre-caching (if Flutter stack present)
if [ -f "workshop/01_starter/pubspec.yaml" ] && command -v flutter &> /dev/null; then
    echo "[4/5] Pre-caching Flutter platform engine & web artifacts..."
    flutter precache || echo "[WARN] flutter precache returned non-zero."
    (cd workshop/01_starter && flutter pub get || echo "[WARN] flutter pub get returned non-zero.")
fi

# 4. Node.js / Go dependency pre-caching (if present)
if [ -f "workshop/01_starter/go.mod" ] && command -v go &> /dev/null; then
    echo "[5/5] Pre-caching Go modules..."
    (cd workshop/01_starter && go mod download || echo "[WARN] go mod download returned non-zero.")
elif [ -f "workshop/01_starter/package.json" ] && command -v npm &> /dev/null; then
    echo "[5/5] Pre-caching npm packages..."
    (cd workshop/01_starter && npm install --prefer-offline || echo "[WARN] npm install returned non-zero.")
fi

echo ""
echo "[OK] Offline bundle created at '$BUNDLE_DIR'."
echo "Tip: Copy '$BUNDLE_DIR' to a USB flash drive and install offline via:"
echo "     python3 -m pip install --no-index --find-links=$BUNDLE_DIR/pip_wheels -r $BUNDLE_DIR/requirements.lock"
