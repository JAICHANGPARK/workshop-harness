---
name: hands-on-curriculum-builder
description: 핸즈온 실습 단계별 커리큘럼(Step-by-Step Labs), starter 및 final 코드, 프롬프트 팩(Prompt Pack), Output Schema 명세서 작성을 관리하는 스킬
---

# Hands-on Curriculum Builder Skill

## 📌 목적
참가자가 실습 시간 내(예: 60분~120분)에 명확한 목표를 달성할 수 있도록, 커리큘럼을 단계별(Lab 1, Lab 2, Lab 3)로 모듈화하고, 시작점(`01_starter`)과 정답 완성본(`02_final`) 및 복사 가능한 프롬프트 팩(`prompt-pack/`)을 구성합니다.

---

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

---

## 🔗 출처 및 참고 문헌 필수 규약 (Mandatory References Protocol)

모든 실습 가이드 문서(`03_labs/README.md` 등) 및 외부 데이터/공식 API를 참고한 문서의 최하단에는 **반드시 `## 🔗 참고 (References)` 섹션을 포함**시켜 공식 문서 및 인용 출처를 명시해야 합니다.

```markdown
## 🔗 참고 (References)

- **Official API Documentation**: [Google Gemini API Docs](https://ai.google.dev/docs)
- **Framework Guide**: [Flutter Developer Docs](https://docs.flutter.dev)
- **Base Workshop Repository**: [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
```
