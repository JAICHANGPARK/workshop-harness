# Installation & Agent Setup

This guide explains how to install **Workshop Harness** and connect it with various AI Coding Agents (Google Antigravity, Gemini CLI, Claude Code, OpenAI Codex, Cursor, etc.).

---

## Environment Setup

### 1. Astral uv Installation
`uv` is an extremely fast Python package manager written in Rust.

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Workshop Harness & Skills Installation

```bash
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# Run skills installation script
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

This installs all 15 skill directories into `~/.gemini/skills/` so **Google Antigravity** and **Gemini CLI** natively detect them.

---

## AI Agent Integration Guide

### 1. Google Antigravity & Gemini CLI
- **Native Skill Discovery**: All 15 skills in `~/.gemini/skills/` are automatically available.
- **Natural Language Trigger Example**:
  - *"Scaffold a new Gemma 4 local RAG workshop."*
  - *"Export this workshop to Open Codelabs format and push via oc CLI."*

### 2. Anthropic Claude (Claude Code CLI & Desktop)
- Reads `CLAUDE.md` and `AGENTS.md` at the project root as standard instructions.
- **Claude Code Example**:
  ```bash
  claude "Read skills/open-codelabs-integrator/SKILL.md and export the workshop via python3 harness_cli.py export-codelab --target my-bwai-workshop --push"
  ```

### 3. Cursor / Windsurf / OpenAI Codex / Aider
- Follows the [`AGENTS.md`](../agents-spec/agents-md.md) open specification.

---

## Verification

Verify that the CLI runs cleanly:

```bash
uv run harness_cli.py --help
```
