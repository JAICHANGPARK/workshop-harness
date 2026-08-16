# Workshop Harness (한국어)

> **AI 에이전트 하네스, 15개 스킬 모음 및 CLI 자동화 툴킷**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 개요

**Workshop Harness**는 기술 워크숍(Build with AI, DevFest, 커뮤니티 개발자 랩)을 주최하는 오거나이저, 발표자, 퍼실리테이터, 그리고 기술 조교(TA)를 위한 **원클릭 AI 에이전트 오케스트레이션 툴킷**입니다.

[AGENTS.md 표준 명세](https://agents.md/)를 준수하여 **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Cursor**, **Aider** 등 다양한 AI 에이전트와 네이티브 상호운용성을 제공합니다.

---

## Quickstart Guide

```bash
# 1. 저장소 복제
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 15개 스킬 자동 설치 (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. 원클릭 워크숍 자동 생성
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 15개 에이전트 스킬 목록

- `workshop-scaffolder`: 표준 리포지토리 스캐폴딩
- `cross-architecture-checker`: 칩셋/OS 호환성 진단 & Fallback
- `prerequisite-checker`: 통합 사전 가이드 작성
- `hands-on-curriculum-builder`: 랩 가이드 & starter/final 코드
- `pdf-handout-generator`: ReportLab 기반 PDF 핸드아웃
- `workshop-troubleshooter`: RAM/OS별 트러블슈팅 FAQ
- `workshop-runbook-generator`: 분단위 진행 타임라인 런북
- `live-debug-assistant`: 현장 10초 핫픽스
- `workshop-faq-generator`: 참가자 FAQ 자동 작성
- `workshop-tester`: 코드 스모크 테스트 & 깨진 링크 오디팅
- `workshop-web-researcher`: 최신 SDK 버전 실시간 웹 오디팅
- `workshop-persona-loop-evaluator`: 초/중/고급 페르소나 멀티 리뷰
- `open-codelabs-integrator`: Open Codelabs 매니페스트 내보내기 & `oc` push
- `colab-workshop-integrator`: Google Colab 노트북(`.ipynb`) 변환, 뱃지 삽입 및 Colab CLI 테스트
- `workshop-slide-generator`: Marp 마크다운 및 인터랙티브 웹 발표 슬라이드 자동 생성
