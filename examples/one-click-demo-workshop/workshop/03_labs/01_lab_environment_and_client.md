# Lab 01: Environment Verification & AI Client Sanity Check

## Objective
Verify your local and cloud development environment using `./scripts/check_env.sh` and connect `workshop/01_starter/main.py` to Google GenAI (`gemini-3.8-flash`) or Local Ollama (`gemma4:e4b`).

## Instructions
1. Run `./scripts/check_env.sh` (or `.\scripts\check_env.ps1` on Windows) to verify Python, `uv`, and local port readiness.
2. Open `workshop/01_starter/main.py` and inspect `TODO: [Lab 01 - Exercise]` inside `lab1_sanity_check()`.
3. Configure `GEMINI_API_KEY` in `.env` or start your local Ollama runtime (`ollama serve` with `gemma4:e4b`).
4. Run the starter script to verify connectivity:
   ```bash
   python3 workshop/01_starter/main.py
   ```
