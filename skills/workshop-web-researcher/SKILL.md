---
name: workshop-web-researcher
description: Performs live web searches to verify the latest release versions and tags for tools (Ollama, LM Studio, uv, Docker) and AI models (Gemini, Gemma 4, Claude, Llama, etc.), ensuring data currency and preventing hardcoded legacy versions in generated documentation.
---

# Workshop Web Researcher Skill

## Purpose
AI model knowledge cutoffs can cause agents to reference obsolete tool versions, retired API model tags, or outdated SDK method signatures. This skill enforces a **dynamic verification protocol** that queries live web sources before generating any technical documentation or code.

---

## Dynamic Discovery Protocol

### Mandatory Verification Before Generation
Before writing any code, README, setup guide, or prompt pack that references software tools or AI models, the agent **must**:

1. **Query Official Release Sources**: Search official GitHub release notes, PyPI, npm, or vendor documentation.
2. **Compare Against Training Data**: Check if the agent's internal default matches the latest live release tag.
3. **Apply Verified Versions**: Write the verified latest release version in all code imports and setup guides.
4. **Stamp Currency Label**: Add a dynamic timestamp label at the top of generated markdown files:
   ```markdown
   > Latest tool and model release versions verified on: YYYY-MM-DD
   ```

---

## Primary Verification Lookup Table

| Target Tool / Model | Primary Official Source URL | Example Query | Latest Recommended Tags (November 2026) |
|---|---|---|---|
| **Google GenAI SDK** | `https://pypi.org/project/google-genai/` | `site:pypi.org google-genai latest SDK methods` | `google-genai>=3.0.0` (Python, default API `v1`), `@google/genai>=3.0.0` (TS/JS, Node.js 22+), `com.google.genai:google-genai:2.1.0` (Java 17+), `com.google.genai:google-genai-kotlin-android:1.8.0` (Kotlin/Android) |
| **Google Agent Development Kit (ADK)** | `https://adk.dev` | `site:adk.dev OR site:github.com/google/adk-python` | `google-adk>=2.14.0`, `@google/adk`, `google.golang.org/adk/v2`, `com.google.adk:google-adk` (`adk web`, `adk run`, `adk eval`, `adk deploy`) |
| **Google Agents CLI (`google-agents-cli`)** | `https://github.com/google/agents-cli` | `site:github.com/google/agents-cli setup eval deploy` | `google-agents-cli>=1.4.1` (`uvx google-agents-cli setup`, `npx skills add google/agents-cli`; 7 ADLC skills: `workflow`, `scaffold`, `adk-code`, `eval`, `deploy`, `publish`, `observability`) |
| **Google Gemini 4 & 3.8 Frontier/Flash API** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini-4-carbon gemini-4-hydrogen` | `gemini-4-carbon`, `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` |
| **Google Gemini Live & Audio API** | `https://ai.google.dev/gemini-api/docs/live` | `site:ai.google.dev gemini live api` | `gemini-3.8-live`, `gemini-3.8-live-extended-thinking`, `gemini-3.5-transcribe-live`, `gemini-3.5-live-translate-preview`, `gemini-3.8-flash-tts` (with Voice Remixing `POST /v1beta/voices`), `gemini-3.8-flash-lite-tts` |
| **Google Gemini Image, Video & Embedding** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini image video embedding` | `gemini-nano-banana-2.1` (`gemini-3.1-flash-image`), `gemini-3-pro-image`, `gemini-omni-1.2-flash` (GA, instead of legacy `gemini-omni-1.1-flash`), `gemini-embedding-2` (GA) |
| **Google Managed Agents** | `https://ai.google.dev/gemini-api/docs/managed-agents-quickstart` | `site:ai.google.dev antigravity deep research agent` | `antigravity-preview-09-2026`, `deep-research-preview-04-2026`, `deep-research-max-preview-04-2026` |
| **Flutter Gemini Live, GenUI & A2UI** | `https://pub.dev/packages/genui` | `site:pub.dev genui a2ui_flutter gemini_live flutter` | `genui`, `a2ui_flutter>=0.1.0`, `a2ui_core>=0.5.0`, `gemini_live`, `google_generative_ai` |
| **Anthropic Claude API & SDKs** | `https://docs.anthropic.com/en/docs/about-claude/models` | `site:docs.anthropic.com claude models release` | `claude-fable-5-2` (Nov 2026 apex), `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`; Python `anthropic>=2.8.0` / `claude-agent-sdk>=0.2.181`, TS `@anthropic-ai/sdk>=1.7.0` |
| **OpenAI Responses API & SDKs** | `https://platform.openai.com/docs/models` | `site:platform.openai.com/docs/models latest` | `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`, `gpt-image-2.6-sunburst`, `gpt-image-2.6-flare`; Python `openai>=3.50.0` / `openai-agents>=0.24.0`, TS `openai>=7.55.0` |
| **Ollama** | `https://github.com/ollama/ollama/releases` | `site:github.com/ollama/ollama releases latest` | `ollama` latest engine |
| **Gemma 4, EmbeddingGemma 2 & Specialized Gemma** | `https://ollama.com/library/gemma4` | `site:ollama.com/library gemma4 embeddinggemma-2` | Cloud: `gemma-4-31b-it`, `gemma-4-26b-a4b-it`, `gemma-4-12b-it`; Local Ollama: `gemma4:e2b`, `gemma4:e4b`, `gemma4:12b`, `gemma4:26b`, `gemma4:31b`; Multimodal Embeddings: `embeddinggemma-2` (`:740m`, `:570m`, `:440m`, `:270m`), `google/embeddinggemma-2`; Specialized: `translategemma`, `functiongemma`, `medgemma1.5`, `shieldgemma` |
| **LangChain / LangGraph** | `https://github.com/langchain-ai/langchain/releases` | `site:github.com/langchain-ai/langchain releases latest` | `langchain>=0.3`, `langgraph` |
| **LM Studio** | `https://github.com/lmstudio-ai/lms/releases` | `site:github.com/lmstudio-ai/lms releases` | `lms` CLI latest |
| **Astral uv** | `https://github.com/astral-sh/uv/releases` | `site:github.com/astral-sh/uv releases` | `uv` package manager |
| **Docker Engine** | `https://docs.docker.com/engine/release-notes/` | `docker engine release notes latest` | Latest official Docker Engine |

---

## SDK Breaking Changes & Migration Checks

When researching technical topics, verify:
1. **Google Gemini 4 & 3.8 Models (November 2026 Lineup)**:
   - **`gemini-4-carbon`** (GA Nov 2026, 1M unified context window): Flagship frontier reasoning model built for sustained agentic coding, multi-agent coordination (`root_agent`), scientific discovery, and cybersecurity defense. Supports adjustable `thinking_level` (`low`, `medium`, `high`).
   - **`gemini-4-hydrogen`** (GA Nov 2026, 1M input / up to 1M output context window): High-efficiency Gemini 4 workhorse optimized for rapid agentic execution, Search AI Mode query fan-out, everyday coding, and parallel sub-agent workers. Flat-priced across the full 1M context window and supports `thinking_level` (`low`, `medium`, `high`, `xhigh`; set `low` or `medium` on high-volume tasks to optimize output token spend).
   - **Multi-Model Orchestrator Pattern**: Pair **`gemini-4-carbon`** as the deep coordinator/architect with **`gemini-4-hydrogen`** as high-speed parallel execution workers/verifiers.
   - **`gemini-4-argon`** (1M context window): Enterprise frontier reasoning model tailored for legal/financial analysis, software engineering, and security workflows.
   - **`gemini-3.8-flash`** (1M context window): Fast, cost-effective multimodal Flash model for high-frequency everyday applications, mobile/web UI streaming, and standard loops (`gemini-3.7-flash` is deprecated). Use `gemini-3.5-flash-lite` or `gemini-3.1-flash-lite` for ultra-low-cost, high-throughput tasks.
   - **Dynamic Active Model Discovery**: Always verify active endpoints programmatically via `client.models.list()` when building dynamic model selectors.
2. **Google Gemini Live Real-time Multimodal & Audio API**:
   - Primary Live model: **`gemini-3.8-live`** for low-latency bidirectional audio/video/text streaming over WebSockets with non-blocking asynchronous function calling (`behavior: "NON_BLOCKING"`) and full-session `send_client_content`.
   - High-Reasoning Live model: **`gemini-3.8-live-extended-thinking`** for background reasoning with spoken conversational fillers (`interaction_status`: `IN_PROGRESS` vs `IDLE`).
   - Speech-to-Text & Translation: **`gemini-3.5-transcribe`**, **`gemini-3.5-transcribe-live`**, and **`gemini-3.5-live-translate-preview`** for speech-to-speech live streaming translation.
   - Expressive TTS & Voice Remixing: **`gemini-3.8-flash-tts`** and **`gemini-3.8-flash-lite-tts`** for multi-speaker dialogue, Voice Design, Voice Replication, and natural-language Voice Remixing (`POST /v1beta/voices`).
   - **Flutter / Dart SDK**: Use the pub.dev **`gemini_live`** package for zero-Firebase direct WebSocket integration or `firebase_ai` for enterprise apps.
   - **Python SDK**: Use `client.aio.live.connect(model="gemini-3.8-live", config=...)` with `send_realtime_input` from `google-genai >= 3.0.0`.
   - **JavaScript / TypeScript SDK**: Use `@google/genai >= 3.0.0` (requires Node.js 22+) `ai.live.connect` and Ephemeral Tokens for browser-based client security.
3. **Google Gemini Image, Video, Document & Multimodal Embeddings**:
   - Image Generation: **`gemini-nano-banana-2.1`** (`gemini-3.1-flash-image`, default high-efficiency image generation, conversational editing with up to 14 reference images, video-to-image context, and SynthID watermarking), **`gemini-3-pro-image`** (Nano Banana Pro), and **`gemini-3.1-flash-lite-image`**.
   - Video Generation & Editing: **`gemini-omni-1.2-flash`** (GA Nov 2026; use instead of deprecated `gemini-omni-1.1-flash`, which auto-routes starting Dec 3, 2026) for video generation, conversational video editing, and subject consistency across up to 6 reference images.
   - Embeddings: **`gemini-embedding-2`** (GA Nov 2026; `gemini-embedding-2-preview` is deprecated and auto-routes to `gemini-embedding-2` in the same embedding space) and **`gemini-embedding-001`** via `client.models.embed_content`.
   - Native Document & Tool Responses: Supports native ingestion of PDF, PPT, ODP, ODS, and DOC files, plus returning audio, video, and Office/OpenDocument files directly in tool function responses.
4. **Anthropic Claude Generation 5.5 & Fable 5.2 (`anthropic >= 2.8.0`, `@anthropic-ai/sdk >= 1.7.0`, API `2026-10-21`)**:
   - **Canonical Hyphenated Model IDs**: Always use exact hyphenated API tags (1M context window, 128K max output across all active tiers; never use dot-notation like deprecated `claude-sonnet-5.5` or `claude-opus-5.5`):
     - **`claude-fable-5-2`** (GA Nov 9, 2026; use instead of legacy `claude-fable-5-1` / `claude-fable-5.1`): Apex model for long-running agentic coding, multi-agent orchestration, and scientific/financial reasoning (`claude-mythos-5-2` is restricted to vetted cyber/bio partner programs).
     - **`claude-opus-5-5`**: Flagship reasoning model for heavy enterprise workloads and complex multi-step coding agents.
     - **`claude-sonnet-5-5`**: Balanced production and coding workhorse ($2 / $10 per 1M tokens).
     - **`claude-haiku-5-5`** (GA Oct 2026): High-speed, ultra-low-latency tier with full 1M context window.
   - **API `2026-10-21` Breaking Changes**: SDKs transmit keys via `Authorization: Bearer <key>` (`ANTHROPIC_API_KEY`). Legacy sampling parameters (`temperature`, `top_p`, `top_k`) return HTTP `400`; use Adaptive Thinking (`thinking={"type": "adaptive"}`, `output_config={"effort": "high"}`) and Pydantic tool schemas for Structured Outputs. For autonomous agents, check `claude-agent-sdk >= 0.2.181`.
5. **OpenAI GPT-6 & GPT-6.1 Series (`openai >= 3.50.0` Python, `openai >= 7.55.0` Node/TS, `openai-agents >= 0.24.0`)**:
   - **`gpt-6-astra`**: Ultimate flagship model for deep reasoning, complex software migrations, and long-horizon agentic work.
   - **`gpt-6.1-sol`**: Primary production and coding workhorse ($2 / $10 per 1M tokens) supporting `reasoning={"effort": "medium"}` (`none`, `low`, `medium`, `high`, `xhigh`, `max`).
   - **`gpt-6.1-terra`** (GA late Oct 2026; use instead of legacy `gpt-5.6-terra` and `gpt-5.4`): Fast visual reasoning, computer use (CUA), and structured document parsing.
   - **`gpt-6-luna`**: Cost-efficient high-volume lightweight tier.
   - **`gpt-image-2.6-sunburst`** & **`gpt-image-2.6-flare`** (GA Nov 2026): Image generation and editing models with SVG and animated GIF support (`v1/images/generations`, `v1/images/edits`).
   - **Responses API Standard**: Use `client.responses.create(...)` and `client.responses.parse(..., text_format=MyPydanticModel)` (or `openai-agents` `Agent(..., output_type=MyPydanticModel)`); legacy isolated `o1` / `o3` / `o4-mini` reasoning endpoints are retired.
   - **Google ADK Multi-Provider Routing (`LiteLlm`)**: When combining Anthropic or OpenAI models inside `google-adk`, wrap via `from google.adk.models.lite_llm import LiteLlm` (`LiteLlm(model="anthropic/claude-sonnet-5-5")` or `LiteLlm(model="openai/gpt-6.1-sol")` with `litellm >= 1.84.0`).
6. **Unified Google GenAI SDK v3 (`google-genai >= 3.0.0`, Default API `v1`)**:
   - Migrate from legacy `google-generativeai` (`import google.generativeai as genai`) to the official unified **`google-genai >= 3.0.0`** SDK (which defaults to stable Gemini Developer API `v1` and `httpx2` in Python, and requires Node.js 22+ in `@google/genai >= 3.0.0`), supporting both the stateful **Interactions API** (`client.interactions.create`) and **`generate_content`** (`client.models.generate_content`):
   ```python
   # Modern Google GenAI SDK v3 (November 2026 standard: Interactions API + generate_content)
   from google import genai
   from google.genai import types

   client = genai.Client()

   # Option A: Stateful Interactions API with Gemini 4 Hydrogen (Fast agentic workhorse)
   interaction = client.interactions.create(
       model="gemini-4-hydrogen",
       input="Design a local RAG architecture with Gemma 4 and Gemini Embedding 2."
   )
   print(interaction.output_text)

   # Option B: Direct Content Generation with Gemini 4 Carbon & Thinking Config
   response = client.models.generate_content(
       model="gemini-4-carbon",
       contents="Audit this multi-agent architecture and propose security guardrails.",
       config=types.GenerateContentConfig(
           temperature=0.7,
           thinking_config=types.ThinkingConfig(thinking_budget=2048)
       )
   )
   print(response.text)
   ```
7. **Google Gemma 4, EmbeddingGemma 2 & Specialized Gemma Open-Weight Family (Apache 2.0)**:
   - **Gemma 4 Core Models (`transformers >= 5.10.1` `AutoModelForMultimodalLM` & Ollama)**:
     - **Local Ollama Tags** (`ollama.com/library/gemma4`): **`gemma4:e2b`** (2B effective edge, 128K ctx, Text+Image+Audio, ~4.3 GB), **`gemma4:e4b`** (4B effective default, 128K ctx, Text+Image+Audio, ~6.6 GB), **`gemma4:12b`** (12B unified encoder-free multimodal dense, 256K ctx, ~7.8 GB; never use non-existent `gemma4:e12b`), **`gemma4:26b`** (25.8B MoE with 4B active parameters, 256K ctx, ~16 GB; use `gemma4:26b` on Ollama instead of `gemma4:26b-a4b`), and **`gemma4:31b`** (31.3B dense workstation, 256K ctx, ~19 GB).
     - **Cloud Gemini Developer API & Hugging Face IDs**: **`gemma-4-31b-it`**, **`gemma-4-26b-a4b-it`**, **`gemma-4-12b-it`**, **`gemma-4-e4b-it`**, **`gemma-4-e2b-it`** (`google/gemma-4-*-it`), supporting native `<|think|>` reasoning and Function Calling.
   - **EmbeddingGemma 2 (`embeddinggemma-2`, GA Oct 2026; supersedes legacy v1 `embeddinggemma:300m`)**:
     - Maps **text, source code, images, video, and audio** into a unified **768-dimensional vector space** with **Matryoshka Representation Learning (MRL)** truncation (`768` -> `512` / `256` / `128`), **8K context window**, and **100+ languages**.
     - **Modular Memory Architecture** on Ollama (`/api/embed`) & Hugging Face (`google/embeddinggemma-2`): **`embeddinggemma-2`** / **`embeddinggemma-2:740m`** (~1.3 GB full multimodal), **`embeddinggemma-2:570m`** (~950 MB text+code+audio), **`embeddinggemma-2:440m`** (~690 MB text+code+vision), and **`embeddinggemma-2:270m`** (~304 MB text+code only for 8GB RAM / CPU-only laptops).
   - **Specialized Gemma Models**: **`translategemma`** (4B/12B/27B text & visual translation across 55 languages), **`functiongemma`** (270M on-device Function Calling specialist), **`medgemma1.5`** (multimodal EHR & CT/MRI/X-ray/histopathology clinical model), and **`shieldgemma`** (ShieldGemma 2 safety policy classifier).
8. **Structured Outputs**: Verify the latest JSON Schema / Pydantic V2 integration API (`response_mime_type="application/json"`, `response_schema=MyModel`).
9. **Pydantic V2 vs V1**: Ensure all schema definitions use Pydantic V2 (`model_validate`, `field_validator`, `BaseModel`).

---

## Anti-Pattern Rules (Prohibited Actions)

- **Prohibited**: Hardcoding legacy retired models like `gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`, `gemini-3.1-flash`, `gemini-3.1-pro`, `gemini-3.7-flash`, `gemini-omni-1.1-flash`, `gemini-embedding-2-preview`, `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-5.4`, `gpt-5.6-terra`, `o1-mini`, `o3-mini`, `o4-mini`, `claude-3-*`, `claude-sonnet-4*`, `claude-fable-5.1`, `llama-2`, `gemma-1`, `gemma2:*`, `gemma3:*`, or `embeddinggemma:300m`.
- **Prohibited**: Using deprecated `google-generativeai` (Python) or `@google/generative-ai` (JS) import patterns instead of modern `google-genai` and `@google/genai`.
- **Prohibited**: Relying on unpinned `latest` tags without confirming what exact model version tag it resolves to.
- **Prohibited**: Omitting currency timestamp labels from generated preparation guides.

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
