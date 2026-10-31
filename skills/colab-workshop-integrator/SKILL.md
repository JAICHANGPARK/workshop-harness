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

## Typography, Developer Terminology & Bilingual Notation Rules

- **Developer-Friendly Terminology & English Original Notation (영어 원문 병기 & 직역 금지)**:
  - Never use awkward literal translations (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기").
  - Always use developer-friendly terminology commonly used by real-world software engineers AND include the original English technical term in parentheses (`개발자 친화적 용어 (English Original)`), such as:
    - **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**, **스모크 테스트 (Smoke Test)**, **보일러플레이트 코드 (Boilerplate Code)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.

---

## 🔗 Official References
- **Google Colab CLI Repository**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)
- **Google Developers Blog Announcement**: [Introducing the Google Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/)
- **Google Colab Platform**: [https://colab.research.google.com](https://colab.research.google.com)
