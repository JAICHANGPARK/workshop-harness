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

## Typography, Developer Terminology & Bilingual Notation Rules

- **Developer-Friendly Terminology & English Original Notation (영어 원문 병기 & 직역 금지)**:
  - Never use awkward literal translations (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기").
  - Always use developer-friendly terminology commonly used by real-world software engineers AND include the original English technical term in parentheses (`개발자 친화적 용어 (English Original)`), such as:
    - **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**, **스모크 테스트 (Smoke Test)**, **보일러플레이트 코드 (Boilerplate Code)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
