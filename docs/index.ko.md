# Workshop Harness (한국어)

> **AI 에이전트 하네스, 21개 전문 스킬 모음 및 CLI 자동화 툴킷**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-21%20Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.10.31-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

---

## 개요

**Workshop Harness**는 기술 워크숍(Build with AI, DevFest, 커뮤니티 개발자 랩)을 주최하는 오거나이저, 발표자, 퍼실리테이터, 그리고 기술 조교(TA)를 위한 **원클릭 AI 에이전트 오케스트레이션 툴킷**입니다.

[AGENTS.md 표준 명세](https://agents.md/)를 준수하여 **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Cursor**, **Aider** 등 모든 AI 코딩 에이전트와 네이티브 상호운용성을 제공합니다.

---

## Quickstart Guide

```bash
# 1. 저장소 복제
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 21개 스킬 자동 설치 (~/.gemini/skills/ 및 ~/.gemini/config/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. 원클릭 워크숍 자동 생성 (기본 모델: gemini-3.8-flash)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 21개 에이전트 스킬 목록

- `workshop-scaffolder`: 표준 워크숍 리포지토리 스캐폴딩
- `cross-architecture-checker`: 칩셋/OS 호환성 진단 & Fallback 가이드 생성 (`docs/18-intel-mac-prep.md`)
- `prerequisite-checker`: 통합 사전 준비 가이드 및 `check_env` 자동 점검 스크립트
- `hands-on-curriculum-builder`: 단계별 실습 커리큘럼 & starter/final 코드
- `pdf-handout-generator`: ReportLab + PyMuPDF 기반 PDF 핸드아웃 및 미리보기
- `workshop-troubleshooter`: RAM(8G/16G/32G+)/OS별 트러블슈팅 매트릭스
- `workshop-runbook-generator`: 발표자 & TA 전용 분단위 진행 타임라인 런북 (`RUNBOOK.md`)
- `live-debug-assistant`: 현장 터미널 에러 10초 핫픽스 & API Key 보안 프로토콜
- `workshop-faq-generator`: 참가자 사전 FAQ 자동 작성 (`docs/20-faq.md`)
- `workshop-tester`: 코드 스모크 테스트, 2026 모델 태그 최신성 & 깨진 링크 자동 검증
- `workshop-web-researcher`: 2026 최신 SDK/AI 모델 버전 실시간 웹 오디팅
- `workshop-persona-loop-evaluator`: 비개발자/초급/중급/시니어 4-페르소나 루프 엔지니어링 리뷰
- `open-codelabs-integrator`: Open Codelabs 매니페스트 내보내기(`codelab.yaml`) & `oc` push
- `colab-workshop-integrator`: Google Colab 노트북(`.ipynb`) 변환, 뱃지 삽입 및 Colab CLI 테스트
- `workshop-slide-generator`: Google Slides `.pptx`, Marp 마크다운 및 인터랙티브 웹 발표 슬라이드 자동 생성
- `adk-workshop-builder`: 공식 5대 언어(Python, Go, Java, Kotlin, TypeScript, Polyglot) Google ADK 멀티에이전트 실습 빌더
- `eli5-concept-explainer`: 3단계 ELI5 물리 비유 & 멘탈 맵 해설 (`docs/eli5-concept-cheat-sheet.md`)
- `android-workshop-builder`: Jetpack Compose Material 3, `com.google.genai` 및 `android` CLI 기반 Android GenAI 실습 빌더
- `flutter-workshop-builder`: Flutter 3.x, `google_generative_ai` 및 Flutter Web 무설치 폴백 기반 크로스플랫폼 실습 빌더
- `a2ui-workshop-builder`: A2UI 선언형 JSON 스트리밍 및 Flutter `genui` 동적 위젯 서피스 실습 빌더
- `agents-cli-workshop-builder`: Google Agents CLI(`google-agents-cli`) 및 7대 공식 스킬 기반 에이전트 개발 생명주기(ADLC) 실습 빌더
