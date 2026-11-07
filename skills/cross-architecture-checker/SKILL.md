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
4. **`ollama` in stack**:
   - *Risk*: High RAM model selection (`12B+`) crashes 8GB RAM laptops.
   - *Fix*: Provide model quantization tiers (`gemma4:e2b` for 8GB, `gemma4:e4b` for 16GB, `gemma4:e12b` for 32GB+).
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
