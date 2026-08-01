---
name: open-codelabs-integrator
description: Integrates workshop content created by workshop-harness with Open Codelabs platform. Automates converting workshop labs into Open Codelabs manifest format (codelab.yaml), generating step-by-step markdown, mapping starter/final code workspaces, attaching prerequisites & materials, and publishing via oc CLI, REST API, or stdio MCP server (oc mcp serve).
---

# Open Codelabs Integrator Skill

## Purpose

Seamlessly bridges `workshop-harness` generated workshops with the **Open Codelabs** interactive hands-on platform (`https://github.com/JAICHANGPARK/open-codelabs`). It transforms static workshop markdown docs, lab instructions, and code scaffolds into structured Open Codelabs manifests (`codelab.yaml`), enabling facilitators to publish codelabs, manage code-server workspaces, issue quizzes, and run live interactive sessions with zero manual copy-pasting.

---

## 🚀 Key Integration Features

1. **Manifest Auto-Generation (`codelab.yaml`)**:
   - Parses `workshop/03_labs/README.md` and `gemma4-local-setup-guide.md` into standard Open Codelabs manifest specs (`version: 1`).
   - Splits monolithic lab documentation into sequential step files (`steps/step_01.md`, `steps/step_02.md`, etc.).
   - Maps `docs/02-prerequisites.md` and repository links as Open Codelabs materials.

2. **One-Click Publishing (`oc codelab push`)**:
   - Uses the `oc` CLI to push published manifests, guide markdowns, steps, quizzes, and materials directly to a local or remote Open Codelabs backend (`Axum / SQLite / Postgres / Firebase`).

3. **Agentic MCP Interoperability (`oc mcp serve`)**:
   - Leverages `open-codelabs` stdio MCP server to allow AI Agents (Antigravity, Claude, Codex, Cursor) to dynamically query connection status, create/update codelabs, inspect participant progress, triage help queues, and manage code-server workspace snapshots.

---

## 📁 Open Codelabs Bundle Directory Structure

When exported, `workshop-harness` produces the following Open Codelabs bundle inside `output/open-codelabs/`:

```text
output/open-codelabs/
├── codelab.yaml           # Master manifest file (version 1)
├── guide.md               # Preparation & Setup Guide
├── steps/
│   ├── step_01.md         # Lab 01: Environment Check & Hello World
│   ├── step_02.md         # Lab 02: Structured Output & Core Logic
│   └── step_03.md         # Lab 03: Complete Pipeline & Verification
└── materials/             # Extra assets & link references
```

---

## 📄 `codelab.yaml` Manifest Specification

```yaml
version: 1
title: "Local RAG with Gemma 4 & Ollama"
description: "Hands-on workshop building a local retrieval-augmented generation pipeline."
author: "Workshop Facilitator"
is_public: true
quiz_enabled: false
require_quiz: false
require_feedback: true
require_submission: false
guide_markdown: "guide.md"
steps:
  - title: "Lab 01: Environment Verification & Basic API"
    file: "steps/step_01.md"
  - title: "Lab 02: Structured Output & JSON Schema"
    file: "steps/step_02.md"
  - title: "Lab 03: Full RAG Pipeline & Verification"
    file: "steps/step_03.md"
materials:
  - title: "Starter Code Repository"
    type: "link"
    url: "https://github.com/JAICHANGPARK/workshop-harness"
```

---

## 🛠 `oc` CLI & Integration Workflows

### 1. Generate Open Codelabs Bundle
From your `workshop-harness` project root:
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop
```

### 2. Publish Bundle to Open Codelabs
```bash
# Set target server profile or URL
oc connect use --name local
oc auth login

# Push manifest bundle directly
oc codelab push --manifest output/open-codelabs/codelab.yaml
```

### 3. One-Click Export & Push
```bash
python3 harness_cli.py export-codelab --target my-bwai-workshop --push
```

### 4. Connect AI Agent via MCP (`oc mcp serve`)
Start Open Codelabs MCP server for agentic automation:
```bash
oc mcp serve
```
Available Agent Tools:
- `create_codelab`, `replace_codelab_steps`, `push_codelab`
- `list_materials`, `add_material`
- `list_attendees`, `list_help_requests`, `resolve_help_request`
- `get_workspace_info`, `list_workspace_branches`

---

## 🔗 References

- **Open Codelabs Repository**: [https://github.com/JAICHANGPARK/open-codelabs](https://github.com/JAICHANGPARK/open-codelabs)
- **Open Codelabs CLI Reference**: [Open Codelabs CLI Docs](https://github.com/JAICHANGPARK/open-codelabs/blob/main/docs/user-guide/cli.md)
- **Open Codelabs MCP Guide**: [Open Codelabs MCP Docs](https://github.com/JAICHANGPARK/open-codelabs/blob/main/docs/user-guide/mcp.md)
- **Workshop Harness**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
