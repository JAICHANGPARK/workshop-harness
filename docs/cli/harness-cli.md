# CLI Reference (`harness_cli.py`)

`harness_cli.py` is the primary entrypoint CLI tool for **Workshop Harness** powered by **Astral uv**.

---

## Command Summary Table

| Subcommand | Primary Flags | Description |
|---|---|---|
| `generate-all` | `--name`, `--topic`, `--stack`, `--model`, `--dir` | One-click full workshop generation across all 21 skills |
| `init` | `--name`, `--topic`, `--stack`, `--model`, `--dir` | Scaffolds repository structure, multi-language starter/final code, & script templates |
| `list-models` | `--provider` | Displays the verified 2026 Frontier & Open-Weight Model Catalog |
| `audit-models` | `--target`, `--fix` | Audits and auto-upgrades deprecated model tags and legacy SDK imports |
| `audit-compat` | `--stack`, `--target` | Audits tech stack cross-architecture risks across hardware chipsets |
| `audit-loop` | `--topic`, `--target` | Loop engineering 4-persona review (Non-Coder, Novice, Intermediate, Senior) |
| `test` | `--target` | Runs code smoke tests, model currency checks, & audits relative markdown broken links |
| `build-pdf` | `--target` | Compiles markdown documentation into publication-ready PDF handouts |
| `export-codelab` | `--target`, `--output`, `--push` | Exports Open Codelabs manifest bundle (`codelab.yaml`) & pushes via `oc` CLI |
| `export-colab` | `--target`, `--output`, `--repo`, `--test` | Exports Google Colab interactive notebooks (`.ipynb`) & 'Open in Colab' badges |
| `test-colab` | `--target` | Runs headless smoke test on Colab notebooks using Google Colab CLI (`colab`) |
| `build-slides` | `--target`, `--output`, `--export-pdf` | Generates Marp Markdown (`slides.md`), `.pptx`, and interactive Web Presentation (`index.html`) |

---

## Usage Examples

### 1. `generate-all` (One-Click Full Orchestration)

```bash
uv run harness_cli.py generate-all \
  --name "my-bwai-workshop" \
  --topic "Local RAG with Gemma 4" \
  --stack "python,ollama,docker" \
  --model "gemini-3.8-flash"
```

### 2. `list-models` & `audit-models` (2026 Model Catalog & Currency Audit)

```bash
# View verified 2026 models across Gemini 4 Argon, Gemini 3.8, Gemma 4, Claude 5.5, GPT-6, and Ollama
uv run harness_cli.py list-models

# Audit and automatically upgrade deprecated model strings in a workshop project
uv run harness_cli.py audit-models --target my-bwai-workshop --fix
```

### 3. `build-slides` (Presentation Slide Generation)

```bash
uv run harness_cli.py build-slides \
  --target my-bwai-workshop
```

### 4. `export-colab` (Google Colab Export & Badges)

```bash
uv run harness_cli.py export-colab \
  --target my-bwai-workshop \
  --repo "JAICHANGPARK/my-bwai-workshop"
```

### 5. `test-colab` (Google Colab CLI Smoke Test)

```bash
uv run harness_cli.py test-colab \
  --target my-bwai-workshop
```

### 6. `export-codelab` (Open Codelabs Export & Push)

```bash
uv run harness_cli.py export-codelab \
  --target my-bwai-workshop \
  --push
```

### 7. `audit-compat` (Architecture Compatibility Audit)

```bash
uv run harness_cli.py audit-compat \
  --stack "lmstudio,docker,mlx,gemini-live"
```

### 8. `test` (Code, Model Currency & Link Integrity Check)

```bash
uv run harness_cli.py test \
  --target my-bwai-workshop
```

