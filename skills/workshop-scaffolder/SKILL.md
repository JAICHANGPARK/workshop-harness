---
name: workshop-scaffolder
description: Scaffolds a standard workshop repository structure including docs/, workshop/, prompt-pack/, scripts/, and output/ directories with pre-configured templates and automation scripts.
---

# Workshop Scaffolder Skill

## Purpose
Generates a complete, standardized workshop repository structure so that organizers can immediately begin populating content without worrying about directory layout, naming conventions, or missing boilerplate files.

## Generated Directory Structure

```text
my-workshop-repo/
├── README.md
├── RUNBOOK.md
├── AGENTS.md
├── gemma4-local-setup-guide.md
├── pyproject.toml
├── docs/
│   ├── 00-architecture-compatibility-matrix.md
│   ├── 00-persona-loop-review-report.md
│   ├── 01-hardware-and-env.md
│   ├── 02-prerequisites.md
│   └── 20-faq.md
├── workshop/
│   ├── 01_starter/
│   ├── 02_final/
│   └── 03_labs/
├── prompt-pack/
├── scripts/
│   ├── check_env.sh / check_env.ps1
│   ├── check_architecture_compat.sh / .ps1
│   ├── bundle_offline_assets.sh
│   ├── verify_workshop.py
│   └── generate_prep_pdf.py
└── output/pdf/
```
