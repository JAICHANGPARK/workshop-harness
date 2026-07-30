---
name: prerequisite-checker
description: Generates OS-specific (macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) prerequisite setup guides covering language/SDK installation (Python, Node.js, Go, Flutter, Rust, Docker), latest AI model downloads, Google AI Studio / GCP Gemini API Key issuance steps, and automated environment verification scripts (check_env.sh, check_env.ps1).
---

# Prerequisite Checker & API Key / SDK Installation Guide Skill

## Purpose
Prevents attendees from being blocked on workshop day due to missing development languages, SDKs, AI models, or **Google AI Studio / GCP Gemini API Keys** by generating comprehensive, OS-specific setup documentation and automated verification scripts.

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
if [ -z "$GEMINI_API_KEY" ] && [ ! -f .env ]; then
    echo "[WARN] GEMINI_API_KEY is not set and .env file missing."
    echo "       Issue your key at https://aistudio.google.com and save it in .env"
else
    echo "[OK] GEMINI_API_KEY configured."
fi
```
