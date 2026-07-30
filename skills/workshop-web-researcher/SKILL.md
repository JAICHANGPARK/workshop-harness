---
name: workshop-web-researcher
description: 워크숍 사전 준비 가이드 및 실습 코드 제작 시 웹 검색을 수행하여 도구(Ollama, LM Studio, uv, Docker) 및 최신 AI 모델(Gemini, Gemma 4, Claude, Llama 등)의 최신 릴리스 버전과 태그를 조사하고 데이터의 최신성(Latest Currency)을 보장하는 스킬
---

# Workshop Web Researcher Skill (Dynamic AI Model & SDK Currency Protocol)

## 📌 목적
LLM 에이전트의 지식 컷오프(Cut-off)로 인해 **과거의 오래된 AI 모델명(예: `gpt-3.5`, `llama-2`, `gemma-1/2` 등)이나 Deprecated된 CLI 플래그가 워크숍 가이드 및 코드에 하드코딩되는 현상을 완벽히 방지**합니다.

실시간 웹 검색 및 최신 API/릴리스 태그 파인딩을 통해 현 시점 최신의 AI 모델 태그와 SDK 버전을 동적으로 주입합니다.

---

## 🎯 4대 동적 최신화 규칙 (Latest Currency Protocol)

### 1. 🚫 오래된 AI 모델명 하드코딩 엄금 (No Legacy Model Hardcoding)
- 과거 모델명(`gpt-3.5-turbo`, `gemini-1.0-pro`, `llama-2`, `gemma-1/2`)을 사전 준비 문서나 스크립트에 절대 하드코딩하지 않습니다.
- 코드 및 가이드 작성 시 **반드시 `search_web`으로 현 시점의 최신 릴리스 모델 태그**를 파악합니다.
  - 예: `ollama pull gemma4:e4b` (Gemma 4 최신 양자화 태그)
  - 예: `gemini-2.0-flash` 또는 현 시점 최신 Gemini 릴리스 모델

### 2. 🔍 실시간 모델 태그 파인딩 검색 쿼리 패턴
문서 생성 전 아래 검색 쿼리를 실행하여 최신 명칭을 확인합니다:
- `Ollama official latest model release tags <provider/model>`
- `Google AI Studio Gemini latest model naming convention`
- `HuggingFace trending GGUF models for local LLM 8GB RAM`

### 3. 📅 기준 확인일 및 최신 모델 라벨 표기 (Timestamped Currency Label)
생성되는 문서 및 스크립트 상단에 **모델 정보 확인 시점**을 의무적으로 명시합니다:

```markdown
> 💡 **최신 모델 기준 확인일**: YYYY-MM-DD (공식 Ollama/Gemini API 기준 최신 릴리스 모델 수록)
```

### 4. 🔄 대체 모델 가이드 공식 (Fallback Naming Pattern)
특정 모델 태그가 미래에 업데이트될 것에 대비해 모델 선택 공식을 함께 수록합니다:

```bash
# 최신 릴리스 모델 다운로드 예시
ollama pull gemma4:e4b   # (권장: 4-bit 양자화 기본 모델)
ollama pull gemma4:e2b   # (8GB RAM 경량화 모델)
```

---

## 🔗 참고 (References)

- **Ollama Model Library**: [https://ollama.com/library](https://ollama.com/library)
- **Google AI Studio Models**: [https://ai.google.dev/gemini-api/docs/models/gemini](https://ai.google.dev/gemini-api/docs/models/gemini)
- **HuggingFace Hub**: [https://huggingface.co/models](https://huggingface.co/models)
