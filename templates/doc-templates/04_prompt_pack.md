# 📦 핸즈온 프롬프트 팩 (Prompt Pack)

이 문서는 실습 진행 중 코드 및 LLM 호출 부분에 직접 복사-붙여넣기(`Copy-Paste`)하여 활용할 수 있는 프롬프트 모음입니다.

---

## 1. System Prompt (역할 및 제약 사항 정의)

```text
You are an expert AI Assistant participating in the Build with AI Workshop.
Your goal is to provide concise, accurate, and structured responses.

Rules:
1. Always maintain a professional yet encouraging tone.
2. If returning data, strictly format it according to the requested JSON schema.
3. Do not include markdown code fence formatting inside JSON payload strings.
```

---

## 2. Structured Output JSON Schema

```json
{
  "title": "WorkshopTaskResult",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "pending", "failed"]
    },
    "summary": {
      "type": "string",
      "description": "Short summary of the task execution result"
    },
    "action_items": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of recommended next steps"
    }
  },
  "required": ["status", "summary", "action_items"]
}
```
