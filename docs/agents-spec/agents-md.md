# AI Agent Interoperability Standard (`AGENTS.md`)

`workshop-harness` adheres to the open **[AGENTS.md specification](https://agents.md/)** to ensure 100% vendor-agnostic interoperability across all AI coding agents.

---

## Benefits of AGENTS.md

1. **Vendor Independence**: Prevents lock-in to any specific LLM provider or IDE plugin.
2. **Context Optimization**: Provides agents with instant repo layout, CLI command workflows, and skill definitions upon initialization.
3. **Multi-Agent Collaboration**: Enables multiple agents (e.g. Antigravity + Claude + Cursor) to share the same guidelines and rules.

---

## Specification Files in Repository

- **AGENTS.md**: [`AGENTS.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/AGENTS.md) (Open standard specification)
- **CLAUDE.md**: [`CLAUDE.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/CLAUDE.md) (Anthropic Claude Code instructions)
- **Native Skills**: `skills/*/SKILL.md` (Google Antigravity & Gemini CLI skills)
