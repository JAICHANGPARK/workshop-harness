# 워크숍 사전 준비 및 모델 다운로드 안내

현장 네트워크(WiFi) 혼잡으로 인한 다운로드 지연을 방지하기 위해 **반드시 행사 참가 전 아래 항목을 준비**해 주시기 바랍니다.

---

## ⚡ 사전 다운로드 요약 체크리스트

1. **Python 3.9+ 및 `uv` 패키지 매니저 설치**:
   - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

2. **Ollama 또는 LM Studio 다운로드 & 실행**:
   - Ollama 다운로드: https://ollama.com
   - LM Studio 다운로드: https://lmstudio.ai

3. **로컬 LLM 모델 사전 받기 (16GB RAM 기준)**:
   ```bash
   ollama pull gemma4:e4b
   ```
   > 8GB RAM 노트북 사용자는 `ollama pull gemma4:e2b`를 받아주세요.

4. **실습 프로젝트 의존성 사전 설치**:
   ```bash
   cd workshop/01_starter
   uv sync
   ```

---

## 🔍 사전 환경 검증 스크립트 실행

프로젝트에 포함된 사전 점검 스크립트를 실행하여 준비 상태를 최종 확인하세요.

- **macOS / Linux**:
  ```bash
  chmod +x scripts/check_env.sh
  ./scripts/check_env.sh
  ```

- **Windows**:
  ```powershell
  .\scripts\check_env.ps1
  ```
