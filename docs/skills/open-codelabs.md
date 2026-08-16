# Open Codelabs Integrator Skill

The **Open Codelabs Integrator** skill ([`skills/open-codelabs-integrator/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/open-codelabs-integrator/SKILL.md)) bridges `workshop-harness` generated content with **[Open Codelabs](https://github.com/JAICHANGPARK/open-codelabs)**, a Google Codelab-style interactive hands-on platform.

---

## Key Capabilities

1. **Automatic Bundle Export (`output/open-codelabs/`)**:
   - Parses `workshop/03_labs/README.md` and `gemma4-local-setup-guide.md` into `codelab.yaml`, `guide.md`, and individual step markdown files (`steps/step_01.md`, `steps/step_02.md`).
2. **1-Click `oc` CLI Push**:
   - Executes `oc codelab push --manifest output/open-codelabs/codelab.yaml` to sync directly with local or remote Open Codelabs instances.
3. **stdio MCP Interoperability (`oc mcp serve`)**:
   - Enables AI agents to interactively create/update codelabs, manage code-server workspace snapshots, and triage attendee help queues via stdio MCP.

---

## CLI Usage Example

```bash
# Export bundle only
uv run harness_cli.py export-codelab --target my-bwai-workshop

# Export bundle and push via oc CLI
uv run harness_cli.py export-codelab --target my-bwai-workshop --push
```

---

## Sample `codelab.yaml` Manifest

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
