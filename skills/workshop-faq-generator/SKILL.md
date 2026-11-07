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

## Typography, Developer Terminology & Bilingual Notation Rules

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
