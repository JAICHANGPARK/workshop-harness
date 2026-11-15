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
| **8GB RAM** | 270M - 8B (4-bit quantized) | `gemma4:e2b`, `embeddinggemma-2:270m`, `functiongemma`, `qwen3:8b`, or `deepseek-r1:8b` | `2048` |
| **16GB RAM** | 4B - 14B parameters | `gemma4:e4b`, `gemma4:12b`, `embeddinggemma-2`, `translategemma`, `qwen3:14b`, or `deepseek-r1:14b` | `4096` |
| **32GB+ RAM** | 26B MoE - 31B parameters | `gemma4:26b`, `gemma4:31b`, `medgemma1.5`, `qwen3.6:27b`, `qwen3-coder:30b`, or `llama4:scout` | `8192` - `32768` |

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

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
