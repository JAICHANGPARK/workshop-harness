---
name: workshop-scaffolder
description: BWAI 및 핸즈온 워크숍 프로젝트의 표준 저장소 구조(docs, workshop/starter, final, labs, scripts, prompt-pack 등)를 자동으로 생성 및 초기화하는 스킬
---

# Workshop Scaffolder Skill

## 📌 목적
Build with AI(BWAI), DevFest, 커뮤니티 세션 등의 핸즈온 워크숍을 신속하게 시작할 수 있도록, 검증된 최적의 리포지토리 표준 구조를 스캐폴딩합니다.

## 📁 생성되는 디렉토리 및 파일 구조

```text
<workshop-name>/
├── README.md                           # 워크숍 개요, 타임테이블, Quick Start
├── gemma4-local-setup-guide.md          # 통합 사전 준비 가이드 (가장 먼저 볼 문서)
├── AGENTS.md                           # LLM/에이전트 규칙 및 프로젝트 가이드라인
├── docs/                               # 주제별/OS별 상세 가이드 (01~20)
│   ├── 01-hardware-and-model-selection.md
│   ├── 02-windows-guide.md
│   ├── 03-memory-based-model-selection.md
│   ├── 16-uv-setup.md
│   ├── 19-troubleshooting-and-final-check.md
│   └── 20-faq.md
├── workshop/                           # 당일 핸즈온 실습
│   ├── 01_starter/                     # 참가자용 초기 뼈대 코드
│   │   ├── README.md
│   │   ├── pyproject.toml / pubspec.yaml / go.mod
│   │   └── run.sh / run.ps1
│   ├── 02_final/                       # 참고/정답 완성 코드
│   │   ├── README.md
│   │   ├── pyproject.toml / pubspec.yaml / go.mod
│   │   └── run.sh / run.ps1
│   └── 03_labs/                        # Step-by-Step 실습 문서
│       └── README.md
├── prompt-pack/                        # 핸즈온용 프롬프트 모음
│   ├── README.md
│   ├── 01-system-prompts.md
│   └── 02-output-schema.md
├── scripts/                            # 하네스 스크립트
│   ├── check_env.sh                    # 환경 점검 (Linux/macOS)
│   ├── check_env.ps1                   # 환경 점검 (Windows)
│   └── generate_hands_on_prep_pdf.py   # PDF 핸드아웃 자동 생성
├── output/                             # 빌드 출력 (PDF 등)
│   └── pdf/
└── tmp/                                # 빌드 임시 파일 (Contact Sheet)
    └── pdfs/
```

## 🛠️ 실행 방법

1. **스캐폴딩 CLI 실행**:
   `workshop-harness/harness_cli.py`를 호출하거나 스크립트를 사용합니다:
   ```bash
   python3 workshop-harness/harness_cli.py init --name "my-bwai-workshop" --topic "Local RAG with Gemma 4"
   ```

2. **구조 검증**:
   - `workshop/01_starter` 디렉토리에 참가자가 시작할 코드가 정상 준비되었는지 확인
   - `workshop/02_final` 디렉토리에 완성본 실행 코드가 동작하는지 확인
   - `docs/`에 하드웨어 사양별(8GB, 16GB, 32GB 메모리, Apple Silicon, Intel Mac, Windows) 분기 가이드가 작성되었는지 확인

## 📋 핵심 작성 가이드라인

- **독립 실행 가능성**: `workshop/01_starter`와 `02_final`은 각자 독립적으로 실행 가능한 패키지(예: `pyproject.toml`, `uv.lock` 또는 `pubspec.yaml`)를 가져야 함.
- **실행 스크립트 제공**: Cross-platform 지원을 위해 bash (`run.sh`)와 PowerShell (`run.ps1`) 실행 파일 모두 작성.
- **사전 다운로드 안내**: 현장 WiFi 마비를 방지하기 위해 1GB 이상의 모델/패키지는 반드시 행사 전 사전 다운로드 명령어를 README 상단에 명시.
