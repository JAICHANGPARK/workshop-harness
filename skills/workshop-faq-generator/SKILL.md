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

- **Original Technical Term First, Real-World Developer Terminology & Natural Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never use awkward word-for-word literal translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
  - **Use the original English technical term first and append the developer-friendly term in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence grammar used by local software engineers**:
    - **Korean (KO)**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**. Never use awkward literals ("손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트") or double passives (`~되어집니다` -> `~됩니다`).
    - **Japanese (JA)**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never 「手で触る実験室」, 「走る本」, 「骨組みコード」, 「思考の予算」; write in natural Japanese engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」 (Never 「手把手的实验室」, 「奔跑的书」, 「骨架代码」, 「思考预算」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
