#!/usr/bin/env python3
"""
generate_prep_pdf.py - Workshop Harness PDF Generator
Uses ReportLab, PyMuPDF (fitz), and Pillow to build markdown guide documents from the docs/
directory into a single publication-quality PDF handout with a preview contact sheet image.
"""

import os
import sys
import glob
import re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

def format_pdf_text(text: str) -> str:
    """Sanitize forbidden em-dashes, escape XML special characters, then apply basic bold/italic markdown formatting."""
    if "\u2014" in text:
        text = re.sub(r"(?<=\S)\u2014(?=\S)", " - ", text).replace("\u2014", "-")
    escaped = xml_escape(text)
    escaped = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped)
    escaped = re.sub(r'\*(.*?)\*', r'<i>\1</i>', escaped)
    return escaped

def _select_pdf_font(md_files) -> str:
    """Detect Korean, Japanese, or Chinese content in docs and register a built-in ReportLab CID font."""
    from reportlab.lib.fonts import addMapping
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    sample = ""
    for fp in md_files[:10]:
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                sample += f.read(4096)
        except Exception:
            continue

    cid_font = None
    if re.search(r"[\uac00-\ud7a3]", sample):
        cid_font = "HYGothic-Medium"
    elif re.search(r"[\u3040-\u30ff]", sample):
        cid_font = "HeiseiKakuGo-W5"
    elif re.search(r"[\u4e00-\u9fff]", sample):
        cid_font = "STSong-Light"

    if cid_font:
        pdfmetrics.registerFont(UnicodeCIDFont(cid_font))
        for bold_flag in (0, 1):
            for italic_flag in (0, 1):
                addMapping(cid_font, bold_flag, italic_flag, cid_font)
        return cid_font
    return "Helvetica"


def generate_pdf(docs_dir: str, output_pdf_path: str, preview_dir: str):
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        print(f"Error: reportlab is not installed ({exc}). Run: pip install reportlab pymupdf pillow")
        sys.exit(1)

    print(f"📄 Building PDF from docs in '{docs_dir}' -> '{output_pdf_path}'...")
    
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)

    md_files = sorted(glob.glob(os.path.join(docs_dir, "*.md")))
    if not md_files:
        md_files = sorted(glob.glob("*.md"))

    base_font = _select_pdf_font(md_files)
    is_ko = base_font == "HYGothic-Medium"

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=base_font,
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName=base_font,
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#202124'),
        spaceBefore=12,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=base_font,
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#3c4043'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=base_font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#3c4043'),
        spaceAfter=6
    )

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    
    # Title Page
    if is_ko:
        story.append(Paragraph("핸즈온 워크숍 사전 준비 및 실습 가이드", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a73e8'), spaceAfter=20))
        story.append(Paragraph("사전 개발 환경 세팅, 트러블슈팅 FAQ, 핵심 개념 치트시트를 한 권으로 묶은 핸드아웃입니다.", body_style))
    else:
        story.append(Paragraph("BWAI Workshop Guide & Handout", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a73e8'), spaceAfter=20))
        story.append(Paragraph("This document contains full preparation guides and hands-on session materials.", body_style))
    story.append(Spacer(1, 20))

    for filepath in md_files:
        filename = os.path.basename(filepath)
        story.append(Paragraph(f"Doc: {filename}", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10))

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("# "):
                story.append(Paragraph(format_pdf_text(line_str[2:]), h1_style))
            elif line_str.startswith("## "):
                story.append(Paragraph(format_pdf_text(line_str[3:]), h2_style))
            elif line_str.startswith("### "):
                story.append(Paragraph(format_pdf_text(line_str[4:]), h2_style))
            elif line_str.startswith("- ") or line_str.startswith("* "):
                story.append(Paragraph(f"• {format_pdf_text(line_str[2:])}", body_style))
            else:
                story.append(Paragraph(format_pdf_text(line_str), body_style))

        story.append(Spacer(1, 15))
        story.append(PageBreak())

    doc.build(story)
    print(f"✅ PDF Build Successful: {output_pdf_path}")

    # Generate preview image if pymupdf & pillow installed
    try:
        import fitz  # PyMuPDF
        from PIL import Image

        pdf_doc = fitz.open(output_pdf_path)
        print(f"🖼️ Rendering {len(pdf_doc)} pages preview contact sheet...")
        
        images = []
        for page_index in range(min(len(pdf_doc), 8)): # Top 8 pages
            page = pdf_doc.load_page(page_index)
            pix = page.get_pixmap(dpi=150)
            img_path = os.path.join(preview_dir, f"page_{page_index+1}.png")
            pix.save(img_path)
            images.append(Image.open(img_path))
        
        if images:
            # Stitch into contact sheet
            w, h = images[0].size
            cols = 4
            rows = (len(images) + cols - 1) // cols
            contact = Image.new('RGB', (w * cols, h * rows), (240, 240, 240))
            for idx, img in enumerate(images):
                r = idx // cols
                c = idx % cols
                contact.paste(img, (c * w, r * h))
            contact_path = os.path.join(preview_dir, "contact_sheet.png")
            contact.save(contact_path)
            print(f"🖼️ Contact sheet preview created: {contact_path}")
    except Exception as e:
        print(f"ℹ️ Preview generation skipped ({e})")

if __name__ == "__main__":
    docs_path = sys.argv[1] if len(sys.argv) > 1 else "docs"
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else "output/pdf/prep-guide.pdf"
    preview = sys.argv[3] if len(sys.argv) > 3 else "tmp/pdfs"
    generate_pdf(docs_path, out_pdf, preview)
