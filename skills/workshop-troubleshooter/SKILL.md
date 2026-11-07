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
