---
name: workshop-persona-loop-evaluator
description: Reviews and validates workshop curriculum and code from the perspectives of beginner, intermediate, and advanced attendee personas using the Loop Engineering methodology. Generates a multi-persona review report (docs/00-persona-loop-review-report.md).
---

# Workshop Persona Loop Evaluator Skill

## Purpose
Applies the **Loop Engineering** methodology to evaluate workshop materials through the lens of three distinct attendee personas, identifying gaps, ambiguities, and difficulty mismatches before the live session.

## Persona Definitions

### 1. Beginner Persona
- **Profile**: First-time attendee, no prior AI/ML experience, may struggle with terminal commands
- **Evaluation Criteria**:
  - Are all setup steps explicit with no assumed knowledge?
  - Are terminal commands copy-paste ready?
  - Is jargon defined on first use?
  - Can this person complete Lab 01 independently?

### 2. Intermediate Persona
- **Profile**: Working developer with Python/JS experience, familiar with APIs but new to local LLMs
- **Evaluation Criteria**:
  - Is there enough depth to stay engaged beyond "Hello World"?
  - Are architecture decisions explained (why RAG vs fine-tuning)?
  - Are stretch goals provided for fast completers?

### 3. Advanced Persona
- **Profile**: ML engineer or senior developer, may already have production LLM experience
- **Evaluation Criteria**:
  - Are there non-trivial challenges (custom tool calls, multi-agent patterns)?
  - Is the content technically accurate and up-to-date?
  - Are performance optimization opportunities mentioned?

## Review Loop Process

```
For each persona:
  1. Read all lab guides as if you are that persona
  2. Attempt to follow each step mentally
  3. Flag any step where the persona would get stuck
  4. Rate overall difficulty fit (Too Easy / Just Right / Too Hard)
  5. Suggest specific improvements
```

## Output Artifacts
- `docs/00-persona-loop-review-report.md` - Multi-persona evaluation report with ratings and improvement suggestions
