#!/usr/bin/env python3
"""
verify_workshop.py - Workshop Integrity & Link Auditor
Automatically verifies markdown relative path links, image file existence, code execution,
bundle artifacts (Colab, Open Codelabs, Slides), 2026 model currency, typography, and API key hygiene.
"""

import os
import sys
import re
import json
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
        rel_md = md_file.relative_to(target_dir)
        rel_md_str = str(rel_md)
        if any(part in rel_md.parts for part in [".git", ".venv", "node_modules", "site", "tmp"]):
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
    print("\n🔍 Running Code & Artifact Smoke Tests...")
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

    # Verify ADK agent.py modules if present
    for stage in ["01_starter", "02_final"]:
        agent_py = target_dir / "workshop" / stage / "agent.py"
        if agent_py.exists():
            check_cmd = [
                sys.executable,
                "-c",
                f"import importlib.util; spec = importlib.util.spec_from_file_location('agent', r'{agent_py}'); "
                f"mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); "
                f"assert hasattr(mod, 'root_agent'), 'Missing root_agent symbol'",
            ]
            res = subprocess.run(check_cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"✅ workshop/{stage}/agent.py root_agent check: PASSED")
            else:
                print(f"❌ workshop/{stage}/agent.py root_agent check: FAILED ({res.stderr.strip()})")
                passed = False

    # Verify evalset.json if present
    evalset = target_dir / "workshop" / "02_final" / "evalset.json"
    if evalset.exists():
        try:
            data = json.loads(evalset.read_text(encoding="utf-8"))
            if isinstance(data, list) and len(data) > 0:
                print("✅ workshop/02_final/evalset.json schema check: PASSED")
            else:
                print("❌ workshop/02_final/evalset.json schema check: FAILED (Empty evalset)")
                passed = False
        except Exception as exc:
            print(f"❌ workshop/02_final/evalset.json JSON check: FAILED ({exc})")
            passed = False

    # Verify Polyglot ADK language tracks if present
    polyglot_final = target_dir / "workshop" / "02_final" / "polyglot"
    if polyglot_final.exists():
        expected_polyglot = [
            polyglot_final / "go" / "main.go",
            polyglot_final / "java" / "src" / "main" / "java" / "com" / "example" / "adk" / "SreAdkJavaApp.java",
            polyglot_final / "kotlin" / "src" / "main" / "kotlin" / "com" / "example" / "adk" / "SreAdkKotlinApp.kt",
            polyglot_final / "typescript" / "src" / "agent.ts",
        ]
        if all(p.exists() and p.stat().st_size > 0 for p in expected_polyglot):
            print("✅ workshop/02_final/polyglot (Go, Java, Kotlin, TypeScript ADK) check: PASSED")
        else:
            print("❌ workshop/02_final/polyglot check: FAILED (Missing language track files)")
            passed = False

    # Verify exported Google Colab notebooks if present
    colab_dir = target_dir / "output" / "colab"
    if colab_dir.exists():
        for nb_name in ["workshop_starter.ipynb", "workshop_solution.ipynb"]:
            nb_path = colab_dir / nb_name
            if nb_path.exists():
                try:
                    nb_json = json.loads(nb_path.read_text(encoding="utf-8"))
                    assert nb_json.get("nbformat") == 4 and isinstance(nb_json.get("cells"), list)
                    for cell in nb_json["cells"]:
                        if cell.get("cell_type") == "code":
                            src_lines = [
                                ln for ln in "".join(cell.get("source", [])).splitlines()
                                if not ln.strip().startswith("!")
                            ]
                            compile("\n".join(src_lines), str(nb_path), "exec")
                    print(f"✅ output/colab/{nb_name} notebook syntax check: PASSED")
                except Exception as exc:
                    print(f"❌ output/colab/{nb_name} notebook syntax check: FAILED ({exc})")
                    passed = False

    # Verify exported Open Codelabs bundle if present
    codelab_yaml = target_dir / "output" / "open-codelabs" / "codelab.yaml"
    if codelab_yaml.exists():
        codelab_dir = codelab_yaml.parent
        guide_md = codelab_dir / "guide.md"
        steps_dir = codelab_dir / "steps"
        manifest_text = codelab_yaml.read_text(encoding="utf-8", errors="ignore")
        has_required_keys = all(k in manifest_text for k in ["version:", "title:", "guide_markdown:", "steps:"])
        if guide_md.exists() and steps_dir.exists() and list(steps_dir.glob("step_*.md")) and has_required_keys:
            print("✅ output/open-codelabs bundle check: PASSED")
        else:
            print("❌ output/open-codelabs bundle check: FAILED (Missing guide.md, step files, or required manifest keys)")
            passed = False

    # Verify exported presentation slides if present
    slides_dir = target_dir / "output" / "slides"
    if slides_dir.exists():
        if (slides_dir / "slides.md").exists() and (slides_dir / "index.html").exists():
            print("✅ output/slides presentation deck check: PASSED")
        else:
            print("❌ output/slides presentation deck check: FAILED (Missing slides.md or index.html)")
            passed = False

    return passed


def audit_model_and_sdk_currency(target_dir: Path):
    print("\n🔍 Auditing 2026 Model & SDK Currency...")
    deprecated_patterns = {
        "gemini-1.5-flash": "gemini-3.8-flash",
        "gemini-1.5-pro": "gemini-4-argon",
        "gemini-2.0-flash": "gemini-3.8-flash",
        "gemini-2.0-flash-live": "gemini-3.8-live",
        "gemini-2.5-flash": "gemini-3.8-flash",
        "gemini-2.5-pro": "gemini-4-argon",
        "gemini-2.5-flash-lite": "gemini-3.5-flash-lite",
        "gemini-3.1-flash": "gemini-3.8-flash",
        "gemini-3.1-pro": "gemini-4-argon",
        "gemini-3.1-flash-live-preview": "gemini-3.8-live",
        "gemini-2.5-flash-preview-tts": "gemini-3.8-flash-tts",
        "gemini-3.1-flash-image-preview": "gemini-nano-banana-2.1",
        "gpt-4o-mini": "gpt-6-luna",
        "gpt-4o": "gpt-6.1-sol",
        "gpt-5.4-mini": "gpt-6-luna",
        "claude-3-5-sonnet": "claude-sonnet-5.5",
        "claude-3-7-sonnet": "claude-sonnet-5.5",
        "claude-opus-4": "claude-opus-5.5",
        "google.generativeai": "from google import genai (google-genai >= 2.30.1)",
        "google-generativeai": "google-genai (>= 2.30.1)",
    }
    scan_exts = {".py", ".ts", ".js", ".go", ".kt", ".dart", ".md"}
    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".dart_tool", "build", "tmp", "site"}
    ignore_files = {"verify_workshop.py", "harness_cli.py", "CHANGELOG.md", "test_harness.py"}
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
    print("\n🔍 Auditing Typography (No Em Dash), Developer Terminology & API Key Hygiene...")
    md_files = list(target_dir.glob("**/*.md"))
    em_dash_findings = []
    literal_findings = []
    leaked_key_findings = []

    awkward_literals = {
        "손으로 하는 실험실": "Hands-on Lab (핸즈온 랩)",
        "달리는 책": "Runbook (런북)",
        "발판 설치": "Scaffolding (스캐폴딩)",
        "뼈대 공사": "Scaffolding (스캐폴딩)",
        "뼈대 코드": "Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)",
        "생각 예산": "Thinking Budget (추론 예산)",
        "사고 예산": "Thinking Budget (추론 예산)",
        "구조화된 출력물": "Structured Outputs (구조화 출력)",
        "도구 부르기": "Tool Calling (툴 콜링)",
        "함수 부르기": "Function Calling (함수 호출)",
        "검색 증강된 생성": "RAG (Retrieval-Augmented Generation, 검색 증강 생성)",
        "끼워넣기 벡터": "Embedding (임베딩)",
        "미세 조정하기": "Fine-tuning (파인튜닝)",
        "다중 대리인 지휘": "Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)",
        "하위 대리인 넘기기": "Sub-Agent Delegation (서브 에이전트 위임)",
        "대리인 개발 키트": "ADK (Agent Development Kit, 에이전트 개발 키트)",
        "궤도 채점": "Trajectory Evaluation (궤적 평가)",
        "경로 채점": "Trajectory Evaluation (궤적 평가)",
        "연기 시험": "Smoke Test (스모크 테스트)",
        "후퇴 경로": "Fallback (폴백)",
        "비상 후퇴": "Fallback (폴백)",
        "상투적인 판박이 코드": "Boilerplate Code (보일러플레이트 코드)",
        "의존성 주사": "Dependency Injection (의존성 주입)",
        "차가운 시작": "Cold Start (콜드 스타트)",
        "기억 장치 넘침": "OOM (Out-Of-Memory, 메모리 부족 에러)",
        "부서지는 변경": "Breaking Changes (브레이킹 체인지)",
        "깨지는 변경": "Breaking Changes (브레이킹 체인지)",
        "속도 제한 걸림": "Rate Limit (레이트 리밋)",
        "맥락 창문": "Context Window (컨텍스트 윈도우)",
        "문맥 창문": "Context Window (컨텍스트 윈도우)",
        "체제 지시문": "System Instruction (시스템 프롬프트)",
        "인간 고리 안": "Human-in-the-Loop (HITL, 사용자 승인 체크포인트)",
        "사람을 루프에": "Human-in-the-Loop (HITL, 사용자 승인 체크포인트)",
    }
    ignore_literal_files = {"harness_cli.py", "verify_workshop.py", "terminology-and-style-guide.md", "test_harness.py"}
    api_key_pattern = re.compile(r"AIzaSy[A-Za-z0-9_-]{25,}")
    safe_placeholders = {"AIzaSyYourGeminiApiKeyHere", "AIzaSyYourGeneratedApiKeyHere"}

    for md_file in md_files:
        rel_md = md_file.relative_to(target_dir)
        if any(part in rel_md.parts for part in [".git", ".venv", "node_modules", "tmp", "site"]):
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        rel_path = str(rel_md)
        if "\u2014" in content:
            for line_no, line in enumerate(content.splitlines(), 1):
                if "\u2014" in line:
                    em_dash_findings.append(f"{rel_path}:{line_no}")
        if md_file.name not in ignore_literal_files:
            for line_no, line in enumerate(content.splitlines(), 1):
                if any(m in line.lower() for m in ["❌", "prohibited", "never", "직역 금지", "awkward literal"]):
                    continue
                for bad_lit, good_term in awkward_literals.items():
                    if bad_lit in line:
                        literal_findings.append(f"{rel_path}:{line_no} ('{bad_lit}' -> '{good_term}')")

    # Scan for accidental hardcoded Google API keys
    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".dart_tool", "build", "tmp", "site"}
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix not in {".py", ".ts", ".js", ".go", ".kt", ".dart", ".java", ".md", ".json", ".yaml", ".yml", ".env"}:
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for line_no, line in enumerate(text.splitlines(), 1):
                for match in api_key_pattern.findall(line):
                    if match not in safe_placeholders and "Your" not in match and "Example" not in match:
                        rel_p = str(fpath.relative_to(target_dir))
                        leaked_key_findings.append(f"{rel_p}:{line_no}")

    if em_dash_findings or literal_findings or leaked_key_findings:
        if em_dash_findings:
            print(f"❌ Em dash (\\u2014) detected in {len(em_dash_findings)} location(s): {', '.join(em_dash_findings[:10])}")
            print("💡 Rule violation: Never use em dashes (\\u2014) in documentation or .md files. Use '-', ':', or '()' instead.")
        if literal_findings:
            print(f"❌ Awkward literal translation detected in {len(literal_findings)} location(s): {', '.join(literal_findings[:5])}")
            print("💡 Rule violation: Use developer-friendly terminology paired with the English original term in parentheses.")
        if leaked_key_findings:
            print(f"❌ Potential exposed API Key detected in: {', '.join(leaked_key_findings[:5])}")
        return False
    else:
        print("✅ Typography, Developer Terminology & API Key Hygiene check PASSED (Zero forbidden em dashes, literal translations, or leaked keys).")
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
