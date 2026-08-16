---
name: workshop-runbook-generator
description: Generates a minute-by-minute facilitator and TA timeline runbook (RUNBOOK.md), including opening scripts, slide sync markers, TA response time rules, and progress checkpoint curl commands.
---

# Workshop Runbook Generator Skill

## Purpose
Generates `RUNBOOK.md` at the repository root, a minute-by-minute execution playbook for workshop facilitators and Teaching Assistants (TAs). Ensures the live session runs smoothly, stays on schedule, and provides explicit troubleshooting escalation protocols when attendees hit roadblocks.

---

## Runbook Structure & Timeline Matrix

### Phase 1: Pre-Session Setup (T-60 to T-0 min)
- **T-60 min**: Test venue WiFi speed and verify local LLM port connectivity (`curl http://localhost:11434/api/version`).
- **T-30 min**: Display opening slide with repository URL, WiFi SSID/Password, and prerequisite check script (`./scripts/check_env.sh`).
- **T-10 min**: Verify TA assignments and open live debug chat channel.

### Phase 2: Live Session Execution (T+0 to T+120 min)

| Time Marker | Facilitator Action & Speaker Script | TA Focus & Intervention | Progress Checkpoint Flag |
|---|---|---|---|
| **T+00 - T+10** | **Opening & Logistics**: "Welcome! Please clone the repo and run `check_env.sh`." | Assist attendees with terminal navigation & API keys. | `check_env.sh` returns `[OK]` |
| **T+10 - T+30** | **Lab 01**: Basic integration & Hello World model call. | Help resolve port 11434 / 1234 connection errors. | `curl http://localhost:11434/api/tags` 200 OK |
| **T+30 - T+65** | **Lab 02**: Structured Output & Pydantic schema parsing. | Assist with JSON parsing and schema validation errors. | `uv run python main.py` outputs valid JSON |
| **T+65 - T+105** | **Lab 03**: Agent / RAG pipeline completion. | Debug vector retrieval & prompt formatting. | End-to-end pipeline run succeeds |
| **T+105 - T+120**| **Wrap-up & Q&A**: Survey link, GitHub star callout, next steps. | Collect attendee feedback & log unresolved edge cases. | Survey submissions |

---

## Operational TA Rules & Escalation Protocols

1. **2-Minute Rule**: TAs must limit individual attendee debugging to **2 minutes**. If unresolved, guide attendee to switch to the reference code (`02_final`) to stay on schedule.
2. **3-Attendee Cluster Escalation Rule**: If 3 or more attendees hit the identical error simultaneously, the TA notifies the facilitator to pause and address the issue on the main stage screen.
3. **Backup Plan Trigger (Network Failure)**:
   - *Trigger*: Venue WiFi drops or experiences severe latency.
   - *Action*: Facilitator announces switch from Cloud Gemini API to local Ollama runtime (`gemma4:e2b`) pre-bundled in offline assets.

---

## Output Artifact Specifications

- **File Path**: `RUNBOOK.md` at repository root.
