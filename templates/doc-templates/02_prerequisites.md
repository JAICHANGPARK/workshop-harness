# 워크숍 사전 준비 및 언어/SDK 설치 가이드

현장 와이파이 혼잡으로 인한 다운로드 지연 및 설치 오류를 방지하기 위해 **반드시 행사 참가 전 아래 언어, SDK 및 모델을 설치**해 주시기 바랍니다.

---

## 🛠️ 개발 언어 및 SDK OS별 설치 명령어

### 1. Python (3.9+) & `uv` 패키지 매니저
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
  *(참고: 설치 시 "Add Python to PATH" 체크 필수)*
- **Linux**:
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip python3-venv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

### 2. Node.js & npm (v20+)
- **macOS**: `brew install node`
- **Windows**: `winget install OpenJS.NodeJS`
- **Linux**: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs`

---

### 3. Go Language (1.21+)
- **macOS**: `brew install go`
- **Windows**: `winget install GoLang.Go`
- **Linux**: `sudo apt install -y golang-go`

---

### 4. Flutter SDK & Dart
- **macOS**: `brew install --cask flutter`
- **Windows**: `winget install Flutter.Flutter`
- **Linux**: `sudo snap install flutter --classic`

---

### 5. Docker Desktop
- **macOS**: `brew install --cask docker`
- **Windows**: `winget install Docker.DockerDesktop` *(WSL2 기능 체크 필수)*

---

## ⚡ 사전 다운로드 요약 체크리스트

1. **Ollama / LM Studio 다운로드 & 모델 받아두기**:
   ```bash
   ollama pull gemma4:e4b
   ```
   *(8GB RAM 노트북은 `ollama pull gemma4:e2b` 권장)*

2. **실습 프로젝트 의존성 사전 동기화**:
   ```bash
   cd workshop/01_starter
   uv sync
   ```

---

## 🔍 사전 환경 검증 스크립트 실행

- **macOS / Linux**:
  ```bash
  chmod +x scripts/check_env.sh
  ./scripts/check_env.sh
  ```

- **Windows**:
  ```powershell
  .\scripts\check_env.ps1
  ```

---

## 🔗 참고 (References)

- **Astral uv Official Guide**: [https://astral.sh/uv](https://astral.sh/uv)
- **Flutter Official Installation Guide**: [https://docs.flutter.dev/get-started/install](https://docs.flutter.dev/get-started/install)
- **Docker Desktop Documentation**: [https://docs.docker.com/desktop](https://docs.docker.com/desktop)
- **Google Gemma Model Library**: [https://ollama.com/library/gemma4](https://ollama.com/library/gemma4)
