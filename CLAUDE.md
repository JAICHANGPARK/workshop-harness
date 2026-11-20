# CLAUDE.md - Claude Code Agent Instructions for Workshop Harness

> Standard Claude Code Context & Instructions for Workshop Harness (22 Agent Skills)

This repository provides native compatibility with **Anthropic Claude Code CLI**, **Claude Fable 5.2 / Claude Opus 5.5 / Claude Sonnet 5.5 / Claude Haiku 5.5**, and **Claude Desktop**.

---

## 🎯 Repository Overview & Claude Code Role

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, Hands-on Labs).

### 🤖 CRITICAL RULES FOR CLAUDE CODE:
1. **🌐 Mandatory Autonomous Pre-Flight Web Search (`workshop-web-researcher`)**:
   - **Never rely on static model training data.** AI training weights contain obsolete/deprecated APIs and retired model tags.
   - **Claude Code MUST AUTONOMOUSLY execute live web searches** (`search_web` / web search) before generating any workshop code, Colab notebooks, or curriculum to verify current SDK methods, modern imports, and active model tags (e.g. `gemini-4-carbon`, `gemini-4-neon`, `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.8-live`, `gemini-omni-1.2-flash`, `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`, `gemma4:e4b`, `gemma4:12b`, `gemma4:26b`, `embeddinggemma-2`, `translategemma`, `functiongemma`, `medgemma1.5`, `google-genai >= 3.0.0`, `anthropic >= 2.8.0`, `@anthropic-ai/sdk >= 1.7.0`, `openai >= 3.50.0`, `google-adk >= 2.14.0`, `litellm >= 1.84.0`, `google-agents-cli >= 1.4.1`, `com.google.genai`, `genui`, `a2ui_flutter`).
2. **🌍 Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
   - **English (EN)**: Write in clear, idiomatic, direct technical English.
   - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: When generating or localizing documentation, `.md` files, presentation slides, runbooks, setup guides, or **code comments** in Korean, Japanese, or Chinese, **NEVER use awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in practice:
     - **Korean (KO) Real-World Developer Vernacular**: Write natural developer terms (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
     - **Japanese (JA) Real-World Developer Vernacular**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
     - **Chinese (ZH) Real-World Developer Vernacular**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
     - **Code Comments**: Preserve exact English identifiers (`root_agent`, `FunctionTool`, `thinking_budget`, `response_schema`) and write comments in concise, natural developer prose. See [`docs/agents-spec/terminology-and-style-guide.md`](docs/agents-spec/terminology-and-style-guide.md).
3. **🚫 Typography Rule (No Em Dash in Markdown & Documentation)**:
   - **NEVER generate em dash characters (`\u2014`)** anywhere in generated `.md` files, documentation, slides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()`.
   - Run `python3 harness_cli.py audit-typography --target <dir> --fix` to audit and sanitize markdown typography automatically.
4. **🚫 No Emojis in Documentation (Default: Clean Professional Text)**:
   - **Do NOT use emojis in generated documentation, slide decks, setup guides, code comments, or runbooks by default.**
   - Emojis may only be used if the user explicitly requests them in their prompt.
5. **Natural Language Prompt ➔ 3-Step Autonomous Generation & Domain/Language Tailoring**:
   - **Users communicate using natural language prompts. Do NOT ask users to execute Python CLI commands directly or ask unnecessary flag questions.**
   - When a user requests a workshop in natural language (e.g. *"Claude 최신 모델로 멀티 에이전트 워크숍 만들어줘"*, *"Gemma 4와 EmbeddingGemma 2로 로컬 RAG 실습 만들어줘"*), **Claude Code must autonomously**: (1) run a pre-flight web search, (2) execute `python3 harness_cli.py prompt "<user prompt>"` to generate the deterministic 9-step package, and (3) when a specific domain or `KO`/`JA`/`ZH` language is requested, tailor `workshop/03_labs/*.md` and starter/solution examples in natural developer terminology, rebuild bundles (`build-pdf`, `export-colab`, `export-codelab`, `build-slides`), and re-run `python3 harness_cli.py test --target <dir>`.

---

## 🧭 Natural Language Prompt ➔ Skill Autonomous Execution Mapping

| User Natural Language Prompt | Autonomous Claude Action & Triggered Skill | Execution Command / Action |
|:---|:---|:---|
| *"Create a 1-hour workshop for Local RAG with Gemma 4"* | Read `skills/workshop-web-researcher/SKILL.md` ➔ `skills/workshop-scaffolder/SKILL.md` | 1. Web search latest Gemma 4 & Ollama APIs<br>2. Run `python3 harness_cli.py prompt "Create a 1-hour workshop for Local RAG with Gemma 4"` |
| *"Claude 최신 모델로 멀티 에이전트 워크숍 만들어줘"* / *"OpenAI GPT로 실습 만들어줘"* | Read `skills/workshop-web-researcher/SKILL.md` ➔ `skills/workshop-scaffolder/SKILL.md` | Run `python3 harness_cli.py prompt "<user prompt>"` (auto-infers provider, model & runs full 9-step build) |
| *"Build Google ADK & agents-cli multi-agent lifecycle workshop"* | Read `skills/adk-workshop-builder/SKILL.md` + `skills/agents-cli-workshop-builder/SKILL.md` | Run `python3 harness_cli.py prompt "Build Google ADK & agents-cli multi-agent lifecycle workshop"` |
| *"Build Android Jetpack Compose GenAI workshop with android CLI"* | Read `skills/android-workshop-builder/SKILL.md` | Run `python3 harness_cli.py prompt "Build Android Jetpack Compose GenAI workshop"` |
| *"Build Flutter GenUI and A2UI dynamic surface workshop"* | Read `skills/flutter-workshop-builder/SKILL.md` + `skills/a2ui-workshop-builder/SKILL.md` | Run `python3 harness_cli.py prompt "Build Flutter GenUI and A2UI dynamic surface workshop"` |
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

## 📁 22 Specialized Agent Skills Index

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
22. [`skills/eli5/SKILL.md`](skills/eli5/SKILL.md)

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



