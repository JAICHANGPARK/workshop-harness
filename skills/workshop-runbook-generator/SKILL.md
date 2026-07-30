---
name: workshop-runbook-generator
description: 발표자와 보조 진행자(TA)를 위한 분단위 진행 타임라인 런북(RUNBOOK.md), 시동 멘트, TA 가이드라인, 참가자 진행률 체크포인트를 작성하는 스킬
---

# Workshop Runbook Generator Skill

## 📌 목적
세션 진행자(Facilitator/Speaker)와 보조 진행자(TA)가 행사 당일 혼선 없이 세션을 끌고 나갈 수 있도록, 시간대별 발표 멘트, 화면 공유 타임라인, TA 조치 시널, 1분 점검 퀴즈가 포함된 **진행자용 런북(`RUNBOOK.md`)**을 자동 생성합니다.

---

## ⏱️ 런북 타임라인 표준 템플릿 (`RUNBOOK.md`)

```markdown
# 🎤 [진행자 & TA 전용] 워크숍 세션 진행 런북 (Runbook)

- 세션명: Build Your Own AI App
- 진행자 (Speaker): main facilitator
- 보조 진행자 (TA): 2~3명 권장
- 전체 진행 시간: 60분 (또는 90분)

---

## ⏰ 타임라인 및 진행 가이드

### 00m ~ 10m: 오프닝 & 사전 준비 환경 최종 체크
- **발표자 액션**:
  - 화면 공유: `gemma4-local-setup-guide.md` 및 사전 체크리스트 화면 띄우기
  - 멘트: *"노트북 환경 점검 스크립트 `./scripts/check_env.sh`를 실행하여 OK 메시지가 나오는지 확인해주세요."*
- **TA 역할**:
  - 강의장 뒤편/옆편을 순회하며 빨간색/노란색 에러 경고가 떠 있는 참가자 확인 및 1:1 조치
  - 모델 미다운로드 참가자에게 로컬 USB로 GGUF 모델 파일 전달

### 10m ~ 25m: Lab 01 - 기본 연결 및 Hello World
- **발표자 액션**:
  - 화면 공유: `workshop/01_starter` 코드와 IDE (VS Code / Antigravity)
  - 핵심 실습 부분(`TODO: [Lab 1]`) 주석 설명 및 실행 시연
- **체크포인트 퀴즈 (1분)**:
  - *"터미널에 LLM 응답 스트리밍이 정상 출력되는 분은 손을 들어주시거나 OK 스티커를 붙여주세요."*

### 25m ~ 45m: Lab 02 - Structured Output & Tool Call
- **발표자 액션**:
  - `prompt-pack/README.md`의 Pydantic Schema 및 System Prompt 적용 방법 시연
- **TA 역할**:
  - JSON 파싱 에러 (`ValidationError`) 발생 참가자 가이드 (대괄호/따옴표 누락 확인)

### 45m ~ 55m: Lab 03 - 전체 앱 완주 및 검증
- **발표자 액션**:
  - 완성본 (`workshop/02_final`) 코드 시연 및 결과 결과물 비교
- **TA 역할**:
  - 아직 미완성인 참가자에게 정답 코드 수동 복사 안내

### 55m ~ 60m: Q&A, 설문 및 마무리
- **발표자 액션**:
  - 설문 링크 공유 및 기념 촬영, 세션 회고
```
