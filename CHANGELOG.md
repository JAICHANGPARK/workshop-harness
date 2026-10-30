# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v2026.10.31] - 2026-10-31

### Fixed & Improved

- **Workshop Integrity Verifier (`templates/script-templates/verify_workshop.py`)**:
  - Stripped fenced code blocks and inline code spans prior to Markdown link auditing to eliminate false positives on example syntax in skill documentation.
  - Added `file://` URI detection and fixed hardcoded local `file://` paths across `docs/agents-spec/agents-md.md`, `docs/skills/overview.md`, `docs/skills/architecture-checker.md`, and `docs/skills/open-codelabs.md`.
  - Synchronized model currency ignore rules (`harness_cli.py`, `CHANGELOG.md`, `verify_workshop.py`) and enforced non-zero exit codes when any of the 4 verification gates fail.
- **Harness CLI & Out-of-the-Box Scaffolding (`harness_cli.py`, `pyproject.toml`)**:
  - Propagated non-zero exit codes from `harness_cli.py test` and `harness_cli.py audit-models` for CI/CD enforcement.
  - Auto-generated `.gitignore`, `docs/18-intel-mac-prep.md` (Intel Mac Ollama CLI & Colab fallback guide), and `docs/eli5-concept-cheat-sheet.md` (3-tier ELI5 AI concept cheat sheet) during `init` and `generate-all`.
  - Added `[project.scripts]` entrypoint (`workshop-harness = "harness_cli:main"`) and included `scripts/` in package build targets.
- **Documentation, Landing Page & Multilingual READMEs (`mkdocs.yml`, `docs/*`, `website/*`, `README*.md`)**:
  - Updated `mkdocs.yml`, `docs/skills/overview.md`, `docs/index.{ko,ja,zh}.md`, `website/index.html`, and `website/app.js` to reflect all 21 specialized agent skills and the 9-step `generate-all` pipeline.
  - Fixed unclosed HTML tags in `website/index.html` and fixed the `metrics-ribbon` IntersectionObserver selector in `website/app.js`.
  - Synchronized `.cursorrules` and `.windsurfrules` with October 2026 model tags and removed literal em-dash characters.

---

## [v2026.10.29] - 2026-10-29

### Added & Updated

- **21st Agent Skill: `skills/agents-cli-workshop-builder` (`google-agents-cli`)**:
  - Added full Agent Development Lifecycle (ADLC) workshop support for Google Agents CLI (`google/agents-cli`, `uvx google-agents-cli setup`, `npx skills add google/agents-cli`).
  - Integrated the 7 official agent skills (`google-agents-cli-workflow`, `google-agents-cli-scaffold`, `google-agents-cli-adk-code`, `google-agents-cli-eval`, `google-agents-cli-deploy`, `google-agents-cli-publish`, `google-agents-cli-observability`).
  - Added 3-stage ADLC lab curriculum covering scaffolding (`scaffold enhance`), synthetic trajectory dataset generation and LLM-as-a-Judge optimization (`eval dataset synthesize`, `eval run`, `eval grade`, `eval optimize`), Cloud Run / Vertex AI Agent Engine deployment (`deploy`), Gemini Enterprise registry publishing (`publish`), and Cloud Trace diagnostics (`observability`).
- **Official Multi-Language Google ADK Workshop Scaffolding (`skills/adk-workshop-builder` & `harness_cli.py`)**:
  - Upgraded `harness_cli.py init` and `generate-all` to scaffold complete starter (`01_starter`), reference solution (`02_final`), build manifests, and 3-stage hands-on lab guides (`03_labs/`) across all 5 official ADK language tracks plus Polyglot mode:
    - **Python (`--stack "python,adk,agents-cli"`)**: `google-adk`, `LlmAgent`, mandatory `root_agent` entry point, `sub_agents`, `sre_agent/` package layout, `evalset.json`, and `adk web` / `adk run` / `adk api_server` / `adk eval` / `adk deploy` workflows.
    - **Go (`--stack "go,adk"`)**: `google.golang.org/adk/v2` (`llmagent.New`, `functiontool.New` with JSON Schema struct tags, `gemini.NewModel`, `SubAgents`, `runner.New`, `session.InMemoryService()`).
    - **Java 21+ (`--stack "java,adk"`)**: `com.google.adk:google-adk` (`LlmAgent.builder()`, `SequentialAgent.builder()`, `FunctionTool.create()`, `outputKey` placeholders, `InMemoryRunner`) with Maven (`pom.xml`) and Gradle (`build.gradle`).
    - **Kotlin (`--stack "kotlin,adk"`)**: `com.google.adk:google-adk-kotlin-core` and `com.google.adk:google-adk` (`LlmAgent`, `Instruction`, `Gemini`, `FunctionTool.create(::fn)`).
    - **TypeScript (`--stack "typescript,adk"`)**: `@google/adk` with Zod-typed `FunctionTool`, `LlmAgent`, and `subAgents` on `rootAgent`.
    - **Polyglot (`--stack "adk,polyglot,agents-cli"`)**: Scaffolds Python alongside `polyglot/{go,java,kotlin,typescript}` tracks; added reference example at `examples/adk-polyglot-workshop/`.
- **October 2026 Frontier & Open-Weight AI Model Catalog Upgrade**:
  - Updated all 21 skills, templates, and CLI registries to the verified October 2026 lineup:
    - **Google Gemini (`google-genai >= 2.30.1`, `@google/genai >= 2.29.1` Interactions API)**: `gemini-4-argon` (flagship 1M context reasoning & orchestration), `gemini-3.8-flash` (default high-speed workhorse), `gemini-3.5-flash-lite`, `gemini-3.8-live`, `gemini-3.8-live-extended-thinking`, `gemini-3.5-transcribe-live`, `gemini-3.8-flash-tts`, `gemini-nano-banana-2.1`, `gemini-omni-1.1-flash`, `gemini-embedding-2`, `antigravity-preview-09-2026`.
    - **Google Gemma 4**: Cloud `gemma-4-31b-it`, `gemma-4-26b-a4b-it`; Local Ollama RAM tiers (`gemma4:e2b` for 8GB, `gemma4:e4b` for 16GB, `gemma4:e12b` / `gemma4:26b-a4b` / `gemma4:31b` for 32GB+).
    - **Anthropic Claude 5.5**: `claude-opus-5.5`, `claude-sonnet-5.5`, `claude-fable-5.1`, `claude-haiku-5.5`.
    - **OpenAI GPT-6 / 5.6**: `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-luna`, `gpt-5.6-terra`, `gpt-5.4`.
    - **Local Open-Weight**: `qwen3.6:27b`, `qwen3-coder:30b`, `qwen3:14b`, `qwen3:8b`, `deepseek-r1:14b`, `deepseek-r1:8b`, `llama4:scout`.
- **Harness CLI & Automated Verification Suite (`harness_cli.py`, `verify_workshop.py`)**:
  - Added `list-models` subcommand to inspect the 2026 model catalog by provider.
  - Added `audit-models --target <dir> --fix` subcommand to detect and auto-upgrade deprecated model strings and legacy SDK imports (`google-generativeai`).
  - Added `--model` CLI flag and `--target` alias on `init` and `generate-all`.
  - Upgraded `verify_workshop.py` to enforce 4 automated gates: markdown link integrity, code smoke tests, 2026 model/SDK currency audit, and typography/credential hygiene.
  - Enhanced `audit-loop` with real file-system inspection across the 4 attendee personas (Non-Coder, Novice, Intermediate, Senior Engineer).

---

## [v2026.08.29] - 2026-08-29

### Added & Updated

- **3 New Agent Skills (Total 20 Skills)**:
  - **`skills/android-workshop-builder`**: Builds Jetpack Compose & Kotlin 2.x Android GenAI workshops with `com.google.genai` SDK, Google `android` CLI (`android init`, `android skills add --all`, `android docs`, `android layout`, `android run`), and official Android Skills (`camerax`, `edge-to-edge`, `adaptive`, `navigation-3`, `appfunctions`, `testing-setup`).
  - **`skills/flutter-workshop-builder`**: Builds Flutter GenAI workshops with Flutter 3.x, `google_generative_ai`, official Flutter Agent Plugins (`github.com/flutter/agent-plugins`), Package Skills (`docs.flutter.dev/ai/package-skills` / `dart run skills@ get`), Dart & Flutter MCP Server diagnostics, and zero-install Flutter Web fallback.
  - **`skills/a2ui-workshop-builder`**: Builds Generative UI & dynamic surface workshops on A2UI (`a2ui.org`) protocol and Flutter `genui` SDK (`genui`, `genui_catalog`), covering `WidgetCatalog` registration, `SurfaceController` streaming, and interactive action loops.
- **CLI Engine & Scaffolding Updates (`harness_cli.py`)**:
  - Added `--stack android` and `--stack "flutter,genui,a2ui"` scaffolding support with build definitions, manifests, and test entrypoints.
  - Extended `audit-compat` for AVD emulator CPU virtualization and Flutter platform requirements.
- **Prerequisite Guides & Environment Scripts**:
  - Updated `templates/doc-templates/02_prerequisites.md`, `check_env.sh`, and `check_env.ps1` to verify `android` CLI, Flutter SDK, Dart toolchain, and Android development tools.

---

## [v2026.08.26] - 2026-08-26

### Added & Updated

- **Gemini 3.7 Flash & Google GenAI SDK Support**:
  - Integrated `gemini-3.7-flash` as primary workhorse model for coding and agentic tasks.
  - Added support for thinking budget control (`thinking_config` / `thinkingLevel`).
  - Standardized on unified `google-genai` Python and `@google/genai` JavaScript/TypeScript SDKs.
- **Gemini Live API & Real-Time Multimodal Streaming**:
  - Added full support for `gemini-3.1-flash-live-preview` (low-latency voice/audio/video) and `gemini-3.5-live-translate-preview`.
  - Added pub.dev `gemini_live` Flutter package integration (zero Firebase dependency, direct WebSocket streaming).
  - Added 3-step Gemini Live real-time curriculum track to `hands-on-curriculum-builder`.
  - Added acoustic echo/VAD prevention and microphone permission audit rules to `cross-architecture-checker` and `prerequisite-checker`.
- **Next-Gen Model Specifications**:
  - Added Anthropic Claude Generation 5 (`claude-sonnet-5`, `claude-opus-5`, `claude-fable-5`).
  - Added OpenAI GPT-5.6 series (`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`).
- **On-Device AI & LiteRT-LM Integration**:
  - Added Google LiteRT-LM, Gemma 4 (`.litertlm`), and Apple MLX (`mlx-lm`) on-device hands-on lab guidelines.
- **15 Agent Skills Metadata & Localization Sync**:
  - Synchronized 15 skills metadata across `docs/`, `README.md`, `CLAUDE.md`, `AGENTS.md`, and `website/app.js` (EN, KO, JA, ZH).

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
