---
name: workshop-troubleshooter
description: Generates OS-specific and RAM-tier-specific (8GB, 16GB, 32GB+) troubleshooting guides and FAQ documents covering offline/network failure scenarios, model download failures, API port mismatches (Ollama 11434 vs LM Studio 1234), and GPU/CPU fallback strategies.
---

# Workshop Troubleshooter Skill

## Purpose
Attendees encounter predictable failure patterns based on their hardware tier, local LLM port configurations, and operating system. This skill pre-generates troubleshooting matrices so facilitators can resolve issues in under 30 seconds during the live session.

## RAM-Tier Troubleshooting Matrix

| RAM Tier | Max Model Size | Recommended Configuration |
|---|---|---|
| 8GB | 2B parameters max | `gemma4:e2b` or `phi-4-mini` with `num_ctx=2048` |
| 16GB | 4B parameters comfortable | `gemma4:e4b` with `num_ctx=4096` |
| 32GB+ | 12B+ parameters | `gemma4:e12b` or `qwen3:14b` with `num_ctx=8192` |

## Local LLM Server Port & Error Resolution Table

| Error Message / Symptom | Root Cause | Port / Tool | Fix Action |
|---|---|---|---|
| `connection refused :11434` | Ollama server process not running | Port 11434 (Ollama) | Run `ollama serve &` in terminal |
| `connection refused :1234` | LM Studio server not started | Port 1234 (LM Studio) | Go to LM Studio `Developer` tab -> Click `Start Server` |
| `404 Not Found` on `/v1/chat/completions` | Port mismatch (pointing to Ollama 11434 instead of LM Studio 1234, or vice versa) | Port 11434 / 1234 | Update client `base_url`: `http://localhost:11434/v1` for Ollama, `http://localhost:1234/v1` for LM Studio |
| `Error: model not found` | Model not downloaded into local runtime | Ollama / LM Studio | Run `ollama pull gemma4:e4b` or search & download in LM Studio GUI |
| `Error: insufficient memory` | Model exceeds available RAM | Hardware limit | Switch to smaller quantization: `gemma4:e2b` |
| `CUDA out of memory` | GPU VRAM exhausted | GPU limit | Force CPU mode: `CUDA_VISIBLE_DEVICES="" ollama serve` |
| `API key invalid` | Expired or misconfigured Gemini/GCP key | Cloud API | Re-issue at [aistudio.google.com](https://aistudio.google.com) |

## Output Artifacts
- `docs/troubleshooting.md` - Complete troubleshooting guide by OS, port, and RAM tier
