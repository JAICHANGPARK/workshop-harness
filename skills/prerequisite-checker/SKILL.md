---
name: prerequisite-checker
description: OS별(macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) 사전 준비 가이드 문서 작성 및 언어/SDK(Python, Node.js, Go, Flutter, Rust, Docker)와 최신 AI 모델, Google AI Studio / GCP Gemini API Key 발급 절차 및 자동 점검 스크립트(check_env.sh, check_env.ps1) 생성을 담당하는 스킬
---

# Prerequisite Checker & API Key / SDK Installation Guide Skill

## 📌 목적
참가자들이 워크숍 당일 현장에서 개발 언어, SDK, AI 모델 및 **Google AI Studio / GCP Gemini API Key 미발급**으로 막히지 않도록 단계별 키 발급 절차와 환경 검증 스크립트를 자동 생성합니다.

---

## 🔑 Google AI Studio & GCP Key 발급 가이드 생성 규약

### 1. Google AI Studio Gemini API Key (개인/참가자용)
- **발급 URL**: [https://aistudio.google.com](https://aistudio.google.com)
- **절차**: Google 로그인 > Get API key > Create API key > `AIzaSy...` 키 복사
- **`.env` 저장**: `GEMINI_API_KEY="AIzaSy..."`

### 2. GCP Vertex AI Key (기업/GCP 프로젝트용)
- **발급 URL**: [https://console.cloud.google.com](https://console.cloud.google.com)
- **절차**: Vertex AI API 활성화 (`gcloud services enable aiplatform.googleapis.com`) > Service Account 생성 및 `Vertex AI User` 역할 부여 > JSON 키 다운로드
- **환경변수**: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"`

### 3. 🚨 보안 가이드라인 (Security Guidelines)
- `.env` 및 `*.json` 파일은 절대 Git 저장소에 커밋되어선 안 되며, 스킬 실행 시 `.env.sample` 및 `.gitignore`에 자동 수록합니다.

---

## 🤖 최신 AI 모델 파인딩 원칙 (Latest AI Model Currency Protocol)
- 과거 모델명(`gpt-3.5`, `llama-2`, `gemma-1`)을 하드코딩하지 않습니다.
- `workshop-web-researcher` 스킬을 통해 현 시점 최신 릴리스 모델 태그(예: `gemma4:e4b`, `gemini-2.0-flash`)를 동적으로 조회합니다.
- 사전 준비 문서 상단에 **`> 💡 최신 모델 기준 확인일: YYYY-MM-DD`**를 명시합니다.

---

## 🛠️ 언어 & SDK별 OS 설치 명령어 매트릭스

### Python (3.9+) & `uv` 매니저
- **macOS**: `brew install python@3.11 && curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `winget install Python.Python.3.11` 및 `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Linux**: `sudo apt update && sudo apt install -y python3 python3-pip python3-venv`

---

## 🔍 자동 환경 검증 스크립트 (`check_env.sh` / `check_env.ps1`)

```bash
# Example: API Key & SDK Check Snippet
if [ -z "$GEMINI_API_KEY" ] && [ ! -f .env ]; then
    echo "[WARN] GEMINI_API_KEY is not set and .env file missing."
    echo "       Please issue your key at https://aistudio.google.com and put it in .env"
else
    echo "[OK] GEMINI_API_KEY configured."
fi
```
