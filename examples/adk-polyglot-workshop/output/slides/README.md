# Presentation Slides for adk-polyglot-workshop

> Topic: Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)

---

## 📊 1. Google Slides (구글 프레젠테이션) 사용 방법

### 방법 A: PPTX 1초 가져오기 (가장 추천)
1. **Google Slides ([slides.google.com](https://slides.google.com))** 접속
2. **`새 프레젠테이션 시작`** 클릭
3. 상단 메뉴에서 **`파일(File)` ➔ `슬라이드 가져오기(Import slides)`** 클릭
4. **`업로드(Upload)`** 탭에서 **`output/slides/slides.pptx`** 파일을 드래그하여 업로드
5. **`모든 슬라이드 선택(Select all slides)`** ➔ **`슬라이드 가져오기(Import slides)`** 클릭
6. 16:9 와이드스크린 다크 테마의 완성된 구글 슬라이드가 즉시 생성됩니다!

### 방법 B: Google Apps Script 매크로로 자동 생성
1. [script.google.com](https://script.google.com) 접속 후 **새 프로젝트** 생성
2. `output/slides/create_google_slides.gs` 파일의 코드를 복사하여 붙여넣기
3. 상단 메뉴의 **`실행(Run)`** 클릭
4. 구글 드라이브 내에 새 구글 프레젠테이션이 자동 생성됩니다.

---

## 🌐 2. 단독 웹 브라우저 프레젠테이션 (Zero-Setup)

- 별도 도구 설치 없이 브라우저에서 바로 발표할 수 있습니다:
```bash
open output/slides/index.html
```
- 단축키:
  - `Space` / `→` : 다음 슬라이드
  - `←` : 이전 슬라이드
  - `F` : 전체화면 (Fullscreen)
  - `Home` / `End` : 처음 / 마지막 슬라이드

---

## 📝 3. Marp Markdown & PDF 변환

- VS Code Marp 확장 프로그램을 통해 `slides.md`를 열어 발표 및 편집할 수 있습니다.
- Marp CLI를 통한 PDF 컴파일:
```bash
npx @marp-team/marp-cli@latest output/slides/slides.md --pdf -o output/slides/slides.pdf
```
