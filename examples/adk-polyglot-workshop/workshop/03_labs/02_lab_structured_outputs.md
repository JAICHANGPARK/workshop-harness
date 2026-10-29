# Lab 02: Multi-Agent Hierarchy, Sub-Agent Delegation & Structured Outputs

## Objective
Wire specialized sub-agents (`slo_specialist`, `report_specialist`) under a root coordinator (`root_agent` running `gemini-4-argon`) and enforce deterministic JSON schema outputs.

## Instructions
1. Review `prompt-pack/README.md` for the target JSON Schema.
2. In Python (`workshop/01_starter/agent.py`), attach `sub_agents=[slo_specialist, report_specialist]` to `root_agent`.
3. If exploring the Go, Java, Kotlin, or TypeScript tracks under `workshop/02_final/polyglot/`, compare how `SubAgents` / `subAgents` and `SequentialAgent` delegate tasks across languages.
4. Launch the interactive ADK Dev UI to inspect sub-agent handoff events visually:
   ```bash
   cd workshop/02_final && adk web
   ```
