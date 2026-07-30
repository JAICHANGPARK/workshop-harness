---
name: prerequisite-checker
description: OS별(macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) 사전 준비 가이드 문서 작성 및 언어/SDK(Python, Node.js, Go, Flutter, Rust, Docker) 설치 가이드와 자동 점검 스크립트(check_env.sh, check_env.ps1) 생성을 담당하는 스킬
---

# Prerequisite Checker & SDK Installation Guide Skill

## 📌 목적
참가자들이 워크숍 당일 현장에서 개발 언어 및 SDK 미설치로 막히지 않도록, **OS별(macOS, Windows, Linux) 주요 언어/SDK(Python, Node.js, Go, Flutter/Dart, Rust, Docker, uv 등)의 공식 설치 명령어와 PATH 환경변수 설정 가이드**를 포함한 사전 준비 문서를 자동 생성합니다.

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

### 2. Node.js & npm / pnpm
- **macOS**: `brew install node`
- **Windows**: `winget install OpenJS.NodeJS`
- **Linux**:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt install -y nodejs
  ```

---

### 3. Go Language (1.21+)
- **macOS**: `brew install go`
- **Windows**: `winget install GoLang.Go`
- **Linux**: `sudo apt install -y golang-go`

---

### 4. Dart & Flutter SDK
- **macOS**: `brew install --cask flutter`
- **Windows**: `winget install Flutter.Flutter`
- **Linux**: `sudo snap install flutter --classic`
- **환경변수 점검**: `flutter doctor`

---

### 5. Docker & Docker Desktop
- **macOS**: `brew install --cask docker`
- **Windows**: `winget install Docker.DockerDesktop` *(WSL2 백엔드 활성화 필수)*
- **Linux**: `curl -fsSL https://get.docker.com | sh`

---

## 🔍 자동 환경 검증 스크립트 (`check_env.sh` / `check_env.ps1`)

스킬 실행 시 감지된 워크숍 대상 SDK에 따라 맞춤형 환경 검증 구문을 동적으로 생성합니다.

```bash
# Example: SDK Check Snippet
if command -v flutter &> /dev/null; then
    echo "[OK] Flutter SDK installed: $(flutter --version | head -n 1)"
else
    echo "[WARN] Flutter SDK not found. Install via: winget install Flutter.Flutter (Win) or brew install --cask flutter (Mac)"
fi
```
