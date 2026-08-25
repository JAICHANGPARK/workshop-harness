---
name: hands-on-curriculum-builder
description: Builds step-by-step hands-on lab curriculum (Lab 1, Lab 2, Lab 3), starter and final code templates, prompt packs with Output Schema specifications, and enforces a mandatory references section in all generated documents.
---

# Hands-on Curriculum Builder Skill

## Purpose
Modularizes workshop content into sequential, timed hands-on labs (60 to 120 minutes total). Enforces a clean separation between starter scaffolding (`01_starter`), reference solutions (`02_final`), step-by-step lab guides (`03_labs/README.md`), and structured prompt engineering packs (`prompt-pack/README.md`).

> 🌐 **Mandatory Pre-Flight Web Research Protocol**:
> Before generating any lab code or instructions, the agent **MUST** perform live web searches (`search_web` / `workshop-web-researcher`) to verify the latest SDK syntax (e.g. `google-genai` SDK vs legacy `google-generativeai`, current LangChain/Ollama versions, latest model tags) and ensure zero deprecated code.

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
    Live1["Lab 01: WebSocket Connection & Ephemeral Tokens (15-20 min)<br>Connect to gemini-3.1-flash-live-preview via LiveSession / SDK"]
    Live2["Lab 02: Real-time Bidirectional Audio & VAD Handling (30-35 min)<br>Stream 16kHz PCM audio chunks and handle model speech playback<br>(Flutter: gemini_live | Python: google-genai | JS: @google/genai)"]
    Live3["Lab 03: Real-time Multimodal (Camera/Video) & Live Tool Calling (30-35 min)<br>Stream JPEG video frames and execute real-time function calling"]

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
