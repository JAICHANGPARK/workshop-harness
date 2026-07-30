![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.07.30-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

---

## 개요

Workshop Harness는 Build with AI (BWAI), DevFest, 커뮤니티 세션, 기술 실습 등의 워크숍을 준비하는 주최자, 발표자, TA를 위한 AI 에이전트 하네스, 스킬(Skills) 모음 및 CLI 자동화 툴킷입니다.

다음과 같은 실제 현장 워크숍 운영 경험에서 검증된 구조와 노하우를 표준화하였습니다:
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)

---

## 원클릭 풀 오케스트레이션 (One-Click Full Orchestration)

단 한 줄의 CLI 명령어 또는 에이전트 자연어 요청만으로 12개 스킬 전체가 연쇄 발동되어 완벽한 워크숍 패키지를 원클릭으로 생성합니다:

```bash
# 12개 전체 스킬 원클릭 연속 발동 생성 명령어
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 목차

- [개요](#개요)
- [원클릭 풀 오케스트레이션](#원클릭-풀-오케스트레이션-one-click-full-orchestration)
- [전체 12개 에이전트 스킬 명세서](#전체-12개-에이전트-스킬-명세서)
- [크로스 아키텍처 호환성 고려사항](#크로스-아키텍처-호환성-고려사항)
- [CLI 사용법 (harness_cli.py)](#cli-사용법-harness_clipy)
- [에이전트 스킬 설치 방법](#에이전트-스킬-설치-방법)
- [표준 워크숍 리포지토리 구조](#표준-워크숍-리포지토리-구조)
- [라이선스](#라이선스)

---

## 전체 12개 에이전트 스킬 명세서

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

---

## CLI 사용법 (`harness_cli.py`)

Python 3.9+ 환경에서 `harness_cli.py` 도구를 이용해 손쉽게 워크숍 프로젝트를 구성하고 관리할 수 있습니다.

```bash
# 1. 12개 전체 스킬 원클릭 연속 발동 생성
python3 harness_cli.py generate-all --name my-bwai-workshop --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. 기술 스택 크로스 아키텍처 호환성 위험 오디팅
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. 루프 엔지니어링 기반 초급/중급/고급 참가자 페르소나 멀티 리뷰
python3 harness_cli.py audit-loop --topic "Local RAG with Gemma 4"

# 4. 워크숍 코드 실행 및 마크다운 깨진 링크 자동 검증
python3 harness_cli.py test --target my-bwai-workshop

# 5. 마크다운 가이드 문서들을 PDF 핸드아웃으로 빌드
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## 에이전트 스킬 설치 방법

Google Antigravity 또는 Gemini CLI 에이전트 환경에서 이 12개 스킬을 상시 활용하려면 아래 명령으로 설치하세요:

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
├── gemma4-local-setup-guide.md          # 행사 전 통합 사전 준비 가이드
├── docs/                               # 상세 가이드 문서 (00 ~ 20)
│   ├── 00-architecture-compatibility-matrix.md # 크로스 아키텍처 대비 가이드
│   ├── 00-persona-loop-review-report.md# 루프 엔지니어링 페르소나 리뷰 리포트
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

## 라이선스

[MIT License](LICENSE)
