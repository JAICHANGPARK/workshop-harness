# -*- coding: utf-8 -*-
"""
harness/exporters.py - PDF, Open Codelabs, Google Colab, Presentation Slides & 9-Step Orchestrator
"""

import shutil
import subprocess
import sys
from pathlib import Path

from .auditors import audit_compatibility, audit_models, audit_persona_loop, audit_typography
from .registry import HARNESS_ROOT, MODEL_REGISTRY, TEMPLATES_DIR, ensure_uv_dependencies
from .router import parse_natural_prompt
from .scaffolder import init_workshop


def _run_python_script(args_list) -> int:
    """Execute a python script using uv's harness project environment if available, otherwise sys.executable."""
    if shutil.which("uv"):
        res = subprocess.run(["uv", "run", "--project", str(HARNESS_ROOT), "python"] + args_list, check=False)
    else:
        res = subprocess.run([sys.executable] + args_list, check=False)
    return res.returncode


def test_workshop(target_dir: str) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    script = target / "scripts" / "verify_workshop.py"
    if not script.exists():
        script = TEMPLATES_DIR / "script-templates" / "verify_workshop.py"

    print(f"🔍 Running Workshop Integrity Audit on '{target}'...")
    return _run_python_script([str(script), str(target)]) == 0


def build_pdf(target_dir: str) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    ensure_uv_dependencies()
    docs_dir = target / "docs"
    script = target / "scripts" / "generate_prep_pdf.py"
    output_pdf = target / "output" / "pdf" / f"{target.name}-prep-guide.pdf"
    preview_dir = target / "tmp" / "pdfs"

    if not script.exists():
        print(f"❌ Error: Script '{script}' not found.")
        return False

    print(f"📄 Building PDF for {target.name}...")
    return _run_python_script([str(script), str(docs_dir), str(output_pdf), str(preview_dir)]) == 0


def export_codelab(target_dir: str, output_dir: str = None, push: bool = False) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    script = target / "scripts" / "export_open_codelabs.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_open_codelabs.py"

    print(f"📦 Exporting Open Codelabs Bundle for '{target.name}'...")
    cmd = [str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if push:
        cmd.append("--push")

    return _run_python_script(cmd) == 0


def export_colab(target_dir: str, output_dir: str = None, repo: str = None, test: bool = False) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"📦 Exporting Google Colab Notebooks for '{target.name}'...")
    cmd = [str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if repo:
        cmd.extend(["--repo", str(repo)])
    if test:
        cmd.append("--test")

    return _run_python_script(cmd) == 0


def test_colab(target_dir: str) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"🧪 Testing Google Colab Notebooks via Colab CLI for '{target.name}'...")
    return _run_python_script([str(script), "--target", str(target), "--test"]) == 0


def build_slides(target_dir: str, output_dir: str = None, export_pdf: bool = False) -> bool:
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"❌ Error: Target directory '{target}' does not exist.")
        return False
    ensure_uv_dependencies()
    script = target / "scripts" / "build_slides.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "build_slides.py"

    print(f"🎨 Building Presentation Slides for '{target.name}'...")
    cmd = [str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if export_pdf:
        cmd.append("--export-pdf")

    return _run_python_script(cmd) == 0


def generate_all(
    name: str,
    topic: str,
    stack_str: str = None,
    target_dir: str = None,
    model_name: str = None,
    lang: str = None,
):
    if not stack_str:
        inferred = parse_natural_prompt(topic or name or "")
        inferred_list = inferred["stack"].split(",")
        if any(k in inferred_list for k in ["claude", "openai", "adk", "flutter", "android", "typescript", "go", "java", "kotlin"]):
            stack_str = inferred["stack"]
            if not model_name:
                model_name = inferred["model"]
        else:
            stack_str = "python,ollama,docker"
            if not model_name and inferred["model"] != MODEL_REGISTRY["google-gemini"]["default_workhorse"]:
                model_name = inferred["model"]

    print("=" * 70)
    print(f"⚡ [ONE-CLICK FULL ORCHESTRATOR - uv Powered] Building Workshop: '{name}'")
    print("=" * 70)

    ensure_uv_dependencies()

    # 1. Scaffolding Structure
    proj_dir = init_workshop(name, topic, target_dir, stack_str, model_name, lang=lang)

    # 2. Audit Cross-Architecture Compatibility
    print("\n[Step 2/9] Auditing Cross-Architecture Compatibility...")
    audit_compatibility(stack_str, str(proj_dir))

    # 3. Audit Model, SDK Currency & Typography (No Em Dash)
    print("\n[Step 3/9] Auditing 2026 Frontier Model, SDK Currency & Typography (No Em Dash)...")
    audit_models(str(proj_dir), fix=True)
    audit_typography(str(proj_dir), fix=True)

    # 4. Loop Engineering Multi-Persona Evaluation
    print("\n[Step 4/9] Running Loop Engineering 4-Persona Review...")
    audit_persona_loop(topic, str(proj_dir))

    # 5. Build PDF Handout & Previews
    print("\n[Step 5/9] Building Publication PDF Handouts & Previews...")
    if not build_pdf(str(proj_dir)):
        sys.exit(1)

    # 6. Export Open Codelabs Bundle & Manifest
    print("\n[Step 6/9] Exporting Open Codelabs Interactive Bundle & Manifest...")
    if not export_codelab(str(proj_dir)):
        sys.exit(1)

    # 7. Export Google Colab Notebooks (.ipynb) & Badges
    print("\n[Step 7/9] Exporting Google Colab Interactive Notebooks & Badges...")
    if not export_colab(str(proj_dir)):
        sys.exit(1)

    # 8. Build Presentation Slide Deck (Marp, PPTX & Web HTML)
    print("\n[Step 8/9] Building Presentation Slide Decks (Marp, PPTX & Web HTML)...")
    if not build_slides(str(proj_dir)):
        sys.exit(1)

    # 9. Final Integrity, Artifact, Link & Smoke Code Execution Gate
    print("\n[Step 9/9] Running Final Workshop Code, Bundle & Link Integrity Verification...")
    if not test_workshop(str(proj_dir)):
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f"🎉 SUCCESS! Complete Workshop Package '{proj_dir.name}' generated in ONE-CLICK via uv!")
    print(f"📁 Path: {proj_dir}")
    print("=" * 70)
    return proj_dir


def generate_from_prompt(
    prompt: str,
    target_dir: str = None,
    init_only: bool = False,
    name_override: str = None,
    stack_override: str = None,
    model_override: str = None,
) -> Path:
    """Zero-config natural language prompt entrypoint: infers name, topic, stack, lang, and 2026 model, then builds immediately."""
    parsed = parse_natural_prompt(prompt)
    final_name = name_override or parsed["name"]
    final_topic = parsed["topic"]
    final_stack = stack_override or parsed["stack"]
    final_model = model_override or parsed["model"]
    final_lang = parsed["lang"]

    print("=" * 70)
    print("🗣️  [NATURAL LANGUAGE PROMPT ROUTER] Resolved Workshop Spec:")
    print(f"   • Prompt : {prompt}")
    print(f"   • Name   : {final_name}")
    print(f"   • Topic  : {final_topic}")
    print(f"   • Stack  : {final_stack}")
    print(f"   • Model  : {final_model}")
    print(f"   • Lang   : {final_lang}")
    print("=" * 70)

    if init_only:
        return init_workshop(final_name, final_topic, target_dir, final_stack, final_model, lang=final_lang)
    return generate_all(final_name, final_topic, final_stack, target_dir, final_model, lang=final_lang)
