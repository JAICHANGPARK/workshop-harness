#!/usr/bin/env bash
# Headless Smoke Test via Google Colab CLI
set -e

echo "[INFO] Checking Google Colab CLI installation..."
if command -v colab &> /dev/null; then
    echo "[INFO] Running Colab Headless Test on workshop_solution.ipynb..."
    colab run workshop_solution.ipynb
    echo "[OK] Colab notebook verified successfully."
else
    echo "[INFO] Google Colab CLI (colab) not found."
    echo "Install with: pip install google-colab-cli"
    echo "Repository: https://github.com/googlecolab/google-colab-cli"
fi
