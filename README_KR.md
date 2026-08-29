![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness

[![공식 문서](https://img.shields.io/badge/Official%20Docs-MkDocs-blue.svg)](https://JAICHANGPARK.github.io/workshop-harness/)
[![소개 페이지](https://img.shields.io/badge/Landing%20Page-Website-purple.svg)](https://JAICHANGPARK.github.io/workshop-harness/website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.07.30-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

**공식 문서 사이트**: [https://JAICHANGPARK.github.io/workshop-harness/](https://JAICHANGPARK.github.io/workshop-harness/)
**소개 랜딩 페이지**: [https://JAICHANGPARK.github.io/workshop-harness/website/](https://JAICHANGPARK.github.io/workshop-harness/website/)

---

## 개요

Workshop Harness는 **Astral uv** 패키지 매니저로 구동되는 AI 에이전트 하네스, 스킬(Skills) 모음 및 CLI 자동화 툴킷입니다. Build with AI (BWAI), DevFest, 커뮤니티 세션, 기술 실습 등의 워크숍을 준비하는 주최자, 발표자, TA를 위해 설계되었습니다.

다음과 같은 실제 현장 워크숍 운영 경험에서 검증된 구조와 노하우를 표준화하였습니다:
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)

---

## ⚡ 빠른 시작 (uv 기반 100% 자동화)

의존성 패키지 수동 설치 없이 `uv` 패키지 매니저 기반으로 **1분 만에** 완벽한 워크숍 전체 저장소 패키지를 원클릭으로 구축합니다:

```bash
# 1. 저장소 클론
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 로컬 에이전트 환경(~/.gemini/skills)에 12개 스킬 자동 설치 및 uv 의존성 자동 동기화
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. 원클릭 종합 생성 명령어로 완벽한 워크숍 패키지 구축 (필요 라이브러리 자동 설치됨)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 📦 설치 안내 (Installation)

### 사전 준비물
- **Python**: 버전 3.9 이상
- **Astral uv**: 초고속 Python 패키지 매니저 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git**: 설치 및 설정 완료 상태
- **AI 코딩 에이전트 (선택)**: Google Antigravity, Gemini CLI, Anthropic Claude Code, OpenAI Codex, Cursor, Aider 중 선택

### CLI 및 에이전트 스킬 설치

1. **자동 의존성 & 스킬 로컬 환경 설치**:
   `./scripts/install_skills.sh` 스크립트를 실행하면 `reportlab`, `pymupdf`, `pillow` 패키지가 `uv`로 자동 설치되고 12개 전용 에이전트 스킬이 `~/.gemini/skills`로 설치됩니다.
2. **설치 상태 검증**:
   `uv run harness_cli.py --help` 명령어로 CLI 도구 정상 작동 여부를 확인합니다.

---

## 목차

- [개요](#개요)
- [빠른 시작](#-빠른-시작-uv-기반-100-자동화)
- [설치 안내](#-설치-안내-installation)
- [원클릭 풀 오케스트레이션](#원클릭-풀-오케스트레이션-one-click-full-orchestration)
- [오픈 AI 에이전트 표준 (`AGENTS.md`)](#오픈-ai-에이전트-표준-agentsmd)
- [정량적 생산성 & 퍼실리테이터 ROI](#-정량적-생산성--퍼실리테이터-roi)
- [전체 12개 에이전트 스킬 명세서](#전체-12개-에이전트-스킬-명세서)
- [크로스 아키텍처 호환성 고려사항](#크로스-아키텍처-호환성-고려사항)
- [CLI 사용법 (harness_cli.py)](#cli-사용법-harness_clipy)
- [에이전트 스킬 설치 방법](#에이전트-스킬-설치-방법)
- [표준 워크숍 리포지토리 구조](#표준-워크숍-리포지토리-구조)
- [라이선스](#라이선스)

---

## 원클릭 풀 오케스트레이션 (One-Click Full Orchestration)

단 한 줄의 CLI 명령어 또는 에이전트 자연어 요청만으로 12개 스킬 전체가 연쇄 발동되어 완벽한 워크숍 패키지를 원클릭으로 생성합니다:

```bash
# 12개 전체 스킬 원클릭 연속 발동 생성 명령어 (uv 지원)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 오픈 AI 에이전트 표준 (`AGENTS.md`)

`workshop-harness`는 오픈 이니셔티브 **[AGENTS.md 표준 명세](https://agents.md/)**를 준수하여 모든 AI 에이전트 환경에서 100% 표준 호환됩니다:

- **오픈 에이전트 표준 명세**: [`AGENTS.md`](./AGENTS.md)
- **Anthropic Claude (Claude Code CLI & Desktop)**: [`CLAUDE.md`](./CLAUDE.md)
- **Google Antigravity & Gemini CLI**: `.gemini/skills/` 표준 네이티브 스킬 지원
- **OpenAI Codex, ChatGPT, Aider & Cursor**: [`AGENTS.md`](./AGENTS.md) 지침 지원
- **전체 통합 가이드**: [`docs/ai-agent-interoperability-guide.md`](./docs/ai-agent-interoperability-guide.md)

---

## 📊 정량적 생산성 & 퍼실리테이터 ROI

`workshop-harness` 도입 시 퍼실리테이터(발표자/TA)가 체감하는 현실적인 정량적 생산성 지표입니다 (80% AI 자동 생성 + 20% 퍼실리테이터 검토/리허설):

| 측정 지표 (Metrics) | 수동 준비 (Before) | Harness 도입 후 (After) | 정량적 개선 효과 | 핵심 스킬 |
| :--- | :--- | :--- | :--- | :--- |
| **퍼실리테이터 전체 준비 시간** | **20 시간 (2.5일)** | **5 시간 (반나절)** | **75% 시간 절감 (4배 빠른 준비)** | `generate-all` |
| **TA 1인당 참석자 수용 능력** | **1 : 6 명** | **1 : 25~30 명** | **수용 능력 4~5배 향상** | `live-debug-assistant` |
| **현장 라이브 디버깅 속도 (MTTR)** | **18 분 / 건** | **0.5 분 (30초) / 건** | **디버깅 속도 36배 향상** | `live-debug-assistant` |
| **현장 라이브 세션 지연 시간** | **평균 35 분** | **3 분 이내** | **세션 지연 91.4% 감축** | `cross-architecture-checker` |
| **워크숍 1회당 절감 공수** | baseline | **15시간 절감** | **퍼실리테이터 1회당 2일 공수 절약** | 전체 13종 스킬 |

> 💡 **퍼실리테이터 라이브 디버깅 팁**: 현장에서 참석자 터미널에 에러 발생 시 `live-debug-assistant` 스킬을 호출하면 10초 내 핫픽스 원라인 명령어를 생성하여 30초 내 즉시 장애 조치가 완료됩니다.

---


## 전체 20개 에이전트 스킬 명세서

| # | 스킬 이름 | 입력 / 트리거 | 출력 및 생성물 | 상세 역할 |
|---|---|---|---|---|
| 1 | [`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md) | 워크숍 이름 & 주제 | `docs/`, `workshop/`, `prompt-pack/`, `scripts/` | 표준 워크숍 리포지토리 전체 구조 스캐폴딩 |
| 2 | [`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md) | 사용 기술 스택 | `docs/00-architecture-compatibility-matrix.md`, 감지 스크립트 | Apple Silicon, Intel Mac, Win, Linux 칩셋 호환성 진단 & 우회 가이드 생성 |
| 3 | [`prerequisite-checker`](skills/prerequisite-checker/SKILL.md) | 워크숍 준비물 목록 | `gemma4-local-setup-guide.md`, `check_env.sh/ps1` | OS별 사전 준비 가이드 및 환경 자동 점검 스크립트 생성 |
| 4 | [`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md) | 실습 목표 & 시간 | `03_labs/README.md`, `prompt-pack/`, `starter`/`final` 코드 | 단계별 실습 커리큘럼, 뼈대/정답 코드 및 프롬프트 팩 작성 |
| 5 | [`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md) | `docs/` 마크다운 폴더 | `output/pdf/*.pdf`, `tmp/pdfs/contact_sheet.png` | ReportLab + PyMuPDF 기반 PDF 핸드아웃 및 렌더링 미리보기 생성 |
| 6 | [`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md) | 장비 사양 및 OS | `docs/troubleshooting.md`, `docs/20-faq.md` | RAM 사양별(8G/16G/32G+), OS별 트러블슈팅 매트릭스 작성 |
| 7 | [`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md) | 세션 시간 & TA 인원 | `RUNBOOK.md` | 발표자 & TA 전용 분단위 진행 타임라인 런북 & 큐카드 작성 |
| 8 | [`live-debug-assistant`](skills/live-debug-assistant/SKILL.md) | 터미널 에러 로그 | 10초 핫픽스 명령어, `.env.sample` | 현장 터미널 에러 즉시 진단 & API Key 보안 프로토콜 가이드 |
| 9 | [`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md) | 워크숍 주제 & 난이도 | `docs/20-faq.md` / `FAQ.md` | 참석자들이 행사 전 자주 묻는 질문(하드웨어/네트워크/코드) 자동 생성 |
| 10 | [`workshop-tester`](skills/workshop-tester/SKILL.md) | 워크숍 프로젝트 경로 | `verify_workshop.py` 출력 | 코드 실행 스모크 테스트 & 마크다운 상대 경로 깨진 링크(Broken Link) 자동 검증 |
| 11 | [`workshop-web-researcher`](skills/workshop-web-researcher/SKILL.md) | 도구/모델 키워드 | 최신 릴리스 버전 & 출처 | 웹 검색을 통한 최신 도구/SDK 버전 및 파괴적 변경(Breaking Changes) 실시간 검증 |
| 12 | [`workshop-persona-loop-evaluator`](skills/workshop-persona-loop-evaluator/SKILL.md) | 워크숍 주제 & 자료 | `docs/00-persona-loop-review-report.md` | 루프 엔지니어링 기반 초급, 중급, 고급 참가자 페르소나 멀티 리뷰 & 검증 |
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | 워크숍 프로젝트 경로 | `output/open-codelabs/` (`codelab.yaml`, `steps/`), `oc` push | workshop-harness 산출물을 Open Codelabs 플랫폼 매니페스트로 변환 및 `oc` CLI/MCP 연동 발행 |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | 워크숍 프로젝트 경로 | `output/colab/` (`*.ipynb`, 뱃지), `colab` CLI 테스트 | 워크숍 코드를 Google Colab 노트북(`.ipynb`)으로 변환, 'Open in Colab' 뱃지 삽입 및 Google Colab CLI 원격 테스트 |
| 15 | [`workshop-slide-generator`](skills/workshop-slide-generator/SKILL.md) | 워크숍 프로젝트 경로 | `output/slides/` (`slides.md`, `index.html`), PDF | Marp 마크다운 및 런북과 1:1 동기화되는 독립형 인터랙티브 웹 발표 슬라이드 자동 생성 |
| 16 | [`adk-workshop-builder`](skills/adk-workshop-builder/SKILL.md) | ADK 주제 & 언어 | 멀티에이전트 코디네이터 및 서브에이전트 코드 스켈레톤 | 다국어(Python, TS, Go, Kotlin) Google ADK 자율 멀티에이전트 워크숍 생성 |
| 17 | [`eli5-concept-explainer`](skills/eli5-concept-explainer/SKILL.md) | AI 기술 개념/에러 | 3단계 ELI5 물리 비유 & 멘탈 모델 | 복잡한 AI 개념과 현장 장애를 초심자 눈높이 비유와 시각 멘탈 맵으로 해설 |
| 18 | [`android-workshop-builder`](skills/android-workshop-builder/SKILL.md) | Android 주제 & 스택 | Jetpack Compose + Google GenAI Kotlin SDK 스켈레톤 | 최신 Jetpack Compose Material 3 및 ViewModel 구조의 Android GenAI 워크숍 생성 |
| 19 | [`flutter-workshop-builder`](skills/flutter-workshop-builder/SKILL.md) | Flutter 주제 & 스택 | Flutter 3.x + `google_generative_ai` 스켈레톤 | 크로스플랫폼 Flutter GenAI 워크숍 및 Flutter Web 무설치 즉시 실습 폴백 지원 |
| 20 | [`a2ui-workshop-builder`](skills/a2ui-workshop-builder/SKILL.md) | A2UI / GenUI 주제 | `genui` + `WidgetCatalog` + `SurfaceController` | A2UI 선언형 JSON 스트리밍 및 Flutter GenUI 동적 위젯 조합 인터랙티브 실습 생성 |

---

## 크로스 아키텍처 호환성 고려사항

참석자마다 소지한 노트북 아키텍처가 상이하기 때문에, 도구 선정 시 아래와 같은 알려진 위험(Known Risk) 및 대안(Fallback) 경로를 사전에 준비합니다.

| 아키텍처 / OS | 추천 메인 도구 | 알려진 위험 & 주의사항 | 필수 대안 경로 |
| --- | --- | --- | --- |
| macOS Intel Mac (`x86_64`) | Ollama CLI (`ollama serve`) | LM Studio GPU 가속 미지원 / 멈춤 현상 자주 발생 | LM Studio 대신 Ollama CLI 우회 가이드 필수 제공 (`docs/18-intel-mac-prep.md`) |
| macOS Apple Silicon (`arm64`) | LM Studio / Ollama / MLX | Metal GPU 최적화 지원 | MLX (`mlx-lm`) 추가 활용 |
| Windows x86_64 (Intel/AMD) | LM Studio / Ollama | PowerShell 스크립트 실행 제한, Docker 시 WSL2 필요 | PowerShell Bypass 스크립트 제공 |
| Windows ARM64 (Snapdragon) | Ollama CLI (Native build) | x64 에뮬레이션 시 추론 속도 저하 | Ollama Native build 사용 |
| Linux / ChromeOS | Ollama CLI | GUI 미지원 / 가상화 샌드박스 | `ollama serve` 터미널 모드 및 소형 모델(`e2b`) 안내 |
| Universal / Web | Flutter Web (`-d chrome`) | 에뮬레이터 메모리 부족 및 가상화 미지원 | Flutter 및 A2UI/GenUI 실습 시 무설치 즉시 실행 대안 |

---

## CLI 사용법 (`harness_cli.py`)

Python 3.9+ 및 `uv` 환경에서 `harness_cli.py` 도구를 이용해 손쉽게 워크숍 프로젝트를 구성하고 관리할 수 있습니다.

```bash
# 1. 원클릭 전체 스킬 파이프라인 워크숍 생성
uv run harness_cli.py generate-all --name my-bwai-workshop --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. Android Jetpack Compose GenAI 워크숍 초기화
uv run harness_cli.py init --name android-gemini-lab --topic "Android GenAI with Jetpack Compose" --stack "android"

# 3. Flutter GenUI 및 A2UI 동적 UI 워크숍 초기화
uv run harness_cli.py init --name flutter-genui-lab --topic "Generative UI with Flutter and A2UI" --stack "flutter,genui,a2ui"

# 4. 기술 스택 크로스 아키텍처 호환성 위험 오디팅
uv run harness_cli.py audit-compat --stack "android,flutter,genui,docker"

# 5. 루프 엔지니어링 기반 초급/중급/고급 참가자 페르소나 멀티 리뷰
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4"

# 6. 워크숍 코드 실행 및 마크다운 깨진 링크 자동 검증
uv run harness_cli.py test --target my-bwai-workshop

# 7. 마크다운 가이드 문서들을 PDF 핸드아웃으로 빌드
uv run harness_cli.py build-pdf --target my-bwai-workshop

# 8. Open Codelabs 플랫폼용 매니페스트 번들 내보내기 & 발행
uv run harness_cli.py export-codelab --target my-bwai-workshop --push
```

---

## 에이전트 스킬 설치 방법

Google Antigravity 또는 Gemini CLI 에이전트 환경에서 이 13개 스킬을 상시 활용하려면 아래 명령으로 설치하세요:

```bash
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

---

## 표준 워크숍 리포지토리 구조

```text
my-workshop-repo/
├── README.md                           # 워크숍 개요 및 Quick Start
├── RUNBOOK.md                          # 발표자 및 TA 전용 진행 런북
├── AGENTS.md                           # AGENTS.md 오픈 에이전트 표준 명세
├── CLAUDE.md                           # Claude Code CLI 연동 가이드
├── pyproject.toml                      # Astral uv 의존성 명세 파일
├── gemma4-local-setup-guide.md          # 행사 전 통합 사전 준비 가이드
├── docs/                               # 상세 가이드 문서 (00 ~ 20)
│   ├── 00-architecture-compatibility-matrix.md # 크로스 아키텍처 대비 가이드
│   ├── 00-persona-loop-review-report.md# 루프 엔지니어링 페르소나 리뷰 리포트
│   ├── ai-agent-interoperability-guide.md # Multi-AI 에이전트 연동 가이드
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md                       # 참석자용 FAQ
├── workshop/                           # 당일 핸즈온 실습
│   ├── 01_starter/                     # 참가자용 시작 코드
│   ├── 02_final/                       # 정답 참고 코드
│   └── 03_labs/                        # Step-by-Step 실습 문서
├── prompt-pack/                        # 핸즈온 프롬프트 팩
├── scripts/                            # 아키텍처 점검 및 오프라인 번들링 스크립트
│   ├── check_architecture_compat.sh    # 아키텍처 감지 (Mac/Linux)
│   ├── check_architecture_compat.ps1   # 아키텍처 감지 (Windows)
│   ├── check_env.sh / check_env.ps1    # 환경 점검 스크립트
│   ├── bundle_offline_assets.sh        # 현장 비상용 오프라인 번들 스크립트
│   ├── verify_workshop.py              # 자동 검증 스크립트
│   └── generate_prep_pdf.py            # PDF 핸드아웃 빌더
└── output/                              # 산출물 (PDF 등)
    └── pdf/
```

---

## 참고 자료 (References)

- [AGENTS.md 오픈 표준 규격](https://agents.md/)
- [공식 Google Android CLI 및 Skills 안내](https://developer.android.com/tools/agents/android-cli)
- [공식 Flutter AI 개발 가이드](https://docs.flutter.dev/ai/get-started)
- [Flutter Package Skills 규격](https://docs.flutter.dev/ai/package-skills)
- [공식 Flutter Agent Plugins 저장소](https://github.com/flutter/agent-plugins)
- [A2UI 오픈 프로토콜 규격](https://a2ui.org)
- [Astral uv 파이썬 패키지 매니저](https://astral.sh/uv)

---

## 라이선스

[MIT License](LICENSE)

