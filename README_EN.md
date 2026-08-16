![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness (English)

[![Official Docs](https://img.shields.io/badge/Official%20Docs-MkDocs-blue.svg)](https://JAICHANGPARK.github.io/workshop-harness/)
[![Landing Page](https://img.shields.io/badge/Landing%20Page-Website-purple.svg)](https://JAICHANGPARK.github.io/workshop-harness/website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.08.16-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

**Official Documentation**: [https://JAICHANGPARK.github.io/workshop-harness/](https://JAICHANGPARK.github.io/workshop-harness/)  
**Landing Page**: [https://JAICHANGPARK.github.io/workshop-harness/website/](https://JAICHANGPARK.github.io/workshop-harness/website/)

---

## Overview

Workshop Harness is an AI Agent Harness, 14 Skill Suite, and CLI Automation Toolkit powered by **Astral uv**, designed for event organizers, speakers, and TAs orchestrating technical workshops (Build with AI, DevFest, community coding labs).

Adhering to the [AGENTS.md open specification](https://agents.md/), this harness provides seamless native interoperability across all AI coding agents including **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Cursor**, and **Aider**.

---

## ⚡ Quick Start (uv Powered)

```bash
# 1. Clone repository
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. Auto-install all 14 skills to local environment (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. One-click full workshop package generation
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 🧩 14 Specialized Agent Skills Specification

| # | Skill Name | Input / Trigger | Output & Artifacts | Primary Role |
|---|---|---|---|---|
| 1 | [`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md) | Workshop name & topic | `docs/`, `workshop/`, `prompt-pack/`, `scripts/` | Scaffolds standard repository structure |
| 2 | [`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md) | Tech stack list | `docs/00-architecture-compatibility-matrix.md` | Audits Apple Silicon, Intel Mac, Win, Linux compatibility & fallbacks |
| 3 | [`prerequisite-checker`](skills/prerequisite-checker/SKILL.md) | Prerequisites list | `gemma4-local-setup-guide.md`, `check_env.sh/ps1` | Generates OS-specific setup guides & automated verification scripts |
| 4 | [`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md) | Session goal & duration | `03_labs/README.md`, `prompt-pack/`, `starter`/`final` code | Builds step-by-step curriculum, starter vs final code, and prompt packs |
| 5 | [`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md) | `docs/` markdown directory | `output/pdf/*.pdf`, `tmp/pdfs/contact_sheet.png` | Builds publication-ready PDF handouts & preview contact sheets via ReportLab |
| 6 | [`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md) | Hardware specs & OS | `docs/troubleshooting.md`, `docs/20-faq.md` | Generates troubleshooting matrix by RAM (8G/16G/32G+) and OS |
| 7 | [`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md) | Session duration & TAs | `RUNBOOK.md` | Creates minute-by-minute facilitator timeline runbook & cue cards |
| 8 | [`live-debug-assistant`](skills/live-debug-assistant/SKILL.md) | Terminal error log | 10-second hotfix command, `.env.sample` | Diagnoses live terminal errors & enforces API Key security protocols |
| 9 | [`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md) | Workshop topic & level | `docs/20-faq.md` / `FAQ.md` | Automatically generates attendee FAQ (hardware, network, code) |
| 10 | [`workshop-tester`](skills/workshop-tester/SKILL.md) | Workshop project path | `verify_workshop.py` audit output | Audits code execution smoke tests and markdown broken relative links |
| 11 | [`workshop-web-researcher`](skills/workshop-web-researcher/SKILL.md) | Tool/Model query | Updated release tags & docs | Fetches latest tool/SDK release versions & prevents deprecated flags |
| 12 | [`workshop-persona-loop-evaluator`](skills/workshop-persona-loop-evaluator/SKILL.md) | Workshop topic & materials | `docs/00-persona-loop-review-report.md` | Multi-persona loop engineering audit for beginner, intermediate, and advanced attendees |
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | Workshop project path | `output/open-codelabs/` (`codelab.yaml`), `oc` push | Converts workshop artifacts to Open Codelabs platform manifests and publishes via `oc` CLI/MCP |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | Workshop project path | `output/colab/` (`*.ipynb`, badges), `colab` CLI test | Converts workshop to Google Colab interactive notebooks (.ipynb), adds badges, and runs headless tests via Google Colab CLI |

---

## 🛠️ CLI Usage (`harness_cli.py`)

```bash
# 1. One-Click Full Generation Across All 14 Skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. Export Google Colab Notebooks & Badges
uv run harness_cli.py export-colab --target my-bwai-workshop --repo "JAICHANGPARK/my-bwai-workshop"

# 3. Headless Smoke Test via Google Colab CLI
uv run harness_cli.py test-colab --target my-bwai-workshop

# 4. Export Open Codelabs Bundle & Push via oc CLI
uv run harness_cli.py export-codelab --target my-bwai-workshop --push

# 5. Audit tech stack cross-architecture risks
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 6. Build Publication PDF Handout
uv run harness_cli.py build-pdf --target my-bwai-workshop
```

---

## License

[MIT License](LICENSE)
