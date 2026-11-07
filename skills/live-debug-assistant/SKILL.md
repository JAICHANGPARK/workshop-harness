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

- **Original Technical Term First, Real-World Developer Terminology & Natural Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never use awkward word-for-word literal translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
  - **Use the original English technical term first and append the developer-friendly term in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence grammar used by local software engineers**:
    - **Korean (KO)**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**. Never use awkward literals ("손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트") or double passives (`~되어집니다` -> `~됩니다`).
    - **Japanese (JA)**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never 「手で触る実験室」, 「走る本」, 「骨組みコード」, 「思考の予算」; write in natural Japanese engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」 (Never 「手把手的实验室」, 「奔跑的书」, 「骨架代码」, 「思考预算」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
