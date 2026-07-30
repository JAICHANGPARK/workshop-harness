---
name: workshop-troubleshooter
description: 장비 사양별(8GB, 16GB, 32GB RAM), OS별(Windows, Intel/Silicon Mac, Linux), 오프라인/네트워크 장애 상황별 트러블슈팅 가이드 및 FAQ 문서를 구축하는 스킬
---

# Workshop Troubleshooter Skill

## 📌 목적
워크숍 진행 중 참가자들에게 발생할 수 있는 주요 장애 요인(RAM 부족, GPU 지원 미비, 포트 충돌, 오프라인 환경 등)을 사전 분류하고, 현장 진행 요원(TA) 및 참가자가 즉각 대처할 수 있도록 매트릭스 형태의 트러블슈팅 가이드와 FAQ를 작성합니다.

## 🔍 핵심 트러블슈팅 매트릭스 패턴

### 1. 장비 사양 및 메모리 (RAM) 문제
- **증상**: 모델 로딩 중 `Out of Memory (OOM)` / 커널 킬 (Killed) / PC 먹통
- **원인**: 8GB RAM 장비에서 7B/13B 이상의 모델을 로드하려고 함
- **해결책**:
  - 즉시 8GB 권장 모델(`gemma4:e2b` 등 2B~3B 이하 경량 모델)로 모델 교체
  - LM Studio / Ollama Context Window 길이를 2048 이하로 축소
  - 다른 백그라운드 프로그램(Chrome 탭, VS Code 서드파티 확장 등) 종료

### 2. Windows OS 특화 문제
- **증상**: PowerShell 실행 정책 에러 (`Execution_Policies`), Docker Daemon 연결 실패
- **원인**: PowerShell Script 보안 제약 또는 WSL2 / Docker Desktop 미실행
- **해결책**:
  - `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` 스크립트 안내
  - `wsl --status` 및 Docker Desktop 프로세스 재시작 구문 제공

### 3. Intel Mac / 구형 Mac 특화 문제
- **증상**: LM Studio Metal acceleration 미지원 또는 실행 불가
- **원인**: Apple Silicon(M1/M2/M3/M4)이 아닌 Intel CPU 기반 Mac
- **해결책**:
  - LM Studio 대신 **Ollama CLI** (`ollama serve`) 기준 가이드로 즉시 우회 안내
  - Ollama CPU fallback 동작 모드 활용

### 4. 현장 WiFi / 네트워크 단절 상황 (Offline Emergency Fallback)
- **증상**: 현장 와이파이 마비로 모델 / 패키지 다운로드 불가
- **대처방안**:
  - 오프라인 USB 핫스팟/로컬 파일 서버 공유 안내 (GGUF 모델 파일, Docker tar 이미지)
  - Ollama 모델 임포트 명령어: `ollama create my-gemma4 -f Modelfile`
  - Python wheel 파일 로컬 설치: `pip install --no-index --find-links=./wheels -r requirements.txt`

## 📄 가이드 생성 산출물
- `docs/19-troubleshooting-and-final-check.md`
- `docs/20-faq.md`
