---
name: live-debug-assistant
description: Analyzes terminal error logs in under 10 seconds and outputs actionable fix commands. Includes API Key security scanning protocol to prevent accidental credential exposure.
---

# Live Debug Assistant Skill

## Purpose
During live workshop sessions, attendees frequently paste terminal error logs into chat or show them on screen. This skill enables facilitators and TAs to diagnose errors within 10 seconds and provide a copy-paste-ready fix command.

## Diagnosis Protocol

### Step 1: Error Pattern Matching
```
Input:  Raw terminal error log (stderr output)
Output: { "error_type": "...", "root_cause": "...", "fix_command": "..." }
```

### Step 2: Common Error Patterns

| Error Pattern | Diagnosis | Fix Command |
|---|---|---|
| `ConnectionRefusedError: [Errno 61]` | Ollama server not running | `ollama serve &` |
| `ModuleNotFoundError: No module named 'xxx'` | Missing Python package | `uv pip install xxx` |
| `Error: model 'xxx' not found` | Model not pulled | `ollama pull xxx` |
| `PermissionError: [Errno 13]` | Insufficient file permissions | `chmod +x script.sh` |
| `ENOSPC: no space left on device` | Disk full | `ollama rm <unused-model>` |

## API Key Security Protocol

### Credential Leak Prevention
When processing error logs, the agent **must** scan for and redact any exposed credentials:

```
Detected patterns to redact:
- AIzaSy[A-Za-z0-9_-]{33}     -> [REDACTED_GEMINI_KEY]
- sk-[A-Za-z0-9]{48}          -> [REDACTED_OPENAI_KEY]
- ghp_[A-Za-z0-9]{36}         -> [REDACTED_GITHUB_TOKEN]
```

### Security Enforcement
- If a credential is detected in a public channel (chat, screen share), immediately warn the attendee
- Guide them to revoke and re-issue the compromised key
- Verify `.gitignore` includes `.env` and `*.json` patterns
