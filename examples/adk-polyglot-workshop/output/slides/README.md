# Presentation Slides for adk-polyglot-workshop

> Topic: Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)

---

## 1. Google Slides (구글 프레젠테이션) Import Guide

### Option A: Native PPTX Import (Recommended)
1. Open **Google Slides ([slides.google.com](https://slides.google.com))**
2. Click **Blank presentation (새 프레젠테이션 시작)**
3. Select **File (파일) -> Import slides (슬라이드 가져오기)**
4. In the **Upload (업로드)** tab, drag and drop **`output/slides/slides.pptx`**
5. Click **Select all slides (모든 슬라이드 선택) -> Import slides (슬라이드 가져오기)**
6. A 16:9 widescreen dark-theme presentation deck is ready immediately.

### Option B: Google Apps Script Automation
1. Visit [script.google.com](https://script.google.com) and create a **New project (새 프로젝트)**
2. Copy and paste the contents of `output/slides/create_google_slides.gs`
3. Click **Run (실행)** in the top toolbar
4. A new Google Slides presentation will be created in your Google Drive automatically.

---

## 2. Standalone Web Presentation (Zero-Setup HTML)

Present directly in any web browser without installing external slide software:
```bash
open output/slides/index.html
```
Keyboard shortcuts:
- `Space` / `Right Arrow`: Next slide
- `Left Arrow`: Previous slide
- `F`: Toggle Fullscreen
- `Home` / `End`: Jump to first / last slide

---

## 3. Marp Markdown & PDF Compilation

Open `slides.md` with the VS Code Marp extension or compile to PDF using Marp CLI:
```bash
npx @marp-team/marp-cli@latest output/slides/slides.md --pdf -o output/slides/slides.pdf
```
