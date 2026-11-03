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
        echo "  - LLM Runtime: LM Studio (GUI) or Ollama"
        echo "  - Android Labs: Use ARM64 AVD system image for fast hardware virtualization"
        echo "  - Flutter/GenUI Labs: Supports iOS Simulator, macOS Desktop, and Flutter Web"
    elif [ "$ARCH_TYPE" = "x86_64" ]; then
        echo -e "${YELLOW}[ATTENTION] Intel Mac detected${NC}"
        echo "  - ⚠️ WARNING: LM Studio has known performance & stability issues on Intel Mac."
        echo -e "  - ${GREEN}👉 MUST USE: Ollama CLI (ollama serve)${NC} instead of LM Studio."
        echo "  - Android Labs: Use x86_64 AVD image or connect physical device via USB"
        echo "  - Flutter/GenUI Labs: Use Flutter Web (flutter run -d chrome) for fastest execution"
    fi
elif [ "$OS_TYPE" = "Linux" ]; then
    echo -e "${GREEN}[RECOMMENDED] Linux Workstation ($ARCH_TYPE)${NC}"
    echo "  - LLM Runtime: Ollama CLI (curl -fsSL https://ollama.com/install.sh | sh)"
    echo "  - Android Labs: Ensure KVM permissions (sudo usermod -aG kvm \$USER)"
    echo "  - Flutter/GenUI Labs: Use Flutter Web or Linux Desktop target"
fi
echo "--------------------------------------------------"

