# Lab 03: Trajectory Evaluation (adk eval), ADLC Optimization & Deployment

## Objective
Evaluate multi-agent tool trajectories against `evalset.json` (`adk eval` / `agents-cli eval`), run `InMemoryRunner` tests, and prepare for Cloud Run / Vertex AI Agent Engine deployment.

## Instructions
1. Run the reference solution:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. Evaluate the ADK agent trajectory against `workshop/02_final/evalset.json`:
   ```bash
   adk eval workshop/02_final/sre_agent workshop/02_final/evalset.json
   ```
3. Run the automated workshop integrity verifier:
   ```bash
   python3 scripts/verify_workshop.py .
   ```