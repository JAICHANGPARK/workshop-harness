---
name: workshop-faq-generator
description: Auto-generates attendee FAQ documents (FAQ.md / docs/20-faq.md) tailored to the workshop topic, tech stack, and target audience level (beginner/intermediate) covering hardware, network, and code-related questions.
---

# Workshop FAQ Generator Skill

## Purpose
Pre-generates a comprehensive, topic-tailored FAQ document (`docs/20-faq.md`) covering hardware requirements, software installations, API keys, venue network resilience, offline fallbacks, and code debugging. Reduces repetitive attendee Q&A by up to 80% during live workshop sessions.

---

## 5 Core FAQ Domains

When auto-generating `docs/20-faq.md`, the agent must populate questions across 5 core domains:

### 1. Hardware & Operating System
- **Q: What are the minimum RAM and CPU specs required for local LLM labs?**
  - *A*: Minimum 8GB RAM for 2B parameter models (`gemma4:e2b`). 16GB RAM recommended for 4B parameter models (`gemma4:e4b`).
- **Q: Can I complete the workshop on an Intel Mac or Windows ARM device?**
  - *A*: Yes. Intel Mac users will use Ollama CLI mode or Cloud Gemini API. Windows ARM users can use native ARM64 Ollama builds.

### 2. Software & Package Runtimes
- **Q: Do I need Docker installed for this workshop?**
  - *A*: Only if vector database container labs are explicitly enabled in the curriculum; otherwise, Python `uv` is sufficient.
- **Q: What is `uv` and why are we using it instead of `pip` or `conda`?**
  - *A*: `uv` is an extremely fast Python package and project manager that automatically installs required Python versions and dependencies without manual venv creation.

### 3. API Keys & Billing Safety
- **Q: Where do I get a free Gemini API Key?**
  - *A*: Visit [https://aistudio.google.com](https://aistudio.google.com), sign in with any Google account, and click **Get API Key**.
- **Q: Will I be charged for using Gemini API during the workshop?**
  - *A*: Google AI Studio provides a free tier ample for workshop labs.

### 4. Venue Network & Offline Mode
- **Q: What if the venue WiFi drops or becomes congested?**
  - *A*: Follow the offline setup guide in `docs/01-hardware-and-env.md` to pre-download model weights (`ollama pull gemma4:e4b`) before arriving at the venue.

### 5. Code & Lab Resetting
- **Q: I modified starter code and hit syntax errors. How do I reset to a clean state?**
  - *A*: Copy the reference code snippet from `workshop/02_final/` or run `git checkout workshop/01_starter/`.

---

## Output Artifact Specifications

- **File Path**: `docs/20-faq.md`
- **Formatting**: GitHub Flavored Markdown with expandable `<details><summary>` tags for quick attendee browsing.

---

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
