---
name: pdf-handout-generator
description: Converts markdown documentation files into publication-ready PDF handouts and preview contact sheets using ReportLab, PyMuPDF (fitz), and Pillow.
---

# PDF Handout Generator Skill

## Purpose
Generates printable, publication-quality PDF handouts from the `docs/` markdown directory and creates a visual contact sheet preview image for quick inspection before distribution.

## Dependencies
- `reportlab` (>=4.0.0)
- `pymupdf` (>=1.23.0, imported as `fitz`)
- `pillow` (>=10.0.0)

All dependencies are auto-installed via `uv` when running `harness_cli.py build-pdf`.

## Output Artifacts
- `output/pdf/<project-name>-prep-guide.pdf` - Combined PDF handout
- `tmp/pdfs/contact_sheet.png` - Visual thumbnail preview of all PDF pages
