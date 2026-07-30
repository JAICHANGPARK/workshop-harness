![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.07.30-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

---

## Overview

Workshop Harness is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit designed for event organizers, speakers, and TAs orchestrating technical workshops, Build with AI (BWAI) events, DevFests, and hands-on coding labs.

It standardizes the proven architecture and operational battle-tested workflows from real-world events including:
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)

---

## Table of Contents

- [Overview](#overview)
- [One-Click Full Orchestration](#one-click-full-orchestration)
- [AI Agent Interoperability (Claude, Codex, Antigravity, Cursor)](#ai-agent-interoperability-claude-codex-antigravity-cursor)
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
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## AI Agent Interoperability (Claude, Codex, Antigravity, Cursor)

Workshop Harness is designed to be 100% vendor-agnostic and works seamlessly across all AI coding tools and LLMs:

- **Anthropic Claude (Claude Code CLI & Desktop)**: See [`CLAUDE.md`](./CLAUDE.md)
- **OpenAI Codex, ChatGPT & Aider**: See [`CODEX.md`](./CODEX.md) or [`AGENTS.md`](./AGENTS.md)
- **Google Antigravity & Gemini CLI**: Standard native `.gemini/skills/` integration
- **Cursor & Windsurf IDE**: Integrated via `.cursorrules` and `AGENTS.md`
- **Full Guide**: See [`docs/ai-agent-interoperability-guide.md`](./docs/ai-agent-interoperability-guide.md)

---

## 12 Specialized Agent Skills Specification

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

Using Python 3.9+, you can manage workshops via the command-line interface:

```bash
# 1. One-Click Full Workshop Generation Across All 12 Skills
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. Audit tech stack for cross-architecture risks
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. Loop Engineering multi-persona audit for beginner, intermediate, and advanced attendees
python3 harness_cli.py audit-loop --topic "Local RAG with Gemma 4"

# 4. Test workshop code execution & markdown broken links
python3 harness_cli.py test --target my-bwai-workshop

# 5. Build PDF handout from markdown docs
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## Installing Agent Skills

Install all 12 skills into your local agent environment (`~/.gemini/skills`):

```bash
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

---

## Standard Workshop Repository Structure

```text
my-workshop-repo/
├── README.md                           # Workshop overview and quick start
├── RUNBOOK.md                          # Facilitator and TA timeline runbook
├── CLAUDE.md                           # Claude Code CLI integration guide
├── CODEX.md                            # OpenAI Codex & ChatGPT integration guide
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
