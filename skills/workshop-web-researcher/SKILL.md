---
name: workshop-web-researcher
description: Performs live web searches to verify the latest release versions and tags for tools (Ollama, LM Studio, uv, Docker) and AI models (Gemini, Gemma 4, Claude, Llama, etc.), ensuring data currency and preventing hardcoded legacy versions in generated documentation.
---

# Workshop Web Researcher Skill

## Purpose
AI model knowledge has a training cutoff date, meaning generated code and documentation may reference outdated model names or versions. This skill enforces a **dynamic verification protocol** that queries live sources before generating any model-dependent content.

## Dynamic Model Discovery Protocol

### Mandatory Verification Before Generation
Before writing any code or documentation that references an AI model or tool version, the agent **must**:

1. **Search** the official source (GitHub releases, PyPI, npm, Ollama model library) for the latest stable version
2. **Compare** against the version in the agent's training data
3. **Use** the verified latest version in all generated output
4. **Stamp** the document with a currency label: `> Latest versions verified on: YYYY-MM-DD`

### Verification Sources

| Tool / Model | Primary Source |
|---|---|
| Ollama | `https://github.com/ollama/ollama/releases` |
| LM Studio | `https://github.com/lmstudio-ai/lms/releases` |
| Gemma models | `https://ollama.com/library/gemma4` |
| Gemini API | `https://ai.google.dev/gemini-api/docs` |
| Python / uv | `https://github.com/astral-sh/uv/releases` |
| Docker | `https://docs.docker.com/engine/release-notes/` |

### Anti-Patterns (Prohibited)
- Hardcoding `gemma-1`, `gpt-3.5-turbo`, `llama-2` without live verification
- Using `latest` tag without confirming what version it resolves to
- Omitting the currency timestamp from generated documentation
