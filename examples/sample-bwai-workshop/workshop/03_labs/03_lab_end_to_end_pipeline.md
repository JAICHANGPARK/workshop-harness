# Lab 03: End-to-End Pipeline & Automated Verification

## Objective
Run the complete reference pipeline in `workshop/02_final/main.py` with automatic local/cloud fallback and verify all workshop quality gates.

## Instructions
1. Execute the completed reference solution:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. Compare your implementation in `workshop/01_starter/main.py` against `workshop/02_final/main.py`.
3. Run the automated workshop integrity verifier:
   ```bash
   python3 scripts/verify_workshop.py .
   ```
