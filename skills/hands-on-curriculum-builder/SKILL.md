---
name: hands-on-curriculum-builder
description: 핸즈온 실습 단계별 커리큘럼(Step-by-Step Labs), starter 및 final 코드, 프롬프트 팩(Prompt Pack), Output Schema 명세서 작성을 관리하는 스킬
---

# Hands-on Curriculum Builder Skill

## 📌 목적
참가자가 실습 시간 내(예: 60분~120분)에 명확한 목표를 달성할 수 있도록, 커리큘럼을 단계별(Lab 1, Lab 2, Lab 3)로 모듈화하고, 시작점(`01_starter`)과 정답 완성본(`02_final`) 및 복사 가능한 프롬프트 팩(`prompt-pack/`)을 구성합니다.

## 🧱 구조 설계 패턴

### 1. `starter` vs `final` 코드 분리 원칙
- **`01_starter/`**:
  - 기본적인 프로젝트 구조, 의존성 패키지 파일(`pyproject.toml`, `pubspec.yaml`, `go.mod`), CLI/UI 진입점 제공
  - 참가자가 직접 채워 넣어야 하는 핵심 로직 부분에 `TODO: [Lab 1] ...` 주석 표시
- **`02_final/`**:
  - 모든 `TODO`가 완벽히 작성되고 정상 작동하는 정답 예시 코드
  - 막힌 참가자가 언제든 비교 및 참고할 수 있도록 준비

### 2. 단계별 실습 가이드 (`03_labs/README.md` 또는 `session-1/README.md`)
- **Lab 01: 기본 연동 및 Hello World**:
  - LLM API / Local Ollama 호출 확인 및 응답 수신
- **Lab 02: 구조화된 출력 (Structured Output / Output Schema)**:
  - Pydantic / JSON Schema를 적용하여 타입 안전한 데이터 파싱
- **Lab 03: 에이전트 / RAG 파이프라인 완성**:
  - Vector Search 또는 Tool Call 연동 후 최종 애플리케이션 완성

### 3. 프롬프트 팩 (`prompt-pack/`) 구성
- 참가자가 복잡한 시스템 프롬프트를 일일이 타이핑하지 않고 바로 복사-붙여넣기(`Copy-Paste`) 할 수 있는 Markdown 모음집.
  - `01-system-prompts.md`: 역할 정의, 규칙, 예시 (Few-shot)
  - `02-output-schema.md`: JSON Schema / Pydantic 모델 명세
  - `03-failure-handling.md`: 에러 예외 처리 및 재시도 프롬프트

## 🛠️ 실습 커리큘럼 빌드 워크플로우

1. **실습 시간(Duration) 산정**:
   - 60분 세션: Lab 1 (15분) + Lab 2 (20분) + Lab 3 (20분) + Q&A (5분)
2. **코드 템플릿 검증**:
   - `01_starter`에서 `run.sh` / `run.ps1` 실행 시 에러 없이 시작 가이드가 출력되는지 확인
   - `02_final`에서 `run.sh` / `run.ps1` 실행 시 성공 결과가 출력되는지 테스트
3. **프롬프트 테스트**:
   - 제시된 system prompt 및 output schema가 대상 모델(예: Gemma 4)에서 환각 없이 정상 동작하는지 사전 검증
