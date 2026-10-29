# Hands-on Lab Session Guide (Step-by-Step)

This guide outlines the session schedule and step-by-step objectives for the day-of workshop. Write your code in the `workshop/01_starter` folder. If you get stuck, refer to the completed reference code in `workshop/02_final`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & final environment check
- **10m - 25m**: **Lab 01** - Connect to local LLM server & run a basic prompt
- **25m - 45m**: **Lab 02** - Structured Output (JSON Schema) & Tool Integration
- **45m - 55m**: **Lab 03** - End-to-end application scenario & result verification
- **55m - 60m**: Q&A and wrap-up

---

## Labs

### Lab 01: Environment & AI Client Integration
- **Objective**: Verify your local or cloud AI environment (`gemini-3.8-flash` / `gemma4:e4b`) and run a basic sanity check
- **Lab File**: `workshop/01_starter/main.py` (or `workshop/01_starter/agent.py` for ADK tracks)
- **Key Code Marker**: Fill in the `TODO: [Lab 01]` sections

### Lab 02: Structured Output & Multi-Agent Delegation
- **Objective**: Use typed schemas / Output Schema to parse LLM responses into deterministic JSON objects and configure sub-agent routing
- **Lab File**: `workshop/01_starter/main.py`
- **Reference Prompt**: Copy and apply contents from [`prompt-pack/README.md`](../../prompt-pack/README.md)

### Lab 03: Complete Hands-on Application & Testing
- **Objective**: Integrate the full pipeline (User Input -> System Prompt -> Agent/Tool Execution -> Parsed Output -> Verification)
- **Lab File**: `workshop/02_final/main.py`
- **Run Command**:
  ```bash
  ./run.sh  # (Windows: .\run.ps1)
  ```
