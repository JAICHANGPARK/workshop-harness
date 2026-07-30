---
name: workshop-runbook-generator
description: Generates a minute-by-minute facilitator and TA timeline runbook (RUNBOOK.md), including opening talking points, TA coordination guidelines, and attendee progress checkpoints.
---

# Workshop Runbook Generator Skill

## Purpose
Prevents time overruns and ensures consistent pacing across sessions by providing facilitators and TAs with a minute-level execution timeline, pre-written talking points, and progress checkpoints.

## Runbook Structure

### 1. Timeline Table
```markdown
| Time (min) | Phase          | Facilitator Action              | TA Action                    |
|------------|----------------|--------------------------------|------------------------------|
| 00:00-05:00 | Opening        | Welcome & agenda overview      | Distribute handouts          |
| 05:00-10:00 | Environment    | Screen-share `check_env.sh`    | Walk around, debug blockers  |
| 10:00-35:00 | Lab 01         | Live code demo                 | Monitor chat for questions   |
| 35:00-60:00 | Lab 02         | Guided practice                | Help stuck attendees 1:1     |
| 60:00-85:00 | Lab 03         | Self-paced + stretch goals     | Triage advanced questions    |
| 85:00-90:00 | Wrap-up        | Recap & survey link            | Collect feedback             |
```

### 2. Opening Talking Points
Pre-written scripts for the facilitator to use verbatim during the first 5 minutes to set expectations (WiFi info, repo URL, survey link).

### 3. TA Guidelines
- Maximum response time per attendee: **2 minutes**
- Escalation threshold: if 3+ attendees hit the same error, pause for group troubleshooting
- Use the `live-debug-assistant` skill for rapid terminal error diagnosis

### 4. Progress Checkpoints
Defined "green flag" checks at the end of each lab phase:
- Lab 01: `curl http://localhost:11434/api/generate` returns 200
- Lab 02: Structured JSON output parses without errors
- Lab 03: Full pipeline end-to-end demo succeeds

## Output Artifacts
- `RUNBOOK.md` - Complete facilitator runbook at the repository root
