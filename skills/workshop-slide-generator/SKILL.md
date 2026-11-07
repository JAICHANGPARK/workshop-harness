---
name: workshop-slide-generator
description: Generates high-impact, professional workshop presentation slide decks in Marp Markdown (slides.md) and standalone interactive HTML format (index.html). Syncs 1:1 with facilitator RUNBOOK.md timeline markers, hands-on lab steps, and 'Open in Colab' links.
---

# Workshop Slide Generator Skill

## Purpose

Automates the creation of high-impact, professional presentation slide decks for technical workshop facilitators. It reads workshop metadata (`README.md`), hands-on lab instructions (`workshop/03_labs/README.md`), and facilitator timelines (`RUNBOOK.md`) to produce ready-to-present slide decks synchronized 1:1 with session agenda milestones.

> 🌐 **Mandatory Autonomous Pre-Flight Web Search**:
> Before writing code snippets or architecture bullet points for slides, perform live web search (`search_web`) to verify latest SDK imports and active model names.
>
> 🌍 **Developer-Idiomatic Localization Protocol**:
> When generating slide content in Korean, Japanese, or Chinese:
> - **NEVER perform awkward literal / word-for-word machine translations**.
> - **MUST use authentic developer community terminology & jargon**:
>   - **Korean (KO)**: "프롬프트 엔지니어링", "핸즈온 랩", "스캐폴딩", "의존성 주입", "양자화", "파인튜닝", "런북", "임베딩" (Never ❌ "손으로 하는 실험실").
>   - **Japanese (JA)**: 「ハンズオン」, 「デプロイ」, 「スキャフォールディング」, 「トークン」, 「ファインチューニング」, 「ランブック」.
>   - **Chinese (ZH)**: 「实战工作坊」, 「脚手架」, 「提示词工程」, 「微调」, 「演练手册」.

---

## 🚀 Key Features

1. **Standard Slide Deck Architecture**:
   - **Slide 1: Title & Hero**: Workshop name, speaker info, community banner.
   - **Slide 2: Agenda & Learning Goals**: Minute-by-minute session flow.
   - **Slide 3: Prerequisites & Architecture Check**: OS-specific setup guidance & offline asset fallback.
   - **Slide 4: Concept & Architecture Overview**: High-level workflow with Mermaid diagram support.
   - **Slide 5~7: Hands-on Labs (1, 2, 3)**: Step-by-step instructions, code snippets, expected outputs, and 'Open in Colab' QR/links.
   - **Slide 8: Live Troubleshooting & Common Errors**: 10-second hotfixes and RAM tier guidance.
   - **Slide 9: Q&A, Wrap-up & Survey**: Feedback link and community resource QR.

2. **Facilitator Runbook 1:1 Sync**:
   - Slide numbers and section titles precisely match the `[Slide #X]` sync markers in `RUNBOOK.md`.

3. **Multi-Format Export Support**:
   - **Marp Markdown**: Uses modern styling (`theme: gaia` / `uncover`), CSS variables, scoped header footers, and presenter notes (`<!-- speaker notes -->`).
   - **Standalone Web Presentation**: Built-in dark/light theme, full-screen mode (`F`), slide overview (`O`), and presenter timer.

---

### 3. Deliverables Artifacts Structure

Generated inside `<workshop-project>/output/slides/`:

```
output/slides/
├── slides.pptx               # 16:9 Google Slides & PowerPoint Native Deck (Ready for Google Slides Import)
├── create_google_slides.gs   # Google Apps Script macro for direct Google Drive creation
├── slides.md                 # Marp Markdown presentation deck
├── index.html                # Standalone interactive zero-dependency Web presentation
├── README.md                 # Slide presentation and Google Slides import guide
```

---

## ⚡ Step-by-Step Google Slides Integration

### Method 1: Google Slides 1-Click Import (Recommended)
1. Open [slides.google.com](https://slides.google.com) and click **Blank Presentation** (+).
2. Go to **File ➔ Import slides** (`파일 ➔ 슬라이드 가져오기`).
3. Under the **Upload** tab, drag and drop `output/slides/slides.pptx`.
4. Click **Select all slides** ➔ **Import slides**.
5. The full 16:9 widescreen dark presentation is immediately imported and ready to present!

### Method 2: Google Apps Script Creation
1. Open [script.google.com](https://script.google.com) and create a New Project.
2. Paste the code from `output/slides/create_google_slides.gs` and click **Run**.
3. A new Google Slides file is directly created in your Google Drive.

---

## ⚡ CLI Command Reference

```bash
# Build Google Slides (.pptx), Marp Markdown, and Web HTML
python3 harness_cli.py build-slides --target my-bwai-workshop
```

### 2. Present Slides Locally in Browser
```bash
open my-bwai-workshop/output/slides/index.html
```

### 3. (Optional) Export to PDF / PPTX via Marp CLI
```bash
# Export using Marp CLI if installed
npx @marp-team/marp-cli@latest output/slides/slides.md --pdf -o output/slides/slides.pdf
npx @marp-team/marp-cli@latest output/slides/slides.md --pptx -o output/slides/slides.pptx
```

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
