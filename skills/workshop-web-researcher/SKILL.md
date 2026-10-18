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

| Target Tool / Model | Primary Official Source URL | Example Query | Latest Recommended Tags (2026) |
|---|---|---|---|
| **Google GenAI SDK** | `https://pypi.org/project/google-genai/` | `site:pypi.org google-genai latest SDK methods` | `google-genai>=2.30.1` (Python), `@google/genai>=2.29.1` (TS/JS) |
| **Google Agent Development Kit (ADK)** | `https://adk.dev` | `site:adk.dev OR site:github.com/google/adk-python` | `google-adk`, `@google/adk`, `google.golang.org/adk/v2`, `com.google.adk:google-adk` (`adk web`, `adk run`, `adk eval`, `adk deploy`) |
| **Google Agents CLI (`google-agents-cli`)** | `https://github.com/google/agents-cli` | `site:github.com/google/agents-cli setup eval deploy` | `uvx google-agents-cli setup`, `npx skills add google/agents-cli` (7 ADLC skills: `workflow`, `scaffold`, `adk-code`, `eval`, `deploy`, `publish`, `observability`) |
| **Google Gemini Frontier & Flash API** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini model versions` | `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` |
| **Google Gemini Live & Audio API** | `https://ai.google.dev/gemini-api/docs/live` | `site:ai.google.dev gemini live api` | `gemini-3.8-live`, `gemini-3.8-live-extended-thinking`, `gemini-3.5-transcribe-live`, `gemini-3.5-live-translate-preview`, `gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts` |
| **Google Gemini Image, Video & Embedding** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini image video embedding` | `gemini-nano-banana-2.1`, `gemini-3-pro-image`, `gemini-omni-1.1-flash`, `gemini-embedding-2` |
| **Google Managed Agents** | `https://ai.google.dev/gemini-api/docs/managed-agents-quickstart` | `site:ai.google.dev antigravity deep research agent` | `antigravity-preview-09-2026`, `deep-research-preview-04-2026`, `deep-research-max-preview-04-2026` |
| **Flutter Gemini Live & GenUI** | `https://pub.dev/packages/genui` | `site:pub.dev genui gemini_live flutter` | `genui`, `gemini_live`, `google_generative_ai` |
| **Anthropic Claude API** | `https://docs.anthropic.com/en/docs/about-claude/models` | `site:docs.anthropic.com claude models release` | `claude-sonnet-5.5` (`claude-sonnet-5-5`), `claude-opus-5.5` (`claude-opus-5-5`), `claude-fable-5.1` (`claude-fable-5-1`), `claude-haiku-5.5` |
| **OpenAI API** | `https://platform.openai.com/docs/models` | `site:platform.openai.com/docs/models latest` | `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.4` |
| **Ollama** | `https://github.com/ollama/ollama/releases` | `site:github.com/ollama/ollama releases latest` | `ollama` latest engine |
| **Gemma 4 & Local Open-Weight Models** | `https://ollama.com/library/gemma` | `site:ollama.com/library gemma qwen3 deepseek llama4` | Cloud: `gemma-4-31b-it`, `gemma-4-26b-a4b-it`; Local: `gemma4:e2b`, `gemma4:e4b`, `gemma4:e12b`, `gemma4:26b-a4b`, `qwen3.6:27b`, `qwen3-coder:30b`, `deepseek-r1:14b`, `llama4:scout` |
| **LangChain / LangGraph** | `https://github.com/langchain-ai/langchain/releases` | `site:github.com/langchain-ai/langchain releases latest` | `langchain>=0.3`, `langgraph` |
| **LM Studio** | `https://github.com/lmstudio-ai/lms/releases` | `site:github.com/lmstudio-ai/lms releases` | `lms` CLI latest |
| **Astral uv** | `https://github.com/astral-sh/uv/releases` | `site:github.com/astral-sh/uv releases` | `uv` package manager |
| **Docker Engine** | `https://docs.docker.com/engine/release-notes/` | `docker engine release notes latest` | Latest official Docker Engine |

---

## SDK Breaking Changes & Migration Checks

When researching technical topics, verify:
1. **Google Gemini 4 & 3.8 Models**:
   - Use **`gemini-4-argon`** (1M context window) for flagship frontier reasoning, complex multi-step coding, research, and agentic/robotics workflows.
   - Use **`gemini-3.8-flash`** (1M context window) as the default fast, balanced production workhorse for coding, agentic, and multimodal tasks (succeeding `gemini-3.7-flash`). Use `gemini-3.5-flash-lite` or `gemini-3.1-flash-lite` for high-throughput, low-cost execution.
   - Leverage selectable `thinking_level` (`low`, `medium`, `high`) or `thinking_config` parameters to control reasoning depth vs latency.
2. **Google Gemini Live Real-time Multimodal & Audio API**:
   - Primary Live model: **`gemini-3.8-live`** for low-latency bidirectional audio/video/text streaming over WebSockets with non-blocking asynchronous function calling (`behavior: "NON_BLOCKING"`) and full-session `send_client_content`.
   - High-Reasoning Live model: **`gemini-3.8-live-extended-thinking`** for background reasoning with spoken conversational fillers (`interaction_status`: `IN_PROGRESS` vs `IDLE`).
   - Speech-to-Text & Translation: **`gemini-3.5-transcribe`**, **`gemini-3.5-transcribe-live`**, and **`gemini-3.5-live-translate-preview`** for speech-to-speech live streaming translation.
   - Expressive TTS: **`gemini-3.8-flash-tts`** and **`gemini-3.8-flash-lite-tts`** for multi-speaker dialogue, Voice Design, and Voice Replication.
   - **Flutter / Dart SDK**: Use the pub.dev **`gemini_live`** package for zero-Firebase direct WebSocket integration or `firebase_ai` for enterprise apps.
   - **Python SDK**: Use `client.aio.live.connect(model="gemini-3.8-live", config=...)` with `send_realtime_input` from `google-genai >= 2.30.1`.
   - **JavaScript / TypeScript SDK**: Use `@google/genai >= 2.29.1` `ai.live.connect` and Ephemeral Tokens for browser-based client security.
3. **Google Gemini Image, Video & Multimodal Embeddings**:
   - Image Generation: **`gemini-nano-banana-2.1`** (default high-efficiency image generation and conversational editing with up to 14 reference images), **`gemini-3-pro-image`** (Nano Banana Pro), and **`gemini-3.1-flash-lite-image`**.
   - Video Generation & Editing: **`gemini-omni-1.1-flash`** via the Interactions API for text-to-video, first/last frame transitions, and video extensions up to 40s.
   - Embeddings: **`gemini-embedding-2`** (multimodal embeddings across text, images, video, audio, documents) and **`gemini-embedding-001`** via `client.models.embed_content`.
4. **Anthropic Claude Generation 5.5 / 5**:
   - Use **`claude-sonnet-5.5`** (`claude-sonnet-5-5` / `claude-sonnet-5`) as the balanced coding and agentic production workhorse (1M context window).
   - Use **`claude-opus-5.5`** (`claude-opus-5-5` / `claude-opus-5`) for frontier reasoning and complex engineering.
   - Use **`claude-fable-5.1`** (`claude-fable-5-1`) for long-horizon autonomous agents, and **`claude-haiku-5.5`** for ultra-fast low-latency routing.
5. **OpenAI GPT-6 & GPT-5.6 Series**:
   - Use **`gpt-6-astra`** for flagship reasoning, coding, and multi-step agentic workflows.
   - Use **`gpt-6.1-sol`** / **`gpt-6-sol`** (or `gpt-5.6-sol`) as the balanced coding and reasoning workhorse.
   - Use **`gpt-6-luna`** (or `gpt-5.6-luna`) for high-speed, cost-efficient inference, and **`gpt-5.6-terra`** / **`gpt-5.4`** for extended exploration and computer-use (CUA).
6. **New Unified Google GenAI SDK (`google-genai >= 2.30.1`)**:
   - Migrate from legacy `google-generativeai` (`import google.generativeai as genai`) to the official unified **`google-genai`** SDK, supporting both the stateful **Interactions API** (`client.interactions.create`) and **`generate_content`** (`client.models.generate_content`):
   ```python
   # Modern Google GenAI SDK (2026 standard: Interactions API + generate_content)
   from google import genai
   from google.genai import types

   client = genai.Client()

   # Option A: Stateful Interactions API (Recommended for multi-turn & agents)
   interaction = client.interactions.create(
       model="gemini-3.8-flash",
       input="Design a local RAG architecture with Gemma 4 and Gemini Embedding 2."
   )
   print(interaction.output_text)

   # Option B: Direct Content Generation with Thinking & Structured Output
   response = client.models.generate_content(
       model="gemini-3.8-flash",
       contents="Implement local RAG with Gemma 4",
       config=types.GenerateContentConfig(
           temperature=0.7,
           thinking_config=types.ThinkingConfig(thinking_budget=1024)
       )
   )
   print(response.text)
   ```
7. **Structured Outputs**: Verify the latest JSON Schema / Pydantic V2 integration API (`response_mime_type="application/json"`, `response_schema=MyModel`).
8. **Pydantic V2 vs V1**: Ensure all schema definitions use Pydantic V2 (`model_validate`, `field_validator`, `BaseModel`).

---

## Anti-Pattern Rules (Prohibited Actions)

- **Prohibited**: Hardcoding legacy retired models like `gemini-3.8-flash`, `gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`, `gemini-3.8-live`, `gpt-6-luna`, `gpt-4-*`, `claude-3-*`, `llama-2`, or `gemma-1`.
- **Prohibited**: Using deprecated `google-generativeai` (Python) or `@google/generative-ai` (JS) import patterns instead of modern `google-genai` and `@google/genai`.
- **Prohibited**: Relying on unpinned `latest` tags without confirming what exact model version tag it resolves to.
- **Prohibited**: Omitting currency timestamp labels from generated preparation guides.
