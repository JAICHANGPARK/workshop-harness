---
name: workshop-troubleshooter
description: Generates OS-specific and RAM-tier-specific (8GB, 16GB, 32GB+) troubleshooting guides and FAQ documents covering offline/network failure scenarios, model download failures, API port mismatches (Ollama 11434 vs LM Studio 1234), and GPU/CPU fallback strategies.
---

# Workshop Troubleshooter Skill

## Purpose
Hardware variations, operating system firewall policies, and local LLM server port mismatches cause predictable attendee failures during live workshops. This skill pre-generates complete troubleshooting matrices (`docs/20-faq.md` and troubleshooting guides) so facilitators and TAs can resolve issues in under 30 seconds.

---

## RAM-Tier Sizing & Model Selection Matrix

| Hardware RAM Tier | Maximum Parameter Size | Recommended Ollama Model Tag | Context Window Limit (`num_ctx`) |
|---|---|---|---|
| **8GB RAM** | 2B parameters max | `gemma4:e2b` or `phi-4-mini` | `2048` |
| **16GB RAM** | 4B parameters comfortable | `gemma4:e4b` | `4096` |
| **32GB+ RAM** | 12B - 14B parameters | `gemma4:e12b` or `qwen3:14b` | `8192` |

---

## Local LLM Server Port & Network Error Resolution

| Symptom / Error Message | Root Cause | Port / Tool | Immediate Fix Action |
|---|---|---|---|
| `connection refused :11434` | Ollama server process not running | Port 11434 (Ollama) | Run `ollama serve &` in terminal |
| `connection refused :1234` | LM Studio server not started | Port 1234 (LM Studio) | Go to LM Studio `Developer` tab -> Click `Start Server` |
| `404 Not Found` on `/v1/chat/completions` | Port mismatch (pointing to Ollama 11434 instead of LM Studio 1234, or vice versa) | Port 11434 / 1234 | Update client `base_url`: `http://localhost:11434/v1` for Ollama, `http://localhost:1234/v1` for LM Studio |
| `Error: model not found` | Model tag not pulled into local server runtime | Ollama / LM Studio | Run `ollama pull gemma4:e4b` or search in LM Studio UI |
| `CUDA out of memory` / `VRAM exhausted` | GPU memory exceeded by large context or model size | VRAM limit | Force CPU mode: `CUDA_VISIBLE_DEVICES="" ollama serve` |
| `Windows Firewall blocking port` | Local firewall blocking incoming loopback connections | Windows Security | Run PowerShell: `New-NetFirewallRule -DisplayName "Ollama Port" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow` |

---

## Network Offline & Venue WiFi Fallback Protocol

If the venue network becomes unavailable:
1. Run `./scripts/bundle_offline_assets.sh` prior to the event to pre-download model weights and pip packages.
2. Direct attendees to load pre-cached GGUF model binaries locally via `ollama create my-local-model -f Modelfile`.
3. Provide local fallback scripts running without external internet access.

---

## Output Artifact Specifications

- **File Path**: `docs/20-faq.md` and `docs/01-hardware-and-env.md`
