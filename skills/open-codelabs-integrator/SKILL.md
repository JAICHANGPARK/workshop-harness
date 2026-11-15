---
name: open-codelabs-integrator
description: Integrates workshop content created by workshop-harness with Open Codelabs platform. Automates converting workshop labs into Open Codelabs manifest format (codelab.yaml), generating step-by-step markdown, mapping starter/final code workspaces, attaching prerequisites & materials, and publishing via oc CLI, REST API, or stdio MCP server (oc mcp serve).
---

# Open Codelabs Integrator Skill

## Purpose

Seamlessly bridges `workshop-harness` generated workshops with the **Open Codelabs** interactive hands-on platform (`https://github.com/JAICHANGPARK/open-codelabs`). It transforms static workshop markdown docs, lab instructions, and code scaffolds into structured Open Codelabs manifests (`codelab.yaml`), enabling facilitators to publish codelabs, manage code-server workspaces, issue quizzes, and run live interactive sessions with zero manual copy-pasting.

---

## 🚀 Key Integration Features

1. **Manifest Auto-Generation (`codelab.yaml`)**:
   - Parses `workshop/03_labs/README.md` and `SETUP_GUIDE.md` into standard Open Codelabs manifest specs (`version: 1`).
   - Splits monolithic lab documentation into sequential step files (`steps/step_01.md`, `steps/step_02.md`, etc.).
   - Maps `docs/02-prerequisites.md` and repository links as Open Codelabs materials.

2. **One-Click Publishing (`oc codelab push`)**:
   - Uses the `oc` CLI to push published manifests, guide markdowns, steps, quizzes, and materials directly to a local or remote Open Codelabs backend (`Axum / SQLite / Postgres / Firebase`).

3. **Agentic MCP Interoperability (`oc mcp serve`)**:
   - Leverages `open-codelabs` stdio MCP server to allow AI Agents (Antigravity, Claude, Codex, Cursor) to dynamically query connection status, create/update codelabs, inspect participant progress, triage help queues, and manage code-server workspace snapshots.

---

## 📁 Open Codelabs Bundle Directory Structure

When exported, `workshop-harness` produces the following Open Codelabs bundle inside `output/open-codelabs/`:

```text
output/open-codelabs/
├── codelab.yaml           # Master manifest file (version 1)
├── guide.md               # Preparation & Setup Guide
├── steps/
│   ├── step_01.md         # Lab 01: Environment Check & Hello World
│   ├── step_02.md         # Lab 02: Structured Output & Core Logic
│   └── step_03.md         # Lab 03: Complete Pipeline & Verification
└── materials/             # Extra assets & link references
```

---

## 📄 `codelab.yaml` Manifest Specification

```yaml
version: 1
title: "Local RAG with Gemma 4 & Ollama"
description: "Hands-on workshop building a local retrieval-augmented generation pipeline."
author: "Workshop Facilitator"
is_public: true
quiz_enabled: false
require_quiz: false
require_feedback: true
require_submission: false
guide_markdown: "guide.md"
steps:
  - title: "Lab 01: Environment Verification & Basic API"
    file: "steps/step_01.md"
  - title: "Lab 02: Structured Output & JSON Schema"
    file: "steps/step_02.md"
  - title: "Lab 03: Full RAG Pipeline & Verification"
    file: "steps/step_03.md"
materials:
  - title: "Starter Code Repository"
    type: "link"
    url: "https://github.com/JAICHANGPARK/workshop-harness"
```

---

## 🛠 `oc` CLI & Integration Workflows

### 1. Generate Open Codelabs Bundle
From your `workshop-harness` project root:
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop
```

### 2. Publish Bundle to Open Codelabs
```bash
# Set target server profile or URL
oc connect use --name local
oc auth login

# Push manifest bundle directly
oc codelab push --manifest output/open-codelabs/codelab.yaml
```

### 3. One-Click Export & Push
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop --push
```

### 4. Connect AI Agent via MCP (`oc mcp serve`)
Start Open Codelabs MCP server for agentic automation:
```bash
oc mcp serve
```
Available Agent Tools:
- `create_codelab`, `replace_codelab_steps`, `push_codelab`
- `list_materials`, `add_material`
- `list_attendees`, `list_help_requests`, `resolve_help_request`
- `get_workspace_info`, `list_workspace_branches`

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
