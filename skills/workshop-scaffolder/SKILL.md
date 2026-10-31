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

- **Developer-Friendly Terminology & English Original Notation (영어 원문 병기 & 직역 금지)**:
  - Never use awkward literal translations (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기").
  - Always use developer-friendly terminology commonly used by real-world software engineers AND include the original English technical term in parentheses (`개발자 친화적 용어 (English Original)`), such as:
    - **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**, **스모크 테스트 (Smoke Test)**, **보일러플레이트 코드 (Boilerplate Code)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
