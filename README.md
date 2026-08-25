![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness

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

Workshop Harness is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit powered by **Astral uv**. It is designed for event organizers, speakers, and TAs orchestrating technical workshops, Build with AI (BWAI) events, DevFests, and hands-on coding labs.

It standardizes the proven architecture and operational battle-tested workflows from real-world events including:
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)

---

## ⚡ Quick Start (uv Powered)

Build a complete end-to-end workshop repository in under **1 minute** with 100% automated dependency management using `uv`:

```bash
# 1. Clone the repository
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. Install 12 Agent Skills & auto-sync dependencies via uv
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. Generate a complete workshop package with ONE CLICK (All dependencies auto-installed)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 📦 Installation

### Prerequisites
- **Python**: Version 3.9 or higher
- **Astral uv**: Fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git**: Installed and configured
- **AI Coding Agent (Optional)**: Google Antigravity, Gemini CLI, Anthropic Claude Code, OpenAI Codex, Cursor, or Aider

### Installing CLI & Agent Skills

1. **Automatic Skill & Dependency Installation**:
   Run the installation script to automatically set up `reportlab`, `pymupdf`, `pillow` via `uv` and copy 12 skills to `~/.gemini/skills`:
   ```bash
   ./scripts/install_skills.sh
   ```

2. **Verifying Installation**:
   Ensure the CLI works smoothly with `uv`:
   ```bash
   uv run harness_cli.py --help
   ```

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#-quick-start-uv-powered)
- [Installation](#-installation)
- [One-Click Full Orchestration](#one-click-full-orchestration)
- [Open AI Agent Standard (`AGENTS.md`)](#open-ai-agent-standard-agentsmd)
- [Quantified Productivity & Facilitator ROI](#-quantified-productivity--facilitator-roi)
- [12 Specialized Agent Skills Specification](#12-specialized-agent-skills-specification)
- [Cross-Architecture Compatibility Matrix](#cross-architecture-compatibility-matrix)
- [CLI Tool Usage (`harness_cli.py`)](#cli-tool-usage-harness_clipy)
- [Installing Agent Skills](#installing-agent-skills)
- [Standard Workshop Repository Structure](#standard-workshop-repository-structure)
- [Changelog](#changelog)
- [License](#license)

---

## One-Click Full Orchestration

With a single CLI command or natural language prompt, Workshop Harness triggers all 12 skills in sequence:

```bash
# One-Click Full Workshop Generation Across All 12 Skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## Open AI Agent Standard (`AGENTS.md`)

Workshop Harness adopts the open **[AGENTS.md specification](https://agents.md/)**, making it 100% vendor-agnostic across all AI coding agents:

- **Open Agent Standard Specification**: [`AGENTS.md`](./AGENTS.md)
- **Anthropic Claude (Claude Code CLI & Desktop)**: [`CLAUDE.md`](./CLAUDE.md)
- **Google Antigravity & Gemini CLI**: Native `.gemini/skills/` integration
- **OpenAI Codex, ChatGPT, Aider & Cursor**: Supported via [`AGENTS.md`](./AGENTS.md)
- **Full Guide**: [`docs/ai-agent-interoperability-guide.md`](./docs/ai-agent-interoperability-guide.md)

---

## 📊 Quantified Productivity & Facilitator ROI

Realistic quantitative metrics experienced by facilitators (speakers/TAs) using `workshop-harness` (80% AI automated scaffolding + 20% facilitator review/rehearsal):

| Metric | Manual Prep (Before) | With Harness (After) | Quantitative Gain | Key Skill |
| :--- | :--- | :--- | :--- | :--- |
| **Facilitator Prep Time** | **20.0 Hours (2.5 days)** | **5.0 Hours (0.5 day)** | **75% Time Saved (4x Faster)** | `generate-all` |
| **Attendee Capacity per TA** | **1 : 6 Attendees** | **1 : 25~30 Attendees** | **4-5x Support Capacity** | `live-debug-assistant` |
| **Live Debugging MTTR** | **18 Min / Case** | **0.5 Min (30s) / Case** | **36x Faster Resolution** | `live-debug-assistant` |
| **Live Session Delays** | **~35 Min Avg** | **< 3 Min** | **91.4% Delay Reduction** | `cross-architecture-checker` |
| **Facilitator Labor Savings** | 100% Baseline | **15 Hours Saved** | **~2 Days Saved / Workshop** | All 15 Skills |

> 💡 **Facilitator Live Debugging Tip**: When an attendee hits a terminal error during a live lab, invoking `live-debug-assistant` generates a 10-second hotfix command for immediate 30-second resolution.

---


## 15 Specialized Agent Skills Specification

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
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | Workshop project path | `output/open-codelabs/` (`codelab.yaml`, `steps/`), `oc` push | Converts workshop artifacts to Open Codelabs platform manifests and publishes via `oc` CLI/MCP |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | Workshop project path | `output/colab/` (`*.ipynb`, badges), `colab` CLI test | Generates Google Colab interactive notebooks (.ipynb), 'Open in Colab' badges & automated headless testing via Google Colab CLI |
| 15 | [`workshop-slide-generator`](skills/workshop-slide-generator/SKILL.md) | Workshop project path | `output/slides/` (`slides.md`, `index.html`), PDF export | Generates Marp Markdown (`slides.md`) and interactive standalone Web Presentation (`index.html`) synced with runbook |

---

## Cross-Architecture Compatibility Matrix

Participants bring a wide variety of hardware architectures. This matrix identifies known risks and mandatory fallback paths prior to the session.

| Architecture / OS | Recommended Tool | Known Risks | Mandatory Fallback Path |
| --- | --- | --- | --- |
| macOS Intel Mac (`x86_64`) | Ollama CLI (`ollama serve`) | LM Studio GPU acceleration unavailable / crashes frequently | Must provide Ollama CLI fallback guide (`docs/18-intel-mac-prep.md`) |
| macOS Apple Silicon (`arm64`) | LM Studio / Ollama / MLX | Full Metal GPU hardware acceleration supported | MLX (`mlx-lm`) optional |
| Windows x86_64 (Intel/AMD) | LM Studio / Ollama | PowerShell execution policy restriction, WSL2 required for Docker | Provide PowerShell bypass script |
| Windows ARM64 (Snapdragon) | Ollama CLI (Native) | Performance degradation under x64 emulation | Use Ollama native build |
| Linux / ChromeOS | Ollama CLI | No GUI support / Sandbox container | Use `ollama serve` terminal mode & small models (`e2b`) |

---

## CLI Tool Usage (`harness_cli.py`)

Using Python 3.9+ and `uv`, you can manage workshops via the command-line interface:

```bash
# 1. One-Click Full Workshop Generation Across All 15 Skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. Audit tech stack for cross-architecture risks
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. Loop Engineering multi-persona audit for beginner, intermediate, and advanced attendees
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4"

# 4. Test workshop code execution & markdown broken links
uv run harness_cli.py test --target my-bwai-workshop

# 5. Build PDF handout from markdown docs
uv run harness_cli.py build-pdf --target my-bwai-workshop

# 6. Export Open Codelabs bundle & manifest and push via oc CLI
uv run harness_cli.py export-codelab --target my-bwai-workshop --push
```

---

## Standard Workshop Repository Structure

```text
my-workshop-repo/
├── README.md                           # Workshop overview and quick start
├── RUNBOOK.md                          # Facilitator and TA timeline runbook
├── AGENTS.md                           # AGENTS.md open specification standard
├── CLAUDE.md                           # Claude Code CLI integration guide
├── pyproject.toml                      # Astral uv project dependency specification
├── gemma4-local-setup-guide.md          # Integrated pre-workshop setup guide
├── docs/                               # Detailed documentation (00 to 20)
│   ├── 00-architecture-compatibility-matrix.md # Architecture fallback matrix
│   ├── 00-persona-loop-review-report.md# Multi-persona loop review report
│   ├── ai-agent-interoperability-guide.md # Multi-AI agent guide
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md                       # Attendee FAQ
├── workshop/                           # Hands-on lab code
│   ├── 01_starter/                     # Starter template for attendees
│   ├── 02_final/                       # Final reference code
│   └── 03_labs/                        # Step-by-step lab instructions
├── prompt-pack/                        # Prompt pack for attendees
├── scripts/                            # Architecture check & bundling scripts
│   ├── check_architecture_compat.sh    # Architecture detector (Mac/Linux)
│   ├── check_architecture_compat.ps1   # Architecture detector (Windows)
│   ├── check_env.sh / check_env.ps1    # Environment verification scripts
│   ├── bundle_offline_assets.sh        # Emergency offline asset bundler
│   ├── verify_workshop.py              # Automated integrity auditor
│   └── generate_prep_pdf.py            # PDF handout builder
└── output/                             # Generated output files
    └── pdf/
```

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for full release history.

---

## License

[MIT License](LICENSE)
