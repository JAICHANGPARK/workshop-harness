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
