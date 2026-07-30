#!/usr/bin/env python3
"""
verify_workshop.py - Workshop Integrity & Link Auditor
마크다운 상대 경로 링크, 이미지 존재 여부, 코드 실행 상태를 자동으로 점검하는 하네스 검증 도구
"""

import os
import sys
import re
import glob
import subprocess
from pathlib import Path

def audit_markdown_links(target_dir: Path):
    print("🔍 Auditing Markdown Links & Assets...")
    md_files = list(target_dir.glob("**/*.md"))
    broken_links = []
    total_links = 0

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for md_file in md_files:
        if ".venv" in str(md_file) or "node_modules" in str(md_file):
            continue

        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        matches = link_pattern.findall(content)
        for text, url in matches:
            if url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("mailto:"):
                continue

            total_links += 1
            # Clean anchor tags
            clean_url = url.split("#")[0]
            if not clean_url:
                continue

            target_path = (md_file.parent / clean_url).resolve()
            if not target_path.exists():
                broken_links.append((str(md_file.relative_to(target_dir)), url))

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

def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    print(f"🚀 Starting Workshop Harness Integrity Test for: '{target.name}'")
    print("-" * 60)

    links_ok = audit_markdown_links(target)
    code_ok = test_code_execution(target)

    print("-" * 60)
    if links_ok and code_ok:
        print("✨ All Workshop Harness Integrity Tests PASSED! Ready for publication.")
        sys.exit(0)
    else:
        print("❌ Integrity tests FAILED. Please fix the reported errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
