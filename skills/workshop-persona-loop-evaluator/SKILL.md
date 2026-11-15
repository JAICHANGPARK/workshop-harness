---
name: workshop-persona-loop-evaluator
description: Evaluates and audits workshop curriculum, lab guides, starter/final code, and setup documents through 4 distinct attendee reviewer personas (Non-Coder, Novice, Intermediate, Senior Engineer). Generates a multi-persona evaluation report at docs/00-persona-loop-review-report.md using Loop Engineering.
---

# Workshop Persona Loop Evaluator Skill

## Purpose
Applies **Loop Engineering** and multi-persona simulation to evaluate workshop materials before a live session. The agent assumes 4 distinct attendee reviewer roles to identify difficulty mismatches, missing prerequisites, vague instructions, security risks, and architecture flaws.

---

## The 4 Attendee Reviewer Personas

### 1. Non-Coder / Complete Beginner Persona (Non-Coder)
- **Profile**: Product managers, designers, non-technical founders, marketers, or beginners with zero programming/terminal background.
- **Review Lens**:
  - Are terminal commands 100% copy-paste ready without assumed shell knowledge?
  - Are visual GUI steps (e.g., VS Code extension installation, clicking buttons) included?
  - Is technical jargon (e.g., `virtualenv`, `npm`, `CLI`, `API key`, `localhost`) explained in plain language?
  - Would this attendee get stuck at step 1 due to missing OS prep?
- **Key Metric**: *Zero friction to first successful run (No terminal blockers).*

### 2. Novice / Beginner Developer Persona (Novice)
- **Profile**: Junior developers, students, or hobbyists with basic Python/JS syntax knowledge who struggle with environment variables, virtualenvs, pathing, and package conflicts.
- **Review Lens**:
  - Are virtual environment (`venv` / `uv`) creation and package installation explicit?
  - Is the delta between `01_starter` and `02_final` code clear?
  - Are common runtime errors (e.g., `ModuleNotFoundError`, `APIKeyError`, `PortInUse`) covered with 10-second hotfix instructions?
  - Are API keys safely loaded via `.env` instead of hardcoded strings?
- **Key Metric**: *Clear starter-to-final path and instant error recovery.*

### 3. Intermediate Developer Persona (Intermediate)
- **Profile**: Experienced full-stack or backend developers familiar with REST APIs and basic LLM prompts, seeking non-trivial practical application.
- **Review Lens**:
  - Does the curriculum go beyond basic "Hello World" into real-world patterns (RAG, structured output, function calling)?
  - Is the code modular, readable, and idiomatic?
  - Are stretch goals / bonus tasks provided for attendees who finish labs quickly?
  - Are trade-offs (e.g., local Gemma vs Cloud Gemini) clearly explained?
- **Key Metric**: *High engagement and practical architectural depth.*

### 4. Advanced / Senior Engineer Persona (Advanced / Senior)
- **Profile**: Senior software engineers, tech leads, or AI/ML architects evaluating technical rigor, production readiness, and edge case resilience.
- **Review Lens**:
  - Is the architecture scalable, secure, and production-ready (no security vulnerabilities, proper error handling, CORS/rate limit considerations)?
  - Are prompt engineering templates, RAG vector retrieval strategies, and chunking parameters optimized?
  - Are cross-platform hardware risks (Apple Silicon Metal vs Intel Mac vs Windows WSL2) addressed?
  - Is memory overhead and GPU/CPU resource consumption documented?
- **Key Metric**: *Production-grade technical accuracy, security, and performance.*

---

## 4-Persona Evaluation Loop Workflow

When invoking this skill, the agent executes a 4-phase audit loop:

```text
[Phase 1: Non-Coder Audit]     -> Evaluate CLI commands, jargon definitions, GUI steps
[Phase 2: Novice Audit]        -> Evaluate venv setup, starter-to-final diff, hotfix FAQ
[Phase 3: Intermediate Audit]  -> Evaluate code modularity, API depth, stretch goals
[Phase 4: Senior Audit]        -> Evaluate architecture, security, performance, hardware risks
```

---

## Review Scoring Rubric (1 - 5 Points)

Each persona evaluates the workshop across 5 core dimensions:

1. **Clarity & Setup Guidance**: Are instructions unambiguous?
2. **Pacing & Timing**: Can labs be completed within allotted minutes?
3. **Technical Rigor & Code Quality**: Is code clean, modular, and idiomatic?
4. **Safety & Security**: Are API keys protected and fallback guides provided?
5. **Engagement & Value**: Is the outcome rewarding for this persona?

---

## Output Artifact

Generates `docs/00-persona-loop-review-report.md`:

```markdown
# Multi-Persona Loop Engineering Review Report

## Executive Summary & Overall Fit
- Overall Workshop Readiness Score: 4.6 / 5.0

## Persona Breakdown & Findings

### 1. Non-Coder Review (Non-Coder)
- Score: 4.5 / 5.0
- Positives: Visual setup guide included.
- Blockers Identified: `uv` command missing explanation in Lab 01.
- Action Item: Add terminal copy button & plain-text explanation.

### 2. Novice Developer Review (Novice)
- Score: 4.8 / 5.0
- Action Item: Add `.env.sample` troubleshooting note.

### 3. Intermediate Developer Review (Intermediate)
- Score: 4.7 / 5.0
- Action Item: Add Lab 03 stretch challenge for custom RAG prompt tuning.

### 4. Senior Engineer Review (Advanced / Senior)
- Score: 4.4 / 5.0
- Action Item: Note Intel Mac GPU acceleration limitation & Ollama fallback.

## Recommended Action Items Prior to Event
1. [High] Fix missing `.env.sample` reference in Lab 01.
2. [Medium] Add stretch challenge to Lab 03 for fast completers.
```

---

## CLI Integration

Execute the multi-persona review loop via `harness_cli.py`:

```bash
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4"
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
