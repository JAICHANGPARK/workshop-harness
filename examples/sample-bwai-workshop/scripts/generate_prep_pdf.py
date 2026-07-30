#!/usr/bin/env python3
"""
generate_prep_pdf.py - Workshop Harness PDF Generator
ReportLab, PyMuPDF(fitz), Pillow를 사용하여 docs/ 디렉토리의 마크다운 가이드 문서들을
출판용 품질의 단일 PDF 핸드아웃으로 빌드하고, 미리보기 contact sheet 이미지를 생성합니다.
"""

import os
import sys
import glob
import re
from pathlib import Path

def generate_pdf(docs_dir: str, output_pdf_path: str, preview_dir: str):
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Code
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
    except ImportError:
        print("❌ Error: reportlab is not installed. Run: pip install reportlab pymupdf pillow")
        sys.exit(1)

    print(f"📄 Building PDF from docs in '{docs_dir}' -> '{output_pdf_path}'...")
    
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#202124'),
        spaceBefore=12,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#3c4043'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
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
    story.append(Paragraph("BWAI Workshop Guide & Handout", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a73e8'), spaceAfter=20))
    story.append(Paragraph("This document contains full preparation guides and hands-on session materials.", body_style))
    story.append(Spacer(1, 20))

    md_files = sorted(glob.glob(os.path.join(docs_dir, "*.md")))
    if not md_files:
        # Fallback to main README or root md files
        md_files = sorted(glob.glob("*.md"))

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
                story.append(Paragraph(line_str[2:], h1_style))
            elif line_str.startswith("## "):
                story.append(Paragraph(line_str[3:], h2_style))
            elif line_str.startswith("### "):
                story.append(Paragraph(line_str[4:], h2_style))
            elif line_str.startswith("- ") or line_str.startswith("* "):
                story.append(Paragraph(f"• {line_str[2:]}", body_style))
            else:
                # Clean basic markdown tags
                clean_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_str)
                clean_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_text)
                story.append(Paragraph(clean_text, body_style))

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
