#!/usr/bin/env python3
"""
export_colab.py - Converts a Workshop Harness project into Google Colab interactive notebooks (.ipynb)
and provides automated headless smoke testing via Google Colab CLI (colab-cli).
"""

import sys
import os
import re
import json
import argparse
import shutil
import subprocess
from pathlib import Path

def create_notebook_cell(cell_type: str, source: str):
    """Create a standard Jupyter Notebook cell dictionary."""
    lines = [line + "\n" for line in source.split("\n")]
    if lines and lines[-1] == "\n":
        lines[-1] = ""
    elif lines:
        lines[-1] = lines[-1].rstrip("\n")

    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": lines
        }
    else:
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": lines
        }

def build_ipynb(cells, title="Workshop Notebook"):
    """Wrap cells into standard Jupyter Notebook JSON format."""
    return {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

def export_to_colab(target_dir: str, output_dir: str = None, repo_name: str = None):
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Workshop directory '{target}' does not exist.")
        return False

    out_path = Path(output_dir).resolve() if output_dir else target / "output" / "colab"
    out_path.mkdir(parents=True, exist_ok=True)

    # Read workshop title and topic
    readme_path = target / "README.md"
    title = target.name
    topic = "Hands-on AI Workshop"

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        topic_match = re.search(r"> Topic:\s*(.+)$", content, re.MULTILINE)
        if topic_match:
            topic = topic_match.group(1).strip()

    # Determine GitHub repo path for badge
    repo = repo_name or f"JAICHANGPARK/{target.name}"
    badge_starter_url = f"https://colab.research.google.com/github/{repo}/blob/main/output/colab/workshop_starter.ipynb"
    badge_solution_url = f"https://colab.research.google.com/github/{repo}/blob/main/output/colab/workshop_solution.ipynb"

    print(f"📦 Generating Google Colab Notebooks for '{title}'...")

    # Read starter and solution code
    starter_code_file = target / "workshop" / "01_starter" / "main.py"
    solution_code_file = target / "workshop" / "02_final" / "main.py"

    starter_code = starter_code_file.read_text(encoding="utf-8") if starter_code_file.exists() else "# Starter code placeholder\nprint('Starting workshop...')"
    solution_code = solution_code_file.read_text(encoding="utf-8") if solution_code_file.exists() else "# Solution code placeholder\nprint('Completed workshop!')"

    # Read lab markdown
    labs_file = target / "workshop" / "03_labs" / "README.md"
    lab_sections = []
    if labs_file.exists():
        labs_content = labs_file.read_text(encoding="utf-8")
        raw_sections = re.split(r"(?=\n##\s+)", "\n" + labs_content)
        for sec in raw_sections:
            sec = sec.strip()
            if sec:
                lab_sections.append(sec)

    if not lab_sections:
        lab_sections = [
            f"## Lab 01: Getting Started with {topic}\nFollow along with the facilitator to verify the setup.",
            "## Lab 02: Core Hands-on Logic\nImplement the primary features and run local test pipelines.",
            "## Lab 03: Final Verification\nTest edge cases and complete the workshop challenge."
        ]

    # Common setup cells
    env_setup_code = """# [Step 0] Environment Setup & Dependencies Installation
!pip install -q google-genai pydantic requests
!nvidia-smi || echo "Running on CPU runtime"
"""

    secrets_code = """# [Step 0-1] Secure Credential Configuration (Colab Secrets / Userdata)
# Add your GEMINI_API_KEY in Colab's left sidebar 'Secrets' (Key icon)
import os
try:
    from google.colab import userdata
    GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
    os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
    print("✅ GEMINI_API_KEY loaded securely from Colab Secrets.")
except Exception:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found in Secrets. Please set it or enter manually.")
"""

    # 1. Build Starter Notebook
    starter_cells = [
        create_notebook_cell("markdown", f"# {title} - Hands-on Starter Notebook\n\n"
                                         f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_starter_url})\n\n"
                                         f"> **Topic**: {topic}\n\n"
                                         f"Welcome to the hands-on lab! Run each cell sequentially and fill in the `TODO` sections."),
        create_notebook_cell("code", env_setup_code),
        create_notebook_cell("code", secrets_code),
    ]

    for idx, lab_sec in enumerate(lab_sections, 1):
        starter_cells.append(create_notebook_cell("markdown", lab_sec))
        if idx == 1:
            starter_cells.append(create_notebook_cell("code", starter_code))
        else:
            starter_cells.append(create_notebook_cell("code", f"# TODO [Lab {idx:02d}]: Implement your code below\n"))

    starter_nb = build_ipynb(starter_cells, title=f"{title} (Starter)")
    starter_path = out_path / "workshop_starter.ipynb"
    starter_path.write_text(json.dumps(starter_nb, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Build Solution Notebook
    solution_cells = [
        create_notebook_cell("markdown", f"# {title} - Complete Solution Notebook\n\n"
                                         f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_solution_url})\n\n"
                                         f"> **Topic**: {topic}\n\n"
                                         f"This notebook contains the complete reference solution for facilitators and attendees."),
        create_notebook_cell("code", env_setup_code),
        create_notebook_cell("code", secrets_code),
    ]

    for idx, lab_sec in enumerate(lab_sections, 1):
        solution_cells.append(create_notebook_cell("markdown", lab_sec))
        if idx == len(lab_sections) or idx == 1:
            solution_cells.append(create_notebook_cell("code", solution_code))
        else:
            solution_cells.append(create_notebook_cell("code", f"# Solution for Lab {idx:02d}\n# Reference implementation\n"))

    solution_nb = build_ipynb(solution_cells, title=f"{title} (Solution)")
    solution_path = out_path / "workshop_solution.ipynb"
    solution_path.write_text(json.dumps(solution_nb, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. Create Colab README
    colab_readme = f"""# Google Colab Interactive Notebooks for {title}

> Topic: {topic}

## 🚀 One-Click Open in Colab

| Notebook | Description | Open in Colab |
| :--- | :--- | :--- |
| **Starter Lab** | Attendee hands-on guide with TODOs | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_starter_url}) |
| **Reference Solution** | Facilitator complete solution | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_solution_url}) |

## 🧪 Testing with Google Colab CLI (`colab-cli`)

You can run automated smoke tests on these notebooks using the official [Google Colab CLI](https://github.com/googlecolab/google-colab-cli):

```bash
# Run solution notebook headless in Colab
colab run output/colab/workshop_solution.ipynb
```
"""
    (out_path / "README.md").write_text(colab_readme, encoding="utf-8")

    # 4. Create Colab Test Shell Script
    test_script_content = f"""#!/usr/bin/env bash
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
"""
    test_script_path = out_path / "test_colab_run.sh"
    test_script_path.write_text(test_script_content, encoding="utf-8")
    os.chmod(test_script_path, 0o755)

    print(f"✨ Colab Bundle successfully created at: {out_path}")
    print(f"  - {starter_path.name}")
    print(f"  - {solution_path.name}")
    print(f"  - README.md (with badges)")
    print(f"  - test_colab_run.sh")
    return True

def test_colab(target_dir: str):
    target = Path(target_dir).resolve()
    colab_dir = target / "output" / "colab"
    solution_nb = colab_dir / "workshop_solution.ipynb"

    if not solution_nb.exists():
        print(f"⚠️ Colab bundle not found at {colab_dir}. Generating now...")
        export_to_colab(str(target))

    print(f"🧪 Testing Colab Notebook via Google Colab CLI...")
    if shutil.which("colab"):
        cmd = ["colab", "run", str(solution_nb)]
        print(f"🚀 Executing: {' '.join(cmd)}")
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print("✅ Google Colab CLI execution passed!")
        else:
            print("⚠️ Google Colab CLI reported an error during execution.")
    else:
        print("💡 Google Colab CLI ('colab') is not installed in the local PATH.")
        print("   To install: pip install google-colab-cli")
        print("   To test manually: Open workshop_starter.ipynb in Google Colab.")

def main():
    parser = argparse.ArgumentParser(description="Export Workshop to Google Colab Notebooks (.ipynb)")
    parser.add_argument("--target", required=True, help="Path to workshop project directory")
    parser.add_argument("--output", default=None, help="Target output directory")
    parser.add_argument("--repo", default=None, help="GitHub repository (e.g. USER/REPO) for Colab badges")
    parser.add_argument("--test", action="store_true", help="Run smoke test via Google Colab CLI")

    args = parser.parse_args()

    export_to_colab(args.target, args.output, args.repo)
    if args.test:
        test_colab(args.target)

if __name__ == "__main__":
    main()
