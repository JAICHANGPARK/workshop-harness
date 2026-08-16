# CLAUDE.md - Claude Code Agent Instructions for Workshop Harness

> Standard Claude Code Context & Instructions for Workshop Harness (15 Agent Skills)

This repository provides native compatibility with **Anthropic Claude Code CLI**, **Claude 3.7 Sonnet**, and **Claude Desktop**.

---

## 🎯 Repository Overview & Claude Code Role

`workshop-harness` is an AI Agent Harness, Skill Suite, and CLI Automation Toolkit for technical workshops (Build with AI, DevFest, Hands-on Labs).

### 🤖 CRITICAL RULES FOR CLAUDE CODE:
1. **🌐 Mandatory Autonomous Pre-Flight Web Search (`workshop-web-researcher`)**:
   - **Never rely on static model training data.** AI training weights contain obsolete/deprecated APIs and retired model tags.
   - **Claude Code MUST AUTONOMOUSLY execute live web searches** (`search_web` / web search) before generating any workshop code, Colab notebooks, or curriculum to verify current SDK methods, modern imports, and active model tags (e.g. `gemini-3.7-flash`, `google-genai`).
2. **🌍 Developer-Idiomatic Localization Protocol (No Literal Translations)**:
   - When generating or translating presentation slides, runbooks, or setup guides in Korean, Japanese, or Chinese, **do NOT use literal machine translations**.
   - **Always use developer-idiomatic community terminology**:
     - **Korean (KO)**: "프롬프트 엔지니어링", "핸즈온 랩", "스캐폴딩", "의존성 주입", "양자화", "파인튜닝", "런북", "임베딩" (Never ❌ "손으로 하는 실험실").
     - **Japanese (JA)**: 「ハンズオン」, 「デプロイ」, 「スキャフォールディング」, 「トークン」, 「ファインチューニング」, 「ランブック」.
     - **Chinese (ZH)**: 「实战工作坊」, 「脚手架」, 「提示词工程」, 「微调」, 「演练手册」.
3. **🚫 Typography Rule (No Em Dash)**:
   - **NEVER generate em dash characters (`—` or `\u2014`)** anywhere in slides, docs, code, or markdown. Always use standard hyphens (`-`), colons (`:`), or parentheses.
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
| *"Build Google Slides presentation for this workshop"* | Read `skills/workshop-slide-generator/SKILL.md` | Run `python3 harness_cli.py build-slides --target <dir>` |
| *"Convert workshop to Google Colab notebooks with badges"* | Read `skills/colab-workshop-integrator/SKILL.md` | Run `python3 harness_cli.py export-colab --target <dir>` |
| *"Audit cross-architecture risks for Intel Mac and Windows"* | Read `skills/cross-architecture-checker/SKILL.md` | Run `python3 harness_cli.py audit-compat --stack "<stack>"` |
| *"Review workshop from beginner & senior developer perspectives"* | Read `skills/workshop-persona-loop-evaluator/SKILL.md` | Run `python3 harness_cli.py audit-loop --topic "<topic>"` |
| *"Attendee terminal error: CUDA OutOfMemoryError"* | Read `skills/live-debug-assistant/SKILL.md` | Provide 10-sec hotfix command & quantization fallback |
| *"Generate PDF handouts and contact sheet previews"* | Read `skills/pdf-handout-generator/SKILL.md` | Run `python3 harness_cli.py build-pdf --target <dir>` |
| *"Export and push to Open Codelabs platform"* | Read `skills/open-codelabs-integrator/SKILL.md` | Run `python3 harness_cli.py export-codelab --target <dir> --push` |

---

## 📁 15 Specialized Agent Skills Index

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

---

## 🔗 References

- [AGENTS.md Specification](./AGENTS.md)
- [Official Repository](https://github.com/JAICHANGPARK/workshop-harness)
