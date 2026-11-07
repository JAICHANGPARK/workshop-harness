---
name: workshop-runbook-generator
description: Generates a minute-by-minute facilitator and TA timeline runbook (RUNBOOK.md), including opening scripts, slide sync markers, TA response time rules, and progress checkpoint curl commands.
---

# Workshop Runbook Generator Skill

## Purpose
Generates `RUNBOOK.md` at the repository root, a minute-by-minute execution playbook for workshop facilitators and Teaching Assistants (TAs). Ensures the live session runs smoothly, stays on schedule, and provides explicit troubleshooting escalation protocols when attendees hit roadblocks.

---

## Runbook Structure & Timeline Matrix

### Phase 1: Pre-Session Setup (T-60 to T-0 min)
- **T-60 min**: Test venue WiFi speed and verify local LLM port connectivity (`curl http://localhost:11434/api/version`).
- **T-30 min**: Display opening slide with repository URL, WiFi SSID/Password, and prerequisite check script (`./scripts/check_env.sh`).
- **T-10 min**: Verify TA assignments and open live debug chat channel.

### Phase 2: Live Session Execution (T+0 to T+120 min)

| Time Marker | Facilitator Action & Speaker Script | TA Focus & Intervention | Progress Checkpoint Flag |
|---|---|---|---|
| **T+00 - T+10** | **Opening & Logistics**: "Welcome! Please clone the repo and run `check_env.sh`." | Assist attendees with terminal navigation & API keys. | `check_env.sh` returns `[OK]` |
| **T+10 - T+30** | **Lab 01**: Basic integration & Hello World model call. | Help resolve port 11434 / 1234 connection errors. | `curl http://localhost:11434/api/tags` 200 OK |
| **T+30 - T+65** | **Lab 02**: Structured Output & Pydantic schema parsing. | Assist with JSON parsing and schema validation errors. | `uv run python main.py` outputs valid JSON |
| **T+65 - T+105** | **Lab 03**: Agent / RAG pipeline completion. | Debug vector retrieval & prompt formatting. | End-to-end pipeline run succeeds |
| **T+105 - T+120**| **Wrap-up & Q&A**: Survey link, GitHub star callout, next steps. | Collect attendee feedback & log unresolved edge cases. | Survey submissions |

---

## Operational TA Rules & Escalation Protocols

1. **2-Minute Rule**: TAs must limit individual attendee debugging to **2 minutes**. If unresolved, guide attendee to switch to the reference code (`02_final`) to stay on schedule.
2. **3-Attendee Cluster Escalation Rule**: If 3 or more attendees hit the identical error simultaneously, the TA notifies the facilitator to pause and address the issue on the main stage screen.
3. **Backup Plan Trigger (Network Failure)**:
   - *Trigger*: Venue WiFi drops or experiences severe latency.
   - *Action*: Facilitator announces switch from Cloud Gemini API to local Ollama runtime (`gemma4:e2b`) pre-bundled in offline assets.

---

## Output Artifact Specifications

- **File Path**: `RUNBOOK.md` at repository root.

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
