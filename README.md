# 🚀 Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)

**`workshop-harness`**는 **Build with AI (BWAI)**, DevFest, 커뮤니티 세션, 기술 실습 등의 워크숍을 준비하는 주최자와 발표자를 위한 **AI 에이전트 하네스 & 스킬(Skills) 모음 및 CLI 자동화 툴킷**입니다.

Build with AI Seoul (`2026-bwai-seoul`), Golang Korea (`2026-bwai-golang-korea`), Mongo (`2026-bwai-mongo`), Cloud Pangyo (`2026-bwai-cloud-pangyo`) 프로젝트 등 실제 다수의 현장 워크숍 운영 경험에서 검증된 구조와 노하우를 표준화하였습니다.

---

## 💡 주요 기능 & 포함된 6개 에이전트 스킬 (Agent Skills)

AI 코딩 에이전트(Google Antigravity, Gemini CLI 등)가 사전 준비 자료, 크로스 아키텍처 점검, 실습 코드, 프롬프트 팩, PDF 핸드아웃 생성을 자동 수행할 수 있도록 6개의 전용 스킬을 제공합니다.

| 스킬 이름 | 역할 & 설명 | 주요 산출물 |
| --- | --- | --- |
| **[`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md)** | 표준 워크숍 리포지토리 디렉토리 및 파일 스캐폴딩 | `docs/`, `workshop/` (`starter`, `final`, `labs`), `scripts/` |
| **[`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md)** | **노트북 아키텍처(Apple Silicon, Intel Mac, Win, Linux) 호환성 진단 & 대체 경로(Fallback) 구성** | `docs/00-architecture-compatibility-matrix.md`, 점검 스크립트 |
| **[`prerequisite-checker`](skills/prerequisite-checker/SKILL.md)** | OS별 사전 준비 가이드 및 환경 점검 자동화 스크립트 생성 | `gemma4-local-setup-guide.md`, `check_env.sh`, `check_env.ps1` |
| **[`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md)** | 단계별 실습 가이드, `starter` vs `final` 코드, 프롬프트 팩 구성 | `03_labs/README.md`, `prompt-pack/`, starter & final 프로젝트 |
| **[`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md)** | 마크다운 가이드를 출판 품질의 PDF 핸드아웃 및 미리보기(Contact Sheet)로 변환 | `scripts/generate_prep_pdf.py`, `output/pdf/*.pdf`, 미리보기 이미지 |
| **[`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md)** | 사양별(8G/16G/32G RAM), OS별 트러블슈팅 매트릭스 & FAQ 작성 | `docs/troubleshooting.md`, `docs/20-faq.md` |

---

## 💻 크로스 아키텍처 호환성 고려 (Cross-Architecture Matrix)

참석자마다 소지한 노트북 아키텍처가 상이하기 때문에, 도구 선정 시 아래와 같은 알려진 위험(Known Risk) 및 대안(Fallback) 경로를 사전에 준비합니다.

| 아키텍처 / OS | 추천 메인 도구 | 알려진 위험 & 주의사항 (Known Risk) | 필수 대안 경로 (Fallback) |
| --- | --- | --- | --- |
| **macOS Intel Mac** (`x86_64`) | **Ollama CLI** (`ollama serve`) | 🚨 **LM Studio GPU 가속 미지원 / 멈춤 현상 자주 발생** | **LM Studio 대신 Ollama CLI 우회 가이드 필수 제공** (`docs/18-intel-mac-prep.md`) |
| **macOS Apple Silicon** (`arm64`) | LM Studio / Ollama / MLX | Metal GPU 최적화 지원 | MLX (`mlx-lm`) 추가 활용 |
| **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell 스크립트 실행 제한, Docker 시 WSL2 필요 | PowerShell Bypass 스크립트 제공 |
| **Windows ARM64** (Snapdragon) | Ollama CLI (Native build) | x64 에뮬레이션 시 추론 속도 저하 | Ollama Native build 사용 |
| **Linux / ChromeOS** | Ollama CLI | GUI 미지원 / 가상화 샌드박스 | `ollama serve` 터미널 모드 및 소형 모델(`e2b`) 안내 |

---

## 🛠️ CLI 사용법 (`harness_cli.py`)

Python 3.9+ 환경에서 `harness_cli.py` 도구를 이용해 손쉽게 워크숍 프로젝트를 구성하고 관리할 수 있습니다.

```bash
# 1. 새 워크숍 프로젝트 생성 (기본 구조 및 아키텍처 매트릭스 자동 스캐폴딩)
python3 harness_cli.py init --name my-bwai-workshop --topic "Local RAG with Gemma 4"

# 2. 기술 스택 크로스 아키텍처 호환성 위험 오디팅
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. 마크다운 가이드 문서들을 PDF 핸드아웃으로 빌드
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## 📦 에이전트 스킬 설치 (`install_skills.sh`)

Google Antigravity 또는 Gemini CLI 에이전트 환경에서 이 6개 스킬을 상시 활용하려면 아래 명령으로 설치하세요:

```bash
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

설치 후 에이전트에게 다음과 같이 자연어로 요청할 수 있습니다:
- *"cross-architecture-checker 스킬로 Intel Mac과 Windows 참가자가 겪을 호환성 리스크와 우회 가이드를 만들어줘."*
- *"workshop-scaffolder 스킬로 Gemma 4 핸즈온 워크숍 저장소 구조를 만들어줘."*
- *"pdf-handout-generator 스킬로 docs 문서들을 PDF 핸드아웃으로 만들어줘."*

---

## 📁 표준 워크숍 리포지토리 구조

`workshop-harness`로 생성되는 워크숍 리포지토리 구조:

```text
my-workshop-repo/
├── README.md                           # 워크숍 개요 및 Quick Start
├── gemma4-local-setup-guide.md          # 행사 전 통합 사전 준비 가이드
├── docs/                               # 상세 가이드 문서 (00 ~ 20)
│   ├── 00-architecture-compatibility-matrix.md # 크로스 아키텍처 대비 가이드
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md
├── workshop/                           # 당일 핸즈온 실습
│   ├── 01_starter/                     # 참가자용 시작 코드
│   ├── 02_final/                       # 정답 참고 코드
│   └── 03_labs/                        # Step-by-Step 실습 문서
├── prompt-pack/                        # 핸즈온 프롬프트 팩
├── scripts/                            # 아키텍처 점검 및 빌드 스크립트
│   ├── check_architecture_compat.sh    # 아키텍처 감지 (Mac/Linux)
│   ├── check_architecture_compat.ps1   # 아키텍처 감지 (Windows)
│   ├── check_env.sh / check_env.ps1    # 환경 점검 스크립트
│   └── generate_prep_pdf.py            # PDF 핸드아웃 빌더
└── output/                              # 산출물 (PDF 등)
    └── pdf/
```

---

## 📜 License

[MIT License](LICENSE)
