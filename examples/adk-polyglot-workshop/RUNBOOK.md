# Facilitator & TA Runbook: adk-polyglot-workshop

- **Session Title**: Enterprise Multi-Agent SRE with Polyglot ADK
- **Tech Stack**: `adk,polyglot,python,go,java,kotlin,typescript`
- **Primary Cloud Provider**: Google GenAI (`GEMINI_API_KEY`)
- **Primary Cloud Model**: `gemini-4-hydrogen` | **Coordinator**: `gemini-4-carbon` | **Local Model**: `gemma4:e4b` | **Local Multimodal Embedding**: `embeddinggemma-2`
- **Facilitator**: Workshop Lead Facilitator
- **Teaching Assistants (TA)**: Roaming TA Team

---

## Session Timeline (60 Minutes)

### 00m - 10m: Opening & Environment Verification
- **Facilitator**: Walk through `SETUP_GUIDE.md`, architecture overview, and demo `./scripts/check_env.sh` execution.
- **TA**: Provide 1:1 support for attendees with environment check errors; direct low-RAM or restricted laptops to `output/colab/workshop_starter.ipynb`.

### 10m - 25m: Lab 01 - Environment Setup & Client Sanity Check
- **Facilitator**: Explain `workshop/01_starter` code structure and demo `TODO: [Lab 01]` completion.
- **TA**: Help attendees configure `GEMINI_API_KEY` in `.env` or start the local LLM server (`ollama serve` on port `11434`).

### 25m - 45m: Lab 02 - Structured Outputs, Tool Calling & Agent Routing
- **Facilitator**: Demo typed Output Schema definition (`prompt-pack/README.md`) and sub-agent/tool integration.
- **TA**: Assist attendees with schema validation or port conflict errors.

### 45m - 55m: Lab 03 - End-to-End Pipeline & Verification
- **Facilitator**: Share and demo the `workshop/02_final` reference solution and run `python3 scripts/verify_workshop.py .`.
- **TA**: Verify attendee completion checkpoints.

### 55m - 60m: Q&A & Feedback Survey
- **Facilitator**: Session retrospective, share PDF handouts (`output/pdf/`), and collect attendee feedback survey responses.
