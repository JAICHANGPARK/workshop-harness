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

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Original Technical Term First, Real-World Developer Terminology & Natural Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never use awkward word-for-word literal translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
  - **Use the original English technical term first and append the developer-friendly term in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence grammar used by local software engineers**:
    - **Korean (KO)**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**. Never use awkward literals ("손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트") or double passives (`~되어집니다` -> `~됩니다`).
    - **Japanese (JA)**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never 「手で触る実験室」, 「走る本」, 「骨組みコード」, 「思考の予算」; write in natural Japanese engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」 (Never 「手把手的实验室」, 「奔跑的书」, 「骨架代码」, 「思考预算」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
