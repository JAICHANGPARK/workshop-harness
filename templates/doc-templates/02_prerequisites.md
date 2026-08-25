# Workshop Prerequisites & SDK / API Key Setup Guide

To avoid download delays and configuration errors caused by venue WiFi congestion, **please complete all language, SDK, and API Key setup before the event**.

---

## 1. Google AI Studio & Gemini API Key Setup

Individual developers and workshop attendees can obtain a free Gemini API Key in under one minute via **Google AI Studio**.

### Issuance Steps
1. **Visit Google AI Studio**: Sign in at [https://aistudio.google.com](https://aistudio.google.com)
2. **Create API Key**:
   - Click the **"Get API key"** button in the left sidebar
   - Select **"Create API key"** (link to a new or existing GCP project)
3. **Copy API Key**: Copy the generated key in `AIzaSy...` format.
4. **Set Local Environment Variable**:
   - Create a `.env` file in the workshop project root and save the key:
     ```bash
     GEMINI_API_KEY="AIzaSyYourGeneratedApiKeyHere"
     ```

> **Critical Security Warning**:
> Your API Key is equivalent to a personal password. **Never commit it to a GitHub repository.**
> Verify that `.gitignore` includes `.env` and `*.json` entries.

---

## 2. Google Cloud Platform (GCP) Vertex AI Key Setup

For enterprise or GCP-based workshops, connect via the Vertex AI API.

### GCP Console Setup Steps
1. **Visit Google Cloud Console**: [https://console.cloud.google.com](https://console.cloud.google.com)
2. **Enable Vertex AI API**:
   - Search for `Vertex AI API` and click **[Enable]**
   - Or use Google Cloud SDK terminal:
     ```bash
     gcloud services enable aiplatform.googleapis.com
     ```
3. **Create Service Account & JSON Key**:
   - Navigate to `IAM & Admin` > `Service Accounts`
   - Click **[Create Service Account]** (Role: `Vertex AI User`)
   - In the Keys tab, select **[Add Key] > [JSON]** to download
4. **Set Local Authentication Environment Variable**:
   - **macOS / Linux**:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-gcp-key.json"
     ```
   - **Windows (PowerShell)**:
     ```powershell
     $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your-gcp-key.json"
     ```

---

## 3. Development Language & SDK Installation by OS

### Python (3.9+) & `uv` Package Manager
- **macOS**:
  ```bash
  brew install python@3.11
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell)**:
  ```powershell
  winget install Python.Python.3.11
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  *(Note: Ensure "Add Python to PATH" is checked during installation)*
- **Linux**:
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip python3-venv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

### Node.js & npm (v20+)
- **macOS**: `brew install node`
- **Windows**: `winget install OpenJS.NodeJS`
- **Linux**: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs`

---

### Flutter SDK & Dart
- **macOS**: `brew install --cask flutter`
- **Windows**: `winget install Flutter.Flutter`
- **Linux**: `sudo snap install flutter --classic`
- **Gemini Live Package**: `flutter pub add gemini_live`
- **LiteRT-LM (On-Device)**: `flutter pub add google_litert` (or platform native LiteRT C/Swift libraries)

---

## Pre-Download Checklist

1. **Download Ollama / LM Studio & pull models ahead of time**:
   ```bash
   ollama pull gemma4:e4b
   ```

2. **Sync project dependencies in advance**:
   ```bash
   cd workshop/01_starter
   uv sync
   ```

---

## References

- **Google AI Studio Key Issuance**: [https://aistudio.google.com](https://aistudio.google.com)
- **GCP Vertex AI Setup**: [https://cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs)
- **Astral uv Official Guide**: [https://astral.sh/uv](https://astral.sh/uv)
