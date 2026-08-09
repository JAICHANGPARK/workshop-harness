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
