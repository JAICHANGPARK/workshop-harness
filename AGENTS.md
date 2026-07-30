# AGENTS.md - Agent Instructions for Workshop Harness

> Standard AI Agent Context & Instructions Specification (https://agents.md/)

This repository provides seamless integration for all AI Coding Agents including **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Aider**, and **Cursor / Windsurf**.

---

## 🎯 Repository Overview & Purpose

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, community coding labs).

- **CLI Automation**: `python3 harness_cli.py`
- **12 Agent Skills**: Located under `skills/*/SKILL.md`
- **Document Templates**: Located under `templates/doc-templates/`

---

## ⚡ Quick Agent Commands & Workflows

### 1. One-Click Full Workshop Generation Across All 12 Skills
Execute the full orchestration pipeline:
```bash
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

### 2. Cross-Architecture Compatibility Audit
Audit tech stack risks across Apple Silicon, Intel Mac, Windows, and Linux:
```bash
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"
```

### 3. Loop Engineering Multi-Persona Review
Evaluate curriculum and code from beginner, intermediate, and advanced attendee personas:
```bash
python3 harness_cli.py audit-loop --topic "Local RAG with Gemma 4"
```

### 4. Code Smoke Test & Markdown Link Integrity
Verify markdown relative links and execute test scripts:
```bash
python3 harness_cli.py test --target my-bwai-workshop
```

### 5. Build Publication PDF Handout
Generate PDF handouts from markdown documentation:
```bash
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## 📁 12 Agent Skills Index

When handling user requests, reference the specific skill instructions in `skills/`:

1. [`skills/workshop-scaffolder/SKILL.md`](skills/workshop-scaffolder/SKILL.md)
2. [`skills/cross-architecture-checker/SKILL.md`](skills/cross-architecture-checker/SKILL.md)
3. [`skills/prerequisite-checker/SKILL.md`](skills/prerequisite-checker/SKILL.md)
4. [`skills/hands-on-curriculum-builder/SKILL.md`](skills/hands-on-curriculum-builder/SKILL.md)
5. [`skills/pdf-handout-generator/SKILL.md`](skills/pdf-handout-generator/SKILL.md)
6. [`skills/workshop-troubleshooter/SKILL.md`](skills/workshop-troubleshooter/SKILL.md)
7. [`skills/workshop-runbook-generator/SKILL.md`](skills/workshop-runbook-generator/SKILL.md)
8. [`skills/live-debug-assistant/SKILL.md`](skills/live-debug-assistant/SKILL.md)
9. [`skills/workshop-faq-generator/SKILL.md`](skills/workshop-faq-generator/SKILL.md)
10. [`skills/workshop-tester/SKILL.md`](skills/workshop-tester/SKILL.md)
11. [`skills/workshop-web-researcher/SKILL.md`](skills/workshop-web-researcher/SKILL.md)
12. [`skills/workshop-persona-loop-evaluator/SKILL.md`](skills/workshop-persona-loop-evaluator/SKILL.md)

---

## 🔗 References

- **AGENTS.md Open Specification**: [https://agents.md/](https://agents.md/)
- **Official Repository**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
