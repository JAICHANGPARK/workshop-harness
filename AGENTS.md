# AGENTS.md - Agent Instructions for Workshop Harness

> Standard AI Agent Context & Instructions Specification (https://agents.md/)

This repository provides seamless integration for all AI Coding Agents including **Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex / ChatGPT**, **Aider**, and **Cursor / Windsurf**.

---

## 🎯 Repository Overview & Purpose

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, community coding labs).

- **CLI Automation**: `python3 harness_cli.py`
- **CLI Automation**: `python3 harness_cli.py`
- **20 Agent Skills**: Located under `skills/*/SKILL.md`
- **Document Templates**: Located under `templates/doc-templates/`

---

## 🤖 Natural Language Prompt ➔ Autonomous Skill Execution Rules

> **CRITICAL RULES FOR ALL AI CODING AGENTS (Antigravity, Claude Code, Codex, Cursor, Aider)**:
>
> 1. **🌐 Mandatory Autonomous Pre-Flight Web Search (`workshop-web-researcher`)**:
>    - **NEVER rely solely on LLM internal parametric training data** when generating workshop curriculum, code samples, Colab notebooks, or setup guides. Parametric weights contain outdated/deprecated APIs and retired model tags.
>    - **You MUST AUTONOMOUSLY execute live web searches (`search_web` / web search)** BEFORE writing any code or documentation to verify the newest SDK syntax (e.g. `google-genai` SDK, `com.google.genai:google-genai-kotlin-android`, `google_generative_ai`, `genui`), current model tags (e.g. `gemini-3.7-flash`, `claude-sonnet-5`, `gpt-5.6-sol`, `gemma4`), and breaking changes.
>
> 2. **🌍 Developer-Idiomatic Localization Protocol (No Literal Translations)**:
>    - When translating or authoring slide decks, setup guides, or runbooks into Korean (KR), Japanese (JA), or Chinese (ZH), **NEVER perform awkward literal / word-for-word machine translations**.
>    - **MUST use native developer jargon and community-standard technical terms** used by real-world software engineers:
>      - **Korean (KO)**: Use natural IT developer terms (e.g., "프롬프트 엔지니어링", "핸즈온 랩", "스캐폴딩", "의존성 주입", "양자화", "파인튜닝", "런북", "임베딩"). Never use awkward literal phrasing (e.g. ❌ "손으로 하는 실험실", ❌ "달리는 책").
>      - **Japanese (JA)**: Use standard developer Katakana / technical terms (e.g., 「ハンズオン」, 「デプロイ」, 「スキャフォールディング」, 「トークン」, 「ファインチューニング」, 「ランブック」).
>      - **Chinese (ZH)**: Use Chinese tech community terminology (e.g., 「实战工作坊/动手实验」, 「脚手架」, 「提示词工程」, 「微调」, 「演练手册/Runbook」).
>
> 3. **🚫 Typography Rule (No Em Dash)**:
>    - **NEVER generate em dash characters (`—` or `\u2014`)** in any generated documentation, code comments, slide decks, or markdown files.
>    - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
>
> 4. **🚫 No Emojis in Documentation (Default: Clean Professional Text)**:
>    - **Do NOT include emojis in generated documentation, slide decks, setup guides, code comments, or runbooks by default.**
>    - Only use emojis if the user explicitly requests them in their prompt (e.g., "use emojis in headings").
>
> 5. **🗣️ Natural Language Autonomy**:
>    - Users communicate via **natural language chat prompts**. Do **NOT** instruct users to run Python commands themselves.
>    - When a user requests a task, you MUST autonomously read the relevant `skills/*/SKILL.md` and execute the appropriate harness CLI command or generate the code artifacts on behalf of the user.

| User Chat Prompt Example | Triggered Agent Skill | Autonomous Agent Tool Call / Action |
|:---|:---|:---|
| *"Create a 1-hour hands-on workshop on Gemma 4 Local RAG"* | `workshop-web-researcher` ➔ `workshop-scaffolder` + All Skills | 1. Web search latest Gemma 4 & Ollama/vLLM APIs<br>2. `python3 harness_cli.py generate-all --name "..." --topic "..."` |
| *"Build Android Jetpack Compose GenAI workshop with android CLI"* | `workshop-web-researcher` ➔ `android-workshop-builder` | 1. Web search latest `com.google.genai` SDK & `android` CLI<br>2. `python3 harness_cli.py init --name "..." --stack "android"` |
| *"Build Flutter GenUI and A2UI dynamic surface workshop"* | `workshop-web-researcher` ➔ `flutter-workshop-builder` + `a2ui-workshop-builder` | 1. Web search latest Flutter `genui` & `google_generative_ai`<br>2. `python3 harness_cli.py init --name "..." --stack "flutter,genui,a2ui"` |
| *"Build presentation slides and Google Slides deck"* | `workshop-slide-generator` | `python3 harness_cli.py build-slides --target <dir>` |
| *"Convert workshop to Google Colab interactive notebooks"* | `workshop-web-researcher` ➔ `colab-workshop-integrator` | 1. Web search latest Colab CUDA/pip packages<br>2. `python3 harness_cli.py export-colab --target <dir>` |
| *"Audit hardware risks for Intel Mac and Windows users"* | `cross-architecture-checker` | `python3 harness_cli.py audit-compat --stack "..."` |
| *"Review workshop from beginner, intermediate, and senior personas"* | `workshop-persona-loop-evaluator` | `python3 harness_cli.py audit-loop --topic "..."` |
| *"Attendee terminal error: CUDA OutOfMemoryError"* | `live-debug-assistant` | Provide immediate 10-sec hotfix & CPU/quantization fallback |
| *"Generate publication-ready PDF handouts and previews"* | `pdf-handout-generator` | `python3 harness_cli.py build-pdf --target <dir>` |
| *"Export workshop to Open Codelabs bundle and publish"* | `open-codelabs-integrator` | `python3 harness_cli.py export-codelab --target <dir> --push` |

---

## ⚡ Quick Agent Commands & Workflows (Under-the-Hood)

### 1. One-Click Full Workshop Generation Across Skills
Execute the full orchestration pipeline:
```bash
python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

### 2. Android Hands-on Workshop Initialization
```bash
python3 harness_cli.py init --name "android-gemini-lab" --topic "Android GenAI with Jetpack Compose" --stack "android"
```

### 3. Flutter & A2UI / GenUI Hands-on Workshop Initialization
```bash
python3 harness_cli.py init --name "flutter-genui-lab" --topic "Generative UI with Flutter and A2UI" --stack "flutter,genui,a2ui"
```

### 4. Cross-Architecture Compatibility Audit
Audit tech stack risks across Apple Silicon, Intel Mac, Windows, and Linux:
```bash
python3 harness_cli.py audit-compat --stack "android,flutter,genui,docker"
```

### 5. Loop Engineering Multi-Persona Review
Evaluate curriculum and code from beginner, intermediate, and advanced attendee personas:
```bash
python3 harness_cli.py audit-loop --topic "Local RAG with Gemma 4"
```

### 6. Code Smoke Test & Markdown Link Integrity
Verify markdown relative links and execute test scripts:
```bash
python3 harness_cli.py test --target my-bwai-workshop
```

### 7. Build Publication PDF Handout
Generate PDF handouts from markdown documentation:
```bash
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

### 8. Export & Push to Open Codelabs Platform
Convert workshop to Open Codelabs bundle (`codelab.yaml`) and push via `oc` CLI:
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop --push
```

### 9. Export Google Colab Notebooks & Run Smoke Test via Colab CLI
Convert workshop to Google Colab interactive notebooks (`.ipynb`) with 'Open in Colab' badges and verify via `colab` CLI:
```bash
python3 harness_cli.py export-colab --target my-bwai-workshop
python3 harness_cli.py test-colab --target my-bwai-workshop
```

### 10. Build Presentation Slide Deck (Google Slides, Marp & Web HTML)
Generate Google Slides 16:9 `.pptx`, Marp Markdown (`slides.md`), and interactive standalone Web HTML presentation:
```bash
python3 harness_cli.py build-slides --target my-bwai-workshop
```

---

## 📁 20 Agent Skills Index

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

---

## 🔗 References

- **AGENTS.md Open Specification**: [https://agents.md/](https://agents.md/)
- **Official Repository**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
- **Open Codelabs Platform**: [https://github.com/JAICHANGPARK/open-codelabs](https://github.com/JAICHANGPARK/open-codelabs)
- **A2UI Open Protocol**: [https://a2ui.org](https://a2ui.org)
- **Google Colab CLI**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)

- **Google Colab CLI**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)
