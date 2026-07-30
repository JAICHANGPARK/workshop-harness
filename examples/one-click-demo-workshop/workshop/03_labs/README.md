# 핸즈온 실습 세션 가이드 (Step-by-Step)

본 가이드는 당일 실습을 진행하는 순서와 단계별 목표를 설명합니다. 실습 코드는 `workshop/01_starter` 폴더에서 작성하며, 막히는 경우 `workshop/02_final` 정답 코드를 참고할 수 있습니다.

---

## ⏱️ 실습 일정 (총 60분)

- **00m ~ 10m**: 워크숍 개요 소개 & 사전 환경 최종 체크
- **10m ~ 25m**: **Lab 01** - 로컬 LLM 서버 연결 및 기본 Prompt 실행
- **25m ~ 45m**: **Lab 02** - Structured Output (JSON Schema) 및 Tool Integration
- **45m ~ 55m**: **Lab 03** - 최종 애플리케이션 시나리오 완주 & 결과 검증
- **55m ~ 60m**: Q&A 및 마무리

---

## 🧪 단계별 실습 (Labs)

### 🔹 Lab 01: 로컬 LLM 서버 API 연동
- **목표**: Ollama / LM Studio local port (11434 / 1234)에 요청을 보내고 스트리밍 응답 받기
- **실습 파일**: `workshop/01_starter/src/lab1_basic.py`
- **핵심 코드 주석 위치**: `TODO: [Lab 1]` 부분 채우기

### 🔹 Lab 02: 구조화된 출력 (Structured Output) 구현
- **목표**: Pydantic / Output Schema를 사용해 로컬 LLM의 응답을 JSON 객체로 파싱
- **실습 파일**: `workshop/01_starter/src/lab2_schema.py`
- **참고 프롬프트**: `prompt-pack/02-output-schema.md` 내용 복사 후 적용

### 🔹 Lab 03: 핸즈온 앱 완성 및 테스트
- **목표**: 전체 파이프라인(User Input -> System Prompt -> LLM Execution -> Parsed Output -> Action) 통합
- **실습 파일**: `workshop/01_starter/src/main.py`
- **실행 명령**:
  ```bash
  ./run.sh  # (Windows: .\run.ps1)
  ```
