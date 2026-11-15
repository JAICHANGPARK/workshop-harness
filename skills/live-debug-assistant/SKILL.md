---
name: live-debug-assistant
description: Analyzes terminal error logs in under 10 seconds and outputs actionable fix commands. Includes API Key security scanning protocol to prevent accidental credential exposure.
---

# Live Debug Assistant Skill

## Purpose
During live workshop sessions, attendees frequently hit unexpected errors and paste unformatted error logs into chat or terminal windows. This skill enables TAs and facilitators to rapidly analyze error tracebacks, redact exposed API keys, identify the root cause, and provide a single copy-paste hotfix command within 10 seconds.

---

## 10-Second Diagnostic Triage Workflow

```text
[Raw Stderr Log] -> [Scan & Redact Secrets] -> [Pattern Match Root Cause] -> [Generate Copy-Paste Fix Command]
```

### Common Error Pattern & Resolution Matrix

| Error Pattern / Traceback | Root Cause | Instant Fix Command |
|---|---|---|
| `ConnectionRefusedError: [Errno 61]` | Ollama server process not running on port 11434 | `ollama serve &` |
| `ModuleNotFoundError: No module named 'xxx'` | Missing dependency in active virtualenv | `uv pip install xxx` |
| `Error: model 'gemma4:e4b' not found` | Model tag not pulled into local runtime | `ollama pull gemma4:e4b` |
| `PermissionError: [Errno 13] Permission denied` | Script lacks execution bit | `chmod +x scripts/*.sh` |
| `ENOSPC: no space left on device` | Local disk full from cached models | `ollama rm <unused-model>` |
| `google.api_core.exceptions.InvalidArgument: 400 API key not valid` | Missing or corrupted `GEMINI_API_KEY` | `export GEMINI_API_KEY="AIzaSy..."` |
| `docker: Cannot connect to the Docker daemon` | Docker service stopped or missing socket permissions | `sudo systemctl start docker` or `sudo usermod -aG docker $USER` |
| `Address already in use: 8080` | Port collision on local web server | `lsof -i :8080 | awk 'NR>1 {print $2}' | xargs kill -9` |

---

## API Key & Credential Security Protocol

Before displaying or processing any raw log output, the agent **must** run automated security regex pattern scans and redact exposed secrets:

```regex
- Google AI Studio Key:  AIzaSy[A-Za-z0-9_-]{33}      -> [REDACTED_GEMINI_API_KEY]
- OpenAI API Key:       sk-[A-Za-z0-9]{48}           -> [REDACTED_OPENAI_KEY]
- Anthropic API Key:    sk-ant-[A-Za-z0-9_-]{48}     -> [REDACTED_ANTHROPIC_KEY]
- GitHub Token:         ghp_[A-Za-z0-9]{36}          -> [REDACTED_GITHUB_TOKEN]
- AWS Access Key:       AKIA[0-9A-Z]{16}             -> [REDACTED_AWS_KEY]
```

### Security Alert & Revocation Trigger
If an un-redacted API key is detected in attendee input:
1. Immediately issue a warning: `🚨 SECURITY ALERT: Exposed API key detected and redacted!`
2. Instruct the attendee to immediately revoke the exposed key in their Google AI Studio / Cloud console.
3. Remind the attendee to store credentials in `.env` and verify `.env` is listed in `.gitignore`.

---

## Structured Agent Response Schema

When providing assistance, output a concise 3-part diagnostic response:

```markdown
### 🔍 Diagnostic Result
- **Error Type**: `ConnectionRefusedError`
- **Root Cause**: Local Ollama server is not running on port 11434.

### ⚡ 10-Second Hotfix
Execute this command in your terminal:
```bash
ollama serve &
```

---

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
