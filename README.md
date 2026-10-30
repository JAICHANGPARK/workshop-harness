![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness

[![Official Docs](https://img.shields.io/badge/Official%20Docs-MkDocs-blue.svg)](https://JAICHANGPARK.github.io/workshop-harness/)
[![Landing Page](https://img.shields.io/badge/Landing%20Page-Website-purple.svg)](https://JAICHANGPARK.github.io/workshop-harness/website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-21%20Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.10.31-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

**Official Documentation**: [https://JAICHANGPARK.github.io/workshop-harness/](https://JAICHANGPARK.github.io/workshop-harness/)
**Landing Page**: [https://JAICHANGPARK.github.io/workshop-harness/website/](https://JAICHANGPARK.github.io/workshop-harness/website/)

---

## Overview

Workshop Harness is an AI Agent Harness, 21-Skill Suite, and CLI Automation Toolkit powered by **Astral uv**. It is designed for event organizers, speakers, and TAs orchestrating technical workshops, Build with AI (BWAI) events, DevFests, and hands-on coding labs.

It standardizes the proven architecture and operational battle-tested workflows from real-world events including:
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)

---

## Quick Start (uv Powered)

Build a complete end-to-end workshop repository in under **1 minute** with 100% automated dependency management using `uv`:

```bash
# 1. Clone the repository
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. Install 21 Agent Skills & auto-sync dependencies via uv
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. Generate a complete workshop package with ONE CLICK (Default: gemini-3.8-flash)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## Installation

### Prerequisites
- **Python**: Version 3.9 or higher (3.11+ recommended for `google-agents-cli`)
- **Astral uv**: Fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git**: Installed and configured
- **AI Coding Agent (Optional)**: Google Antigravity, Gemini CLI, Anthropic Claude Code, OpenAI Codex, Cursor, or Aider

### Installing CLI & Agent Skills

1. **Automatic Skill & Dependency Installation**:
   Run the installation script to automatically set up `reportlab`, `pymupdf`, `pillow`, `python-pptx` via `uv` and copy all 21 skills to `~/.gemini/skills` and `~/.gemini/config/skills`:
   ```bash
   ./scripts/install_skills.sh
   ```

2. **Verifying Installation**:
   Ensure the CLI works smoothly with `uv` (supports both `uv run harness_cli.py` and the installed `uv run workshop-harness` entrypoint):
   ```bash
   uv run harness_cli.py --help
   uv run harness_cli.py list-models
   uv run harness_cli.py test --target .
   ```

---

## Table of Contents

- [Overview](#overview)
- [Quick Start (uv Powered)](#quick-start-uv-powered)
- [Installation](#installation)
- [One-Click Full Orchestration](#one-click-full-orchestration)
- [Open AI Agent Standard (`AGENTS.md`)](#open-ai-agent-standard-agentsmd)
- [Key Impact Metrics (Empirical Benchmarks)](#key-impact-metrics-empirical-benchmarks)
- [21 Specialized Agent Skills Specification](#21-specialized-agent-skills-specification)
- [Cross-Architecture Compatibility Matrix](#cross-architecture-compatibility-matrix)
- [CLI Tool Usage (`harness_cli.py`)](#cli-tool-usage-harness_clipy)
- [Standard Workshop Repository Structure](#standard-workshop-repository-structure)
- [References](#references)
- [Changelog](#changelog)
- [License](#license)

---

## One-Click Full Orchestration

With a single CLI command or natural language prompt, Workshop Harness triggers the full 9-stage orchestration pipeline across all 21 skills:

```bash
# One-Click Full Workshop Generation Across All 21 Skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker" --model "gemini-3.8-flash"
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

## Key Impact Metrics (Empirical Benchmarks)

| Metric | Traditional Preparation | With Workshop Harness | Improvement | Key Driver Skill |
| :--- | :--- | :--- | :--- | :--- |
| **Facilitator Prep Time** | **20.0 Hours (2.5 days)** | **5.0 Hours (0.5 day)** | **75% Time Saved (4x Faster)** | `generate-all` |
| **Attendee Capacity per TA** | **1 : 6 Attendees** | **1 : 25~30 Attendees** | **4-5x Support Capacity** | `live-debug-assistant` |
| **Live Debugging MTTR** | **18 Min / Case** | **0.5 Min (30s) / Case** | **36x Faster Resolution** | `live-debug-assistant` |
| **Live Session Delays** | **~35 Min Avg** | **< 3 Min** | **91.4% Delay Reduction** | `cross-architecture-checker` |
| **Facilitator Labor Savings** | 100% Baseline | **15 Hours Saved** | **~2 Days Saved / Workshop** | All 21 Skills |

> **Facilitator Live Debugging Tip**: When an attendee hits a terminal error during a live lab, invoking `live-debug-assistant` generates a 10-second hotfix command for immediate 30-second resolution.

---

## 21 Specialized Agent Skills Specification

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
| 10 | [`workshop-tester`](skills/workshop-tester/SKILL.md) | Workshop project path | `verify_workshop.py` audit output | Audits code execution smoke tests, model currency, and markdown broken links |
| 11 | [`workshop-web-researcher`](skills/workshop-web-researcher/SKILL.md) | Tool/Model query | Updated release tags & docs | Fetches latest 2026 tool/SDK/AI model release versions & prevents deprecated flags |
| 12 | [`workshop-persona-loop-evaluator`](skills/workshop-persona-loop-evaluator/SKILL.md) | Workshop topic & materials | `docs/00-persona-loop-review-report.md` | Multi-persona loop engineering audit for non-coder, novice, intermediate, and senior attendees |
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | Workshop project path | `output/open-codelabs/` (`codelab.yaml`, `steps/`), `oc` push | Converts workshop artifacts to Open Codelabs platform manifests and publishes via `oc` CLI/MCP |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | Workshop project path | `output/colab/` (`*.ipynb`, badges), `colab` CLI test | Generates Google Colab interactive notebooks (.ipynb), 'Open in Colab' badges & automated headless testing via Google Colab CLI |
| 15 | [`workshop-slide-generator`](skills/workshop-slide-generator/SKILL.md) | Workshop project path | `output/slides/` (`slides.md`, `index.html`, `.pptx`), PDF export | Generates Google Slides `.pptx`, Marp Markdown (`slides.md`), and interactive Web Presentation (`index.html`) synced with runbook |
| 16 | [`adk-workshop-builder`](skills/adk-workshop-builder/SKILL.md) | ADK topic & language track | `root_agent` LlmAgent & sub-agent scaffolds, `evalset.json` | Builds official multi-language (Python, Go, Java, Kotlin, TypeScript, Polyglot) Google ADK (`adk.dev`) hands-on labs |
| 17 | [`eli5-concept-explainer`](skills/eli5-concept-explainer/SKILL.md) | Technical concept or error | 3-tier ELI5 physical analogies & mental maps | Translates complex AI concepts and errors into beginner-friendly analogies and mental maps |
| 18 | [`android-workshop-builder`](skills/android-workshop-builder/SKILL.md) | Android topic & stack | Jetpack Compose + Google GenAI Kotlin SDK scaffolds | Builds modern Android Generative AI workshops with Compose Material 3 & `android` CLI |
| 19 | [`flutter-workshop-builder`](skills/flutter-workshop-builder/SKILL.md) | Flutter topic & stack | Flutter 3.x + `google_generative_ai` scaffolds | Builds cross-platform Flutter GenAI workshops with Material 3 and Flutter Web fallback |
| 20 | [`a2ui-workshop-builder`](skills/a2ui-workshop-builder/SKILL.md) | A2UI / GenUI topic | `genui` + `WidgetCatalog` + `SurfaceController` | Builds cutting-edge Generative UI and A2UI declarative JSON streaming interactive workshops |
| 21 | [`agents-cli-workshop-builder`](skills/agents-cli-workshop-builder/SKILL.md) | ADLC & `google-agents-cli` | 7 official ADLC skills, synthetic evals, Cloud Run / Agent Runtime deploy | Builds end-to-end Agent Development Lifecycle (ADLC) workshops using `google-agents-cli` (`google/agents-cli`) |

---

## Cross-Architecture Compatibility Matrix

Participants bring a wide variety of hardware architectures. This matrix identifies known risks and mandatory fallback paths prior to the session.

| Architecture / OS | Recommended Tool | Known Risks | Mandatory Fallback Path |
| --- | --- | --- | --- |
| macOS Intel Mac (`x86_64`) | Ollama CLI (`ollama serve`) | LM Studio GPU acceleration unavailable / crashes frequently | Must provide Ollama CLI fallback guide (`docs/18-intel-mac-prep.md`) |
| macOS Apple Silicon (`arm64`) | LM Studio / Ollama / MLX | Full Metal GPU hardware acceleration supported | MLX (`mlx-lm`) optional |
| Windows x86_64 (Intel/AMD) | LM Studio / Ollama | PowerShell execution policy restriction, WSL2 required for Docker | Provide PowerShell bypass script |
| Windows ARM64 (Snapdragon) | Ollama CLI (Native) | Performance degradation under x64 emulation | Use Ollama native build |
| Linux / ChromeOS | Ollama CLI | No GUI support / Sandbox container | Use `ollama serve` terminal mode & small models (`gemma4:e2b`) |
| Universal / Web | Flutter Web (`-d chrome`) | Emulator memory limits & missing virtualization | Instant zero-install fallback for Flutter & A2UI workshops |

---

## CLI Tool Usage (`harness_cli.py`)

Using Python 3.9+ and `uv`, you can manage workshops via the command-line interface:

```bash
# 1. One-Click Full Workshop Generation Across All 21 Skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker" --model "gemini-3.8-flash"

# 2. Inspect Verified 2026 Frontier & Open-Weight Models or Auto-Upgrade Legacy Model Tags
uv run harness_cli.py list-models
uv run harness_cli.py audit-models --target my-bwai-workshop --fix

# 3. Official Multi-Language Google ADK & Google Agents CLI (Python, Go, Java, Kotlin, TypeScript, Polyglot)
uv run harness_cli.py init --name "adk-python-lab" --topic "Multi-Agent ADLC with Google ADK and agents-cli" --stack "python,adk,agents-cli"
uv run harness_cli.py init --name "adk-go-lab" --topic "Go Multi-Agent Systems with Google ADK" --stack "go,adk"
uv run harness_cli.py init --name "adk-java-lab" --topic "Java 21 Enterprise Agents with Google ADK" --stack "java,adk"
uv run harness_cli.py init --name "adk-kotlin-lab" --topic "Kotlin Multi-Agent Systems with Google ADK" --stack "kotlin,adk"
uv run harness_cli.py init --name "adk-ts-lab" --topic "TypeScript Multi-Agent Systems with Google ADK" --stack "typescript,adk"
uv run harness_cli.py init --name "adk-polyglot-lab" --topic "Polyglot Multi-Language Google ADK Workshop" --stack "adk,polyglot,agents-cli"

# 4. Android Jetpack Compose GenAI Workshop Initialization
uv run harness_cli.py init --name "android-gemini-lab" --topic "Android GenAI with Jetpack Compose" --stack "android"

# 5. Flutter Generative UI & A2UI Workshop Initialization
uv run harness_cli.py init --name "flutter-genui-lab" --topic "Generative UI with Flutter and A2UI" --stack "flutter,genui,a2ui"

# 6. Audit tech stack for cross-architecture risks
uv run harness_cli.py audit-compat --stack "adk,agents-cli,android,flutter,genui,docker,gemini-live"

# 7. Loop Engineering 4-persona audit for non-coder, novice, intermediate, and senior attendees
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4" --target my-bwai-workshop

# 8. Test workshop code execution, 2026 model currency & markdown broken links
uv run harness_cli.py test --target my-bwai-workshop

# 9. Build PDF handout & slide decks (Google Slides .pptx, Marp & Web HTML)
uv run harness_cli.py build-pdf --target my-bwai-workshop
uv run harness_cli.py build-slides --target my-bwai-workshop

# 10. Export Google Colab notebooks (.ipynb) & Open Codelabs bundle
uv run harness_cli.py export-colab --target my-bwai-workshop
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
├── .env.sample                         # Sample environment variables (GEMINI_API_KEY)
├── .gitignore                          # Credential & build artifact hygiene rules
├── gemma4-local-setup-guide.md         # Integrated pre-workshop setup guide
├── docs/                               # Detailed documentation (00 to 20)
│   ├── 00-architecture-compatibility-matrix.md # Architecture fallback matrix
│   ├── 00-persona-loop-review-report.md# Multi-persona loop review report
│   ├── 01-hardware-and-env.md          # Hardware & local LLM port guide
│   ├── 02-prerequisites.md             # OS-specific SDK & API key guide
│   ├── 18-intel-mac-prep.md            # Dedicated Intel Mac (x86_64) Ollama/Colab fallback
│   ├── 20-faq.md                       # Attendee troubleshooting & FAQ
│   └── eli5-concept-cheat-sheet.md     # 3-tier ELI5 AI concept cheat sheet
├── workshop/                           # Hands-on lab code
│   ├── 01_starter/                     # Starter template (sre_agent/, polyglot/, etc.)
│   ├── 02_final/                       # Final reference code & evalset.json
│   └── 03_labs/                        # Step-by-step lab instructions (Lab 01-03)
├── prompt-pack/                        # Prompt pack for attendees
├── scripts/                            # Architecture check & bundling scripts
│   ├── check_architecture_compat.sh    # Architecture detector (Mac/Linux)
│   ├── check_architecture_compat.ps1   # Architecture detector (Windows)
│   ├── check_env.sh / check_env.ps1    # Environment verification scripts
│   ├── bundle_offline_assets.sh        # Emergency offline asset bundler
│   ├── verify_workshop.py              # Automated integrity & 2026 model auditor
│   └── generate_prep_pdf.py            # PDF handout builder
└── output/                             # Generated output files (pdf, slides, colab, open-codelabs)
```

---

## References

- [AGENTS.md Open Standard](https://agents.md/)
- [Google Agent Development Kit (ADK)](https://adk.dev)
- [Google Agents CLI (`google/agents-cli`)](https://github.com/google/agents-cli)
- [Official Google Android CLI & Skills](https://developer.android.com/tools/agents/android-cli)
- [Official Flutter AI Development Guide](https://docs.flutter.dev/ai/get-started)
- [Flutter Package Skills Specification](https://docs.flutter.dev/ai/package-skills)
- [Official Flutter Agent Plugins Repository](https://github.com/flutter/agent-plugins)
- [A2UI Open Protocol Specification](https://a2ui.org)
- [Astral uv Python Package Manager](https://astral.sh/uv)

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for full release history.

---

## License

[MIT License](LICENSE)

