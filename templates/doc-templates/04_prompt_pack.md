# Hands-on Prompt Pack

This document contains a collection of copy-paste ready prompts for use during the workshop labs, covering system prompts, structured output schemas, and LLM invocation patterns.

---

## 1. System Prompt (Role & Constraint Definition)

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
