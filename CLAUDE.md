# Claude Code Guide for Workshop Harness

This repository is fully compatible with **Anthropic Claude Code CLI** and **Claude Desktop**.

## 🚀 Quick Usage with Claude Code

When working with Claude Code CLI, you can directly instruct Claude using the 12 specialized skills located in the `skills/` directory:

1. **One-Click Full Workshop Generation**:
   > *"Run `python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4"` and verify all artifacts."*

2. **Cross-Architecture Audit**:
   > *"Read `skills/cross-architecture-checker/SKILL.md` and audit potential risks for Intel Mac and Windows users."*

3. **Loop Engineering Multi-Persona Evaluation**:
   > *"Read `skills/workshop-persona-loop-evaluator/SKILL.md` and perform a multi-persona audit for beginner, intermediate, and advanced attendees."*

4. **PDF Handout Build**:
   > *"Run `python3 harness_cli.py build-pdf --target my-bwai-workshop` to generate publication-ready PDF handouts."*

5. **Open Codelabs Export & Push**:
   > *"Read `skills/open-codelabs-integrator/SKILL.md` and export the workshop into Open Codelabs manifest format via `python3 harness_cli.py export-codelab --target my-bwai-workshop --push`."*

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
- `skills/open-codelabs-integrator/SKILL.md`

## 🔗 References
- [AI Agent Interoperability Guide](./docs/ai-agent-interoperability-guide.md)
- [Official Repository](https://github.com/JAICHANGPARK/workshop-harness)
