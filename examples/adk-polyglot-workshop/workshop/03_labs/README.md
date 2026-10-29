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

### Lab 01: Local LLM Server API Integration
- **Objective**: Send a request to the Ollama / LM Studio local port (11434 / 1234) and receive a streaming response
- **Lab File**: `workshop/01_starter/src/lab1_basic.py`
- **Key Code Marker**: Fill in the `TODO: [Lab 1]` sections

### Lab 02: Structured Output Implementation
- **Objective**: Use Pydantic / Output Schema to parse local LLM responses into typed JSON objects
- **Lab File**: `workshop/01_starter/src/lab2_schema.py`
- **Reference Prompt**: Copy and apply contents from `prompt-pack/02-output-schema.md`

### Lab 03: Complete Hands-on Application & Testing
- **Objective**: Integrate the full pipeline (User Input -> System Prompt -> LLM Execution -> Parsed Output -> Action)
- **Lab File**: `workshop/01_starter/src/main.py`
- **Run Command**:
  ```bash
  ./run.sh  # (Windows: .\run.ps1)
  ```
