---
name: hands-on-curriculum-builder
description: Builds step-by-step hands-on lab curriculum (Lab 1, Lab 2, Lab 3), starter and final code templates, prompt packs with Output Schema specifications, and enforces a mandatory references section in all generated documents.
---

# Hands-on Curriculum Builder Skill

## Purpose
Modularizes workshop content into sequential, timed hands-on labs (60 to 120 minutes total). Enforces a clean separation between starter scaffolding (`01_starter`), reference solutions (`02_final`), step-by-step lab guides (`03_labs/README.md`), and structured prompt engineering packs (`prompt-pack/README.md`).

> **Mandatory Pre-Flight Web Research Protocol**:
> Before generating any lab code or instructions, the agent **MUST** perform live web searches (`search_web` / `workshop-web-researcher`) to verify the latest SDK syntax (e.g. `google-genai >= 2.30.1` SDK vs legacy `google-generativeai`, current LangChain/Ollama versions, latest model tags like `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.8-live`, `gemma4`) and ensure zero deprecated code.

---

## Lab Architecture & Timing Rules

A standard technical workshop curriculum is divided into 3 progressive lab phases:

### Standard LLM / RAG Track
```mermaid
flowchart TD
    Lab1["Lab 01: Setup & API Sanity Check (15-20 min)<br>Verify environment, connect to local Ollama / Cloud Gemini API"]
    Lab2["Lab 02: Structured Output & Schema Parsing (25-30 min)<br>Implement Pydantic / JSON Schema type-safe model responses"]
    Lab3["Lab 03: RAG / Agent Multi-step Pipeline (35-40 min)<br>Connect Vector Search or Tool Calling for end-to-end output"]

    Lab1 --> Lab2 --> Lab3
```

### Gemini Live Real-time Streaming & Multimodal Track (Python / JS / Flutter)
```mermaid
flowchart TD
    Live1["Lab 01: WebSocket Connection & Ephemeral Tokens (15-20 min)<br>Connect to gemini-3.8-live via LiveSession / SDK"]
    Live2["Lab 02: Real-time Bidirectional Audio & VAD Handling (30-35 min)<br>Stream 16kHz PCM audio chunks and handle model speech playback<br>(Flutter: gemini_live | Python: google-genai | JS: @google/genai)"]
    Live3["Lab 03: Real-time Multimodal (Camera/Video) & Live Tool Calling (30-35 min)<br>Stream JPEG video frames and execute non-blocking real-time function calling"]

    Live1 --> Live2 --> Live3
```

---

## Starter vs Final Code Separation Guidelines

### 1. `workshop/01_starter/`
- Contains complete project configuration files (`pyproject.toml`, `requirements.txt`, `.env.sample`).
- Contains functional entry points (`main.py` / `index.js` / `main.go`) with clearly marked exercise blocks.
- **Exercise Marker Protocol**:
  ```python
  # =========================================================================
  # TODO: [Lab 02 - Exercise] Implement Structured Output Parser
  # Hint: Use Pydantic BaseModel or Gemini response_schema parameter
  # =========================================================================
  def parse_response(raw_text: str):
      # Pass or placeholder implementation for attendees to complete
      raise NotImplementedError("Lab 02 exercise not yet completed!")
  ```

### 2. `workshop/02_final/`
- Contains 100% completed, verified reference implementation.
- All `TODO:` blocks are fully solved, formatted, and tested.
- Must execute cleanly out-of-the-box via `uv run python main.py` or `./run.sh`.

---

## Prompt Pack & Schema Specifications (`prompt-pack/README.md`)

When generating prompt packs for LLM/RAG workshops:
1. Include explicit System Prompts with role definitions and output formatting rules.
2. Provide JSON Schema / Pydantic models for structured output testing.
3. Provide example inputs and expected model output pairs for attendee verification.

---

## Mandatory References Protocol

Every generated lab document, guide, or README **must include a `## References` section** at the bottom listing authoritative sources:

```markdown
## References

- **Official API Documentation**: [Google Gemini API Docs](https://ai.google.dev/docs)
- **Ollama API Specification**: [Ollama GitHub Documentation](https://github.com/ollama/ollama/tree/main/docs)
- **Astral uv Package Manager**: [Astral uv Docs](https://docs.astral.sh/uv/)
- **Workshop Repository**: [Build with AI Harness](https://github.com/JAICHANGPARK/workshop-harness)
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
