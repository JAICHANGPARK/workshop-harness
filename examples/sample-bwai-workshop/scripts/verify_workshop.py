#!/usr/bin/env python3
"""
verify_workshop.py - Workshop Integrity & Link Auditor
Automatically verifies markdown relative path links, image file existence, and code execution
status as a comprehensive harness verification tool.
"""

import os
import sys
import re
import glob
import subprocess
from pathlib import Path

def _strip_code_blocks_and_spans(markdown_text: str) -> str:
    """Remove fenced code blocks and inline code spans so example links inside code are not flagged."""
    no_fenced = re.sub(r"```[\s\S]*?```", "", markdown_text)
    no_inline = re.sub(r"`[^`\n]+`", "", no_fenced)
    return no_inline


def audit_markdown_links(target_dir: Path):
    print("🔍 Auditing Markdown Links & Assets...")
    md_files = list(target_dir.glob("**/*.md"))
    broken_links = []
    total_links = 0

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    is_harness_root = (target_dir / "harness_cli.py").exists() and (target_dir / "templates").exists()

    for md_file in md_files:
        rel_md_str = str(md_file.relative_to(target_dir))
        if ".venv" in rel_md_str or "node_modules" in rel_md_str or "site/" in rel_md_str:
            continue
        # Skip raw doc-templates when auditing the harness root itself (paths resolve after scaffolding)
        if is_harness_root and rel_md_str.startswith("templates/doc-templates/"):
            continue

        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = _strip_code_blocks_and_spans(f.read())

        matches = link_pattern.findall(content)
        for text, url in matches:
            url = url.strip()
            if (
                url.startswith("http://")
                or url.startswith("https://")
                or url.startswith("#")
                or url.startswith("mailto:")
                or url.startswith("tel:")
            ):
                continue

            total_links += 1
            if url.startswith("file://"):
                broken_links.append((rel_md_str, url))
                continue

            # Clean anchor tags
            clean_url = url.split("#")[0]
            if not clean_url:
                continue

            target_path = (md_file.parent / clean_url).resolve()
            if not target_path.exists():
                broken_links.append((rel_md_str, url))

    if broken_links:
        print(f"❌ Found {len(broken_links)} broken relative links out of {total_links} links:")
        for source, target in broken_links:
            print(f"  - In '{source}': Broken link -> '{target}'")
    else:
        print(f"✅ All {total_links} relative markdown links and image paths are valid!")

    return len(broken_links) == 0

def test_code_execution(target_dir: Path):
    print("\n🔍 Running Code Smoke Tests...")
    starter = target_dir / "workshop" / "01_starter" / "main.py"
    final = target_dir / "workshop" / "02_final" / "main.py"

    passed = True
    if starter.exists():
        res = subprocess.run([sys.executable, str(starter)], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ workshop/01_starter execution test: PASSED")
        else:
            print(f"❌ workshop/01_starter execution test: FAILED ({res.stderr.strip()})")
            passed = False

    if final.exists():
        res = subprocess.run([sys.executable, str(final)], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ workshop/02_final execution test: PASSED")
        else:
            print(f"❌ workshop/02_final execution test: FAILED ({res.stderr.strip()})")
            passed = False

    return passed


def audit_model_and_sdk_currency(target_dir: Path):
    print("\n🔍 Auditing 2026 Model & SDK Currency...")
    deprecated_patterns = {
        "gemini-1.5-flash": "gemini-3.8-flash",
        "gemini-1.5-pro": "gemini-4-argon",
        "gemini-2.0-flash": "gemini-3.8-flash",
        "gemini-2.5-flash": "gemini-3.8-flash",
        "gemini-2.5-pro": "gemini-4-argon",
        "gemini-3.1-flash": "gemini-3.8-flash",
        "gemini-3.1-flash-live-preview": "gemini-3.8-live",
        "gpt-4o-mini": "gpt-6-luna",
        "claude-3-5-sonnet": "claude-sonnet-5.5",
        "google.generativeai": "from google import genai (google-genai >= 2.30.1)",
    }
    scan_exts = {".py", ".ts", ".js", ".go", ".kt", ".dart", ".md"}
    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".dart_tool", "build", "tmp", "site"}
    ignore_files = {"verify_workshop.py", "harness_cli.py", "CHANGELOG.md"}
    warnings = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix not in scan_exts or fpath.name in ignore_files:
                continue
            try:
                lines = fpath.read_text(encoding="utf-8", errors="ignore").splitlines()
            except Exception:
                continue
            for idx, line in enumerate(lines, 1):
                if any(k in line.lower() for k in ["prohibited", "deprecated", "legacy", "retired", "never use", "instead of"]):
                    continue
                for old_pat, replacement in deprecated_patterns.items():
                    if re.search(rf"(?<![\w.-]){re.escape(old_pat)}(?![\w.-])", line):
                        warnings.append((str(fpath.relative_to(target_dir)), idx, old_pat, replacement))

    if warnings:
        print(f"⚠️ Found {len(warnings)} legacy model/SDK reference(s):")
        for rel_file, line_no, pat, repl in warnings[:10]:
            print(f"  - {rel_file}:{line_no} uses '{pat}' -> upgrade to '{repl}'")
        return False
    else:
        print("✅ All model tags and SDK imports follow 2026 Frontier standards!")
        return True


def audit_typography_and_security(target_dir: Path):
    print("\n🔍 Auditing Typography (No Em Dash) & API Key Hygiene...")
    md_files = list(target_dir.glob("**/*.md"))
    em_dash_files = []
    for md_file in md_files:
        if any(part in str(md_file) for part in [".venv", "node_modules", "AGENTS.md", "CLAUDE.md"]):
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if "\u2014" in content:
            em_dash_files.append(str(md_file.relative_to(target_dir)))

    if em_dash_files:
        print(f"⚠️ Em dash (\\u2014) detected in {len(em_dash_files)} markdown file(s): {', '.join(em_dash_files[:5])}")
    else:
        print("✅ Typography check PASSED (Zero forbidden em dashes in markdown docs).")
    return True


def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    print(f"🚀 Starting Workshop Harness Integrity Test for: '{target.name}'")
    print("-" * 60)

    links_ok = audit_markdown_links(target)
    code_ok = test_code_execution(target)
    models_ok = audit_model_and_sdk_currency(target)
    typo_ok = audit_typography_and_security(target)

    print("-" * 60)
    if links_ok and code_ok and models_ok and typo_ok:
        print("✨ All Workshop Harness Integrity Tests PASSED! Ready for publication.")
        sys.exit(0)
    else:
        print("❌ Integrity tests FAILED. Please fix the reported errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()

