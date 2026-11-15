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

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
