#!/usr/bin/env bash
# ==============================================================================
# BWAI Workshop Environment Verification Script (Linux / macOS)
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=== 🔍 BWAI Workshop Environment Checker ==="
echo ""

# 1. Check Python
if command -v python3 &> /dev/null; then
    py_ver=$(python3 --version)
    echo -e "${GREEN}[OK] Python:${NC} $py_ver"
else
    echo -e "${RED}[FAIL] Python 3 is not installed.${NC}"
fi

# 2. Check uv
if command -v uv &> /dev/null; then
    uv_ver=$(uv --version)
    echo -e "${GREEN}[OK] uv package manager:${NC} $uv_ver"
else
    echo -e "${YELLOW}[WARN] uv is not installed. (Recommended: curl -LsSf https://astral.sh/uv/install.sh | sh)${NC}"
fi

# 3. Check Ollama / LM Studio port
if curl -s http://localhost:11434/api/version &> /dev/null; then
    echo -e "${GREEN}[OK] Ollama server is running on port 11434.${NC}"
elif curl -s http://localhost:1234/v1/models &> /dev/null; then
    echo -e "${GREEN}[OK] LM Studio local server is running on port 1234.${NC}"
else
    echo -e "${YELLOW}[WARN] No local LLM server detected on localhost:11434 (Ollama) or localhost:1234 (LM Studio).${NC}"
fi

# 4. Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}[OK] Git is installed:${NC} $(git --version)"
fi

# 5. Check Flutter & Dart (Optional for Mobile Labs)
if command -v flutter &> /dev/null; then
    echo -e "${GREEN}[OK] Flutter SDK:${NC} $(flutter --version | head -n 1)"
elif command -v dart &> /dev/null; then
    echo -e "${GREEN}[OK] Dart SDK:${NC} $(dart --version)"
else
    echo -e "${YELLOW}[INFO] Flutter/Dart not detected in PATH (Required only for Flutter/GenUI/A2UI labs).${NC}"
fi

# 6. Check Java & Android SDK (Optional for Android Labs)
if command -v java &> /dev/null; then
    java_ver=$(java -version 2>&1 | head -n 1)
    echo -e "${GREEN}[OK] Java Runtime:${NC} $java_ver"
else
    echo -e "${YELLOW}[INFO] Java JDK not detected in PATH (Required for Android/Compose labs).${NC}"
fi

# 7. Check Google Android CLI & Skills (Optional for Android Labs)
if command -v android &> /dev/null; then
    echo -e "${GREEN}[OK] Google Android CLI:${NC} $(android --version 2>&1 | head -n 1)"
else
    echo -e "${YELLOW}[INFO] Google Android CLI not detected. (Install: curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh | bash)${NC}"
fi

echo ""
echo "=== Check Completed! ==="


