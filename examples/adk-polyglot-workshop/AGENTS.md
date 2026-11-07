# Agent Instructions, Developer Terminology & Typography Rules for adk-polyglot-workshop

> Topic: **Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)**
> Tech Stack: `python,typescript,go,java,kotlin,adk,agents-cli` | Primary Cloud Model: `gemini-3.8-flash` | Local Model: `gemma4:e4b`

## Mandatory Rules for AI Coding Agents

1. **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
   - When authoring or localizing documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** into Korean (KR), Japanese (JA), or Chinese (ZH), **NEVER perform awkward literal / word-for-word machine translations**.
   - **For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original**:
     - Examples: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Breaking Changes (브레이킹 체인지)**.
     - Prohibited literal translations: never write awkward literal phrases such as "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", or "기억 장치 넘침".
   - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in their exact English form (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments using original English technical terms paired with developer-friendly explanations.

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
