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

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.

---

## 🔗 Official References
- **Google Colab CLI Repository**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)
- **Google Developers Blog Announcement**: [Introducing the Google Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/)
- **Google Colab Platform**: [https://colab.research.google.com](https://colab.research.google.com)
