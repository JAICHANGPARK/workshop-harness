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

| Target Tool / Model | Primary Official Source URL | Example Query |
|---|---|---|
| **Ollama** | `https://github.com/ollama/ollama/releases` | `site:github.com/ollama/ollama releases latest` |
| **Gemma Models** | `https://ollama.com/library/gemma4` | `site:ollama.com/library gemma release` |
| **Google Gemini API** | `https://ai.google.dev/gemini-api/docs/models/gemini` | `site:ai.google.dev gemini model versions` |
| **LM Studio** | `https://github.com/lmstudio-ai/lms/releases` | `site:github.com/lmstudio-ai/lms releases` |
| **Astral uv** | `https://github.com/astral-sh/uv/releases` | `site:github.com/astral-sh/uv releases` |
| **Docker Engine** | `https://docs.docker.com/engine/release-notes/` | `docker engine release notes latest` |

---

## Anti-Pattern Rules (Prohibited Actions)

- ❌ **Prohibited**: Hardcoding legacy models like `gpt-3.5-turbo`, `llama-2`, or `gemma-1` without live verification.
- ❌ **Prohibited**: Relying on unpinned `latest` tags without confirming what exact model version tag it resolves to.
- ❌ **Prohibited**: Omitting currency timestamp labels from generated preparation guides.
