# 워크숍 사전 준비 및 개발 언어 / SDK / API Key 발급 가이드

현장 와이파이 혼잡으로 인한 다운로드 지연 및 발급 오류를 방지하기 위해 **반드시 행사 참가 전 아래 언어, SDK 및 API Key를 준비**해 주시기 바랍니다.

---

## 🔑 1. Google AI Studio & Gemini API Key 발급 가이드

개인 개발자 및 일반 워크숍 참가자는 **Google AI Studio**를 통해 1분 만에 무료 Gemini API Key를 발급받으실 수 있습니다.

### 📌 발급 절차
1. **Google AI Studio 접속**: [https://aistudio.google.com](https://aistudio.google.com) 로그인
2. **API Key 생성**:
   - 좌측 메뉴 상단의 **"Get API key"** 버튼 클릭
   - **"Create API key"** 버튼 선택 (새 프로젝트 또는 기존 GCP 프로젝트 연결)
3. **API Key 복사**: `AIzaSy...` 형식으로 생성된 키를 복사합니다.
4. **로컬 환경변수 설정**:
   - 실습 프로젝트 루트에 `.env` 파일을 생성하고 키를 저장합니다:
     ```bash
     GEMINI_API_KEY="AIzaSyYourGeneratedApiKeyHere"
     ```

> 🚨 **보안 주의사항 (Critical Security)**:
> API Key는 개인 비밀번호와 같습니다. **절대로 GitHub 저장소에 커밋하지 마세요.**
> `.gitignore` 파일에 `.env` 및 `*.json`이 포함되어 있는지 확인하세요.

---

## ☁️ 2. Google Cloud Platform (GCP) Vertex AI 키 발급 가이드

엔터프라이즈 및 GCP 기반 워크숍 진행 시 Vertex AI API를 연동합니다.

### 📌 GCP 콘솔 설정 절차
1. **Google Cloud Console 접속**: [https://console.cloud.google.com](https://console.cloud.google.com)
2. **Vertex AI API 활성화**:
   - 검색창에 `Vertex AI API` 검색 후 **[활성화 (Enable)]** 클릭
   - 또는 Google Cloud SDK 터미널 명령:
     ```bash
     gcloud services enable aiplatform.googleapis.com
     ```
3. **서비스 계정(Service Account) 및 JSON 키 발급**:
   - `IAM & 행정(IAM & Admin)` > `서비스 계정(Service Accounts)` 이동
   - **[서비스 계정 만들기]** 클릭 (역할: `Vertex AI User`)
   - 키 탭에서 **[새 키 만들기] > [JSON]** 선택하여 다운로드
4. **로컬 인증 환경변수 설정**:
   - **macOS / Linux**:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/경로/your-gcp-key.json"
     ```
   - **Windows (PowerShell)**:
     ```powershell
     $env:GOOGLE_APPLICATION_CREDENTIALS="C:\경로\your-gcp-key.json"
     ```

---

## 🛠️ 3. 개발 언어 및 SDK OS별 설치 명령어

### Python (3.9+) & `uv` 패키지 매니저
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

### Node.js & npm (v20+)
- **macOS**: `brew install node`
- **Windows**: `winget install OpenJS.NodeJS`
- **Linux**: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs`

---

### Flutter SDK & Dart
- **macOS**: `brew install --cask flutter`
- **Windows**: `winget install Flutter.Flutter`
- **Linux**: `sudo snap install flutter --classic`

---

## ⚡ 사전 다운로드 요약 체크리스트

1. **Ollama / LM Studio 다운로드 & 모델 받아두기**:
   ```bash
   ollama pull gemma4:e4b
   ```

2. **실습 프로젝트 의존성 사전 동기화**:
   ```bash
   cd workshop/01_starter
   uv sync
   ```

---

## 🔗 참고 (References)

- **Google AI Studio Key Issue**: [https://aistudio.google.com](https://aistudio.google.com)
- **GCP Vertex AI Setup**: [https://cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs)
- **Astral uv Official Guide**: [https://astral.sh/uv](https://astral.sh/uv)
