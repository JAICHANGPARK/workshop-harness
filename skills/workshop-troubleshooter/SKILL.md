---
name: workshop-troubleshooter
description: Generates OS-specific and RAM-tier-specific (8GB, 16GB, 32GB+) troubleshooting guides and FAQ documents covering offline/network failure scenarios, model download failures, API port mismatches (Ollama 11434 vs LM Studio 1234), and GPU/CPU fallback strategies.
---

# Workshop Troubleshooter Skill

## Purpose
Hardware variations, operating system firewall policies, and local LLM server port mismatches cause predictable attendee failures during live workshops. This skill pre-generates complete troubleshooting matrices (`docs/20-faq.md` and troubleshooting guides) so facilitators and TAs can resolve issues in under 30 seconds.

---

## RAM-Tier Sizing & Model Selection Matrix

| Hardware RAM Tier | Maximum Parameter Size | Recommended Local Model Tag | Context Window Limit (`num_ctx`) |
|---|---|---|---|
| **8GB RAM** | 2B - 8B (4-bit quantized) | `gemma4:e2b`, `qwen3:8b`, or `deepseek-r1:8b` | `2048` |
| **16GB RAM** | 4B - 14B parameters | `gemma4:e4b`, `qwen3:14b`, or `deepseek-r1:14b` | `4096` |
| **32GB+ RAM** | 12B - 31B / MoE parameters | `gemma4:e12b`, `gemma4:26b-a4b`, `gemma4:31b`, `qwen3.6:27b`, `qwen3-coder:30b`, or `llama4:scout` | `8192` - `32768` |

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

---

## Typography, Developer Terminology & Bilingual Notation Rules

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
