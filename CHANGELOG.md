# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v2026.11.14] - 2026-11-14

### Changed & Improved

- **Modular Core Package Architecture (`harness/` & `harness_cli.py`)**:
  - Refactored the 4,200-line monolithic `harness_cli.py` into a modular `harness/` Python package (`harness/registry.py`, `harness/router.py`, `harness/scaffolder.py`, `harness/auditors.py`, `harness/exporters.py`) while keeping `harness_cli.py` (~180 lines) 100% backward-compatible with all public symbols and CLI subcommands.
- **Prompt Language Auto-Detection (`KO`/`JA`/`ZH`/`EN`) & 3-Step Agent Tailoring Protocol**:
  - Added `detect_prompt_language()` to `harness/router.py` (`parse_natural_prompt()["lang"]`) and `--lang` support on `init` / `generate-all`, generating localized `README.md` and `RUNBOOK.md` in natural developer terminology (`English Original (개발자 친화적 용어)`) for Korean, Japanese, and Chinese prompts.
  - Updated `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and `.windsurfrules` with the explicit 3-Step Autonomous Loop (1. Pre-flight Web Search -> 2. 9-Step `harness_cli.py prompt` Build -> 3. Domain & Language Tailoring + Bundle Rebuild & `test`).
- **Provider-Neutral Preparation Guide (`SETUP_GUIDE.md`) & 22-Skill Metadata Sync**:
  - Generalized the scaffolded root preparation guide from `gemma4-local-setup-guide.md` to `SETUP_GUIDE.md` across all cloud and local tracks (retaining automatic fallback support in `export_open_codelabs.py`).
  - Synchronized `pyproject.toml` (`version = "2026.11.14"`, wheel/sdist `harness` package inclusion) and aligned the 22-skill index (`eli5` included) across `AGENTS.md`, `CLAUDE.md`, and `scripts/install_skills.sh`.

---

## [v2026.11.13] - 2026-11-13

### Added & Upgraded

- **November 2026 Google Gemini 4 & Multimodal Ecosystem Upgrade (`harness_cli.py`, `skills/workshop-web-researcher/SKILL.md`, `templates/script-templates/verify_workshop.py`)**:
  - Upgraded `MODEL_REGISTRY["google-gemini"]` with Google DeepMind's November 2026 releases:
    - **`gemini-4-carbon`** (`flagship_reasoning`): GA frontier reasoning model for sustained agentic coding, multi-agent coordination (`root_agent`), scientific discovery, and cybersecurity defense (1M unified context window, configurable `thinking_level`: `low`, `medium`, `high`).
    - **`gemini-4-hydrogen`** (`default_workhorse`): GA high-efficiency Gemini 4 workhorse for rapid agentic execution, Search AI Mode query fan-out, everyday coding, and parallel sub-agent workers (1M input / up to 1M output context window, flat-priced, configurable `thinking_level`: `low`, `medium`, `high`, `xhigh`).
    - **`gemini-4-argon`** (`enterprise_reasoning`): Retained as active enterprise frontier reasoning model alongside **`gemini-3.8-flash`** (`fast_multimodal_flash`).
    - **`gemini-omni-1.2-flash`** (`video_omni`): GA video generation and conversational editing model superseding `gemini-omni-1.1-flash`.
    - **`gemini-embedding-2`** (`embedding_multimodal`): Promoted to GA and added deprecation auto-upgrade from `gemini-embedding-2-preview`.
    - **`gemini-3.8-flash-tts`**: Documented Voice Remixing (`POST /v1beta/voices`) alongside Nano Banana 2.1 (`gemini-nano-banana-2.1` / `gemini-3.1-flash-image`) video-to-image context support.
- **Unified Google GenAI v3 & Multi-Platform SDK Upgrades**:
  - Upgraded scaffolded Python dependencies to `google-genai>=3.0.0` (default Gemini Developer API `v1` and `httpx2`) and `google-adk>=2.14.0`, plus `google-agents-cli>=1.4.1` in ADLC documentation.
  - Upgraded TypeScript / Node.js scaffolds to `@google/genai@^3.0.0` (Node.js 22+), Java scaffolds to `com.google.genai:google-genai:2.1.0`, Android Compose scaffolds to `com.google.genai:google-genai-kotlin-android:1.8.0`, and Flutter GenUI / A2UI documentation to include `a2ui_flutter` (`^0.1.0`) and `a2ui_core` (`^0.5.0`) on Flutter 3.38+ / Dart 3.10+.
- **November 2026 Anthropic Claude & OpenAI Multi-Provider Ecosystem Upgrade (`harness_cli.py`, `templates/`, `scripts/`, `skills/`)**:
  - Upgraded `MODEL_REGISTRY["anthropic-claude"]` to canonical hyphenated API model IDs (all 1M context, 128K output on API `2026-10-21`): **`claude-fable-5-2`** (`apex_agentic`, GA Nov 9, 2026), **`claude-opus-5-5`** (`flagship_reasoning`), **`claude-sonnet-5-5`** (`default_workhorse`), and **`claude-haiku-5-5`** (`fast_haiku`), paired with `anthropic>=2.8.0`, `claude-agent-sdk>=0.2.181`, and `@anthropic-ai/sdk@^1.7.0`.
  - Upgraded `MODEL_REGISTRY["openai-gpt"]` to November 2026 Responses API models: **`gpt-6-astra`** (`flagship_reasoning`), **`gpt-6.1-sol`** (`default_workhorse`), **`gpt-6.1-terra`** (`multimodal_computer_use`, superseding `gpt-5.6-terra` and `gpt-5.4`), **`gpt-6-luna`** (`fast_lite`), **`gpt-image-2.6-sunburst`** (`image_default`), and **`gpt-image-2.6-flare`** (`image_fast`), paired with `openai>=3.50.0` (Python), `openai-agents>=0.24.0`, and `openai@^7.55.0` (TypeScript).
  - Added native multi-provider workshop scaffolding (`--stack "python,claude"`, `--stack "python,openai"`, `--stack "typescript,claude"`, `--stack "typescript,openai"`, and `--stack "python,adk,claude"` / `--stack "python,adk,openai"` via `LiteLlm` with `litellm>=1.84.0`) across `pyproject.toml`, `.env.sample`, `RUNBOOK.md`, `check_env.sh/ps1`, Colab `.ipynb` exporters, and starter/reference code.
  - Added **Zero-Config Natural Language Prompt Router (`prompt` / `from-prompt` / `--prompt` & bare prompt invocation)** via `parse_natural_prompt()` and `generate_from_prompt()`, enabling users and AI coding agents to pass Korean/English/Japanese/Chinese prompts (e.g. `"Claude 최신 모델로 멀티 에이전트 워크숍 만들어줘"`, `"OpenAI GPT로 Structured Output (JSON 스키마 응답) 핸즈온 랩 만들어줘"`) and immediately generate the complete 9-step workshop package without manual CLI flag selection.
- **November 2026 Google Gemma 4, EmbeddingGemma 2 & Specialized Gemma Catalog (`harness_cli.py`, `templates/`, `skills/`)**:
  - Expanded `MODEL_REGISTRY["google-gemma"]` and `MODEL_REGISTRY["local-ollama"]` with verified November 2026 Gemma open-weight models (Apache 2.0):
    - **Gemma 4 Core**: Cloud/HF (`gemma-4-31b-it`, `gemma-4-26b-a4b-it`, `gemma-4-12b-it`, `gemma-4-e4b-it`, `gemma-4-e2b-it`) and canonical Ollama tags (`gemma4:e2b`, `gemma4:e4b`, `gemma4:12b`, `gemma4:26b`, `gemma4:31b`).
    - **EmbeddingGemma 2 (`embeddinggemma-2`, GA Oct 2026)**: Multimodal 768-dimensional Matryoshka Representation Learning (MRL: `768` -> `512`/`256`/`128`, 8K context, 100+ languages) modular variants (`embeddinggemma-2` / `:740m` full multimodal, `:570m` text+code+audio, `:440m` text+code+vision, `:270m` text+code 304 MB lightweight) and `google/embeddinggemma-2`.
    - **Specialized Gemma Family**: `translategemma` (55-language text/visual translation), `functiongemma` (270M on-device Function Calling), `medgemma1.5` (clinical EHR & CT/MRI/X-ray/histopathology), and `shieldgemma` (ShieldGemma 2 safety policy classifier).
  - Added `embed_with_embeddinggemma2()` (Ollama `/api/embed` with 256d MRL truncation and offline fallback) in generated Gemma/EmbeddingGemma RAG scaffolds, natural language prompt detection (`"Gemma 4와 EmbeddingGemma 2로 로컬 멀티모달 RAG 워크숍 만들어줘"`, `"TranslateGemma로 다국어 번역 핸즈온 만들어줘"`), and deprecated tag auto-upgrades (`gemma2:*`, `gemma3:*`, `gemma4:e12b` -> `gemma4:12b`, `gemma4:26b-a4b` -> `gemma4:26b`, `embeddinggemma:300m` -> `embeddinggemma-2:270m`, `embeddinggemma:latest` -> `embeddinggemma-2`).
- **Deprecated Model Auto-Auditor (`audit-models` & `verify_workshop.py`)**:
  - Added automatic detection and `--fix` migration rules for `gemini-3.7-flash` -> `gemini-4-hydrogen`, `gemini-omni-1.1-flash` -> `gemini-omni-1.2-flash`, `gemini-embedding-2-preview` -> `gemini-embedding-2`, `claude-fable-5.1` / `claude-fable-5-1` -> `claude-fable-5-2`, dot-notation `claude-{opus,sonnet,haiku}-5.5` -> hyphenated `claude-{opus,sonnet,haiku}-5-5`, `gpt-5.6-terra` / `gpt-5.4` -> `gpt-6.1-terra`, `gpt-4.1` -> `gpt-6.1-sol`, and retired `o1-mini` / `o3-mini` / `o4-mini` tags, plus `sk-ant-...` / `sk-proj-...` key leak checks.
  - Refreshed all 3 reference example workshops (`examples/adk-polyglot-workshop`, `examples/one-click-demo-workshop`, `examples/sample-bwai-workshop`), agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`), multilingual READMEs, and unit tests (`tests/test_harness.py`).

---

## [v2026.11.03] - 2026-11-03

### Fixed & Improved

- **Workshop Scaffolding & Curriculum Generator (`harness_cli.py`)**:
  - Generated a dedicated, lightweight workshop `pyproject.toml` (`[tool.uv] package = false`, `google-genai>=2.30.1`, `pydantic>=2.0.0`, `requests>=2.31.0`, plus `google-adk>=2.0.0` for ADK stacks) instead of copying `workshop-harness`'s own packaging manifest into scaffolded projects.
  - Separated ADK-specific vs. standard Python/Ollama 3-stage lab guides (`workshop/03_labs/01_lab_*.md`, `02_lab_*.md`, `03_lab_*.md`) so non-ADK Python workshops match `workshop/01_starter/main.py` and `workshop/02_final/main.py`.
  - Customized `RUNBOOK.md` with workshop-specific metadata (`name`, `topic`, `stack`, and 2026 cloud/local model tags) during `init` and `generate-all`.
  - Updated `audit_compatibility` to dynamically append a `Stack-Specific Architecture & Risk Audit` table to `<target>/docs/00-architecture-compatibility-matrix.md` when `--target` is provided.
  - Enhanced `audit_persona_loop` to detect `TODO` markers and reference solutions across all supported source extensions (`.py`, `.dart`, `.ts`, `.go`, `.java`, `.kt`) and added explicit `TODO` lab markers to Android starter `MainActivity.kt`.
  - Moved the final `test_workshop` verification gate to Step 9/9 of `generate-all` so exported Open Codelabs, Colab notebooks, and Slide Decks are audited as part of the one-click pipeline.
- **Presentation Slide & Bundle Exporters (`scripts/build_slides.py`, `scripts/export_colab.py`, `scripts/export_open_codelabs.py`)**:
  - Fixed `index.html` lab slide title extraction (`^#{1,2}\s+`) and stripped fenced code blocks prior to summary extraction so code lines no longer leak into slide body paragraphs.
  - Converted relative repository links into inline code references across exported Open Codelabs (`guide.md`, `steps/step_*.md`) and Colab notebooks (`.ipynb`).
  - Removed default emojis across generated slide decks (`slides.md`, `index.html`, `README.md`), Colab notebooks, and starter runner scripts (`run_starter.sh`, `run_starter.ps1`).
- **Comprehensive Workshop Verifier (`templates/script-templates/verify_workshop.py`)**:
  - Added automated verification for ADK `agent.py` (`root_agent` symbol check), `evalset.json` schema validity, Colab `.ipynb` JSON & Python code cell syntax, Open Codelabs bundle completeness, and presentation slide deck outputs.
  - Added API Key leak scanning (`AIzaSy...` pattern detection excluding sample placeholders).
  - Fixed path filtering (`rel_md.parts`) so workshops located inside `/tmp` or `tmp/` directories are audited without skipping markdown files.

---

## [v2026.10.31] - 2026-10-31

### Added

- **Developer Terminology & Bilingual Technical Term Notation Guide (`docs/agents-spec/terminology-and-style-guide.md`)**:
  - Added the official authoring standard requiring developer-friendly terminology paired with original English technical terms in parentheses (`개발자 친화적 용어 (English Original Term)`) across all documentation, `.md` files, slide decks, setup guides, runbooks, and code comments (e.g., `핸즈온 랩 (Hands-on Lab)`, `스캐폴딩 (Scaffolding)`, `런북 (Runbook)`, `Structured Output (JSON 스키마 응답) (Structured Outputs)`, `툴 콜링 / 함수 호출 (Tool Calling / Function Calling)`, `검색 증강 생성 (RAG, Retrieval-Augmented Generation)`, `Thinking Budget (추론 토큰 한도) (Thinking Budget)`, `양자화 (Quantization)`, `멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)`, `서브 에이전트 라우팅 (Sub-Agent Delegation)`, `Trajectory Eval (실행 경로 평가) (Trajectory Evaluation)`, `의존성 주입 (Dependency Injection)`, `폴백 (Fallback)`).
  - Added `AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS` dictionary to automatically detect and replace unnatural literal translations in `harness_cli.py` and `verify_workshop.py`.
- **Automated Typography & Terminology CLI Auditor (`audit-typography`)**:
  - Added `python3 harness_cli.py audit-typography --target <dir> [--fix]` to scan `.md`, `.txt`, `.yaml`, `.ipynb`, and source files for forbidden em dashes (`\u2014`) and awkward literal translations, with automatic hyphen (`-`) and developer-term sanitization.
  - Added `sanitize_no_em_dash` automatic sanitization across `harness_cli.py`, `scripts/build_slides.py`, `scripts/export_colab.py`, `scripts/export_open_codelabs.py`, and `templates/pdf-templates/generate_prep_pdf.py`.
- **Out-of-the-Box Workshop Scaffolding Artifacts (`harness_cli.py`)**:
  - Auto-generated `AGENTS.md` and `CLAUDE.md` (with mandatory No-Em-Dash & Bilingual Developer Terminology rules), `.gitignore`, `docs/18-intel-mac-prep.md` (Intel Mac `x86_64` Ollama CLI & Google Colab fallback guide), and `docs/eli5-concept-cheat-sheet.md` (3-tier ELI5 AI concept cheat sheet) during `init` and `generate-all`.
  - Added `[project.scripts]` CLI entrypoint (`workshop-harness = "harness_cli:main"`) in `pyproject.toml`.

### Changed

- **21 Agent Skills & Agent Rule Specifications (`skills/*/SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`)**:
  - Embedded the `Typography, Developer Terminology & Bilingual Notation Rules` section across all `skills/*/SKILL.md` files and synchronized local installations via `scripts/install_skills.sh`.
  - Updated `mkdocs.yml`, `docs/skills/overview.md`, `docs/index.{ko,ja,zh}.md`, `website/index.html`, `website/app.js`, and multilingual READMEs (`README.md`, `README_EN.md`, `README_KR.md`, `README_JA.md`, `README_ZH.md`) to reflect all 21 skills, the 9-step `generate-all` pipeline, and `v2026.10.31`.

### Fixed

- **Workshop Integrity Verifier (`templates/script-templates/verify_workshop.py`)**:
  - Stripped fenced code blocks and inline code spans prior to Markdown link auditing to eliminate false positives on example syntax in skill documentation.
  - Added `file://` URI detection and replaced hardcoded local `file://` links with repository URLs across `docs/agents-spec/agents-md.md`, `docs/skills/overview.md`, `docs/skills/architecture-checker.md`, and `docs/skills/open-codelabs.md`.
  - Changed `audit_typography_and_security` to return `False` (exit code `1`) on any forbidden em dash (`\u2014`) or awkward literal translation in markdown files, enforcing a strict CI/CD verification gate.
  - Propagated non-zero exit codes from `harness_cli.py test`, `harness_cli.py audit-models`, and `harness_cli.py audit-typography`.
- **Landing Page HTML & Metrics Observer (`website/index.html`, `website/app.js`)**:
  - Fixed unclosed `<div class="hero-cta-group reveal">` markup in `website/index.html` and updated the counter animation selector to `.metrics-ribbon` in `website/app.js`.

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
