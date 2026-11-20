---
name: prerequisite-checker
description: Generates OS-specific (macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) prerequisite setup guides covering language/SDK installation (Python, Node.js, Go, Flutter, Rust, Docker), local LLM server API port configuration (Ollama 11434 vs LM Studio 1234), latest AI model downloads, Google AI Studio / GCP Gemini API Key issuance steps, and automated environment verification scripts (check_env.sh, check_env.ps1).
---

# Prerequisite Checker & API Key / Local Server Guide Skill

## Purpose
Prevents attendees from getting blocked on workshop day due to missing programming languages, SDKs, AI models, local LLM server port misconfigurations, or missing **Google AI Studio / GCP Gemini API Keys** by generating comprehensive OS-specific setup documentation and automated verification scripts.

> **Mandatory Autonomous Pre-Flight Web Search**:
> Before generating setup guides, execute live web search (`search_web`) to verify current download URLs, CLI installer flags, and active model tags (e.g. `gemma4`, `gemini-4-carbon`, `gemini-4-neon`, `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.8-live`, `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`).
>
> **Developer-Idiomatic Localization Protocol**:
> When generating setup guides in Korean, Japanese, or Chinese, use authentic developer jargon and standard IT terminology. Never use awkward literal machine translations.

---

## Local LLM Server API & Port Configuration Matrix

When connecting to local LLM engines via OpenAI-compatible endpoints or native REST APIs, each tool uses distinct ports and base URLs:

| Tool | Default Port | Base API Endpoint / URL | OpenAI Compatibility Endpoint | Key Notes |
|---|---|---|---|---|
| **Ollama** | `11434` | `http://localhost:11434` | `http://localhost:11434/v1` | Natively supports OpenAI SDK (`base_url="http://localhost:11434/v1"`, `api_key="ollama"`) |
| **LM Studio** | `1234` | `http://localhost:1234` | `http://localhost:1234/v1` | Must click "Start Server" in Developer tab; OpenAI compatible endpoint (`api_key="lm-studio"`) |
| **vLLM / LocalAI** | `8000` | `http://localhost:8000` | `http://localhost:8000/v1` | High-throughput server fallback |

### Local API Integration Code Example (Python)

```python
# Connecting to Ollama via OpenAI SDK
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # Change to http://localhost:1234/v1 for LM Studio
    api_key="ollama",                      # Placeholder key required by SDK
)

response = client.chat.completions.create(
    model="gemma4:e4b",
    messages=[{"role": "user", "content": "Hello World"}],
)
print(response.choices[0].message.content)
```

---

## Google AI Studio & GCP Key Issuance Guide

### 1. Google AI Studio Gemini API Key (Individual / Attendee)
- **URL**: [https://aistudio.google.com](https://aistudio.google.com)
- **Steps**: Google Sign-in > Click **Get API Key** > Click **Create API Key** > Copy `AIzaSy...` key.
- **`.env` storage**: `GEMINI_API_KEY="AIzaSy..."`

### 2. GCP Vertex AI Key (Enterprise / GCP Project)
- **URL**: [https://console.cloud.google.com](https://console.cloud.google.com)
- **Steps**: Enable Vertex AI API (`gcloud services enable aiplatform.googleapis.com`) > Create Service Account with `Vertex AI User` role > Download JSON key.
- **Environment variable**: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"`

### 3. Anthropic Claude & OpenAI API Keys (Multi-Provider Cloud Tracks)
- **Anthropic Console (`ANTHROPIC_API_KEY`)**: [https://console.anthropic.com](https://console.anthropic.com) > **API Keys** > Create Key (`sk-ant-...`) for `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`.
- **OpenAI Platform (`OPENAI_API_KEY`)**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) > **Create new secret key** (`sk-proj-...`) for `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`.

### 4. Security Guidelines
- `.env` and `*.json` key files must **never** be committed to Git repositories. The skill enforces `.env.sample` and `.gitignore` inclusion automatically.

---

## Multi-Language SDK Setup Matrix

### 1. Python (3.9+) & uv
- **macOS**: `brew install python@3.11 && curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `winget install Python.Python.3.11` and `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Linux**: `sudo apt update && sudo apt install -y python3 python3-pip python3-venv`

### 2. Node.js (22+ for `@google/genai >= 3.0.0`) & npm / pnpm
- **macOS / Linux**: `curl -fsSL https://fnm.vercel.app/install | bash && fnm install 22`
- **Windows**: `winget install OpenJS.NodeJS.LTS`

### 3. Go (1.21+)
- **macOS**: `brew install go`
- **Windows**: `winget install GoLang.Go`
- **Linux**: `sudo apt install -y golang-go`

### 4. Flutter (3.22+) & Dart (for Gemini Live Mobile/Web)
- **macOS**: `brew install --cask flutter`
- **Windows**: `winget install Flutter.Flutter`
- **Linux**: `sudo snap install flutter --classic`
- **Gemini Live Package**: `flutter pub add gemini_live` (Direct WebSocket, zero Firebase dependency)
- **Microphone / Audio Permissions**: Ensure `android.permission.RECORD_AUDIO` in `AndroidManifest.xml` and `NSMicrophoneUsageDescription` in `Info.plist`.

---

## Automated Verification Script (`check_env.sh` / `check_env.ps1`)

The generated environment verification script tests local ports, binary presence, and API keys:

```bash
#!/usr/bin/env bash
# Automated Environment Verification Script

echo "🔍 Checking Workshop Environment Prerequisites..."

# 1. Check Python / uv
if command -v uv &> /dev/null; then
    echo "[OK] uv package manager detected: $(uv --version)"
elif command -v python3 &> /dev/null; then
    echo "[OK] Python detected: $(python3 --version)"
else
    echo "[FAIL] Neither uv nor python3 found!"
fi

# 2. Check Local LLM Server Port
if nc -z localhost 11434 2>/dev/null; then
    echo "[OK] Ollama server active on port 11434."
elif nc -z localhost 1234 2>/dev/null; then
    echo "[OK] LM Studio server active on port 1234."
else
    echo "[WARN] No local LLM server running on port 11434 (Ollama) or 1234 (LM Studio)."
fi

# 3. Check Gemini API Key
if [ -n "$GEMINI_API_KEY" ]; then
    echo "[OK] GEMINI_API_KEY environment variable set."
else
    echo "[WARN] GEMINI_API_KEY is not set."
fi
```

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
