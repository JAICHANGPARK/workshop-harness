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

## Typography, Developer Terminology & Bilingual Notation Rules

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
