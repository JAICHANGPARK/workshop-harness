# 17 Agent Skill Suite Catalog

`workshop-harness` features **17 specialized agent skills** distilled from real-world workshop facilitation. Each skill is defined with YAML frontmatter and markdown instructions in `skills/*/SKILL.md`.

---

## Skill Suite Catalog

| # | Skill Name | Input / Trigger | Primary Role & Artifacts | SKILL.md Path |
|:---:|---|---|---|---|
| 1 | `workshop-scaffolder` | Workshop name & topic | Scaffolds standard repository structure and boilerplate templates | [`skills/workshop-scaffolder/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-scaffolder/SKILL.md) |
| 2 | `cross-architecture-checker` | Tech stack list | Audits Apple Silicon / Intel Mac / Windows / Linux chipset risks and fallbacks | [`skills/cross-architecture-checker/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/cross-architecture-checker/SKILL.md) |
| 3 | `prerequisite-checker` | Prerequisites list | Generates OS-specific setup guides (`gemma4-local-setup-guide.md`) & `check_env` scripts | [`skills/prerequisite-checker/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/prerequisite-checker/SKILL.md) |
| 4 | `hands-on-curriculum-builder` | Session goal & duration | Builds lab guide (`03_labs/README.md`), starter & final code templates, prompt pack | [`skills/hands-on-curriculum-builder/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/hands-on-curriculum-builder/SKILL.md) |
| 5 | `pdf-handout-generator` | `docs/` markdown folder | Builds publication-ready PDF handouts (`output/pdf/`) & preview contact sheets | [`skills/pdf-handout-generator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/pdf-handout-generator/SKILL.md) |
| 6 | `workshop-troubleshooter` | Hardware specs & OS | Generates troubleshooting matrix by RAM (8G/16G/32G+) & OS in `docs/20-faq.md` | [`skills/workshop-troubleshooter/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-troubleshooter/SKILL.md) |
| 7 | `workshop-runbook-generator` | Session duration & TAs | Creates minute-by-minute facilitator timeline runbook (`RUNBOOK.md`) & cue cards | [`skills/workshop-runbook-generator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-runbook-generator/SKILL.md) |
| 8 | `live-debug-assistant` | Terminal error log | Diagnoses live terminal errors with 10-second hotfix commands & API key security | [`skills/live-debug-assistant/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/live-debug-assistant/SKILL.md) |
| 9 | `workshop-faq-generator` | Topic & level | Automatically generates attendee FAQ (hardware, network, code setup) | [`skills/workshop-faq-generator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-faq-generator/SKILL.md) |
| 10 | `workshop-tester` | Workshop project path | Audits code execution smoke tests and relative markdown broken links | [`skills/workshop-tester/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-tester/SKILL.md) |
| 11 | `workshop-web-researcher` | Tool/Model query | Real-time web auditing of latest tool/SDK releases & breaking changes | [`skills/workshop-web-researcher/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-web-researcher/SKILL.md) |
| 12 | `workshop-persona-loop-evaluator` | Topic & materials | Multi-persona loop engineering audit across 4 attendee levels (Non-Coder, Novice, Intermediate, Senior) | [`skills/workshop-persona-loop-evaluator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-persona-loop-evaluator/SKILL.md) |
| 13 | `open-codelabs-integrator` | Workshop project path | Converts workshop artifacts to Open Codelabs manifests (`codelab.yaml`) & pushes via `oc` CLI/MCP | [`skills/open-codelabs-integrator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/open-codelabs-integrator/SKILL.md) |
| 14 | `colab-workshop-integrator` | Workshop project path | Generates Google Colab interactive notebooks (`.ipynb`), badges, and automates headless smoke tests via `colab` CLI | [`skills/colab-workshop-integrator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/colab-workshop-integrator/SKILL.md) |
| 15 | `workshop-slide-generator` | Workshop project path | Generates Marp Markdown (`slides.md`) and interactive standalone Web Presentation (`index.html`) synced with runbook | [`skills/workshop-slide-generator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/workshop-slide-generator/SKILL.md) |
| 16 | `adk-workshop-builder` | ADK workshop topic & stack | Builds multi-language (Python, TypeScript, Go, Kotlin) ADK autonomous agent and multi-agent system labs | [`skills/adk-workshop-builder/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/adk-workshop-builder/SKILL.md) |
| 17 | `eli5-concept-explainer` | Technical concept or error | Translates complex AI mechanics and errors into 3-tier ELI5 physical analogies & mental maps | [`skills/eli5-concept-explainer/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/eli5-concept-explainer/SKILL.md) |
