---
name: workshop-web-researcher
description: 워크숍 사전 준비 가이드 및 실습 코드 제작 시 웹 검색을 수행하여 도구(Ollama, LM Studio, uv, Docker, LLM 모델 등)의 최신 릴리스 버전, Breaking Changes, 최신 패키지 버전을 조사하고 최신성(Latest Currency)을 보장하는 스킬
---

# Workshop Web Researcher & Live Docs Updater Skill

## 📌 목적
AI 모델, SDK, 패키지 매니저(Ollama, LM Studio, Python uv, Flutter/Dart, Docker 등)는 버전 업데이트가 매우 빈번합니다. 과거의 구버전 명령어나 지원 중단(Deprecated)된 플래그로 자료를 제작하면 현장에서 실행 에러가 발생하므로, **웹 검색(Web Search)을 통해 실시간 최신 버전, 공식 변경사항(Release Notes) 및 최신 태그를 검증하여 자료에 반영**합니다.

---

## 🔍 최신성 검증 4대 룰 (Live Currency Rules)

1. **실시간 패키지 & 도구 릴리스 검색**:
   - `Ollama latest release version & model tags` (예: Gemma 4 최신 양자화 태그)
   - `Python uv latest CLI flags` (`uv sync`, `uv run` 변경사항)
   - `Docker Desktop latest OS compatibility`
2. **파괴적 변경(Breaking Changes) 감지**:
   - 이전 버전과 달라진 API 메서드 파라미터(Deprecated arguments) 필터링
3. **기준 확인일 및 출처 명시 (Citation & Date Timestamp)**:
   - 생성되는 사전 준비 문서 상단에 `기준 확인일: YYYY-MM-DD` 명시
   - 문서 하단에 공식 릴리스 페이지 및 마이그레이션 가이드 URL 링크 첨부
4. **구버전 명령어 호환 우회(Fallback)**:
   - 최신 버전 및 하위 버전(Legacy) 양쪽 모두에서 동작하는 안전한 CLI 구문 채택

---

## 🛠️ 에이전트 프롬프트 활용 예시

- *"workshop-web-researcher 스킬을 사용해서 최신 Ollama와 Gemma 4 모델 태그를 웹 검색으로 확인한 뒤 docs/01-hardware.md의 다운로드 명령어를 최신화해줘."*
- *"uv 패키지 매니저의 최신 설치 명령어와 pyproject.toml 동기화 구문을 검색해서 사전 가이드에 반영해줘."*
