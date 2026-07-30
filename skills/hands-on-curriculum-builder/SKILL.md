---
name: hands-on-curriculum-builder
description: Builds step-by-step hands-on lab curriculum (Lab 1, Lab 2, Lab 3), starter and final code templates, prompt packs with Output Schema specifications, and enforces a mandatory references section in all generated documents.
---

# Hands-on Curriculum Builder Skill

## Purpose
Ensures attendees can achieve clear learning objectives within the allocated session time (e.g., 60-120 minutes) by modularizing the curriculum into sequential labs and providing both starter (`01_starter`) and completed reference (`02_final`) code.

## Design Patterns

### 1. Starter vs Final Code Separation
- **`01_starter/`**: Project scaffold with dependency files (`pyproject.toml`, `pubspec.yaml`, `go.mod`), CLI/UI entry point, and `TODO: [Lab N] ...` comment markers for attendees to fill in.
- **`02_final/`**: Fully working reference solution with all TODOs completed.

### 2. Step-by-Step Lab Guide (`03_labs/README.md`)
- **Lab 01: Basic Integration & Hello World** - Verify LLM API / local Ollama connectivity
- **Lab 02: Structured Output (Output Schema)** - Apply Pydantic / JSON Schema for type-safe parsing
- **Lab 03: Agent / RAG Pipeline Completion** - Wire up Vector Search or Tool Calls for the final application

## Mandatory References Protocol

All lab guides and documents referencing external APIs or official documentation **must include a `## References` section** at the bottom:

```markdown
## References

- **Official API Documentation**: [Google Gemini API Docs](https://ai.google.dev/docs)
- **Framework Guide**: [Flutter Developer Docs](https://docs.flutter.dev)
- **Base Workshop Repository**: [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
```
