# CLAUDE.md - Claude Code Agent Instructions for Workshop Harness

> Standard Claude Code Context & Instructions for Workshop Harness (21 Agent Skills)

This repository provides native compatibility with **Anthropic Claude Code CLI**, **Claude Sonnet 5.5 / Claude Opus 5.5 / Claude Fable 5.1**, and **Claude Desktop**.

---

## 🎯 Repository Overview & Claude Code Role

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, Hands-on Labs).

### 🤖 CRITICAL RULES FOR CLAUDE CODE:
1. **🌐 Mandatory Autonomous Pre-Flight Web Search (`workshop-web-researcher`)**:
   - **Never rely on static model training data.** AI training weights contain obsolete/deprecated APIs and retired model tags.
   - **Claude Code MUST AUTONOMOUSLY execute live web searches** (`search_web` / web search) before generating any workshop code, Colab notebooks, or curriculum to verify current SDK methods, modern imports, and active model tags (e.g. `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.8-live`, `claude-sonnet-5.5`, `claude-opus-5.5`, `gpt-6-astra`, `gpt-6.1-sol`, `gemma4`, `google-genai`, `google-adk`, `google-agents-cli`, `com.google.genai`, `genui`).
2. **🌍 Original Technical Term First, Real-World Developer Terminology & Natural Developer Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
   - **English (EN)**: Write in clear, idiomatic, direct technical English.
   - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: When generating or localizing documentation, `.md` files, presentation slides, runbooks, setup guides, or **code comments** in Korean, Japanese, or Chinese, **NEVER use awkward literal machine translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
   - **Use the original English technical term first with the developer-friendly term in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence grammar used by local software engineers**:
     - **Korean (KO) + English Original & Grammar**: "Hands-on Lab (핸즈온 랩)", "Scaffolding (스캐폴딩)", "Runbook (런북)", "Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)", "Prompt Engineering (프롬프트 엔지니어링)", "Structured Outputs (구조화 출력)", "Tool Calling (툴 콜링)", "RAG (Retrieval-Augmented Generation, 검색 증강 생성)", "Embedding (임베딩)", "Quantization (양자화)", "Thinking Budget (추론 예산)", "Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)", "Sub-Agent Delegation (서브 에이전트 위임)", "Trajectory Evaluation (궤적 평가)", "Dependency Injection (의존성 주입)", "Fallback (폴백)" (Never ❌ "손으로 하는 실험실", ❌ "달리는 책", ❌ "발판 설치", ❌ "뼈대 코드", ❌ "생각 예산", ❌ "대리인 개발 키트"; avoid translationese grammar like `~되어집니다`, `~하는 것이 가능합니다`).
     - **Japanese (JA) + English Original & Grammar**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Quantization (量子化)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」; write in natural Japanese engineer style `〜を設定します`, `〜を実行できます`).
     - **Chinese (ZH) + English Original & Grammar**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Quantization (量化)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」 (Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」; write in concise Chinese developer phrasing).
     - **Code Comments**: Preserve exact English identifiers (`root_agent`, `FunctionTool`, `thinking_budget`, `response_schema`) and pair original English technical terms with developer-friendly explanations. See [`docs/agents-spec/terminology-and-style-guide.md`](docs/agents-spec/terminology-and-style-guide.md).
3. **🚫 Typography Rule (No Em Dash in Markdown & Documentation)**:
   - **NEVER generate em dash characters (`\u2014`)** anywhere in generated `.md` files, documentation, slides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()`.
   - Run `python3 harness_cli.py audit-typography --target <dir> --fix` to audit and sanitize markdown typography automatically.
4. **🚫 No Emojis in Documentation (Default: Clean Professional Text)**:
   - **Do NOT use emojis in generated documentation, slide decks, setup guides, code comments, or runbooks by default.**
   - Emojis may only be used if the user explicitly requests them in their prompt.
5. **Natural Language Autonomy**:
   - **Users communicate using natural language prompts. Do NOT ask users to execute Python CLI commands directly.**
   - When a user asks a question or makes a request, **Claude Code must autonomously read the corresponding skill file (`skills/*/SKILL.md`) and execute the required Python tool or generate the artifacts on behalf of the user.**

---

## 🧭 Natural Language Prompt ➔ Skill Autonomous Execution Mapping

| User Natural Language Prompt | Autonomous Claude Action & Triggered Skill | Execution Command / Action |
|:---|:---|:---|
| *"Create a 1-hour workshop for Local RAG with Gemma 4"* | Read `skills/workshop-web-researcher/SKILL.md` ➔ `skills/workshop-scaffolder/SKILL.md` | 1. Web search latest Gemma 4 & Ollama APIs<br>2. Run `python3 harness_cli.py generate-all --name "<name>" --topic "<topic>"` |
| *"Build Google ADK & agents-cli multi-agent lifecycle workshop"* | Read `skills/adk-workshop-builder/SKILL.md` + `skills/agents-cli-workshop-builder/SKILL.md` | Run `python3 harness_cli.py init --name "<name>" --stack "python,adk,agents-cli"` |
| *"Build Android Jetpack Compose GenAI workshop with android CLI"* | Read `skills/android-workshop-builder/SKILL.md` | Run `python3 harness_cli.py init --name "<name>" --stack "android"` |
| *"Build Flutter GenUI and A2UI dynamic surface workshop"* | Read `skills/flutter-workshop-builder/SKILL.md` + `skills/a2ui-workshop-builder/SKILL.md` | Run `python3 harness_cli.py init --name "<name>" --stack "flutter,genui,a2ui"` |
| *"List or audit workshop AI models and upgrade legacy tags"* | Read `skills/workshop-web-researcher/SKILL.md` | Run `python3 harness_cli.py list-models` or `python3 harness_cli.py audit-models --target <dir> --fix` |
| *"Audit and remove em dashes from markdown docs"* | Read `skills/workshop-tester/SKILL.md` | Run `python3 harness_cli.py audit-typography --target <dir> --fix` |
| *"Build Google Slides presentation for this workshop"* | Read `skills/workshop-slide-generator/SKILL.md` | Run `python3 harness_cli.py build-slides --target <dir>` |
| *"Convert workshop to Google Colab notebooks with badges"* | Read `skills/colab-workshop-integrator/SKILL.md` | Run `python3 harness_cli.py export-colab --target <dir>` |
| *"Audit cross-architecture risks for Intel Mac and Windows"* | Read `skills/cross-architecture-checker/SKILL.md` | Run `python3 harness_cli.py audit-compat --stack "<stack>"` |
| *"Review workshop from beginner & senior developer perspectives"* | Read `skills/workshop-persona-loop-evaluator/SKILL.md` | Run `python3 harness_cli.py audit-loop --topic "<topic>" --target <dir>` |
| *"Attendee terminal error: CUDA OutOfMemoryError"* | Read `skills/live-debug-assistant/SKILL.md` | Provide 10-sec hotfix command & quantization fallback |
| *"Generate PDF handouts and contact sheet previews"* | Read `skills/pdf-handout-generator/SKILL.md` | Run `python3 harness_cli.py build-pdf --target <dir>` |
| *"Export and push to Open Codelabs platform"* | Read `skills/open-codelabs-integrator/SKILL.md` | Run `python3 harness_cli.py export-codelab --target <dir> --push` |

---

## 📁 21 Specialized Agent Skills Index

Claude Code should inspect these Markdown skills whenever relevant:

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

---

## 🔗 References

- [AGENTS.md Specification](./AGENTS.md)
- [Official Repository](https://github.com/JAICHANGPARK/workshop-harness)
- [Google Agent Development Kit (ADK)](https://adk.dev)
- [Google Agents CLI (`google/agents-cli`)](https://github.com/google/agents-cli)
- [Official Google Android CLI & Skills](https://developer.android.com/tools/agents/android-cli)
- [Flutter AI Development Guide](https://docs.flutter.dev/ai/get-started)
- [Flutter Package Skills](https://docs.flutter.dev/ai/package-skills)
- [Flutter Agent Plugins](https://github.com/flutter/agent-plugins)
- [A2UI Open Protocol Specification](https://a2ui.org)



