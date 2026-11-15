---
name: cross-architecture-checker
description: Audits cross-architecture compatibility across Apple Silicon (arm64), Intel Mac (x86_64), Windows (x86/ARM64), Linux, and ChromeOS. Identifies known risks for tools like LM Studio, Docker, and MLX, and generates a fallback matrix document (docs/00-architecture-compatibility-matrix.md).
---

# Cross-Architecture Checker Skill

## Purpose
Workshop attendees bring a wide variety of hardware platforms (Apple Silicon M1-M4, Intel x86_64 Mac, Windows x86_64 / ARM64, Linux, ChromeOS). This skill performs automated and agentic audits of tech stacks against known architecture constraints, identifying compatibility risks *before* the workshop session and producing mandatory alternative fallback workflows.

---

## Hardware & OS Compatibility Matrix

| Architecture / OS | Primary Acceleration | Known Risks & Constraints | Mandatory Fallback Strategy |
|---|---|---|---|
| **macOS Apple Silicon** (`arm64`) | Metal / Unified Memory | Minimal risks; high performance for local LLMs | Standard Ollama or MLX (`mlx-lm`) acceleration |
| **macOS Intel** (`x86_64`) | CPU-only (No Metal) | LM Studio crashes / freezes; high latency; no Metal support | Force Ollama CLI (`ollama serve`) with quantized 2B/4B models (`gemma4:e2b`) or cloud API |
| **Windows 11 x86_64** | CUDA / DirectML / CPU | PowerShell script execution disabled by policy; WSL2 required for Docker | Provide PowerShell bypass scripts (`Set-ExecutionPolicy -Scope Process Bypass`) and native binary fallbacks |
| **Windows ARM64** (Snapdragon) | NPU / DirectML | x64 emulation performance overhead; Docker driver conflicts | Use native ARM64 Ollama builds or cloud Gemini API |
| **Linux** (Debian/Ubuntu/Arch) | CUDA / ROCm / CPU | No GUI support on headless servers; permission issues with docker socket | Terminal-only commands (`ollama serve &`) and user group additions (`sudo usermod -aG docker $USER`) |
| **ChromeOS** (Linux Container) | Virtualized CPU | Low RAM allocation; no direct GPU pass-through | Use cloud API (Google AI Studio / GCP Gemini) or small 2B quantized models |

---

## Tech Stack Audit Rules

When auditing a workshop tech stack string (e.g. `lmstudio,docker,mlx,python`), the agent must evaluate the following rules:

1. **`lmstudio` in stack**:
   - *Risk*: Intel Mac users will experience severe GUI lag or crashes due to lack of Metal support.
   - *Fix*: Mandate Ollama CLI (`http://localhost:11434`) as an alternative in `docs/00-architecture-compatibility-matrix.md`.
2. **`mlx` / `mlx-lm` in stack**:
   - *Risk*: Strictly restricted to Apple Silicon (`arm64`). Fails instantly on Windows, Linux, and Intel Mac.
   - *Fix*: Provide PyTorch / HuggingFace transformers or Ollama fallbacks for non-Apple Silicon users.
3. **`docker` in stack**:
   - *Risk*: Windows Home users without WSL2 or hypervisor enabled will fail to start Docker Desktop.
   - *Fix*: Provide local native executable setup or cloud sandbox alternatives.
4. **`ollama` / `gemma` / `embeddinggemma` in stack**:
   - *Risk*: High RAM model selection (`12B+` / `26B`) crashes 8GB RAM laptops.
   - *Fix*: Provide model quantization & modular memory tiers (`gemma4:e2b` + `embeddinggemma-2:270m` for 8GB, `gemma4:e4b` / `gemma4:12b` + `embeddinggemma-2` for 16GB, `gemma4:26b` / `gemma4:31b` for 32GB+).
5. **`gemini-live` / `audio` in stack (Real-time Streaming & Flutter `gemini_live`)**:
   - *Risk*: Acoustic echo causes Voice Activity Detection (VAD) self-interruption loop; OS mic privacy permissions blocked.
   - *Fix*: Mandate headphones/earphones in `RUNBOOK.md` and verify OS microphone permissions (macOS Privacy Settings, Windows App Permissions, Flutter `RECORD_AUDIO`).

---

## CLI Command Integration

Audit a given tech stack using `harness_cli.py`:

```bash
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"
```

---

## Generated Output Artifacts

1. **`docs/00-architecture-compatibility-matrix.md`**: Complete markdown matrix documenting supported platforms, risks, and fallback instructions for attendees.
2. **`scripts/check_architecture_compat.sh`**: Shell script for macOS/Linux to detect CPU architecture, available RAM, and GPU capabilities.
3. **`scripts/check_architecture_compat.ps1`**: PowerShell script for Windows to audit environment compatibility.

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
