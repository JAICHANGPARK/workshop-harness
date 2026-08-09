---
name: workshop-persona-loop-evaluator
description: Evaluates and audits workshop curriculum, lab guides, starter/final code, and setup documents through 4 distinct attendee reviewer personas (Non-Coder, Novice, Intermediate, Senior Engineer). Generates a multi-persona evaluation report at docs/00-persona-loop-review-report.md using Loop Engineering.
---

# Workshop Persona Loop Evaluator Skill

## Purpose
Applies **Loop Engineering** and multi-persona simulation to evaluate workshop materials before a live session. The agent assumes 4 distinct attendee reviewer roles to identify difficulty mismatches, missing prerequisites, vague instructions, security risks, and architecture flaws.

---

## The 4 Attendee Reviewer Personas

### 1. Non-Coder / Complete Beginner Persona (Non-Coder)
- **Profile**: Product managers, designers, non-technical founders, marketers, or beginners with zero programming/terminal background.
- **Review Lens**:
  - Are terminal commands 100% copy-paste ready without assumed shell knowledge?
  - Are visual GUI steps (e.g., VS Code extension installation, clicking buttons) included?
  - Is technical jargon (e.g., `virtualenv`, `npm`, `CLI`, `API key`, `localhost`) explained in plain language?
  - Would this attendee get stuck at step 1 due to missing OS prep?
- **Key Metric**: *Zero friction to first successful run (No terminal blockers).*

### 2. Novice / Beginner Developer Persona (Novice)
- **Profile**: Junior developers, students, or hobbyists with basic Python/JS syntax knowledge who struggle with environment variables, virtualenvs, pathing, and package conflicts.
- **Review Lens**:
  - Are virtual environment (`venv` / `uv`) creation and package installation explicit?
  - Is the delta between `01_starter` and `02_final` code clear?
  - Are common runtime errors (e.g., `ModuleNotFoundError`, `APIKeyError`, `PortInUse`) covered with 10-second hotfix instructions?
  - Are API keys safely loaded via `.env` instead of hardcoded strings?
- **Key Metric**: *Clear starter-to-final path and instant error recovery.*

### 3. Intermediate Developer Persona (Intermediate)
- **Profile**: Experienced full-stack or backend developers familiar with REST APIs and basic LLM prompts, seeking non-trivial practical application.
- **Review Lens**:
  - Does the curriculum go beyond basic "Hello World" into real-world patterns (RAG, structured output, function calling)?
  - Is the code modular, readable, and idiomatic?
  - Are stretch goals / bonus tasks provided for attendees who finish labs quickly?
  - Are trade-offs (e.g., local Gemma vs Cloud Gemini) clearly explained?
- **Key Metric**: *High engagement and practical architectural depth.*

### 4. Advanced / Senior Engineer Persona (Advanced / Senior)
- **Profile**: Senior software engineers, tech leads, or AI/ML architects evaluating technical rigor, production readiness, and edge case resilience.
- **Review Lens**:
  - Is the architecture scalable, secure, and production-ready (no security vulnerabilities, proper error handling, CORS/rate limit considerations)?
  - Are prompt engineering templates, RAG vector retrieval strategies, and chunking parameters optimized?
  - Are cross-platform hardware risks (Apple Silicon Metal vs Intel Mac vs Windows WSL2) addressed?
  - Is memory overhead and GPU/CPU resource consumption documented?
- **Key Metric**: *Production-grade technical accuracy, security, and performance.*

---

## 4-Persona Evaluation Loop Workflow

When invoking this skill, the agent executes a 4-phase audit loop:

```text
[Phase 1: Non-Coder Audit]     -> Evaluate CLI commands, jargon definitions, GUI steps
[Phase 2: Novice Audit]        -> Evaluate venv setup, starter-to-final diff, hotfix FAQ
[Phase 3: Intermediate Audit]  -> Evaluate code modularity, API depth, stretch goals
[Phase 4: Senior Audit]        -> Evaluate architecture, security, performance, hardware risks
```

---

## Review Scoring Rubric (1 - 5 Points)

Each persona evaluates the workshop across 5 core dimensions:

1. **Clarity & Setup Guidance**: Are instructions unambiguous?
2. **Pacing & Timing**: Can labs be completed within allotted minutes?
3. **Technical Rigor & Code Quality**: Is code clean, modular, and idiomatic?
4. **Safety & Security**: Are API keys protected and fallback guides provided?
5. **Engagement & Value**: Is the outcome rewarding for this persona?

---

## Output Artifact

Generates `docs/00-persona-loop-review-report.md`:

```markdown
# Multi-Persona Loop Engineering Review Report

## Executive Summary & Overall Fit
- Overall Workshop Readiness Score: 4.6 / 5.0

## Persona Breakdown & Findings

### 1. Non-Coder Review (Non-Coder)
- Score: 4.5 / 5.0
- Positives: Visual setup guide included.
- Blockers Identified: `uv` command missing explanation in Lab 01.
- Action Item: Add terminal copy button & plain-text explanation.

### 2. Novice Developer Review (Novice)
- Score: 4.8 / 5.0
- Action Item: Add `.env.sample` troubleshooting note.

### 3. Intermediate Developer Review (Intermediate)
- Score: 4.7 / 5.0
- Action Item: Add Lab 03 stretch challenge for custom RAG prompt tuning.

### 4. Senior Engineer Review (Advanced / Senior)
- Score: 4.4 / 5.0
- Action Item: Note Intel Mac GPU acceleration limitation & Ollama fallback.

## Recommended Action Items Prior to Event
1. [High] Fix missing `.env.sample` reference in Lab 01.
2. [Medium] Add stretch challenge to Lab 03 for fast completers.
```

---

## CLI Integration

Execute the multi-persona review loop via `harness_cli.py`:

```bash
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4"
```
