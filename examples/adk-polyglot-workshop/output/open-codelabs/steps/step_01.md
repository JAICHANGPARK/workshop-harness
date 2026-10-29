# Lab 01: Environment Verification, ADK Scaffolding & Custom Tools

## Objective
Verify your local environment using `./scripts/check_env.sh` and initialize your ADK agent using Google Agent Development Kit (`google-adk` / `google.golang.org/adk/v2` / `com.google.adk:google-adk` / `@google/adk`) with `gemini-3.8-flash`.

## Official Multi-Language ADK Entry Points
- **Python (`google-adk`)**: `workshop/01_starter/sre_agent/agent.py` exposing `root_agent = LlmAgent(...)`
- **Go (`google.golang.org/adk/v2`)**: `llmagent.New`, `functiontool.New`, and `gemini.NewModel`
- **Java (`com.google.adk:google-adk`)**: `LlmAgent.builder()`, `SequentialAgent.builder()`, and `FunctionTool.create()`
- **Kotlin (`com.google.adk:google-adk-kotlin-core`)**: `LlmAgent(...)`, `Gemini("gemini-3.8-flash")`, and `FunctionTool.create(::fn)`
- **TypeScript (`@google/adk`)**: `new LlmAgent({...})` and Zod-typed `new FunctionTool({...})`

## Instructions
1. Run `./scripts/check_env.sh` (or `.\scripts\check_env.ps1` on Windows).
2. If building with ADK & `agents-cli`, install the 7 official agent skills:
   ```bash
   uvx google-agents-cli setup
   ```
3. Open `workshop/01_starter/main.py` (and `workshop/01_starter/agent.py` or `polyglot/`) and inspect the starter tool definitions.
4. Test execution:
   ```bash
   python3 workshop/01_starter/main.py
   ```