---
name: workshop-scaffolder
description: Scaffolds a standard workshop repository structure including docs/, workshop/, prompt-pack/, scripts/, and output/ directories with pre-configured templates and automation scripts.
---

# Workshop Scaffolder Skill

## Purpose
Generates a standardized, production-grade workshop repository structure in one step. Ensures all necessary documentation templates, lab subdirectories, starter/final code skeletons, environment scripts, and build artifacts are properly created with correct file permissions (`chmod +x`).

---

## Standard Repository Layout Specs

```text
<project-name>/
├── README.md                           # Main workshop overview & quick start guide
├── RUNBOOK.md                          # Facilitator & TA execution runbook
├── AGENTS.md                           # AI Agent context specification
├── gemma4-local-setup-guide.md          # Unified attendee preparation guide
├── pyproject.toml                       # Astral uv dependency declaration
├── .env.sample                          # Sample environment file template
├── docs/                               # Detailed technical documentation & reports
│   ├── 00-architecture-compatibility-matrix.md
│   ├── 00-persona-loop-review-report.md
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md
├── workshop/                           # Day-of hands-on lab code
│   ├── 01_starter/                     # Starter code scaffold for attendees
│   │   ├── main.py
│   │   ├── run.sh
│   │   └── run.ps1
│   ├── 02_final/                       # Completed reference solution
│   │   ├── main.py
│   │   ├── run.sh
│   │   └── run.ps1
│   └── 03_labs/                        # Step-by-step lab guides
│       └── README.md
├── prompt-pack/                        # Prompt engineering packs & schemas
│   └── README.md
├── scripts/                            # Cross-architecture checks & verification scripts
│   ├── check_env.sh / check_env.ps1
│   ├── check_architecture_compat.sh / .ps1
│   ├── bundle_offline_assets.sh
│   ├── verify_workshop.py
│   ├── export_open_codelabs.py
│   └── generate_prep_pdf.py
└── output/                             # Build & publication output artifacts
    ├── pdf/                            # Generated PDF handouts
    └── open-codelabs/                  # Open Codelabs bundles (codelab.yaml)
```

---

## Scaffolding Workflow & Execution Rules

When scaffolding a new workshop project:
1. **Directory Creation**: Recursively create `docs/`, `workshop/01_starter/`, `workshop/02_final/`, `workshop/03_labs/`, `prompt-pack/`, `scripts/`, `output/pdf/`, and `tmp/pdfs/`.
2. **Template Copying**: Copy master templates from `templates/doc-templates/` and `templates/script-templates/`.
3. **Executable Bit Enforcement**: Mark all `.sh` and `.py` scripts as executable (`chmod 755`).
4. **Environment Initialization**: Write `.env.sample` containing placeholder keys (`GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`).
5. **Multi-Language Starter Scaffolding (Python, TypeScript, Go, Kotlin)**:
   - **Python**: Generates `pyproject.toml` and `main.py` entrypoints.
   - **TypeScript / JavaScript**: Generates `package.json` with `@google/genai` dependencies and `src/index.ts`.
   - **Go (Golang)**: Generates `go.mod` and `main.go`.
   - **Kotlin / Java**: Generates `build.gradle.kts` and `src/main/kotlin/Main.kt`.

---

## CLI Command Integration

Scaffold a new workshop using `harness_cli.py`:

```bash
# Initialize standalone scaffold
uv run harness_cli.py init --name "my-bwai-workshop" --topic "Local RAG with Gemma 4"

# One-Click Full Orchestration across all skills
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```
