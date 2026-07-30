---
name: workshop-persona-loop-evaluator
description: 루프 엔지니어링(Loop Engineering) 기법을 기반으로 초급, 중급, 고급 참가자 페르소나 입장에서 워크숍 커리큘럼과 코드를 다각도로 리뷰·검증하고 개선 리포트(docs/00-persona-loop-review-report.md)를 생성하는 스킬
---

# Workshop Persona Loop Evaluator Skill (Loop Engineering)

## 📌 목적
워크숍 자료 완성을 앞두고 **루프 엔지니어링(Loop Engineering)** 및 멀티 페르소나 평가 기법을 적용하여, **초급(Beginner), 중급(Intermediate), 고급(Advanced)** 3가지 수준의 참가자 입장에서 워크숍 가이드와 코드를 시뮬레이션 리뷰하고 부족한 점을 자동으로 보완·개선합니다.

---

## 🔄 루프 엔지니어링 3대 페르소나 검증 루프 (Multi-Persona Loop)

### 1. 🐣 초급 참가자 페르소나 (Beginner Persona Audit)
- **검증 관점**: 진입 장벽, 용어 난이도, 생략된 가이드 여부
- **체크리스트**:
  - *"기술 용어(Vector Search, Quantization, Stream, Pydantic)에 대한 쉬운 개념 설명이 1문장 포함되어 있는가?"*
  - *"환경변수 설정이나 설치 명령어가 생략 없이 복사-붙여넣기(`Copy-Paste`) 가능한가?"*
  - *"실습 중 막혔을 때 정답 코드(`02_final`) 안내 위치가 명확한가?"*

### 2. 🐥 중급 참가자 페르소나 (Intermediate Persona Audit)
- **검증 관점**: 적정 코드 작성량, 타임라인 체계성, 실용성
- **체크리스트**:
  - *"60분~90분 실습 시간 내에 참가자가 작성할 `TODO` 코드 범위가 과도하지 않은가?"*
  - *"Structured Output JSON Schema 및 에러 처리 예외 코드가 깔끔하게 분리되어 있는가?"*

### 3. 🦅 고급 참가자 페르소나 (Advanced Persona Audit)
- **검증 관점**: 깊이감, 성능 최적화, 프로덕션 확장성 (Challenge Tasks)
- **체크리스트**:
  - *"기본 실습을 빠르게 마친 고수 참석자를 위한 도전 과제(Challenge Tasks)가 1~2개 제시되어 있는가?"*
  - *"로컬 LLM 컨텍스트 크기, 추론 속도, 메모리 최적화 팁이 수록되어 있는가?"*

---

## 📄 루프 엔지니어링 리뷰 산출물 (`docs/00-persona-loop-review-report.md`)

`harness_cli.py audit-loop` 또는 에이전트 요청 시 아래 형식의 리뷰 검증 리포트를 자동 생성합니다:

```markdown
# 🔄 루프 엔지니어링 (Loop Engineering) 난이도별 참가자 리뷰 리포트

- 워크숍 주제: Local RAG with Gemma 4
- 검증 일시: YYYY-MM-DD
- 상태: Approved / Action Required

---

## 🐣 1. 초급 참가자 (Beginner Persona) 리뷰
- **피드백**: `docs/01-hardware-and-env.md`에 파라미터 'B'에 대한 용어 설명 추가 필요.
- **조치 사항**: 8GB RAM 노트북 사용자를 위한 모델 다운로드 명령어 강조 완료.

## 🐥 2. 중급 참가자 (Intermediate Persona) 리뷰
- **피드백**: `workshop/01_starter` 코드 내 Pydantic import 구문 주석 정리 완료.
- **조치 사항**: JSON 파싱 예외 처리 구문 프롬프트 팩 수록.

## 🦅 3. 고급 참가자 (Advanced Persona) 리뷰
- **피드백**: 기본 실습을 마친 사용자를 위한 멀티에이전트 확장 가이드 필요.
- **조치 사항**: `docs/15-advanced-challenge-task.md` 도전 과제 섹션 자동 수록.
```
