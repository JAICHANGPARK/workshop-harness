# AGENTS.md - Agent Instructions for Workshop Harness

> Standard AI Agent Context & Instructions Specification (https://agents.md/)

This repository provides seamless integration for all AI Coding Agents including **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Aider**, and **Cursor / Windsurf**.

---

## 🎯 Repository Overview & Purpose

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, community coding labs).

- **CLI Automation**: `python3 harness_cli.py` (backed by modular `harness/` core package)
- **22 Agent Skills**: Located under `skills/*/SKILL.md`
- **Document Templates**: Located under `templates/doc-templates/`

---

## 🤖 Natural Language Prompt ➔ Autonomous Skill Execution Rules

> **CRITICAL RULES FOR ALL AI CODING AGENTS (Antigravity, Claude Code, Codex, Cursor, Aider)**:
>
> 1. **🌐 Mandatory Autonomous Pre-Flight Web Search (`workshop-web-researcher`)**:
>    - **NEVER rely solely on LLM internal parametric training data** when generating workshop curriculum, code samples, Colab notebooks, or setup guides. Parametric weights contain outdated/deprecated APIs and retired model tags.
>    - **You MUST AUTONOMOUSLY execute live web searches (`search_web` / web search)** BEFORE writing any code or documentation to verify the newest SDK syntax (e.g. `google-genai >= 3.0.0` SDK, `@google/genai >= 3.0.0`, `anthropic >= 2.8.0`, `@anthropic-ai/sdk >= 1.7.0`, `openai >= 3.50.0` Responses API, `google-adk >= 2.14.0`, `litellm >= 1.84.0`, `google-agents-cli >= 1.4.1`, `com.google.genai:google-genai-kotlin-android:1.8.0`, `google_generative_ai`, `genui`, `a2ui_flutter`), current model tags (e.g. `gemini-4-carbon`, `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.8-live`, `gemini-nano-banana-2.1`, `gemini-omni-1.2-flash`, `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`, `gemma4:e4b`, `gemma4:12b`, `gemma4:26b`, `embeddinggemma-2`, `translategemma`, `functiongemma`, `medgemma1.5`, `qwen3.6`), and breaking changes.
>
> 2. **🌍 Original Technical Term First, Real-World Developer Terminology & Natural Developer Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
>    - **English (EN)**: Write in clear, idiomatic, direct technical English.
>    - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** in Korean, Japanese, or Chinese, **NEVER perform awkward word-for-word literal translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**. Always use **the original English technical term paired with real-world developer terminology (`English Original (개발자 용어)`), vocabulary, and natural sentence grammar actually used by local software engineers**:
>      - **Korean (KO) + English Original & Natural Developer Grammar**:
>        - **Terminology**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**. Never use awkward literal phrasing (e.g., ❌ "손으로 하는 실험실", ❌ "달리는 책", ❌ "발판 설치", ❌ "뼈대 코드", ❌ "생각 예산", ❌ "도구 부르기", ❌ "대리인 개발 키트", ❌ "부서지는 변경").
>        - **Grammar**: Avoid double passives (`~되어집니다` ➔ `~됩니다`), awkward nominalized endings (`~하는 것이 가능합니다` ➔ `~할 수 있습니다`), and inanimate subjects with `가지다` (`에이전트는 ~를 가집니다` ➔ `에이전트에 ~를 설정합니다`).
>      - **Japanese (JA) + English Original & Natural Developer Grammar**:
>        - **Terminology**: Use original English + developer Katakana / Kanji terms, e.g., 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターター / ボイラープレートコード)」, 「Structured Outputs (構造化出力)」, 「Tool Calling (ツール呼び出し / 関数呼び出し)」, 「Quantization (量子化)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「代理人開発キット」, ❌ 「煙の試験」).
>        - **Grammar**: Use natural Japanese engineer documentation style (`〜を設定します`, `〜を実行できます`) instead of stiff translationese (`〜を持つことができます`, `あなたは以下のステップを通して〜`).
>      - **Chinese (ZH) + English Original & Natural Developer Grammar**:
>        - **Terminology**: Use original English + authentic Chinese developer terminology, e.g., 「Hands-on Lab (实战工作坊 / 动手实验)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Tool Calling (工具调用 / 函数调用)」, 「Quantization (量化)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册 / 运维手册)」, 「Smoke Test (冒烟测试)」 (Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「代理人开发套件」, ❌ 「烟雾测试」).
>        - **Grammar**: Use concise Chinese developer documentation phrasing (`传入 API Key`, `初始化 Agent 并配置工具`) instead of awkward literal Europeanized grammar (`通过以下的方式被执行`, `它拥有一个工具`).
>      - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in their exact English form (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments using original English technical terms paired with developer-friendly explanations. See [`docs/agents-spec/terminology-and-style-guide.md`](docs/agents-spec/terminology-and-style-guide.md).
>
> 3. **🚫 Typography Rule (No Em Dash in Markdown & Documentation)**:
>    - **NEVER generate em dash characters (`\u2014`)** in any generated documentation, `.md` files, code comments, slide decks, setup guides, or runbooks.
>    - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
>    - Enforce and auto-sanitize via `python3 harness_cli.py audit-typography --target <dir> --fix` (verified as a hard gate by `python3 harness_cli.py test --target <dir>`).
>
> 4. **🚫 No Emojis in Documentation (Default: Clean Professional Text)**:
>    - **Do NOT include emojis in generated documentation, slide decks, setup guides, code comments, or runbooks by default.**
>    - Only use emojis if the user explicitly requests them in their prompt (e.g., "use emojis in headings").
>
> 5. **🗣️ Natural Language Prompt ➔ 3-Step Autonomous Generation & Domain/Language Tailoring**:
>    - Users communicate via **natural language chat prompts** (e.g. *"Claude 최신 모델로 멀티 에이전트 워크숍 만들어줘"*, *"OpenAI GPT로 구조화 출력 실습 만들어줘"*, *"Gemma 4와 EmbeddingGemma 2로 로컬 멀티모달 RAG 실습 만들어줘"*). Do **NOT** instruct users to run Python commands themselves, and do **NOT** block on unnecessary flag/model questions when sensible 2026 defaults exist.
>    - When a user requests a workshop in natural language, you MUST autonomously execute this **3-Step Loop**:
>      1. **Pre-Flight Web Search (`workshop-web-researcher`)**: Verify the latest SDK syntax and active 2026 model tags via `search_web`.
>      2. **Instant 9-Step Scaffolding (`harness_cli.py prompt`)**: Run `python3 harness_cli.py prompt "<user prompt>"` to generate the deterministic workshop structure (`SETUP_GUIDE.md`, `README.md`, `RUNBOOK.md`, Starter/Final code, 3-stage Labs, PDF Handout, Colab `.ipynb`, Open Codelabs bundle, and Slide Deck).
>      3. **Domain & Language Tailoring + Re-Verification**: When the user specifies a concrete domain scenario or requests Korean/Japanese/Chinese (`KO`/`JA`/`ZH`) materials, enrich `workshop/03_labs/*.md` and starter/solution examples in natural developer terminology (`English Original (개발자 용어)`), rebuild bundles (`build-pdf`, `export-colab`, `export-codelab`, `build-slides`), and re-run `python3 harness_cli.py test --target <dir>`.

| User Chat Prompt Example | Triggered Agent Skill | Autonomous Agent Tool Call / Action |
|:---|:---|:---|
| *"Create a 1-hour hands-on workshop on Gemma 4 Local RAG"* | `workshop-web-researcher` ➔ `workshop-scaffolder` + All Skills | 1. Web search latest Gemma 4 & Ollama/vLLM APIs<br>2. `python3 harness_cli.py prompt "Create a 1-hour hands-on workshop on Gemma 4 Local RAG"` |
| *"Claude 최신 모델로 멀티 에이전트 워크숍 만들어줘"* / *"OpenAI GPT로 실습 만들어줘"* | `workshop-web-researcher` ➔ `workshop-scaffolder` + All Skills | 1. Web search latest `anthropic` / `openai` SDKs<br>2. `python3 harness_cli.py prompt "<user prompt>"` (auto-infers `claude-sonnet-5-5` / `claude-fable-5-2` / `gpt-6.1-sol` + full 9-step build) |
| *"Build Google ADK & agents-cli multi-agent lifecycle workshop"* | `workshop-web-researcher` ➔ `adk-workshop-builder` + `agents-cli-workshop-builder` | 1. Web search latest `google-adk` & `google-agents-cli`<br>2. `python3 harness_cli.py prompt "Build Google ADK & agents-cli multi-agent lifecycle workshop"` |
| *"Build Android Jetpack Compose GenAI workshop with android CLI"* | `workshop-web-researcher` ➔ `android-workshop-builder` | 1. Web search latest `com.google.genai` SDK & `android` CLI<br>2. `python3 harness_cli.py prompt "Build Android Jetpack Compose GenAI workshop"` |
| *"Build Flutter GenUI and A2UI dynamic surface workshop"* | `workshop-web-researcher` ➔ `flutter-workshop-builder` + `a2ui-workshop-builder` | 1. Web search latest Flutter `genui` & `google_generative_ai`<br>2. `python3 harness_cli.py prompt "Build Flutter GenUI and A2UI dynamic surface workshop"` |
| *"List or audit workshop AI models and upgrade legacy tags"* | `workshop-web-researcher` | `python3 harness_cli.py list-models` / `python3 harness_cli.py audit-models --target <dir> --fix` |
| *"Audit and strip forbidden em dashes from markdown docs"* | `workshop-tester` | `python3 harness_cli.py audit-typography --target <dir> --fix` |
| *"Build presentation slides and Google Slides deck"* | `workshop-slide-generator` | `python3 harness_cli.py build-slides --target <dir>` |
| *"Convert workshop to Google Colab interactive notebooks"* | `workshop-web-researcher` ➔ `colab-workshop-integrator` | 1. Web search latest Colab CUDA/pip packages<br>2. `python3 harness_cli.py export-colab --target <dir>` |
| *"Audit hardware risks for Intel Mac and Windows users"* | `cross-architecture-checker` | `python3 harness_cli.py audit-compat --stack "..."` |
| *"Review workshop from beginner, intermediate, and senior personas"* | `workshop-persona-loop-evaluator` | `python3 harness_cli.py audit-loop --topic "..." --target <dir>` |
| *"Attendee terminal error: CUDA OutOfMemoryError"* | `live-debug-assistant` | Provide immediate 10-sec hotfix & CPU/quantization fallback |
| *"Generate publication-ready PDF handouts and previews"* | `pdf-handout-generator` | `python3 harness_cli.py build-pdf --target <dir>` |
| *"Export workshop to Open Codelabs bundle and publish"* | `open-codelabs-integrator` | `python3 harness_cli.py export-codelab --target <dir> --push` |

---

## ⚡ Quick Agent Commands & Workflows (Under-the-Hood)

### 1. Zero-Config Natural Language Prompt Generation (Recommended)
Pass any natural language prompt (KO/EN/JA/ZH) to auto-infer `name`, `topic`, `stack`, and the latest 2026 `model` (`gemini-4-hydrogen`, `gemini-4-carbon`, `claude-sonnet-5-5`, `claude-fable-5-2`, `gpt-6.1-sol`, `gpt-6-astra`) and execute the full 9-step orchestration pipeline:
```bash
python3 harness_cli.py prompt "Claude 최신 모델로 1시간짜리 멀티 에이전트 RAG 워크숍 만들어줘"
python3 harness_cli.py prompt "OpenAI GPT로 구조화 출력 핸즈온 랩 만들어줘"
python3 harness_cli.py prompt "Gemini 4 Carbon과 Google ADK로 엔터프라이즈 에이전트 워크숍 만들어줘"
```

### 1b. Explicit One-Click Full Workshop Generation (`generate-all`)
Execute the full orchestration pipeline with explicit flags:
```bash
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker" --model "gemini-4-hydrogen"
```

### 2. List & Audit 2026 Frontier Models & Markdown Typography (No Em Dash)
Inspect verified 2026 models, auto-upgrade deprecated model strings, or auto-remove forbidden em dashes (`\u2014`) across a project:
```bash
python3 harness_cli.py list-models
python3 harness_cli.py audit-models --target my-bwai-workshop --fix
python3 harness_cli.py audit-typography --target my-bwai-workshop --fix
```

### 3. Google ADK & Agents CLI (`google-agents-cli`) Workshop Initialization
```bash
python3 harness_cli.py init --name "adk-agents-cli-lab" --topic "Multi-Agent ADLC with Google ADK and agents-cli" --stack "python,adk,agents-cli"
```

### 3b. Anthropic Claude & OpenAI Multi-Provider Workshop Initialization
Scaffold workshops powered by Anthropic Claude (`claude-sonnet-5-5`, `claude-opus-5-5`, `claude-fable-5-2`), OpenAI (`gpt-6.1-sol`, `gpt-6-astra`, `gpt-6.1-terra`), or Google ADK via `LiteLlm`:
```bash
python3 harness_cli.py init --name "claude-agent-lab" --topic "Agentic Workflows with Claude Sonnet 5.5" --stack "python,claude" --model "claude-sonnet-5-5"
python3 harness_cli.py init --name "openai-responses-lab" --topic "Structured Agents with OpenAI GPT-6.1 Sol" --stack "python,openai" --model "gpt-6.1-sol"
python3 harness_cli.py init --name "adk-claude-lab" --topic "Multi-Provider ADK Agents with LiteLlm" --stack "python,adk,claude" --model "claude-sonnet-5-5"
```

### 4. Android Hands-on Workshop Initialization
```bash
python3 harness_cli.py init --name "android-gemini-lab" --topic "Android GenAI with Jetpack Compose" --stack "android"
```

### 5. Flutter & A2UI / GenUI Hands-on Workshop Initialization
```bash
python3 harness_cli.py init --name "flutter-genui-lab" --topic "Generative UI with Flutter and A2UI" --stack "flutter,genui,a2ui"
```

### 6. Cross-Architecture Compatibility Audit
Audit tech stack risks across Apple Silicon, Intel Mac, Windows, and Linux:
```bash
python3 harness_cli.py audit-compat --stack "adk,agents-cli,android,flutter,genui,docker,gemini-live"
```

### 7. Loop Engineering 4-Persona Review
Evaluate curriculum and code from non-coder, novice, intermediate, and senior attendee personas:
```bash
python3 harness_cli.py audit-loop --topic "Local RAG with Gemma 4" --target my-bwai-workshop
```

### 8. Code Smoke Test & Markdown Link Integrity
Verify markdown relative links, model currency, and execute test scripts:
```bash
python3 harness_cli.py test --target my-bwai-workshop
```

### 9. Build Publication PDF Handout
Generate PDF handouts from markdown documentation:
```bash
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

### 10. Export & Push to Open Codelabs Platform
Convert workshop to Open Codelabs bundle (`codelab.yaml`) and push via `oc` CLI:
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop --push
```

### 11. Export Google Colab Notebooks & Run Smoke Test via Colab CLI
Convert workshop to Google Colab interactive notebooks (`.ipynb`) with 'Open in Colab' badges and verify via `colab` CLI:
```bash
python3 harness_cli.py export-colab --target my-bwai-workshop
python3 harness_cli.py test-colab --target my-bwai-workshop
```

### 12. Build Presentation Slide Deck (Google Slides, Marp & Web HTML)
Generate Google Slides 16:9 `.pptx`, Marp Markdown (`slides.md`), and interactive standalone Web HTML presentation:
```bash
python3 harness_cli.py build-slides --target my-bwai-workshop
```

---

## 📁 22 Agent Skills Index

When handling user requests, reference the specific skill instructions in `skills/`:

1. [`skills/workshop-scaffolder/SKILL.md`](skills/workshop-scaffolder/SKILL.md)
2. [`skills/cross-architecture-checker/SKILL.md`](skills/cross-architecture-checker/SKILL.md)
3. [`skills/prerequisite-checker/SKILL.md`](skills/prerequisite-checker/SKILL.md)
4. [`skills/hands-on-curriculum-builder/SKILL.md`](skills/hands-on-curriculum-builder/SKILL.md)
5. [`skills/pdf-handout-generator/SKILL.md`](skills/pdf-handout-generator/SKILL.md)
6. [`skills/workshop-troubleshooter/SKILL.md`](skills/workshop-troubleshooter/SKILL.md)
7. [`skills/workshop-runbook-generator/SKILL.md`](skills/workshop-runbook-generator/SKILL.md)
8. [`skills/live-debug-assistant/SKILL.md`](skills/live-debug-assistant/SKILL.md)
9. [`skills/workshop-faq-generator/SKILL.md`](skills/workshop-faq-generator/SKILL.md)
10. [`skills/workshop-tester/SKILL.md`](skills/workshop-tester/SKILL.md)
11. [`skills/workshop-web-researcher/SKILL.md`](skills/workshop-web-researcher/SKILL.md)
12. [`skills/workshop-persona-loop-evaluator/SKILL.md`](skills/workshop-persona-loop-evaluator/SKILL.md)
13. [`skills/open-codelabs-integrator/SKILL.md`](skills/open-codelabs-integrator/SKILL.md)
14. [`skills/colab-workshop-integrator/SKILL.md`](skills/colab-workshop-integrator/SKILL.md)
15. [`skills/workshop-slide-generator/SKILL.md`](skills/workshop-slide-generator/SKILL.md)
16. [`skills/adk-workshop-builder/SKILL.md`](skills/adk-workshop-builder/SKILL.md)
17. [`skills/eli5-concept-explainer/SKILL.md`](skills/eli5-concept-explainer/SKILL.md)
18. [`skills/android-workshop-builder/SKILL.md`](skills/android-workshop-builder/SKILL.md)
19. [`skills/flutter-workshop-builder/SKILL.md`](skills/flutter-workshop-builder/SKILL.md)
20. [`skills/a2ui-workshop-builder/SKILL.md`](skills/a2ui-workshop-builder/SKILL.md)
21. [`skills/agents-cli-workshop-builder/SKILL.md`](skills/agents-cli-workshop-builder/SKILL.md)
22. [`skills/eli5/SKILL.md`](skills/eli5/SKILL.md)

---

## 🔗 References

- **AGENTS.md Open Specification**: [https://agents.md/](https://agents.md/)
- **Official Repository**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
- **Google Agent Development Kit (ADK)**: [https://adk.dev](https://adk.dev)
- **Google Agents CLI (`google/agents-cli`)**: [https://github.com/google/agents-cli](https://github.com/google/agents-cli)
- **Open Codelabs Platform**: [https://github.com/JAICHANGPARK/open-codelabs](https://github.com/JAICHANGPARK/open-codelabs)
- **Official Google Android CLI & Skills**: [https://developer.android.com/tools/agents/android-cli](https://developer.android.com/tools/agents/android-cli)
- **Flutter AI Development**: [https://docs.flutter.dev/ai/get-started](https://docs.flutter.dev/ai/get-started)
- **Flutter Package Skills**: [https://docs.flutter.dev/ai/package-skills](https://docs.flutter.dev/ai/package-skills)
- **Flutter Agent Plugins**: [https://github.com/flutter/agent-plugins](https://github.com/flutter/agent-plugins)
- **A2UI Open Protocol**: [https://a2ui.org](https://a2ui.org)
- **Google Colab CLI**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)

