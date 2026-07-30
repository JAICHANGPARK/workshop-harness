---
name: prerequisite-checker
description: OS별(macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) 사전 준비 가이드 문서 작성 및 언어/SDK(Python, Node.js, Go, Flutter, Rust, Docker)와 최신 AI 모델 설치 가이드 및 자동 점검 스크립트(check_env.sh, check_env.ps1) 생성을 담당하는 스킬
---

# Prerequisite Checker & SDK/Model Installation Guide Skill

## 📌 목적
참가자들이 워크숍 당일 현장에서 개발 언어 및 SDK/AI 모델 미설치로 막히지 않도록, **OS별(macOS, Windows, Linux) 주요 언어/SDK의 공식 설치 명령어와 현 시점 최신 AI 모델(Gemini, Gemma 4, Llama 등) 다운로드 안내**를 포함한 사전 준비 문서를 자동 생성합니다.

---

## 🤖 최신 AI 모델 파인딩 원칙 (Latest AI Model Currency Protocol)
- 에이전트는 지식 컷오프에 기반한 오래된 모델명(`gpt-3.5`, `llama-2`, `gemma-1`)을 절대 추천하지 않습니다.
- `workshop-web-researcher` 스킬을 통해 현 시점 최신 릴리스 모델 태그(예: `gemma4:e4b`, `gemini-2.0-flash`)를 동적으로 조회한 후 설치 가이드에 수록합니다.
- 사전 준비 문서 상단에 **`> 💡 최신 모델 기준 확인일: YYYY-MM-DD`**를 반드시 명시합니다.

---

## 🛠️ 언어 & SDK별 OS 설치 명령어 매트릭스 (SDK Installation Matrix)

### 1. Python (3.9+) 및 `uv` 매니저
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
  *(주의: 설치 시 "Add Python to PATH" 체크 필수)*
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip python3-venv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

### 2. 최신 로컬 LLM AI 모델 다운로드 (Ollama)
- **추천 최신 모델 받기**:
  ```bash
  ollama pull gemma4:e4b   # 기본 4-bit 양자화 모델
  ollama pull gemma4:e2b   # 8GB RAM 이하 경량화 모델
  ```

---

## 🔍 자동 환경 검증 스크립트 (`check_env.sh` / `check_env.ps1`)

스킬 실행 시 감지된 워크숍 대상 SDK 및 최신 AI 모델 유무를 동적으로 검증하는 구문을 생성합니다.

```bash
# Example: SDK & Model Check Snippet
if command -v ollama &> /dev/null; then
    echo "[OK] Ollama installed."
    ollama list | grep -q "gemma4" && echo "[OK] Latest Gemma 4 model present." || echo "[WARN] Gemma 4 model missing. Run: ollama pull gemma4:e4b"
fi
```
