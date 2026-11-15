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
├── SETUP_GUIDE.md                       # Unified attendee preparation guide
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

## CLI & Natural Language Prompt Integration

When a user sends a natural language prompt (in Korean, English, Japanese, or Chinese) asking to create a workshop, do **not** ask the user to manually specify CLI flags (`--name`, `--stack`, `--model`). Immediately execute the zero-config prompt router so the entire workshop package (Starter/Final code, 3-stage Labs, Runbook, Setup Guide, PDF Handout, Google Colab `.ipynb`, Open Codelabs bundle, and Slide Deck) is generated in one shot:

```bash
# Zero-Config Natural Language Prompt -> Full 9-Step Workshop Generation (Gemini 4 / Claude / OpenAI / ADK / Flutter / Android auto-inferred)
uv run harness_cli.py prompt "Claude 최신 모델로 1시간짜리 멀티 에이전트 RAG 워크숍 만들어줘"
uv run harness_cli.py prompt "OpenAI GPT로 Structured Output (JSON 스키마 응답) 핸즈온 랩 만들어줘"
uv run harness_cli.py prompt "Create a 1-hour Gemini 4 Carbon & Google ADK multi-agent workshop"

# Explicit flag overrides (when needed)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
uv run harness_cli.py init --name "my-bwai-workshop" --topic "Local RAG with Gemma 4"
```

---

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
