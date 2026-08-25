# Quickstart Guide

Workshop Harness is powered by **Astral uv**. It resolves dependencies and generates full workshop packages in seconds.

---

## Step 1: Requirements

Ensure the following tools are installed:

- **Python**: Version 3.9+
- **Git**: Latest version
- **Astral uv**: Lightning-fast Python package manager
  ```bash
  # Install uv (macOS / Linux)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

## Step 2: Clone & Install Agent Skills

```bash
# 1. Clone repository
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. Auto-install 16 skills to ~/.gemini/skills/
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

The `install_skills.sh` script copies all 16 agent skill directories to `~/.gemini/skills/` and syncs required dependencies (`reportlab`, `pymupdf`, `pillow`).

---

## Step 3: One-Click Full Workshop Generation

```bash
uv run harness_cli.py generate-all \
  --name "my-bwai-workshop" \
  --topic "Local RAG with Gemma 4" \
  --stack "python,ollama,docker"
```

### 6-Step Pipeline Execution:

1. **Scaffolding (`init_workshop`)**: Generates standard `docs/`, `workshop/01_starter`, `workshop/02_final`, `workshop/03_labs`, `prompt-pack/`, `scripts/`, and `output/` structure.
2. **Cross-Architecture Audit (`audit_compatibility`)**: Evaluates tech stack risks across Apple Silicon, Intel Mac, Windows, and Linux.
3. **Multi-Persona Review (`audit_persona_loop`)**: Evaluates timing and difficulty from beginner, intermediate, and advanced attendee perspectives (`docs/00-persona-loop-review-report.md`).
4. **Integrity Smoke Test (`test_workshop`)**: Runs starter/final Python code smoke tests and audits relative markdown links.
5. **PDF Handout Build (`build_pdf`)**: Compiles markdown docs into publication-ready PDF handouts (`output/pdf/*.pdf`) and preview images.
6. **Open Codelabs Export (`export_codelab`)**: Generates an Open Codelabs manifest (`output/open-codelabs/codelab.yaml`) and step bundle.

---

## Step 4: Verify Output

Inspect your newly created workshop repository:

```bash
cd my-bwai-workshop
ls -la
```

Your setup guides, facilitator runbook, hands-on lab code, PDF handouts, and Open Codelabs bundle are ready for deployment!
