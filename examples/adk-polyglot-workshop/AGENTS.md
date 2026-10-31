# Agent Instructions, Developer Terminology & Typography Rules for adk-polyglot-workshop

> Workshop Example: **adk-polyglot-workshop**
> Primary Cloud Model: `gemini-3.8-flash` | Flagship Reasoning: `gemini-4-argon` | Local Model: `gemma4:e4b`

## Mandatory Rules for AI Coding Agents

1. **Developer-Friendly Terminology & Bilingual Technical Term Notation (영어 원문 병기 & 직역 금지)**:
   - When authoring or localizing documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** into Korean (KR), Japanese (JA), or Chinese (ZH), **NEVER perform awkward literal / word-for-word machine translations**.
   - **Always use real-world developer terminology AND include the original English technical term alongside it in parentheses (`개발자 친화적 용어 (English Original)`)**:
     - Examples: **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**.
     - Prohibited literal translations: never write awkward literal phrases such as "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기", or "기억 장치 넘침".
   - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in their exact English form (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments using developer-friendly terminology with English terms in parentheses.

2. **Typography Rule (No Em Dash in Markdown or Documentation)**:
   - **NEVER generate em dash characters (`\u2014`)** in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks.
   - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
   - Run `python3 scripts/verify_workshop.py .` to verify zero forbidden em dashes or awkward literal translations exist.

3. **No Emojis in Documentation by Default**:
   - Do not include emojis in generated documentation, slide decks, setup guides, or runbooks unless explicitly requested.

4. **2026 Frontier Model & SDK Currency**:
   - Use `google-genai >= 2.30.1` (`from google import genai`) and 2026 model tags (`gemini-3.8-flash`, `gemini-4-argon`, `gemma4:e4b`).
   - Never use deprecated `google-generativeai` or retired `gemini-1.5-*` / `gemini-2.0-*` / `gemini-2.5-*` tags.

## References
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
