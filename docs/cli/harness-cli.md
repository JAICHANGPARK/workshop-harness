# 💻 CLI Reference (`harness_cli.py`)

`harness_cli.py` is the primary entrypoint CLI tool for **Workshop Harness** powered by **Astral uv**.

---

## 🛠️ Command Summary Table

| Subcommand | Primary Flags | Description |
|---|---|---|
| `generate-all` | `--name`, `--topic`, `--stack`, `--dir` | One-click full workshop generation across all 13 skills |
| `init` | `--name`, `--topic`, `--dir` | Scaffolds basic repository structure & script templates |
| `audit-compat` | `--stack` | Audits tech stack cross-architecture risks across hardware chipsets |
| `audit-loop` | `--topic` | Loop engineering multi-persona review for beginner, intermediate, & advanced attendees |
| `test` | `--target` | Runs code smoke tests & audits relative markdown broken links |
| `build-pdf` | `--target` | Compiles markdown documentation into publication-ready PDF handouts |
| `export-codelab` | `--target`, `--output`, `--push` | Exports Open Codelabs manifest bundle (`codelab.yaml`) & pushes via `oc` CLI |

---

## 📖 Usage Examples

### 1. `generate-all` (One-Click Full Orchestration)

```bash
uv run harness_cli.py generate-all \
  --name "my-bwai-workshop" \
  --topic "Local RAG with Gemma 4" \
  --stack "python,ollama,docker"
```

### 2. `export-codelab` (Open Codelabs Export & Push)

```bash
uv run harness_cli.py export-codelab \
  --target my-bwai-workshop \
  --push
```

### 3. `audit-compat` (Architecture Compatibility Audit)

```bash
uv run harness_cli.py audit-compat \
  --stack "lmstudio,docker,mlx"
```

### 4. `test` (Code & Link Integrity Check)

```bash
uv run harness_cli.py test \
  --target my-bwai-workshop
```
