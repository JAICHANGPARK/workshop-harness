# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v2026.08.16] - 2026-08-16

### Added

- **14th Agent Skill: `colab-workshop-integrator`**:
  - Automatically transforms workshop labs and starter/final code into interactive Google Colab Jupyter Notebooks (`.ipynb`).
  - Injects zero-setup cells: automated `%pip install`, GPU accelerator verification (`!nvidia-smi`), and Colab Secrets credential handling (`google.colab.userdata`).
  - Generates 'Open in Colab' SVG badges and Colab README documentation.
  - Integrates with official [Google Colab CLI (`colab-cli`)](https://github.com/googlecolab/google-colab-cli) for automated headless cloud execution and smoke testing.
- **15th Agent Skill: `workshop-slide-generator`**:
  - Generates publication-ready presentation slide decks in Marp Markdown (`output/slides/slides.md`) and standalone zero-dependency interactive Web Presentations (`output/slides/index.html`).
  - Syncs 1:1 with facilitator timeline markers in `RUNBOOK.md`.
  - Supports instant PDF/PPTX compilation via Marp CLI.
- **CLI Commands (`harness_cli.py`)**:
  - Added `build-slides` command with `--target`, `--output`, and `--export-pdf` flags.
  - Added `export-colab` command with `--target`, `--output`, `--repo`, and `--test` flags.
  - Added `test-colab` command for one-click Colab CLI verification.
  - Updated `generate-all` pipeline to full 8-step orchestrator across all 15 skills.
- **Documentation & Agent Standards**:
  - Expanded `AGENTS.md`, multi-language READMEs (EN, KR, JA, ZH), and MkDocs documentation to 15 specialized skills.

---

## [v2026.08.01] - 2026-08-01

### Changed

- **Full English Localization**:
  - Fully translated all 12 `SKILL.md` instruction files to English to ensure global AI agent compatibility across Claude Code, Aider, Cursor, Codex, and Antigravity.
  - Translated all core document templates in `templates/doc-templates/` (Hardware & Env, Prerequisites, Session Guide, Prompt Pack, Troubleshooting FAQ, Facilitator Runbook, FAQ Generator, Persona Loop Review) to English.
  - Updated python scripts (`generate_prep_pdf.py`, `verify_workshop.py`) and `harness_cli.py` docstrings and generated template strings to English.

---

## [v2026.07.30] - 2026-07-30

### Added

- **12 Specialized Agent Skills** for end-to-end workshop automation:
  - `workshop-scaffolder`: Standard repository structure scaffolding
  - `cross-architecture-checker`: Apple Silicon, Intel Mac, Windows, Linux compatibility audit & fallback matrix
  - `prerequisite-checker`: OS-specific SDK/language installation guides, Google AI Studio & GCP Vertex AI API Key issuance steps, and automated `check_env.sh/ps1` verification scripts
  - `hands-on-curriculum-builder`: Step-by-step lab curriculum, starter vs final code, prompt packs with mandatory references protocol
  - `pdf-handout-generator`: ReportLab + PyMuPDF based PDF handout builder with contact sheet preview
  - `workshop-troubleshooter`: RAM-tier (8G/16G/32G+) and OS-specific troubleshooting matrix
  - `workshop-runbook-generator`: Minute-by-minute facilitator & TA timeline runbook (`RUNBOOK.md`)
  - `live-debug-assistant`: 10-second terminal error hotfix diagnosis & API Key security protocol
  - `workshop-faq-generator`: Attendee FAQ auto-generation for hardware, network, and code questions
  - `workshop-tester`: Code execution smoke tests & markdown broken relative link auditor
  - `workshop-web-researcher`: Live web search for latest tool/SDK/AI model release tags & breaking change prevention
  - `workshop-persona-loop-evaluator`: Loop Engineering multi-persona review for beginner, intermediate, and advanced attendees

- **CLI Automation Tool (`harness_cli.py`)**:
  - `generate-all`: One-Click Full Orchestrator triggering all 12 skills in sequence
  - `init`: Workshop project scaffolding with templates, scripts, and directory structure
  - `audit-compat`: Cross-architecture tech stack risk auditing
  - `audit-loop`: Loop Engineering multi-persona evaluation
  - `test`: Code smoke tests & markdown link integrity verification
  - `build-pdf`: Publication-ready PDF handout generation

- **Astral uv Integration**:
  - `pyproject.toml` for declarative dependency management
  - Auto-install of `reportlab`, `pymupdf`, `pillow` via `uv` on first run
  - All CLI commands support `uv run harness_cli.py` execution

- **Open AI Agent Standard**:
  - `AGENTS.md` adopting the open [agents.md](https://agents.md/) specification for vendor-agnostic agent interoperability
  - `CLAUDE.md` for Anthropic Claude Code CLI users

- **Dynamic AI Model Discovery Protocol**:
  - Prevents legacy model hardcoding (`gpt-3.5`, `llama-2`, `gemma-1`) via mandatory web search verification
  - Timestamped currency labels on all generated documentation

- **Google AI Studio & GCP Vertex AI Key Issuance Guide**:
  - Step-by-step Gemini API Key issuance via AI Studio
  - GCP Service Account JSON key generation for Vertex AI
  - `.env.sample` and `.gitignore` security enforcement

- **Mandatory References Protocol**:
  - All generated documents include `References` section with official documentation URLs and source citations

- **Multilingual README Support**:
  - `README.md` (English, primary)
  - `README_KR.md` (Korean)
  - `README_JA.md` (Japanese)
  - `README_ZH.md` (Chinese)

- **Repository Banner Image** (`assets/workshop_harness_banner.jpg`)

- **Document & Script Templates** (8 doc templates, 10+ script templates)

- **Example Project** (`examples/one-click-demo-workshop/`)

### References

- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
