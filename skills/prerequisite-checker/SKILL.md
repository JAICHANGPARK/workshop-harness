---
name: prerequisite-checker
description: Generates OS-specific (macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) prerequisite setup guides covering language/SDK installation (Python, Node.js, Go, Flutter, Rust, Docker), local LLM server API port configuration (Ollama 11434 vs LM Studio 1234), latest AI model downloads, Google AI Studio / GCP Gemini API Key issuance steps, and automated environment verification scripts (check_env.sh, check_env.ps1).
---

# Prerequisite Checker & API Key / Local Server Guide Skill

## Purpose
Prevents attendees from getting blocked on workshop day due to missing programming languages, SDKs, AI models, local LLM server port misconfigurations, or missing **Google AI Studio / GCP Gemini API Keys** by generating comprehensive OS-specific setup documentation and automated verification scripts.

---

## Local LLM Server API & Port Configuration Matrix

When connecting to local LLM engines via OpenAI-compatible endpoints or native REST APIs, each tool uses distinct ports and base URLs:

| Tool | Default Port | Base API Endpoint / URL | OpenAI Compatibility Endpoint | Key Notes |
|---|---|---|---|---|
| **Ollama** | `11434` | `http://localhost:11434` | `http://localhost:11434/v1` | Natively supports OpenAI SDK (`base_url="http://localhost:11434/v1"`, `api_key="ollama"`) |
| **LM Studio** | `1234` | `http://localhost:1234` | `http://localhost:1234/v1` | Must click "Start Server" in Developer tab; OpenAI compatible endpoint (`api_key="lm-studio"`) |
| **vLLM / LocalAI** | `8000` | `http://localhost:8000` | `http://localhost:8000/v1` | High-throughput server fallback |

### Local API Integration Code Example (Python)

```python
# Connecting to Ollama via OpenAI SDK
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # Change to http://localhost:1234/v1 for LM Studio
    api_key="ollama",                      # Placeholder key required by SDK
)

response = client.chat.completions.create(
    model="gemma4:e4b",
    messages=[{"role": "user", "content": "Hello World"}],
)
print(response.choices[0].message.content)
```

---

## Google AI Studio & GCP Key Issuance Guide

### 1. Google AI Studio Gemini API Key (Individual / Attendee)
- **URL**: [https://aistudio.google.com](https://aistudio.google.com)
- **Steps**: Google Sign-in > Click **Get API Key** > Click **Create API Key** > Copy `AIzaSy...` key.
- **`.env` storage**: `GEMINI_API_KEY="AIzaSy..."`

### 2. GCP Vertex AI Key (Enterprise / GCP Project)
- **URL**: [https://console.cloud.google.com](https://console.cloud.google.com)
- **Steps**: Enable Vertex AI API (`gcloud services enable aiplatform.googleapis.com`) > Create Service Account with `Vertex AI User` role > Download JSON key.
- **Environment variable**: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"`

### 3. Security Guidelines
- `.env` and `*.json` key files must **never** be committed to Git repositories. The skill enforces `.env.sample` and `.gitignore` inclusion automatically.

---

## Multi-Language SDK Setup Matrix

### 1. Python (3.9+) & uv
- **macOS**: `brew install python@3.11 && curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `winget install Python.Python.3.11` and `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Linux**: `sudo apt update && sudo apt install -y python3 python3-pip python3-venv`

### 2. Node.js (18+) & npm / pnpm
- **macOS / Linux**: `curl -fsSL https://fnm.vercel.app/install | bash && fnm install 20`
- **Windows**: `winget install OpenJS.NodeJS.LTS`

### 3. Go (1.21+)
- **macOS**: `brew install go`
- **Windows**: `winget install GoLang.Go`
- **Linux**: `sudo apt install -y golang-go`

---

## Automated Verification Script (`check_env.sh` / `check_env.ps1`)

The generated environment verification script tests local ports, binary presence, and API keys:

```bash
#!/usr/bin/env bash
# Automated Environment Verification Script

echo "🔍 Checking Workshop Environment Prerequisites..."

# 1. Check Python / uv
if command -v uv &> /dev/null; then
    echo "[OK] uv package manager detected: $(uv --version)"
elif command -v python3 &> /dev/null; then
    echo "[OK] Python detected: $(python3 --version)"
else
    echo "[FAIL] Neither uv nor python3 found!"
fi

# 2. Check Local LLM Server Port
if nc -z localhost 11434 2>/dev/null; then
    echo "[OK] Ollama server active on port 11434."
elif nc -z localhost 1234 2>/dev/null; then
    echo "[OK] LM Studio server active on port 1234."
else
    echo "[WARN] No local LLM server running on port 11434 (Ollama) or 1234 (LM Studio)."
fi

# 3. Check Gemini API Key
if [ -n "$GEMINI_API_KEY" ]; then
    echo "[OK] GEMINI_API_KEY environment variable set."
else
    echo "[WARN] GEMINI_API_KEY is not set."
fi
```
