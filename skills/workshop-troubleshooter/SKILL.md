---
name: workshop-troubleshooter
description: Generates OS-specific and RAM-tier-specific (8GB, 16GB, 32GB+) troubleshooting guides and FAQ documents covering offline/network failure scenarios, model download failures, and GPU/CPU fallback strategies.
---

# Workshop Troubleshooter Skill

## Purpose
Attendees encounter predictable failure patterns based on their hardware tier and operating system. This skill pre-generates troubleshooting matrices so facilitators can resolve issues in under 30 seconds during the live session.

## RAM-Tier Troubleshooting Matrix

| RAM Tier | Max Model Size | Recommended Configuration |
|---|---|---|
| 8GB | 2B parameters max | `gemma4:e2b` or `phi-4-mini` with `num_ctx=2048` |
| 16GB | 4B parameters comfortable | `gemma4:e4b` with `num_ctx=4096` |
| 32GB+ | 12B+ parameters | `gemma4:e12b` or `qwen3:14b` with `num_ctx=8192` |

## Common Error Resolution Table

| Error Message | Root Cause | Fix Command |
|---|---|---|
| `Error: model not found` | Model not downloaded | `ollama pull gemma4:e4b` |
| `Error: insufficient memory` | Model exceeds available RAM | Switch to smaller quantization: `gemma4:e2b` |
| `connection refused :11434` | Ollama server not running | `ollama serve &` |
| `CUDA out of memory` | GPU VRAM exhausted | Set CPU mode: `CUDA_VISIBLE_DEVICES="" ollama serve` |
| `API key invalid` | Expired or misconfigured key | Re-issue at [aistudio.google.com](https://aistudio.google.com) |

## Output Artifacts
- `docs/troubleshooting.md` - Complete troubleshooting guide by OS and RAM tier
