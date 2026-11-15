---
name: pdf-handout-generator
description: Converts markdown documentation files into publication-ready PDF handouts and preview contact sheets using ReportLab, PyMuPDF (fitz), and Pillow.
---

# PDF Handout Generator Skill

## Purpose
Converts markdown documentation in `docs/` into publication-ready PDF handouts for workshop attendees, TAs, and facilitators. Automatically renders high-resolution page preview thumbnails and generates a visual contact sheet grid image (`contact_sheet.png`) for rapid quality assurance prior to printing or distribution.

---

## Dependencies & Auto-Resolution

PDF generation relies on three Python libraries managed via `uv`:
- **`reportlab`** (>=4.0.0): Builds programmatic PDF layouts, custom typography, page canvas headers/footers, and flowing document elements.
- **`pymupdf`** (`fitz`, >=1.23.0): Renders output PDF pages into high-DPI PNG image files.
- **`pillow`** (`PIL`, >=10.0.0): Tiles individual page images into a multi-column contact sheet matrix.

*Note: Dependencies are automatically checked and installed via `uv` when executing `harness_cli.py build-pdf`.*

---

## Styling & Layout Specifications

The PDF generator engine (`scripts/generate_prep_pdf.py`) applies the following publication standards:

1. **Page Margins & Dimensions**: Letter size (8.5 x 11 in) with 0.5 inch (36 pt) margins.
2. **Color Palette**:
   - Primary Accent: Google Blue (`#4285F4`)
   - Secondary Accent: Slate Dark (`#1E293B`)
   - Background Tint: Neutral Gray (`#F8FAFC`)
   - Text Color: Charcoal (`#0F172A`)
3. **Typography**:
   - Document Title: 24 pt Bold
   - Heading 1: 16 pt Bold with underline accent line
   - Heading 2: 13 pt Bold
   - Body Text: 10 pt Regular with 14 pt line leading
   - Code Blocks: 9 pt Monospace (`Courier`) inside rounded background boxes
4. **Header & Footer Canvas**:
   - Header: Workshop title and document section name right-aligned.
   - Footer: Left-aligned copyright notice and right-aligned dynamic page numbers ("Page X of Y").

---

## CLI Command Usage

Build the PDF handout and contact sheet preview using `harness_cli.py`:

```bash
uv run harness_cli.py build-pdf --target my-bwai-workshop
```

---

## Output Artifact Specifications

1. **`output/pdf/<project-name>-prep-guide.pdf`**: Consolidated PDF handout ready for printing or offline distribution.
2. **`tmp/pdfs/contact_sheet.png`**: High-resolution image preview displaying a 3x3 or 4x4 grid of all compiled PDF pages for visual inspection.

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
