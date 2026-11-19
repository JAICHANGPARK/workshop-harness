#!/usr/bin/env bash
# ==============================================================================
# Workshop Environment Verification Script (Linux / macOS)
# ==============================================================================

set -u

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

FAIL_COUNT=0
WARN_COUNT=0

echo "=== Workshop Environment Checker (macOS / Linux) ==="
echo ""

# 0. Show workshop manifest summary if workshop.json is present
WORKSHOP_STACK=""
if [ -f "workshop.json" ] && command -v python3 &> /dev/null; then
    WORKSHOP_INFO=$(python3 -c "import json; d=json.load(open('workshop.json')); print(f\"{d.get('name','workshop')} | Stack: {','.join(d.get('stack',[]))} | Cloud: {d.get('models',{}).get('cloud','-')}\")" 2>/dev/null || true)
    WORKSHOP_STACK=$(python3 -c "import json; d=json.load(open('workshop.json')); print(','.join(d.get('stack',[])))" 2>/dev/null || true)
    if [ -n "$WORKSHOP_INFO" ]; then
        echo -e "${GREEN}[INFO] Manifest:${NC} $WORKSHOP_INFO"
    fi
fi

# 1. System RAM & Gemma 4 Tier Recommendation
RAM_GB=0
if [ "$(uname -s)" = "Darwin" ] && command -v sysctl &> /dev/null; then
    RAM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
    RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
elif [ -r /proc/meminfo ]; then
    RAM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
    RAM_GB=$(( RAM_KB / 1024 / 1024 ))
fi

if [ "$RAM_GB" -gt 0 ]; then
    if [ "$RAM_GB" -lt 12 ]; then
        echo -e "${YELLOW}[OK] System RAM:${NC} ${RAM_GB}GB -> Recommended local tier: 8GB (gemma4:e2b + embeddinggemma-2:270m, or Google Colab)"
    elif [ "$RAM_GB" -lt 24 ]; then
        echo -e "${GREEN}[OK] System RAM:${NC} ${RAM_GB}GB -> Recommended local tier: 16GB (gemma4:e4b / gemma4:12b + embeddinggemma-2)"
    else
        echo -e "${GREEN}[OK] System RAM:${NC} ${RAM_GB}GB -> Recommended local tier: 32GB+ (gemma4:26b / gemma4:31b + embeddinggemma-2)"
    fi
fi

# 2. Free Disk Space Check
AVAIL_GB=$(df -Pk . 2>/dev/null | awk 'NR==2 {print int($4 / 1024 / 1024)}' || echo 0)
if [ "$AVAIL_GB" -gt 0 ]; then
    if [ "$AVAIL_GB" -lt 10 ]; then
        echo -e "${YELLOW}[WARN] Low Disk Space:${NC} ${AVAIL_GB}GB free (< 10GB recommended for local models / SDKs)"
        WARN_COUNT=$((WARN_COUNT + 1))
    else
        echo -e "${GREEN}[OK] Disk Space:${NC} ${AVAIL_GB}GB available"
    fi
fi

# 3. Check Python
if command -v python3 &> /dev/null; then
    py_ver=$(python3 --version)
    echo -e "${GREEN}[OK] Python:${NC} $py_ver"
else
    echo -e "${RED}[FAIL] Python 3 is not installed.${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 4. Check uv
if command -v uv &> /dev/null; then
    uv_ver=$(uv --version)
    echo -e "${GREEN}[OK] uv package manager:${NC} $uv_ver"
else
    echo -e "${YELLOW}[WARN] uv is not installed. (Recommended: curl -LsSf https://astral.sh/uv/install.sh | sh)${NC}"
    WARN_COUNT=$((WARN_COUNT + 1))
fi

# 5. Check Ollama / LM Studio port
if curl -s --max-time 2 http://localhost:11434/api/version &> /dev/null; then
    echo -e "${GREEN}[OK] Ollama server is running on port 11434.${NC}"
elif curl -s --max-time 2 http://localhost:1234/v1/models &> /dev/null; then
    echo -e "${GREEN}[OK] LM Studio local server is running on port 1234.${NC}"
else
    echo -e "${YELLOW}[WARN] No local LLM server detected on localhost:11434 (Ollama) or localhost:1234 (LM Studio).${NC}"
    WARN_COUNT=$((WARN_COUNT + 1))
fi

# 6. Check Port 8000 conflict (relevant for Google ADK `adk web`)
if command -v lsof &> /dev/null && lsof -iTCP:8000 -sTCP:LISTEN &> /dev/null; then
    echo -e "${YELLOW}[WARN] Port 8000 is currently in use (If running ADK, use: adk web --port 8080).${NC}"
    WARN_COUNT=$((WARN_COUNT + 1))
fi

# 7. Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}[OK] Git:${NC} $(git --version)"
else
    echo -e "${YELLOW}[WARN] Git is not installed.${NC}"
    WARN_COUNT=$((WARN_COUNT + 1))
fi

# 8. Check Node.js / npm (Optional unless TypeScript stack)
if command -v node &> /dev/null; then
    echo -e "${GREEN}[OK] Node.js:${NC} $(node --version)"
elif echo "$WORKSHOP_STACK" | grep -qE "(typescript|ts|node)"; then
    echo -e "${RED}[FAIL] Node.js is required for this TypeScript workshop.${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 9. Check Flutter & Dart (Optional unless Flutter stack)
if command -v flutter &> /dev/null; then
    echo -e "${GREEN}[OK] Flutter SDK:${NC} $(flutter --version | head -n 1)"
elif command -v dart &> /dev/null; then
    echo -e "${GREEN}[OK] Dart SDK:${NC} $(dart --version 2>&1 | head -n 1)"
elif echo "$WORKSHOP_STACK" | grep -qE "(flutter|genui|a2ui)"; then
    echo -e "${RED}[FAIL] Flutter SDK is required for this Flutter/GenUI workshop.${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo -e "${YELLOW}[INFO] Flutter/Dart not detected (Required only for Flutter/GenUI/A2UI labs).${NC}"
fi

# 10. Check Java & Android CLI (Optional unless Android stack)
if command -v java &> /dev/null; then
    java_ver=$(java -version 2>&1 | head -n 1)
    echo -e "${GREEN}[OK] Java Runtime:${NC} $java_ver"
elif echo "$WORKSHOP_STACK" | grep -qE "(android|java)"; then
    echo -e "${RED}[FAIL] Java JDK is required for this Android/Java workshop.${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

if command -v android &> /dev/null; then
    echo -e "${GREEN}[OK] Google Android CLI:${NC} $(android --version 2>&1 | head -n 1)"
fi

# 11. Check Google ADK CLI & Google Agents CLI
if command -v adk &> /dev/null; then
    echo -e "${GREEN}[OK] Google ADK CLI (adk):${NC} $(adk --version 2>&1 | head -n 1)"
fi
if command -v agents-cli &> /dev/null; then
    echo -e "${GREEN}[OK] Google Agents CLI (agents-cli):${NC} detected"
fi

# 12. Check Go (Optional unless Go stack)
if command -v go &> /dev/null; then
    echo -e "${GREEN}[OK] Go Toolchain:${NC} $(go version)"
elif echo "$WORKSHOP_STACK" | grep -qE "(^|,)go(,|$)"; then
    echo -e "${RED}[FAIL] Go toolchain is required for this Go workshop.${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 13. Check Cloud AI Provider API Keys (Gemini / Anthropic Claude / OpenAI)
if [ -f ".env" ]; then
    set -a
    # shellcheck disable=SC1091
    source .env 2>/dev/null || true
    set +a
fi

FOUND_CLOUD_KEY=0
if [ -n "${GEMINI_API_KEY:-}" ] && [ "${GEMINI_API_KEY}" != "YOUR_GEMINI_API_KEY_HERE" ]; then
    echo -e "${GREEN}[OK] GEMINI_API_KEY:${NC} configured"
    FOUND_CLOUD_KEY=1
fi
if [ -n "${ANTHROPIC_API_KEY:-}" ] && [ "${ANTHROPIC_API_KEY}" != "YOUR_ANTHROPIC_API_KEY_HERE" ]; then
    echo -e "${GREEN}[OK] ANTHROPIC_API_KEY:${NC} configured"
    FOUND_CLOUD_KEY=1
fi
if [ -n "${OPENAI_API_KEY:-}" ] && [ "${OPENAI_API_KEY}" != "YOUR_OPENAI_API_KEY_HERE" ]; then
    echo -e "${GREEN}[OK] OPENAI_API_KEY:${NC} configured"
    FOUND_CLOUD_KEY=1
fi
if [ "$FOUND_CLOUD_KEY" -eq 0 ]; then
    echo -e "${YELLOW}[INFO] No cloud API key detected in env/.env (Set GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY if running cloud labs).${NC}"
fi

echo ""
if [ "$FAIL_COUNT" -gt 0 ]; then
    echo -e "${RED}=== Environment Check FAILED ($FAIL_COUNT error(s), $WARN_COUNT warning(s)) ===${NC}"
    exit 1
else
    echo -e "${GREEN}=== Environment Check PASSED (0 errors, $WARN_COUNT warning(s)) ===${NC}"
    exit 0
fi
