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
| **Google GenAI SDK** | `https://pypi.org/project/google-genai/` | `site:pypi.org google-genai latest SDK methods` | `google-genai` (Unified SDK) |
| **Google Gemini API** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini model versions` | `gemini-3.7-flash`, `gemini-3.5-flash`, `gemini-3.1-pro-preview` |
| **Google Gemini Live API** | `https://ai.google.dev/gemini-api/docs/live` | `site:ai.google.dev gemini live api` | `gemini-3.1-flash-live-preview`, `gemini-3.5-live-translate-preview` |
| **Flutter Gemini Live** | `https://pub.dev/packages/gemini_live` | `site:pub.dev gemini_live flutter` | `gemini_live` (pub.dev direct WebSocket package) |
| **Anthropic Claude API** | `https://docs.anthropic.com/en/docs/about-claude/models` | `site:docs.anthropic.com claude models release` | `claude-sonnet-5`, `claude-opus-5`, `claude-fable-5` |
| **OpenAI API** | `https://platform.openai.com/docs/models` | `site:platform.openai.com/docs/models latest` | `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` |
| **Ollama** | `https://github.com/ollama/ollama/releases` | `site:github.com/ollama/ollama releases latest` | `ollama` latest engine |
| **Gemma Models** | `https://ollama.com/library/gemma` | `site:ollama.com/library gemma release tags` | `gemma4`, `gemma:latest` |
| **LangChain / LangGraph** | `https://github.com/langchain-ai/langchain/releases` | `site:github.com/langchain-ai/langchain releases latest` | `langchain>=0.3`, `langgraph` |
| **LM Studio** | `https://github.com/lmstudio-ai/lms/releases` | `site:github.com/lmstudio-ai/lms releases` | `lms` CLI latest |
| **Astral uv** | `https://github.com/astral-sh/uv/releases` | `site:github.com/astral-sh/uv releases` | `uv` package manager |
| **Docker Engine** | `https://docs.docker.com/engine/release-notes/` | `docker engine release notes latest` | Latest official Docker Engine |

---

## SDK Breaking Changes & Migration Checks

When researching technical topics, verify:
1. **Google Gemini 3.x Models**: Use the frontier **`gemini-3.7-flash`** (GA flagship workhorse for coding/agents) and **`gemini-3.5-flash`**. Leverage the new `thinking_level` parameter for controlling reasoning depth.
2. **Google Gemini Live Real-time Multimodal API**:
   - Primary model: **`gemini-3.1-flash-live-preview`** for low-latency bidirectional audio/video/text streaming.
   - Real-time Translation: **`gemini-3.5-live-translate-preview`** for speech-to-speech live streaming translation.
   - **Flutter / Dart SDK**: Use the pub.dev **`gemini_live`** package for zero-Firebase direct WebSocket integration or `firebase_ai` for enterprise apps.
   - **Python SDK**: Use `client.aio.live.connect` with `send_realtime_input` from `google-genai`.
   - **JavaScript / TypeScript SDK**: Use `@google/genai` `ai.live.connect` and Ephemeral Tokens for browser-based client security.
3. **Anthropic Claude Generation 5**: Use **`claude-sonnet-5`** (coding/balanced workhorse), **`claude-opus-5`** (complex reasoning/enterprise), and **`claude-fable-5`** (long-horizon agents).
4. **OpenAI GPT-5.6 Series**: Use **`gpt-5.6-sol`** (flagship coding & reasoning), **`gpt-5.6-terra`** (general agentic workflow), and **`gpt-5.6-luna`** (lightweight fast inference).
5. **New Unified SDKs**: Migrate from legacy `google-generativeai` (`import google.generativeai as genai`) to the official unified **`google-genai`** SDK:
   ```python
   # Modern Google GenAI SDK (2026 standard)
   from google import genai
   from google.genai import types

   client = genai.Client()
   response = client.models.generate_content(
       model="gemini-3.7-flash",
       contents="Implement local RAG with Gemma 4",
       config=types.GenerateContentConfig(
           temperature=0.7,
           thinking_config=types.ThinkingConfig(thinking_budget=1024)
       )
   )
   ```
6. **Structured Outputs**: Verify the latest JSON Schema / Pydantic integration API (`response_mime_type="application/json"`, `response_schema=MyModel`).
7. **Pydantic V2 vs V1**: Ensure all schema definitions use Pydantic V2 (`model_validate`, `field_validator`, `BaseModel`).

---

## Anti-Pattern Rules (Prohibited Actions)

- ❌ **Prohibited**: Hardcoding legacy retired models like `gemini-1.0-pro`, `gpt-3.5-turbo`, `llama-2`, or `gemma-1`.
- ❌ **Prohibited**: Using deprecated `google-generativeai` import patterns instead of modern `google-genai`.
- ❌ **Prohibited**: Relying on unpinned `latest` tags without confirming what exact model version tag it resolves to.
- ❌ **Prohibited**: Omitting currency timestamp labels from generated preparation guides.
