#!/usr/bin/env bash
# Headless Smoke Test via Google Colab CLI
set -e

echo "🔍 Checking Google Colab CLI installation..."
if command -v colab &> /dev/null; then
    echo "⚡ Running Colab Headless Test on workshop_solution.ipynb..."
    colab run workshop_solution.ipynb
    echo "✅ Colab notebook verified successfully!"
else
    echo "💡 Google Colab CLI (colab) not found."
    echo "👉 Install with: pip install google-colab-cli"
    echo "👉 Repo: https://github.com/googlecolab/google-colab-cli"
fi
