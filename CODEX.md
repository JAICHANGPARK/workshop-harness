# OpenAI Codex & ChatGPT Guide for Workshop Harness

This repository provides seamless integration for **OpenAI Codex**, **ChatGPT**, **Cursor**, and **Aider**.

## 🚀 Quick Usage with Codex / ChatGPT

You can instruct OpenAI Codex or ChatGPT using the CLI tool or by referencing the skill markdown files in `skills/`:

1. **CLI Command Execution**:
   ```bash
   python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
   ```

2. **Skill Prompt Instruction**:
   > *"Follow the rules in `skills/cross-architecture-checker/SKILL.md` to generate `docs/00-architecture-compatibility-matrix.md` for a Flutter & Gemini workshop."*

3. **Integrity Testing**:
   ```bash
   python3 harness_cli.py test --target my-bwai-workshop
   ```

## 📁 Key Skill Locations
- `skills/workshop-scaffolder/SKILL.md`
- `skills/cross-architecture-checker/SKILL.md`
- `skills/prerequisite-checker/SKILL.md`
- `skills/hands-on-curriculum-builder/SKILL.md`
- `skills/pdf-handout-generator/SKILL.md`
- `skills/workshop-troubleshooter/SKILL.md`
- `skills/workshop-runbook-generator/SKILL.md`
- `skills/live-debug-assistant/SKILL.md`
- `skills/workshop-faq-generator/SKILL.md`
- `skills/workshop-tester/SKILL.md`
- `skills/workshop-web-researcher/SKILL.md`
- `skills/workshop-persona-loop-evaluator/SKILL.md`

## 🔗 References
- [AI Agent Interoperability Guide](./docs/ai-agent-interoperability-guide.md)
- [Official Repository](https://github.com/JAICHANGPARK/workshop-harness)
