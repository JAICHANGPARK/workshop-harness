---
name: live-debug-assistant
description: 행사 현장에서 참가자가 가져온 터미널 에러 로그를 10초 만에 분석하여 조치 명령어를 알려주는 현장 긴급 진단 및 API Key 보안 관리 스킬
---

# Live Debug Assistant & Security Protocol Skill

## 📌 목적
워크숍 현장에서 진행자(Speaker)와 TA가 참가자들의 돌발적인 설치/실행 에러 로그를 만났을 때, 원인을 빠르게 3문장 이내로 파악하고 **10초 핫픽스(Hotfix) 조치 명령어**를 안내하며, API Key 유출을 방지합니다.

---

## 🚨 현장 자주 발생하는 Top 5 긴급 에러 핫픽스 갤러리

### 1. `ConnectionRefusedError: [Errno 61] Connection refused`
- **원인**: Ollama 또는 LM Studio 로컬 데몬 미실행.
- **10초 조치 명령어**:
  ```bash
  ollama serve
  ```
  *(LM Studio 사용자의 경우 GUI에서 Server Started 클릭)*

### 2. `ValidationError: 1 validation error for OutputSchema`
- **원인**: LLM 응답에 마크다운 코드펜스(```json ... ```)가 포함되어 JSON 파싱 실패.
- **10초 조치 명령어**:
  - System prompt 끝에 `Strictly output raw JSON only without markdown code fences.` 문구 추가.

### 3. `uv: Unknown option / lock error`
- **원인**: 구버전 uv 설치 또는 기존 `.venv` 캐시 충돌.
- **10초 조치 명령어**:
  ```bash
  uv self update && rm -rf .venv && uv sync
  ```

### 4. `PowerShell Execution Policy Error` (Windows)
- **원인**: Windows 스크립트 실행 제한.
- **10초 조치 명령어**:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

### 5. `Docker daemon is not running` (Session 2)
- **원인**: Docker Desktop 미실행 또는 WSL2 디시블.
- **10초 조치 명령어**:
  ```powershell
  # Windows
  wsl --shutdown; wsl
  ```

---

## 🔐 API Key 보안 관리 규트 (Security Protocol)

- **경고**: 외부 API (Gemini API Key, OpenAI Key, Mongo URI 등) 사용 시 절대 원본 코드가 담긴 `.py` 파일에 하드코딩 금지!
- **필수 환경변수 파일 관리**:
  - `.env.sample` 제공: `GEMINI_API_KEY=YOUR_API_KEY_HERE`
  - `.gitignore` 확인: `.env` 및 `*.pem` 파일 커밋 방지
