# Agent Instructions & Typography Rules for adk-polyglot-workshop

> Workshop Example: **adk-polyglot-workshop**
> Primary Cloud Model: `gemini-3.8-flash` | Flagship Reasoning: `gemini-4-argon` | Local Model: `gemma4:e4b`

## Mandatory Rules for AI Coding Agents

1. **Typography Rule (No Em Dash in Markdown or Documentation)**:
   - **NEVER generate em dash characters (`\u2014`)** in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks.
   - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
   - Run `python3 scripts/verify_workshop.py .` to verify zero forbidden em dashes exist.

2. **No Emojis in Documentation by Default**:
   - Do not include emojis in generated documentation, slide decks, setup guides, or runbooks unless explicitly requested.

3. **2026 Frontier Model & SDK Currency**:
   - Use `google-genai >= 2.30.1` (`from google import genai`) and 2026 model tags (`gemini-3.8-flash`, `gemini-4-argon`, `gemma4:e4b`).
   - Never use deprecated `google-generativeai` or retired `gemini-1.5-*` / `gemini-2.0-*` / `gemini-2.5-*` tags.

## References
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
