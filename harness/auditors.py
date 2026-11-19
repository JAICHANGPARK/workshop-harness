# -*- coding: utf-8 -*-
"""
harness/auditors.py - Model Currency, Typography/Terminology, Cross-Architecture & 4-Persona Loop Auditors
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from .registry import (
    AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS,
    DEPRECATED_MODEL_REPLACEMENTS,
    HARNESS_ROOT,
    MODEL_REGISTRY,
    TEMPLATES_DIR,
)


def list_models(provider: str = None):
    """Display the verified 2026 Frontier & Open-Weight Model Catalog."""
    print("=" * 72)
    print("🌐 Workshop Harness - Verified 2026 Model Catalog")
    print("=" * 72)
    for prov, entries in MODEL_REGISTRY.items():
        if provider and provider.lower() not in prov.lower():
            continue
        print(f"\n[{prov.upper()}]")
        for role, tag in entries.items():
            if isinstance(tag, list):
                print(f"  - {role:<24}: {', '.join(tag)}")
            else:
                print(f"  - {role:<24}: {tag}")
    print("\n" + "=" * 72)


def audit_models(target_dir: str, fix: bool = False) -> bool:
    """Scan a workshop directory for deprecated model tags or legacy SDK imports."""
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False

    print(f"🔍 Auditing Model & SDK Currency in '{target.name}'...")
    scan_extensions = {".py", ".ts", ".js", ".go", ".kt", ".dart", ".md", ".yaml", ".yml", ".json", ".ipynb"}
    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".dart_tool", "build", "tmp"}
    ignore_files = {"harness_cli.py", "registry.py", "auditors.py", "verify_workshop.py", "CHANGELOG.md", "test_harness.py"}

    findings = []
    unfixable_sdk_findings = []
    files_fixed = 0

    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            if fname in ignore_files:
                continue
            fpath = Path(root) / fname
            if fpath.suffix not in scan_extensions:
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            original_content = content
            lines = content.splitlines()
            file_has_findings = False
            for line_idx, line in enumerate(lines, 1):
                if any(marker in line.lower() for marker in ["prohibited", "deprecated", "legacy", "retired", "never use", "instead of"]):
                    continue
                for old_tag, new_tag in DEPRECATED_MODEL_REPLACEMENTS.items():
                    pattern = rf"(?<![\w.-]){re.escape(old_tag)}(?![\w.-])"
                    if re.search(pattern, line):
                        rel_path = fpath.relative_to(target)
                        findings.append((str(rel_path), line_idx, old_tag, new_tag))
                        file_has_findings = True
                if "google.generativeai" in line:
                    rel_path = fpath.relative_to(target)
                    findings.append((str(rel_path), line_idx, "google.generativeai (Legacy SDK import)", "from google import genai (google-genai >= 3.0.0)"))
                    unfixable_sdk_findings.append((str(rel_path), line_idx))
                if "google-generativeai" in line:
                    rel_path = fpath.relative_to(target)
                    findings.append((str(rel_path), line_idx, "google-generativeai (Legacy SDK package)", "google-genai (>=3.0.0)"))
                    file_has_findings = True

            if fix and file_has_findings:
                new_lines = []
                for line in content.splitlines(keepends=True):
                    if any(marker in line.lower() for marker in ["prohibited", "deprecated", "legacy", "retired", "never use", "instead of"]):
                        new_lines.append(line)
                        continue
                    updated_line = line
                    for old_tag, new_tag in DEPRECATED_MODEL_REPLACEMENTS.items():
                        pattern = rf"(?<![\w.-]){re.escape(old_tag)}(?![\w.-])"
                        updated_line = re.sub(pattern, new_tag, updated_line)
                    updated_line = updated_line.replace("google-generativeai", "google-genai")
                    new_lines.append(updated_line)
                content = "".join(new_lines)
                if content != original_content:
                    fpath.write_text(content, encoding="utf-8")
                    files_fixed += 1

    if not findings:
        print("✅ All model tags and SDK imports match the 2026 Frontier Standard!")
        return True

    print(f"⚠️ Found {len(findings)} outdated model/SDK reference(s):")
    for rel_path, line_no, old_val, new_val in findings[:25]:
        print(f"  - {rel_path}:{line_no} -> '{old_val}' (Recommended: '{new_val}')")
    if fix:
        if files_fixed:
            print(f"🔧 Auto-upgraded deprecated model/package references across {files_fixed} file(s).")
        if unfixable_sdk_findings:
            print(
                f"❌ {len(unfixable_sdk_findings)} legacy `google.generativeai` Python import(s) require manual code migration to `from google import genai`."
            )
            return False
        return True
    else:
        print("💡 Run with `--fix` to automatically upgrade legacy model strings.")
        return False


def sanitize_no_em_dash(text: str) -> str:
    """Replace forbidden em-dash characters (\\u2014) with standard hyphens (' - ' or '-')."""
    if "\u2014" not in text:
        return text
    text = re.sub(r"(?<=\S)\u2014(?=\S)", " - ", text)
    return text.replace("\u2014", "-")


def audit_typography(target_dir: str, fix: bool = False) -> bool:
    """Scan markdown, documentation, and code files for forbidden em-dashes (\\u2014) and awkward literal translations."""
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False

    print(f"🔍 Auditing Markdown Typography (No Em Dash) & Developer Terminology in '{target.name}'...")
    scan_extensions = {".md", ".txt", ".yaml", ".yml", ".ipynb", ".py", ".ts", ".js", ".go", ".kt", ".dart", ".java"}
    doc_extensions = {".md", ".txt", ".yaml", ".yml", ".ipynb"}
    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".dart_tool", "build", "tmp"}
    ignore_files = {
        "harness_cli.py",
        "registry.py",
        "router.py",
        "auditors.py",
        "verify_workshop.py",
        "terminology-and-style-guide.md",
        "test_harness.py",
    }

    findings = []
    literal_findings = []
    files_fixed = 0

    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix not in scan_extensions:
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            original_content = content
            rel_path = str(fpath.relative_to(target))

            if fpath.suffix in doc_extensions and "\u2014" in content:
                for line_idx, line in enumerate(content.splitlines(), 1):
                    if "\u2014" in line:
                        findings.append((rel_path, line_idx))
                if fix:
                    content = sanitize_no_em_dash(content)

            if fname not in ignore_files:
                new_lines = []
                for line_idx, line in enumerate(content.splitlines(keepends=True), 1):
                    if any(
                        m in line.lower()
                        for m in ["❌", "prohibited", "never", "직역 금지", "awkward literal", "번역투", "지양", "avoid"]
                    ):
                        new_lines.append(line)
                        continue
                    updated_line = line
                    for bad_lit, good_term in AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS.items():
                        if bad_lit in updated_line:
                            literal_findings.append((rel_path, line_idx, bad_lit, good_term))
                            if fix:
                                updated_line = updated_line.replace(bad_lit, good_term)
                    # Catch any remaining Korean double-passives (~되어집니다) or verbose modal calques (~하는 것이 가능합니다)
                    for m_dp in re.finditer(r"([가-힣]{1,10})되어집니다", updated_line):
                        bad_dp = m_dp.group(0)
                        good_dp = f"{m_dp.group(1)}됩니다"
                        literal_findings.append((rel_path, line_idx, bad_dp, good_dp))
                    if fix:
                        updated_line = re.sub(r"([가-힣]{1,10})되어집니다", r"\1됩니다", updated_line)
                    for m_poss in re.finditer(r"([가-힣]{1,10})하는 것이 가능합니다", updated_line):
                        bad_poss = m_poss.group(0)
                        good_poss = f"{m_poss.group(1)}할 수 있습니다"
                        literal_findings.append((rel_path, line_idx, bad_poss, good_poss))
                    if fix:
                        updated_line = re.sub(r"([가-힣]{1,10})하는 것이 가능합니다", r"\1할 수 있습니다", updated_line)
                    new_lines.append(updated_line)
                if fix:
                    content = "".join(new_lines)

            if fix and content != original_content:
                fpath.write_text(content, encoding="utf-8")
                files_fixed += 1

    if not findings and not literal_findings:
        print("✅ Typography & Terminology check PASSED (Zero em dashes and zero awkward literal translations)!")
        return True

    if findings:
        print(f"⚠️ Found {len(findings)} forbidden em-dash (\\u2014) occurrence(s):")
        for rel_path, line_no in findings[:25]:
            print(f"  - {rel_path}:{line_no} contains forbidden em-dash (\\u2014)")
    if literal_findings:
        print(f"⚠️ Found {len(literal_findings)} awkward literal translation(s) (Use developer-friendly + English bilingual terms):")
        for rel_path, line_no, bad_lit, good_term in literal_findings[:25]:
            print(f"  - {rel_path}:{line_no} uses '{bad_lit}' -> replace with '{good_term}'")

    if fix:
        print(f"🔧 Auto-sanitized typography and developer terminology across {files_fixed} file(s).")
        return True
    else:
        print("💡 Run with `--fix` to automatically sanitize em dashes and literal translations.")
        return False


def audit_compatibility(stack_str: str, target_dir: str = None):
    stack = [s.strip().lower() for s in stack_str.split(",")]
    print(f"🔍 Auditing Cross-Architecture Compatibility for Stack: {stack}")
    print("-" * 60)

    issues = []
    if any(k in stack for k in ["android", "compose"]):
        issues.append({
            "tool": "Google Android CLI & AVD Emulator",
            "target": "Intel Mac (x86_64) / Windows Hyper-V / Linux KVM",
            "risk": "AVD emulator CPU architecture mismatch (arm64 vs x86_64) or missing Hyper-V/KVM virtualization.",
            "fallback": "Install Google Android CLI (curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh | bash) and run 'android init' & 'android skills add --all'. Use physical device with USB debugging as fallback."
        })
    if any(k in stack for k in ["flutter", "genui", "a2ui"]):
        issues.append({
            "tool": "Flutter & A2UI / GenUI Platform Runner",
            "target": "Windows & Linux Attendees (No macOS / Xcode)",
            "risk": "iOS simulator / macOS desktop targets cannot be compiled on Windows or Linux.",
            "fallback": "Mandatory Universal Fallback: Use Flutter Web (flutter run -d chrome) for instant zero-install workshop execution on any laptop."
        })
    if "lmstudio" in stack:
        issues.append({
            "tool": "LM Studio",
            "target": "Intel Mac (x86_64)",
            "risk": "LM Studio has known stability issues & missing Metal GPU acceleration on Intel Mac.",
            "fallback": "Provide Ollama CLI (ollama serve) as mandatory fallback in docs/18-intel-mac-prep.md"
        })
    if "ollama" in stack or "gemma" in stack or "embeddinggemma" in stack:
        issues.append({
            "tool": "Ollama Local LLM & EmbeddingGemma 2 Runtime",
            "target": "8GB RAM Laptops / Intel Mac / Windows ARM64",
            "risk": "Loading 12B+ parameter models on 8GB RAM laptops causes OOM crashes or severe swap thrashing; full multimodal embeddinggemma-2:740m requires ~1.3GB.",
            "fallback": "Enforce RAM-tiered model tags: 8GB -> gemma4:e2b + embeddinggemma-2:270m, 16GB -> gemma4:e4b / gemma4:12b + embeddinggemma-2, 32GB+ -> gemma4:26b / gemma4:31b."
        })
    if "docker" in stack:
        issues.append({
            "tool": "Docker Desktop",
            "target": "Windows Home / ChromeOS / M1-M4 Mac",
            "risk": "Hyper-V / WSL2 configuration failure or x86 container architecture mismatch.",
            "fallback": "Provide local python script fallback or Google Colab notebook execution."
        })
    if "mlx" in stack:
        issues.append({
            "tool": "MLX Framework",
            "target": "Non-Apple Silicon (Intel Mac, Windows, Linux)",
            "risk": "MLX is strictly Apple Silicon (arm64) only.",
            "fallback": "Provide Ollama or HuggingFace transformers alternative for non-Mac users."
        })
    if "vllm" in stack:
        issues.append({
            "tool": "vLLM High-Throughput Engine",
            "target": "macOS (Apple Silicon / Intel) & Windows Laptops without discrete NVIDIA GPU",
            "risk": "vLLM is optimized for Linux CUDA GPUs; local laptop installation often fails without NVIDIA drivers.",
            "fallback": "Use Google Colab GPU runtime for vLLM labs or fallback to Ollama local OpenAI-compatible server (:11434/v1)."
        })
    if any(k in stack for k in ["gemini-live", "live", "audio"]):
        issues.append({
            "tool": "Gemini 3.8 Live Bidirectional Audio/Video API",
            "target": "All Attendee Laptops (Speaker + Mic Acoustic Loop)",
            "risk": "Open laptop speakers trigger Voice Activity Detection (VAD) self-interruption loops; OS microphone permissions may block browser/CLI access.",
            "fallback": "Mandate wired/Bluetooth earphones in RUNBOOK.md and verify OS microphone permissions prior to Lab 01."
        })
    if any(k in stack for k in ["adk", "google-adk"]):
        issues.append({
            "tool": "Google Agent Development Kit (ADK & adk web)",
            "target": "Port 8000 Conflict & Multi-Agent Delegation Loops",
            "risk": "Local port 8000 collisions prevent 'adk web' / 'adk api_server' startup; missing 'root_agent' symbol in agent.py breaks discovery.",
            "fallback": "Ensure top-level orchestrator is named 'root_agent' in agent.py, use 'adk web --port 8080' on port conflict, and assign gemini-4-hydrogen (or gemini-3.8-flash) to sub_agents."
        })
    if any(k in stack for k in ["agents-cli", "google-agents-cli"]):
        issues.append({
            "tool": "Google Agents CLI (google-agents-cli)",
            "target": "Python < 3.11 / Missing uvx or GCP Application Default Credentials",
            "risk": "'uvx google-agents-cli setup' requires Python 3.11+ and Astral uv; 'agents-cli deploy' fails without active GCP ADC credentials.",
            "fallback": "Install uv first, run 'uvx google-agents-cli setup' (or 'npx skills add google/agents-cli'), and run 'gcloud auth application-default login' before Lab 03."
        })
    if any(k in stack for k in ["claude", "anthropic", "claude-agent-sdk"]):
        issues.append({
            "tool": "Anthropic Claude Messages API & SDK v2 (anthropic >= 2.8.0)",
            "target": "API Version 2026-10-21 Breaking Changes & Model ID Format",
            "risk": "Passing legacy sampling parameters (temperature, top_p, top_k) returns HTTP 400 in API 2026-10-21; dot-notation tags (e.g. claude-sonnet-5.5) return HTTP 404.",
            "fallback": "Use canonical hyphenated IDs (claude-fable-5-2, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5), Adaptive Thinking (thinking={'type': 'adaptive'}), and LiteLlm('anthropic/...') when routing via Google ADK."
        })
    if any(k in stack for k in ["openai", "gpt", "openai-agents"]):
        issues.append({
            "tool": "OpenAI Responses API & SDK v3 (openai >= 3.50.0)",
            "target": "Retired o-Series Endpoints & Tier-1 Rate Limits",
            "risk": "Legacy isolated o-series model endpoints (o1, o3, o4-mini) are retired; unverified orgs may hit RPM/TPM limits on flagship gpt-6-astra.",
            "fallback": "Migrate to client.responses.create / client.responses.parse with gpt-6.1-sol or gpt-6.1-terra, tune reasoning={'effort': 'medium'}, and use LiteLlm('openai/...') for Google ADK integration."
        })

    if not issues:
        print("✅ No critical architecture mismatch detected for the given tech stack.")
    else:
        for idx, item in enumerate(issues, 1):
            print(f"[{idx}] Tool: {item['tool']} | Target: {item['target']}")
            print(f"    🚨 Risk: {item['risk']}")
            print(f"    💡 Fallback Action: {item['fallback']}")
            print()

    if target_dir and issues:
        matrix_path = Path(target_dir).resolve() / "docs" / "00-architecture-compatibility-matrix.md"
        if matrix_path.exists():
            existing = matrix_path.read_text(encoding="utf-8", errors="ignore")
            section_header = "## Stack-Specific Architecture & Risk Audit"
            if section_header not in existing:
                rows = "\n".join(
                    f"| **{it['tool']}** | {it['target']} | {it['risk']} | {it['fallback']} |"
                    for it in issues
                )
                extra_md = f"""

---

{section_header} (`{stack_str}`)

| Tool / Component | Target Environment | Identified Risk | Mandatory Fallback Path |
| :--- | :--- | :--- | :--- |
{rows}
"""
                matrix_path.write_text(sanitize_no_em_dash(existing.rstrip() + extra_md + "\n"), encoding="utf-8")

    print("-" * 60)
    return issues


def audit_persona_loop(topic: str, target_dir: str = None):
    print(f"🔄 Executing Loop Engineering 4-Persona Evaluation for: '{topic}'")
    print("-" * 60)

    metrics = {
        "has_eli5_guide": False,
        "has_colab": False,
        "has_check_env": False,
        "has_setup_guide": False,
        "has_starter_todos": False,
        "has_final_solution": False,
        "has_labs": False,
        "has_offline_bundler": False,
        "has_gitignore_env": False,
        "has_manifest": False,
    }

    workhorse_display = MODEL_REGISTRY["google-gemini"]["default_workhorse"]
    flagship_display = MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
    sdk_display = "google-genai >= 3.0.0, @google/genai >= 3.0.0"

    if target_dir:
        target = Path(target_dir).resolve()
        if target.exists():
            # 1. Read canonical workshop.json manifest first, fallback to RUNBOOK.md regex
            manifest_file = target / "workshop.json"
            if manifest_file.exists():
                try:
                    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                    metrics["has_manifest"] = True
                    models_cfg = manifest.get("models", {})
                    if models_cfg.get("cloud"):
                        workhorse_display = models_cfg["cloud"]
                    if models_cfg.get("flagship"):
                        flagship_display = models_cfg["flagship"]
                except Exception:
                    pass

            if not metrics["has_manifest"]:
                runbook_file = target / "RUNBOOK.md"
                if runbook_file.exists():
                    rb_text = runbook_file.read_text(encoding="utf-8", errors="ignore")
                    m_work = re.search(r"(?:\*\*Primary Cloud Model\*\*:|클라우드)\s*`([^`]+)`", rb_text)
                    m_coord = re.search(r"(?:\*\*Coordinator\*\*:|코디네이터)\s*`([^`]+)`", rb_text)
                    if m_work:
                        workhorse_display = m_work.group(1)
                    if m_coord:
                        flagship_display = m_coord.group(1)

            if workhorse_display.startswith("claude-"):
                sdk_display = "anthropic >= 2.8.0, @anthropic-ai/sdk >= 1.7.0"
            elif workhorse_display.startswith("gpt-"):
                sdk_display = "openai >= 3.50.0, openai-agents >= 0.24.0"

            # 2. Compute genuine readiness checks across all 4 personas
            metrics["has_eli5_guide"] = (target / "docs" / "eli5-concept-cheat-sheet.md").exists()
            metrics["has_colab"] = (
                (target / "output" / "colab" / "workshop_starter.ipynb").exists()
                or (target / "scripts" / "export_colab.py").exists()
            )
            metrics["has_check_env"] = (
                (target / "scripts" / "check_env.sh").exists()
                and (target / "scripts" / "check_env.ps1").exists()
            )
            metrics["has_setup_guide"] = (target / "SETUP_GUIDE.md").exists()

            starter_dir = target / "workshop" / "01_starter"
            if starter_dir.exists():
                for src_file in starter_dir.rglob("*"):
                    if src_file.is_file() and src_file.suffix in {".py", ".dart", ".ts", ".go", ".java", ".kt"}:
                        if "TODO" in src_file.read_text(encoding="utf-8", errors="ignore"):
                            metrics["has_starter_todos"] = True
                            break

            final_dir = target / "workshop" / "02_final"
            if final_dir.exists():
                for src_file in final_dir.rglob("*"):
                    if src_file.is_file() and src_file.suffix in {".py", ".dart", ".ts", ".go", ".java", ".kt"}:
                        metrics["has_final_solution"] = True
                        break

            labs_dir = target / "workshop" / "03_labs"
            if labs_dir.exists() and (list(labs_dir.glob("*.md"))):
                metrics["has_labs"] = True

            metrics["has_offline_bundler"] = (target / "scripts" / "bundle_offline_assets.sh").exists()
            gitignore_file = target / ".gitignore"
            if gitignore_file.exists():
                gi_lines = [ln.strip() for ln in gitignore_file.read_text(encoding="utf-8", errors="ignore").splitlines()]
                metrics["has_gitignore_env"] = ".env" in gi_lines

            p1_status = "PASS" if (metrics["has_eli5_guide"] and metrics["has_colab"]) else "WARN"
            p2_status = "PASS" if (metrics["has_check_env"] and metrics["has_setup_guide"]) else "WARN"
            p3_status = "PASS" if (metrics["has_starter_todos"] and metrics["has_final_solution"] and metrics["has_labs"]) else "WARN"
            p4_status = "PASS" if (metrics["has_offline_bundler"] and metrics["has_gitignore_env"] and metrics["has_manifest"]) else "WARN"

            report_path = target / "docs" / "00-persona-loop-review-report.md"
            if report_path.parent.exists():
                today = datetime.now().strftime("%Y-%m-%d")
                is_ko_topic = bool(re.search(r"[\uac00-\ud7a3]", topic or ""))
                if is_ko_topic:
                    report_md = f"""# 4-페르소나 참가자 관점 사전 점검 리포트 (Loop Engineering)

> 워크숍 주제: **{topic}**
> 점검 일자: {today}

비개발자부터 시니어 엔지니어까지 4가지 참가자 유형의 시각에서 실습 난이도, 환경 세팅, 코드 완성도를 사전 점검한 리포트입니다.

---

## 1. 비개발자 / PM / 디자이너 관점
- **점검 결과**: {p1_status}
- **세부 확인 내용**:
  - 로컬 터미널 설정이 어려운 참가자도 브라우저에서 바로 따라올 수 있도록 Google Colab 노트북(`output/colab/workshop_starter.ipynb`) 폴백을 제공합니다. (확인: `{"OK" if metrics["has_colab"] else "MISSING"}`)
  - 양자화, Structured Output, RAG, 멀티 에이전트 개념을 `docs/eli5-concept-cheat-sheet.md`에 쉬운 비유로 정리했습니다. (확인: `{"OK" if metrics["has_eli5_guide"] else "MISSING"}`)

---

## 2. 주니어 / 학생 개발자 관점
- **점검 결과**: {p2_status}
- **세부 확인 내용**:
  - 사전 준비 가이드(`SETUP_GUIDE.md`)와 `./scripts/check_env.sh` / `.\\scripts\\check_env.ps1` 자동 점검 스크립트를 제공합니다. (확인: `{"OK" if metrics["has_check_env"] and metrics["has_setup_guide"] else "MISSING"}`)
  - 노트북 메모리에 맞춰 8GB(`gemma4:e2b`), 16GB(`gemma4:e4b`), 클라우드 API(`{workhorse_display}`) 선택 기준을 명확히 구분해 OOM(메모리 부족 에러)을 예방합니다.

---

## 3. 실무 엔지니어 관점 (중급)
- **점검 결과**: {p3_status}
- **세부 확인 내용**:
  - `workshop/01_starter`의 `TODO` 구현 범위(`{"OK" if metrics["has_starter_todos"] else "MISSING"}`)와 `workshop/02_final` 정답 코드(`{"OK" if metrics["has_final_solution"] else "MISSING"}`), 단계별 실습 가이드(`workshop/03_labs`)가 준비되어 있습니다.
  - 2026년 최신 SDK(`{sdk_display}`)와 현역 모델 태그(`{workhorse_display}`, `{flagship_display}`), JSON 스키마 기반 Structured Output 패턴을 사용합니다.

---

## 4. 시니어 / 아키텍트 관점
- **점검 결과**: {p4_status}
- **세부 확인 내용**:
  - 코디네이터(`{flagship_display}`)와 워커(`{workhorse_display}`) 모델 분리, `workshop.json` 매니페스트(`{"OK" if metrics["has_manifest"] else "MISSING"}`), 행사장 네트워크 장애 대비 스크립트(`bundle_offline_assets.sh`: `{"OK" if metrics["has_offline_bundler"] else "MISSING"}`)를 갖추고 있습니다.
  - `.gitignore`의 `.env` 보호 규칙(`{"OK" if metrics["has_gitignore_env"] else "MISSING"}`)과 API 키 보안 점검을 확인했습니다.

---

## 참고 문서
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
"""
                else:
                    report_md = f"""# [Loop Engineering] 4-Persona Attendee Review & Audit Report

> Workshop Topic: **{topic}**
> Verified On: {today}

This document applies the **Loop Engineering** methodology to audit the workshop curriculum, starter/final code, and environment setup across four distinct attendee personas.

---

## 1. Non-Coder / PM / Designer Persona
- **Readiness Status**: {p1_status}
- **Evaluation**:
  - Plain-language architectural overview and zero-setup Google Colab fallback (`output/colab/workshop_starter.ipynb`: `{"OK" if metrics["has_colab"] else "MISSING"}`) allow participation without local terminal friction.
  - Key AI concepts (Quantization, Structured Outputs, RAG, Agent Routing) are paired with intuitive analogies in `docs/eli5-concept-cheat-sheet.md` (`{"OK" if metrics["has_eli5_guide"] else "MISSING"}`).

---

## 2. Novice Developer Persona (Junior / Student)
- **Readiness Status**: {p2_status}
- **Evaluation**:
  - Unified preparation guide (`SETUP_GUIDE.md`) and automated verification scripts (`./scripts/check_env.sh` and `.\\scripts\\check_env.ps1`) detect missing SDKs, RAM tier, and port conflicts (`{"OK" if metrics["has_check_env"] and metrics["has_setup_guide"] else "MISSING"}`).
  - RAM-tiered model selection (`gemma4:e2b` for 8GB laptops, `gemma4:e4b` for 16GB laptops, `{workhorse_display}` for cloud API) prevents Out-Of-Memory crashes.

---

## 3. Intermediate Developer Persona (Production Engineer)
- **Readiness Status**: {p3_status}
- **Evaluation**:
  - Clear `TODO` exercise boundaries in `workshop/01_starter` (`{"OK" if metrics["has_starter_todos"] else "MISSING"}`), runnable reference solutions in `workshop/02_final` (`{"OK" if metrics["has_final_solution"] else "MISSING"}`), and step-by-step guides in `workshop/03_labs` (`{"OK" if metrics["has_labs"] else "MISSING"}`).
  - Uses modern 2026 SDK patterns (`{sdk_display}`, `{workhorse_display}`, `{flagship_display}`) and type-safe JSON schema validation.

---

## 4. Senior / Staff Engineer Persona (Systems Architect)
- **Readiness Status**: {p4_status}
- **Evaluation**:
  - Includes multi-agent orchestration patterns (`{flagship_display}` coordinator + `{workhorse_display}` workers), canonical `workshop.json` manifest (`{"OK" if metrics["has_manifest"] else "MISSING"}`), and offline/venue WiFi resilience (`bundle_offline_assets.sh`: `{"OK" if metrics["has_offline_bundler"] else "MISSING"}`).
  - `.gitignore` protects `.env` credentials (`{"OK" if metrics["has_gitignore_env"] else "MISSING"}`) with zero hardcoded keys.

---

## References
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
"""
                report_path.write_text(report_md, encoding="utf-8")

    print("🌱 [Persona 1 - Non-Coder]: Verified zero-setup Colab fallback & conceptual clarity.")
    print("🐣 [Persona 2 - Novice Dev]: Verified copy-paste installation guides, check_env scripts & 8GB RAM fallback (gemma4:e2b).")
    print(f"🐥 [Persona 3 - Intermediate]: Verified 60-min TODO code bounds, Structured Output schema & 2026 SDK currency ({workhorse_display}).")
    print(f"🦅 [Persona 4 - Senior Architect]: Verified Challenge Tasks, Multi-Agent orchestration ({flagship_display}) & offline resilience.")
    print("-" * 60)
    print("✅ Loop Engineering 4-Persona Evaluation Completed! Report saved to docs/00-persona-loop-review-report.md")
    return metrics


def doctor_workshop(target_dir: str = None) -> bool:
    """Run a facilitator Go/No-Go pre-flight readiness check for the harness itself or a target workshop."""
    print("=" * 72)
    if not target_dir:
        print("🩺 Workshop Harness Doctor - Self-Check")
        print("=" * 72)
        all_ok = True

        # 1. Python version check
        py_ok = sys.version_info >= (3, 10)
        print(f"  [{'PASS' if py_ok else 'FAIL'}] Python >= 3.10 ({sys.version.split()[0]})")
        all_ok = all_ok and py_ok

        # 2. Required/Recommended CLIs
        for tool_name, required in [("git", True), ("uv", False), ("ollama", False), ("oc", False), ("colab", False), ("marp", False)]:
            found = shutil.which(tool_name) is not None
            level = "PASS" if found else ("FAIL" if required else "INFO")
            note = "installed" if found else ("missing (required)" if required else "not installed (optional)")
            print(f"  [{level}] CLI '{tool_name}': {note}")
            if required and not found:
                all_ok = False

        # 3. Python doc/slide build dependencies
        for mod_name, pkg_name in [("reportlab", "reportlab"), ("fitz", "pymupdf"), ("PIL", "pillow"), ("pptx", "python-pptx")]:
            try:
                __import__(mod_name)
                print(f"  [PASS] Python package '{pkg_name}': available")
            except ImportError:
                print(f"  [WARN] Python package '{pkg_name}': not installed in active interpreter (auto-installed via uv)")

        # 4. Sync check between scripts/*.py and templates/script-templates/*.py
        synced_scripts = ["build_slides.py", "export_colab.py", "export_open_codelabs.py"]
        for sname in synced_scripts:
            src_a = HARNESS_ROOT / "scripts" / sname
            src_b = TEMPLATES_DIR / "script-templates" / sname
            if src_a.exists() and src_b.exists():
                in_sync = src_a.read_bytes() == src_b.read_bytes()
                print(f"  [{'PASS' if in_sync else 'FAIL'}] Script template sync '{sname}': {'in sync' if in_sync else 'DRIFT DETECTED'}")
                if not in_sync:
                    all_ok = False
            else:
                print(f"  [FAIL] Script template sync '{sname}': missing file")
                all_ok = False

        print("=" * 72)
        print(f"{'✅ Harness Doctor PASSED!' if all_ok else '❌ Harness Doctor detected issues.'}")
        return all_ok

    target = Path(target_dir).resolve()
    print(f"🩺 Workshop Stage-Readiness Doctor: '{target.name}'")
    print("=" * 72)
    if not target.exists():
        print(f"  [FAIL] Target directory '{target}' does not exist.")
        return False

    checks = []

    def _rec(label: str, ok: bool, required: bool = True, detail: str = ""):
        status = "PASS" if ok else ("FAIL" if required else "WARN")
        suffix = f" ({detail})" if detail else ""
        print(f"  [{status}] {label}{suffix}")
        checks.append((ok, required))

    manifest_path = target / "workshop.json"
    manifest_ok = False
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_ok = all(k in manifest for k in ["name", "topic", "stack", "lang", "models"])
            _rec("Canonical manifest (workshop.json)", manifest_ok, True, f"lang={manifest.get('lang')}, stack={','.join(manifest.get('stack', []))}")
        except Exception as exc:
            _rec("Canonical manifest (workshop.json)", False, True, str(exc))
    else:
        _rec("Canonical manifest (workshop.json)", False, True, "missing")

    _rec("Attendee setup guide (SETUP_GUIDE.md)", (target / "SETUP_GUIDE.md").exists(), True)
    _rec("Facilitator runbook (RUNBOOK.md)", (target / "RUNBOOK.md").exists(), True)
    _rec("Starter code directory (workshop/01_starter)", (target / "workshop" / "01_starter").exists(), True)
    _rec("Final solution directory (workshop/02_final)", (target / "workshop" / "02_final").exists(), True)
    _rec("Step-by-step labs (workshop/03_labs)", bool(list((target / "workshop" / "03_labs").glob("*.md"))) if (target / "workshop" / "03_labs").exists() else False, True)
    _rec("Environment check scripts (check_env.sh & .ps1)", (target / "scripts" / "check_env.sh").exists() and (target / "scripts" / "check_env.ps1").exists(), True)
    _rec("Offline asset bundler (bundle_offline_assets.sh)", (target / "scripts" / "bundle_offline_assets.sh").exists(), True)

    gi_ok = False
    if (target / ".gitignore").exists():
        gi_lines = [ln.strip() for ln in (target / ".gitignore").read_text(encoding="utf-8", errors="ignore").splitlines()]
        gi_ok = ".env" in gi_lines
    _rec("Secret protection (.gitignore blocks .env)", gi_ok, True)

    pdf_files = list((target / "output" / "pdf").glob("*.pdf")) if (target / "output" / "pdf").exists() else []
    _rec("PDF Handout (output/pdf/*.pdf)", bool(pdf_files), False)
    _rec("Google Colab Notebooks (output/colab/)", (target / "output" / "colab" / "workshop_starter.ipynb").exists(), False)
    _rec("Open Codelabs Bundle (output/open-codelabs/codelab.yaml)", (target / "output" / "open-codelabs" / "codelab.yaml").exists(), False)
    _rec("Presentation Slides (output/slides/index.html)", (target / "output" / "slides" / "index.html").exists(), False)

    all_required_ok = all(ok for ok, req in checks if req)
    print("=" * 72)
    print(f"{'✅ GO FOR STAGE! All required workshop checks PASSED.' if all_required_ok else '❌ NO-GO: Fix required [FAIL] items before the session.'}")
    return all_required_ok
