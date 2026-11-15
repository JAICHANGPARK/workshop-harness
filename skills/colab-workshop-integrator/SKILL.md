---
name: colab-workshop-integrator
description: Generates Google Colab ready interactive notebooks (.ipynb) from workshop labs, injects zero-setup runtime cells (pip dependencies, GPU check, Colab Secrets / API keys), creates 'Open in Colab' badges, and automates headless execution & smoke testing via the Google Colab CLI (colab-cli).
---

# Google Colab Workshop Integrator Skill

## Purpose

Bridges `workshop-harness` generated workshops with **Google Colab** and the **Google Colab CLI** (`https://github.com/googlecolab/google-colab-cli`). It transforms static workshop markdown docs, lab instructions, and starter/final code into interactive Jupyter Notebooks (`.ipynb`), injects cloud GPU verification and Secret management cells, inserts "Open in Colab" badges, and enables facilitators to run automated remote headless smoke tests via `colab` CLI.

> 🌐 **Mandatory Pre-Flight Web Research Protocol**:
> Before generating Colab notebooks, perform live web search (`search_web` / `workshop-web-researcher`) to verify current Colab CUDA driver versions, newest PyTorch / HuggingFace Transformers / Google GenAI SDK syntax, and latest pip package names.

---

## 🚀 Key Integration Features

1. **Lab to `.ipynb` Auto-Generation**:
   - Converts `workshop/03_labs/README.md` and code files (`workshop/01_starter`, `workshop/02_final`) into clean, structured Jupyter Notebooks.
   - Generates two flavors:
     - `workshop_starter.ipynb`: Step-by-step guides with starter code cells and attendee TODO prompts.
     - `workshop_solution.ipynb`: Complete reference solution notebook ready for live demo or fallback.

2. **Zero-Setup Runtime Preparation Cells**:
   - **Environment & Dependency Injection**: Automatically adds top `%pip install -q ...` cells based on `pyproject.toml` or workshop tech stack.
   - **Hardware Accelerator Verification**: Injects GPU runtime verification (`!nvidia-smi` / torch CUDA check) for local LLM (Ollama, vLLM, transformers) labs.
   - **Colab Secrets & Credential Protocol**: Injects secure `google.colab.userdata` API key handling instead of hardcoded keys:
     ```python
     # Secure API Key Setup in Colab
     try:
         from google.colab import userdata
         gemini_api_key = userdata.get('GEMINI_API_KEY')
     except ImportError:
         import os
         gemini_api_key = os.environ.get('GEMINI_API_KEY', '')
     ```

3. **'Open in Colab' Badge Auto-Generation**:
   - Injects official SVG badges linking directly to the notebook on GitHub:
     ```markdown
     [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<USER>/<REPO>/blob/main/output/colab/workshop_starter.ipynb)
     ```

4. **Headless Execution & Remote Smoke Testing via Google Colab CLI**:
   - Validates notebooks in a real Colab cloud runtime using `colab-cli`:
     ```bash
     # Run headless test via Google Colab CLI
     colab run output/colab/workshop_solution.ipynb
     ```

---

## 📁 Colab Bundle Directory Structure

When exported, `workshop-harness` produces the following Colab bundle inside `output/colab/`:

```text
output/colab/
├── workshop_starter.ipynb    # Attendee hands-on interactive notebook
├── workshop_solution.ipynb   # Facilitator / Reference solution notebook
├── README.md                 # Colab quickstart guide with 'Open in Colab' badges
└── test_colab_run.sh         # Headless verification script via colab CLI
```

---

## 🛠 Colab Integration Workflows

### 1. Generate Colab Notebooks from Workshop
From your `workshop-harness` project root:
```bash
python3 harness_cli.py export-colab --target my-bwai-workshop
```

### 2. Specify Custom GitHub Repository for Colab Badges
```bash
python3 harness_cli.py export-colab --target my-bwai-workshop --repo "JAICHANGPARK/my-bwai-workshop"
```

### 3. Run Colab Smoke Test via Google Colab CLI
```bash
# Verify notebooks via Colab CLI
python3 harness_cli.py test-colab --target my-bwai-workshop
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
