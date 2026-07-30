---
name: pdf-handout-generator
description: ReportLab, PyMuPDF, Pillow를 사용하여 markdown 가이드 문서들을 하나의 고품질 PDF 핸드아웃으로 병합/변환하고 미리보기 렌더링을 자동화하는 스킬
---

# PDF Handout Generator Skill

## 📌 목적
`docs/` 폴더에 분산된 수십 개의 마크다운 가이드 파일들을 인쇄/배포 가능한 출판용 품질의 단일 PDF 파일(`output/pdf/prep-guide.pdf`)로 생성하고, 렌더링 품질을 시각적으로 빠르게 검증할 수 있도록 미리보기 메타 이미지(Contact Sheet)를 자동 생성합니다.

## 🛠️ 필수 의존성 (Python)

```bash
pip install reportlab pymupdf pillow
```

## 🎨 주요 기술 요구사항 & 디자인 스타일

1. **한국어 폰트 및 스타일링**:
   - macOS: `Pretendard`, `AppleSDGothicNeo`, `NanumGothic` 우선 탐색 후 Fallback
   - 제목, 본문, 코드 블록 (`Courier` / `D2Coding`), 표 스타일링
   - 커스텀 ParagraphStyle (제목 depth별 계층적 여백 및 색상 할당)

2. **문서 요소 자동 파싱 & 렌더링**:
   - 마크다운 `#`, `##`, `###` -> ReportLab `Heading1`, `Heading2`, `Heading3` 변환
   - 볼드 `**text**`, 이탈릭 `*text*`, 인라인 코드 `` `code` `` 변환
   - 마크다운 표 (`| ... |`) -> ReportLab `Table` 객체 변환 (테두리, 헤더 배경색 적용)
   - 마크다운 코드 블록 (```...```) -> 배경 박스가 있는 `Preformatted` 코드로 렌더링
   - 이미지 태그 `![alt](path)` -> ReportLab `Image` 객체로 삽입

3. **페이지 레이아웃 & 번호 매기기**:
   - 표지 (Title Page) 및 목차 (Table of Contents)
   - 헤더(문서 제목) 및 푸터 (페이지 번호 "Page X of Y")

4. **PyMuPDF + Pillow 기반 Contact Sheet (미리보기) 생성**:
   - PDF 생성 완료 후 PyMuPDF(`fitz`)로 페이지별 PNG 렌더링
   - Pillow(`PIL`)를 사용하여 N*M 그리드 미리보기 이미지(`tmp/pdfs/contact-1.png` 등) 생성

## 📜 표준 PDF 빌더 스크립트 구조 (`scripts/generate_prep_pdf.py`)

`workshop-harness/templates/pdf-templates/generate_prep_pdf.py` 템플릿을 참고하여 워크숍 리포지토리에 맞게 자동 커스텀 생성합니다.

```bash
python3 scripts/generate_prep_pdf.py
```
- Output PDF: `output/pdf/<workshop-name>-prep-guide.pdf`
- Output Previews: `tmp/pdfs/<workshop-name>-contact-*.png`
