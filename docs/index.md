# Workshop Harness

> **AI Agent Harness, 16 Skill Suite & CLI Automation Toolkit** for Technical Workshops (Build with AI, DevFest, Hands-on Labs)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)

---

## Overview

**Workshop Harness** is a one-click AI agent orchestration toolkit designed for organizers, speakers, facilitators, and teaching assistants (TAs) hosting technical workshops (Build with AI, DevFest, community developer labs).

Adhering to the [AGENTS.md open specification](https://agents.md/), this harness provides seamless native interoperability across all AI coding agents including **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Cursor**, and **Aider**.

---

## Key Features

- **One-Click Full Generation (`generate-all`)**: Runs an 8-step automated pipeline across all 16 agent skills to generate repo scaffolds, guides, architecture compatibility audits, persona loop evaluations, smoke tests, PDF handouts, Open Codelabs bundles, Google Colab notebooks, and presentation slide decks in under 60 seconds.
- **16 Agent Skills (`skills/*`)**: Packed with 16 specialized agent skills capturing real-world workshop facilitation expertise.
- **Presentation Slide Deck Generator**: Automatically builds Marp Markdown (`slides.md`) and zero-dependency interactive Web Presentations (`index.html`) synced 1:1 with facilitator runbook markers.
- **Google Colab & Colab CLI Integration**: Converts workshops into interactive Jupyter Notebooks (`.ipynb`) with 'Open in Colab' badges, GPU checks, Colab Secrets, and automated headless testing via the official [Google Colab CLI](https://github.com/googlecolab/google-colab-cli).
- **Cross-Architecture Audit**: Automatically diagnoses hardware & GPU compatibility risks across Apple Silicon (M1~M4), Intel Mac (x86_64), Windows (x64/Snapdragon ARM64), and Linux/ChromeOS environments with mandatory fallback guidance.
- **Open Codelabs Platform Integration**: Exports standard Open Codelabs bundles (`codelab.yaml`) and pushes directly via `oc` CLI & stdio MCP server (`oc mcp serve`).
- **Publication-Ready PDF Handouts**: Generates printable PDF preparation guides and thumbnail contact sheets via ReportLab and PyMuPDF engines.

---

## Quickstart Guide

```bash
# 1. Clone repository
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. Auto-install 16 skills to local agent environment (~/.gemini/skills)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. One-click full workshop generation
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## Production Proven

Workshop Harness has been battle-tested across major community technical workshops:

- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
- [Open Codelabs Platform](https://github.com/JAICHANGPARK/open-codelabs)
