---
name: workshop-slide-generator
description: Generates high-impact, professional workshop presentation slide decks in Marp Markdown (slides.md) and standalone interactive HTML format (index.html). Syncs 1:1 with facilitator RUNBOOK.md timeline markers, hands-on lab steps, and 'Open in Colab' links.
---

# Workshop Slide Generator Skill

## Purpose

Automates the creation of publication-ready, beautifully formatted **presentation slide decks** for technical workshops (Build with AI, DevFest, hands-on labs). It parses workshop curriculum (`workshop/03_labs/README.md`), prerequisites, troubleshooting matrices, and facilitator runbooks (`RUNBOOK.md`) to produce:

1. **Marp-compatible Markdown** (`output/slides/slides.md`): Instant export to PDF/PPTX via Marp CLI or VS Code Marp extension.
2. **Standalone Interactive Web Presentation** (`output/slides/index.html`): Zero-dependency HTML/CSS slide deck runnable in any browser with keyboard navigation, presenter notes, and mobile responsiveness.

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
