---
name: workshop-scaffolder
description: Scaffolds a standard workshop repository structure including docs/, workshop/, prompt-pack/, scripts/, and output/ directories with pre-configured templates and automation scripts.
---

# Workshop Scaffolder Skill

## Purpose
Generates a standardized, production-grade workshop repository structure in one step. Ensures all necessary documentation templates, lab subdirectories, starter/final code skeletons, environment scripts, and build artifacts are properly created with correct file permissions (`chmod +x`).

---

## Standard Repository Layout Specs

```text
<project-name>/
├── README.md                           # Main workshop overview & quick start guide
├── RUNBOOK.md                          # Facilitator & TA execution runbook
├── AGENTS.md                           # AI Agent context specification
├── gemma4-local-setup-guide.md          # Unified attendee preparation guide
├── pyproject.toml                       # Astral uv dependency declaration
├── .env.sample                          # Sample environment file template
├── docs/                               # Detailed technical documentation & reports
│   ├── 00-architecture-compatibility-matrix.md
│   ├── 00-persona-loop-review-report.md
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md
├── workshop/                           # Day-of hands-on lab code
│   ├── 01_starter/                     # Starter code scaffold for attendees
│   │   ├── main.py
│   │   ├── run.sh
│   │   └── run.ps1
│   ├── 02_final/                       # Completed reference solution
│   │   ├── main.py
│   │   ├── run.sh
│   │   └── run.ps1
│   └── 03_labs/                        # Step-by-step lab guides
│       └── README.md
├── prompt-pack/                        # Prompt engineering packs & schemas
│   └── README.md
├── scripts/                            # Cross-architecture checks & verification scripts
│   ├── check_env.sh / check_env.ps1
│   ├── check_architecture_compat.sh / .ps1
│   ├── bundle_offline_assets.sh
│   ├── verify_workshop.py
│   ├── export_open_codelabs.py
│   └── generate_prep_pdf.py
└── output/                             # Build & publication output artifacts
    ├── pdf/                            # Generated PDF handouts
    └── open-codelabs/                  # Open Codelabs bundles (codelab.yaml)
```

---

## Scaffolding Workflow & Execution Rules

When scaffolding a new workshop project:
1. **Directory Creation**: Recursively create `docs/`, `workshop/01_starter/`, `workshop/02_final/`, `workshop/03_labs/`, `prompt-pack/`, `scripts/`, `output/pdf/`, and `tmp/pdfs/`.
2. **Template Copying**: Copy master templates from `templates/doc-templates/` and `templates/script-templates/`.
3. **Executable Bit Enforcement**: Mark all `.sh` and `.py` scripts as executable (`chmod 755`).
4. **Environment Initialization**: Write `.env.sample` containing placeholder keys (`GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`).
5. **Multi-Language Starter Scaffolding (Python, TypeScript, Go, Kotlin)**:
   - **Python**: Generates `pyproject.toml` and `main.py` entrypoints.
   - **TypeScript / JavaScript**: Generates `package.json` with `@google/genai` dependencies and `src/index.ts`.
   - **Go (Golang)**: Generates `go.mod` and `main.go`.
   - **Kotlin / Java**: Generates `build.gradle.kts` and `src/main/kotlin/Main.kt`.

---

## CLI Command Integration

Scaffold a new workshop using `harness_cli.py`:

```bash
# Initialize standalone scaffold
uv run harness_cli.py init --name "my-bwai-workshop" --topic "Local RAG with Gemma 4"

# One-Click Full Orchestration across all skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## Typography, Developer Terminology & Bilingual Notation Rules

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
