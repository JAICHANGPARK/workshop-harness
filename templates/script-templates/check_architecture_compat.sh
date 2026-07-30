#!/usr/bin/env bash
# ==============================================================================
# Cross-Architecture & OS Environment Auditor Script (macOS / Linux)
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

OS_TYPE="$(uname -s)"
ARCH_TYPE="$(uname -m)"

echo "=== 💻 Laptop Architecture & OS Auditor ==="
echo "Detected OS: $OS_TYPE"
echo "Detected Architecture: $ARCH_TYPE"
echo "--------------------------------------------------"

if [ "$OS_TYPE" = "Darwin" ]; then
    if [ "$ARCH_TYPE" = "arm64" ]; then
        echo -e "${GREEN}[RECOMMENDED] Apple Silicon Mac (M1/M2/M3/M4)${NC}"
        echo "  - Recommended Tool: LM Studio (GUI) or Ollama"
        echo "  - Recommended Model: gemma4:e4b (16GB RAM) / gemma4:e2b (8GB RAM)"
    elif [ "$ARCH_TYPE" = "x86_64" ]; then
        echo -e "${YELLOW}[ATTENTION] Intel Mac detected${NC}"
        echo "  - ⚠️ WARNING: LM Studio has known performance & stability issues on Intel Mac."
        echo -e "  - ${GREEN}👉 MUST USE: Ollama CLI (ollama serve)${NC} instead of LM Studio."
        echo "  - Recommended Model: gemma4:e4b or gemma4:e2b"
    fi
elif [ "$OS_TYPE" = "Linux" ]; then
    echo -e "${GREEN}[RECOMMENDED] Linux Workstation ($ARCH_TYPE)${NC}"
    echo "  - Recommended Tool: Ollama CLI"
    echo "  - Install via: curl -fsSL https://ollama.com/install.sh | sh"
fi
echo "--------------------------------------------------"
