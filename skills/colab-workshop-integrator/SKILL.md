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

## 🔗 Official References
- **Google Colab CLI Repository**: [https://github.com/googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)
- **Google Developers Blog Announcement**: [Introducing the Google Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/)
- **Google Colab Platform**: [https://colab.research.google.com](https://colab.research.google.com)
