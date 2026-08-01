---
name: prerequisite-checker
description: Generates OS-specific (macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) prerequisite setup guides covering language/SDK installation (Python, Node.js, Go, Flutter, Rust, Docker), local LLM server API port configuration (Ollama 11434 vs LM Studio 1234), latest AI model downloads, Google AI Studio / GCP Gemini API Key issuance steps, and automated environment verification scripts (check_env.sh, check_env.ps1).
---

# Prerequisite Checker & API Key / Local Server Guide Skill

## Purpose
Prevents attendees from being blocked on workshop day due to missing development languages, SDKs, AI models, local LLM server API port misconfigurations, or **Google AI Studio / GCP Gemini API Keys** by generating comprehensive, OS-specific setup documentation and automated verification scripts.

## Local LLM Server API & Port Configuration Matrix

When connecting to local LLMs via OpenAI-compatible endpoints or native REST APIs, each tool uses distinct ports and base URLs:

| Tool | Default Port | Base API Endpoint / URL | OpenAI Compatibility Endpoint | Notes |
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

## Google AI Studio & GCP Key Issuance Guide

### 1. Google AI Studio Gemini API Key (Individual / Attendee)
- **URL**: [https://aistudio.google.com](https://aistudio.google.com)
- **Steps**: Google Sign-in > Get API key > Create API key > Copy `AIzaSy...` key
- **`.env` storage**: `GEMINI_API_KEY="AIzaSy..."`

### 2. GCP Vertex AI Key (Enterprise / GCP Project)
- **URL**: [https://console.cloud.google.com](https://console.cloud.google.com)
- **Steps**: Enable Vertex AI API (`gcloud services enable aiplatform.googleapis.com`) > Create Service Account with `Vertex AI User` role > Download JSON key
- **Environment variable**: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"`

### 3. Security Guidelines
- `.env` and `*.json` files must never be committed to Git repositories. The skill enforces `.env.sample` and `.gitignore` inclusion automatically.

## Latest AI Model Discovery Protocol
- Never hardcode legacy model names (`gpt-3.5`, `llama-2`, `gemma-1`).
- Use `workshop-web-researcher` skill to dynamically query the latest release tags (e.g., `gemma4:e4b`, `gemini-2.0-flash`).
- Include a timestamped currency label at the top of all generated docs: `> Latest model verified on: YYYY-MM-DD`

## SDK Installation Matrix

### Python (3.9+) & uv
- **macOS**: `brew install python@3.11 && curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `winget install Python.Python.3.11` and `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Linux**: `sudo apt update && sudo apt install -y python3 python3-pip python3-venv`

## Automated Verification Script (`check_env.sh` / `check_env.ps1`)

```bash
# Check Local Ollama / LM Studio Port Connectivity
if nc -z localhost 11434 2>/dev/null; then
    echo "[OK] Ollama Local Server detected on port 11434."
elif nc -z localhost 1234 2>/dev/null; then
    echo "[OK] LM Studio Local Server detected on port 1234."
else
    echo "[WARN] No local LLM server detected on port 11434 (Ollama) or 1234 (LM Studio)."
    echo "       Make sure to run 'ollama serve' or start LM Studio Server."
fi
```
