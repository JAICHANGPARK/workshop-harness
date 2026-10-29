#!/usr/bin/env python3
"""
export_open_codelabs.py - Converts a Workshop Harness project into an Open Codelabs bundle & pushes via `oc` CLI.
"""

import sys
import os
import re
import argparse
import shutil
import subprocess
from pathlib import Path

def export_to_open_codelabs(target_dir: str, output_dir: str = None, push: bool = False):
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Workshop directory '{target}' does not exist.")
        return False

    out_path = Path(output_dir).resolve() if output_dir else target / "output" / "open-codelabs"
    steps_path = out_path / "steps"
    steps_path.mkdir(parents=True, exist_ok=True)

    # Read workshop title / topic from README.md
    readme_path = target / "README.md"
    title = target.name
    description = f"Hands-on Workshop generated from {target.name}"
    author = "Workshop Facilitator"

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        topic_match = re.search(r"> Topic:\s*(.+)$", content, re.MULTILINE)
        if topic_match:
            description = topic_match.group(1).strip()

    # Build guide.md from setup guide or docs
    guide_file = target / "gemma4-local-setup-guide.md"
    guide_content = ""
    if guide_file.exists():
        guide_content = guide_file.read_text(encoding="utf-8")
    else:
        # Fallback combining prerequisites and env
        prereq = target / "docs" / "02-prerequisites.md"
        env_doc = target / "docs" / "01-hardware-and-env.md"
        if prereq.exists():
            guide_content += prereq.read_text(encoding="utf-8") + "\n\n"
        if env_doc.exists():
            guide_content += env_doc.read_text(encoding="utf-8")

    if not guide_content:
        guide_content = f"# Preparation Guide for {title}\n\nWelcome to {title}! Please follow facilitator instructions."

    (out_path / "guide.md").write_text(guide_content, encoding="utf-8")

    # Build steps from workshop/03_labs/README.md
    labs_file = target / "workshop" / "03_labs" / "README.md"
    steps_meta = []

    if labs_file.exists():
        labs_content = labs_file.read_text(encoding="utf-8")
        # Split by level 2 headings "## Lab ..." or "## Step ..."
        sections = re.split(r"(?=\n##\s+)", "\n" + labs_content)
        step_idx = 1
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            header_match = re.match(r"^##\s+(.+)$", sec, re.MULTILINE)
            if header_match:
                step_title = header_match.group(1).strip()
                filename = f"step_{step_idx:02d}.md"
                (steps_path / filename).write_text(sec, encoding="utf-8")
                steps_meta.append({"title": step_title, "file": f"steps/{filename}"})
                step_idx += 1

    if not steps_meta:
        # Default placeholder step if labs file not parsed
        step_filename = "step_01.md"
        (steps_path / step_filename).write_text(
            f"# Lab 01: Getting Started\n\nOpen `workshop/01_starter` and inspect main code.",
            encoding="utf-8"
        )
        steps_meta.append({"title": "Lab 01: Getting Started", "file": f"steps/{step_filename}"})

    # Write codelab.yaml manifest
    manifest_lines = [
        "version: 1",
        f'title: "{title}"',
        f'description: "{description}"',
        f'author: "{author}"',
        "is_public: true",
        "quiz_enabled: false",
        "require_quiz: false",
        "require_feedback: true",
        "require_submission: false",
        'guide_markdown: "guide.md"',
        "steps:"
    ]
    for s in steps_meta:
        manifest_lines.append(f'  - title: "{s["title"]}"')
        manifest_lines.append(f'    file: "{s["file"]}"')

    manifest_lines.extend([
        "materials:",
        '  - title: "Starter Code & Workshop Repo"',
        '    type: "link"',
        '    url: "https://github.com/JAICHANGPARK/workshop-harness"'
    ])

    manifest_content = "\n".join(manifest_lines) + "\n"
    manifest_path = out_path / "codelab.yaml"
    manifest_path.write_text(manifest_content, encoding="utf-8")

    print(f"✅ Exported Open Codelabs Bundle to: {out_path}")
    print(f"   📄 Manifest: {manifest_path}")
    print(f"   📑 Guide: {out_path / 'guide.md'}")
    print(f"   🚀 Steps: {len(steps_meta)} step files created in {steps_path}")

    if push:
        oc_bin = shutil.which("oc")
        if not oc_bin:
            print("⚠️ Warning: `oc` CLI tool not found in PATH. Skipping push.")
            print("💡 Install `oc` CLI via `cargo install --path backend --bin oc` inside open-codelabs repo.")
            return True

        print(f"🚀 Pushing manifest bundle to Open Codelabs via `oc codelab push`...")
        cmd = [oc_bin, "codelab", "push", "--manifest", str(manifest_path)]
        res = subprocess.run(cmd, check=False)
        if res.returncode == 0:
            print("🎉 Open Codelabs push completed successfully!")
        else:
            print(f"❌ `oc codelab push` failed with exit code {res.returncode}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Export Workshop Harness project to Open Codelabs bundle")
    parser.add_argument("--target", required=True, help="Path to target workshop directory")
    parser.add_argument("--output", default=None, help="Output directory for Open Codelabs bundle")
    parser.add_argument("--push", action="store_true", help="Automatically push bundle via `oc codelab push`")

    args = parser.parse_args()
    export_to_open_codelabs(args.target, args.output, args.push)

if __name__ == "__main__":
    main()
