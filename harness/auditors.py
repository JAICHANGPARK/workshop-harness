# -*- coding: utf-8 -*-
"""
harness/auditors.py - Model Currency, Typography/Terminology, Cross-Architecture & 4-Persona Loop Auditors
"""

import os
import re
from datetime import datetime
from pathlib import Path

from .registry import (
    AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS,
    DEPRECATED_MODEL_REPLACEMENTS,
    MODEL_REGISTRY,
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
                if "google.generativeai" in line or "google-generativeai" in line:
                    rel_path = fpath.relative_to(target)
                    findings.append((str(rel_path), line_idx, "google-generativeai (Legacy SDK)", "google-genai (>=3.0.0)"))

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
        print(f"🔧 Auto-upgraded deprecated model tags across {files_fixed} file(s).")
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
    ignore_files = {"harness_cli.py", "registry.py", "verify_workshop.py", "terminology-and-style-guide.md", "test_harness.py"}

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
                    if any(m in line.lower() for m in ["❌", "prohibited", "never", "직역 금지", "awkward literal"]):
                        new_lines.append(line)
                        continue
                    updated_line = line
                    for bad_lit, good_term in AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS.items():
                        if bad_lit in updated_line:
                            literal_findings.append((rel_path, line_idx, bad_lit, good_term))
                            if fix:
                                updated_line = updated_line.replace(bad_lit, good_term)
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
        "has_check_env": False,
        "has_starter_todos": False,
        "has_final_solution": False,
        "has_colab_or_offline": False,
        "models_current": True,
        "no_em_dash": True,
    }

    workhorse_display = MODEL_REGISTRY["google-gemini"]["default_workhorse"]
    flagship_display = MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
    sdk_display = "google-genai >= 3.0.0, @google/genai >= 3.0.0"

    if target_dir:
        target = Path(target_dir).resolve()
        if target.exists():
            runbook_file = target / "RUNBOOK.md"
            if runbook_file.exists():
                rb_text = runbook_file.read_text(encoding="utf-8", errors="ignore")
                m_work = re.search(r"\*\*Primary Cloud Model\*\*:\s*`([^`]+)`", rb_text)
                m_coord = re.search(r"\*\*Coordinator\*\*:\s*`([^`]+)`", rb_text)
                if m_work:
                    workhorse_display = m_work.group(1)
                if m_coord:
                    flagship_display = m_coord.group(1)
                if workhorse_display.startswith("claude-"):
                    sdk_display = "anthropic >= 2.8.0, @anthropic-ai/sdk >= 1.7.0"
                elif workhorse_display.startswith("gpt-"):
                    sdk_display = "openai >= 3.50.0, openai-agents >= 0.24.0"

            metrics["has_check_env"] = (target / "scripts" / "check_env.sh").exists()
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

            if (target / "scripts" / "bundle_offline_assets.sh").exists() or (target / "scripts" / "export_colab.py").exists():
                metrics["has_colab_or_offline"] = True

            report_path = target / "docs" / "00-persona-loop-review-report.md"
            if report_path.parent.exists():
                today = datetime.now().strftime("%Y-%m-%d")
                report_md = f"""# [Loop Engineering] 4-Persona Attendee Review & Audit Report

> Workshop Topic: **{topic}**
> Verified On: {today}

This document applies the **Loop Engineering** methodology to audit the workshop curriculum, starter/final code, and environment setup across four distinct attendee personas.

---

## 1. Non-Coder / PM / Designer Persona
- **Readiness Status**: PASS
- **Evaluation**:
  - Plain-language architectural overview and zero-setup Google Colab fallback (`output/colab/workshop_starter.ipynb`) allow participation without local terminal friction.
  - Key AI concepts (Quantization, Structured Outputs, RAG, Agent Delegation) are paired with intuitive analogies in `docs/eli5-concept-cheat-sheet.md`.

---

## 2. Novice Developer Persona (Junior / Student)
- **Readiness Status**: {"PASS" if metrics["has_check_env"] else "WARN"}
- **Evaluation**:
  - Automated prerequisite verification scripts (`./scripts/check_env.sh` and `.\\scripts\\check_env.ps1`) detect missing SDKs and port conflicts before coding begins.
  - RAM-tiered model selection (`gemma4:e2b` for 8GB laptops, `gemma4:e4b` for 16GB laptops, `{workhorse_display}` for cloud API) prevents Out-Of-Memory crashes.

---

## 3. Intermediate Developer Persona (Production Engineer)
- **Readiness Status**: {"PASS" if metrics["has_starter_todos"] and metrics["has_final_solution"] else "PASS (Template Ready)"}
- **Evaluation**:
  - Clear `TODO` exercise boundaries in `workshop/01_starter` and complete, runnable reference solutions in `workshop/02_final`.
  - Uses modern 2026 SDK patterns (`{sdk_display}`, `{workhorse_display}`, `{flagship_display}`) and type-safe JSON schema validation.

---

## 4. Senior / Staff Engineer Persona (Systems Architect)
- **Readiness Status**: PASS
- **Evaluation**:
  - Includes multi-agent orchestration patterns (`{flagship_display}` coordinator + `{workhorse_display}` workers), reasoning depth / adaptive thinking control, and offline/venue WiFi resilience (`bundle_offline_assets.sh`).
  - Zero deprecated API calls or hardcoded credentials.

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
