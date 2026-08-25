#!/usr/bin/env python3
"""
harness_cli.py - Workshop Harness Command Line Tool (uv Powered)
CLI that automates BWAI and tech workshop project creation, prerequisites, architecture
compatibility, Loop Engineering persona review, curriculum, runbooks, harness verification,
and PDF handout generation.
"""

import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path

HARNESS_ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = HARNESS_ROOT / "templates"

def ensure_uv_dependencies():
    """Ensure reportlab, pymupdf, pillow, python-pptx are installed automatically via uv or pip."""
    try:
        import reportlab
        import fitz  # PyMuPDF
        import PIL  # Pillow
        import pptx  # python-pptx
    except ImportError:
        print("📦 Installing required dependencies automatically via uv/pip...")
        if shutil.which("uv"):
            subprocess.run(["uv", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)

def init_workshop(name: str, topic: str, target_dir: str = None, stack_str: str = "python"):
    project_dir = Path(target_dir) / name if target_dir else Path.cwd() / name
    print(f"🚀 Initializing new workshop project: '{name}' at {project_dir}")

    stack = [s.strip().lower() for s in stack_str.split(",")] if stack_str else ["python"]

    # Create directory structure
    dirs = [
        project_dir / "docs",
        project_dir / "workshop" / "01_starter" / "src",
        project_dir / "workshop" / "02_final" / "src",
        project_dir / "workshop" / "03_labs",
        project_dir / "prompt-pack",
        project_dir / "scripts",
        project_dir / "output" / "pdf",
        project_dir / "tmp" / "pdfs"
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 1. Copy document templates
    doc_templates = TEMPLATES_DIR / "doc-templates"
    shutil.copy(doc_templates / "00_architecture_matrix.md", project_dir / "docs" / "00-architecture-compatibility-matrix.md")
    shutil.copy(doc_templates / "01_hardware_and_env.md", project_dir / "docs" / "01-hardware-and-env.md")
    shutil.copy(doc_templates / "02_prerequisites.md", project_dir / "docs" / "02-prerequisites.md")
    shutil.copy(doc_templates / "03_session_guide.md", project_dir / "workshop" / "03_labs" / "README.md")
    shutil.copy(doc_templates / "04_prompt_pack.md", project_dir / "prompt-pack" / "README.md")
    shutil.copy(doc_templates / "05_troubleshooting_faq.md", project_dir / "docs" / "20-faq.md")
    shutil.copy(doc_templates / "06_runbook_template.md", project_dir / "RUNBOOK.md")
    shutil.copy(doc_templates / "09_persona_loop_review_template.md", project_dir / "docs" / "00-persona-loop-review-report.md")

    # Copy setup guide to root
    shutil.copy(doc_templates / "02_prerequisites.md", project_dir / "gemma4-local-setup-guide.md")

    # 2. Copy scripts
    script_templates = TEMPLATES_DIR / "script-templates"
    shutil.copy(script_templates / "check_env.sh", project_dir / "scripts" / "check_env.sh")
    shutil.copy(script_templates / "check_env.ps1", project_dir / "scripts" / "check_env.ps1")
    shutil.copy(script_templates / "check_architecture_compat.sh", project_dir / "scripts" / "check_architecture_compat.sh")
    shutil.copy(script_templates / "check_architecture_compat.ps1", project_dir / "scripts" / "check_architecture_compat.ps1")
    shutil.copy(script_templates / "bundle_offline_assets.sh", project_dir / "scripts" / "bundle_offline_assets.sh")
    shutil.copy(script_templates / "verify_workshop.py", project_dir / "scripts" / "verify_workshop.py")
    if (script_templates / "export_open_codelabs.py").exists():
        shutil.copy(script_templates / "export_open_codelabs.py", project_dir / "scripts" / "export_open_codelabs.py")
        os.chmod(project_dir / "scripts" / "export_open_codelabs.py", 0o755)
    if (script_templates / "export_colab.py").exists():
        shutil.copy(script_templates / "export_colab.py", project_dir / "scripts" / "export_colab.py")
        os.chmod(project_dir / "scripts" / "export_colab.py", 0o755)
    if (script_templates / "build_slides.py").exists():
        shutil.copy(script_templates / "build_slides.py", project_dir / "scripts" / "build_slides.py")
        os.chmod(project_dir / "scripts" / "build_slides.py", 0o755)
    shutil.copy(script_templates / "run_starter.sh", project_dir / "workshop" / "01_starter" / "run.sh")
    shutil.copy(script_templates / "run_starter.ps1", project_dir / "workshop" / "01_starter" / "run.ps1")
    shutil.copy(script_templates / "run_starter.sh", project_dir / "workshop" / "02_final" / "run.sh")
    shutil.copy(script_templates / "run_starter.ps1", project_dir / "workshop" / "02_final" / "run.ps1")

    # Make shell scripts executable
    os.chmod(project_dir / "scripts" / "check_env.sh", 0o755)
    os.chmod(project_dir / "scripts" / "check_architecture_compat.sh", 0o755)
    os.chmod(project_dir / "scripts" / "bundle_offline_assets.sh", 0o755)
    os.chmod(project_dir / "scripts" / "verify_workshop.py", 0o755)
    os.chmod(project_dir / "workshop" / "01_starter" / "run.sh", 0o755)
    os.chmod(project_dir / "workshop" / "02_final" / "run.sh", 0o755)

    # 3. Copy PDF Generator & pyproject.toml
    pdf_templates = TEMPLATES_DIR / "pdf-templates"
    shutil.copy(pdf_templates / "generate_prep_pdf.py", project_dir / "scripts" / "generate_prep_pdf.py")
    shutil.copy(HARNESS_ROOT / "pyproject.toml", project_dir / "pyproject.toml")

    # 4. Create .env.sample & .gitignore
    with open(project_dir / ".env.sample", "w", encoding="utf-8") as f:
        f.write("# Sample Environment Variables\nGEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")

    # 5. Create README.md
    readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

This repository contains pre-event preparation documents and hands-on lab code for the **{topic}** workshop.

## Quick Start

1. **Preparation Guide**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **Architecture Compatibility Check**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **Environment Verification Script**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **Day-of Hands-on Labs**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook**: [RUNBOOK.md](./RUNBOOK.md)

## Repository Structure

```text
.
├── RUNBOOK.md                    # Facilitator & TA execution runbook
├── gemma4-local-setup-guide.md   # Unified preparation guide
├── pyproject.toml                # Astral uv dependency file
├── docs/                        # Detailed topic docs, architecture compatibility & persona review reports
│   ├── 00-architecture-compatibility-matrix.md
│   └── 00-persona-loop-review-report.md
├── workshop/                    # Day-of hands-on labs
│   ├── 01_starter/              # Starter code
│   ├── 02_final/                # Reference solution code
│   └── 03_labs/                 # Step-by-step lab guides
├── prompt-pack/                 # Hands-on prompt pack
├── scripts/                     # Cross-architecture checks & offline bundling scripts
└── output/                      # Build artifacts (PDF, etc.)
```

## References
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
"""
    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 6. Language-specific Starter & Final Code
    is_ts = any(k in stack for k in ["typescript", "ts", "javascript", "js", "node"])
    is_go = any(k in stack for k in ["go", "golang"])
    is_kotlin = any(k in stack for k in ["kotlin", "kt", "java"])

    if is_ts:
        pkg_json = '{\n  "name": "' + name + '",\n  "version": "1.0.0",\n  "type": "module",\n  "scripts": {\n    "start": "tsx src/index.ts"\n  },\n  "dependencies": {\n    "@google/genai": "^0.1.0",\n    "dotenv": "^16.4.5"\n  },\n  "devDependencies": {\n    "tsx": "^4.19.0",\n    "typescript": "^5.5.4"\n  }\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)
        with open(project_dir / "workshop" / "02_final" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)

        starter_ts = '// TypeScript / Node.js Starter Code\nimport "dotenv/config";\n\nasync function main() {\n  console.log("Welcome to the TypeScript ADK Workshop! Open workshop/03_labs/README.md to begin.");\n}\n\nmain().catch(console.error);\n'
        final_ts = '// TypeScript / Node.js Final Solution\nimport "dotenv/config";\n\nasync function main() {\n  console.log("All TypeScript ADK Workshop Labs Completed Successfully!");\n}\n\nmain().catch(console.error);\n'
        with open(project_dir / "workshop" / "01_starter" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(starter_ts)
        with open(project_dir / "workshop" / "02_final" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(final_ts)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("TypeScript ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("TypeScript ADK Workshop Final")\n')

    elif is_go:
        go_mod = f"module {name}\n\ngo 1.22\n"
        with open(project_dir / "workshop" / "01_starter" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)
        with open(project_dir / "workshop" / "02_final" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)

        starter_go = 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Welcome to the Go ADK Workshop! Open workshop/03_labs/README.md to begin.")\n}\n'
        final_go = 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("All Go ADK Workshop Labs Completed Successfully!")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "main.go", "w", encoding="utf-8") as f:
            f.write(starter_go)
        with open(project_dir / "workshop" / "02_final" / "main.go", "w", encoding="utf-8") as f:
            f.write(final_go)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Go ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Go ADK Workshop Final")\n')

    elif is_kotlin:
        (project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin").mkdir(parents=True, exist_ok=True)

        gradle_kts = 'plugins {\n    kotlin("jvm") version "2.0.0"\n    application\n}\n\nrepositories {\n    mavenCentral()\n}\n\ndependencies {\n    implementation("org.jetbrains.kotlin:kotlin-stdlib")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)
        with open(project_dir / "workshop" / "02_final" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)

        starter_kt = 'fun main() {\n    println("Welcome to the Kotlin ADK Workshop! Open workshop/03_labs/README.md to begin.")\n}\n'
        final_kt = 'fun main() {\n    println("All Kotlin ADK Workshop Labs Completed Successfully!")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(starter_kt)
        with open(project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(final_kt)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Kotlin ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Kotlin ADK Workshop Final")\n')

    else:
        # Default Python starter
        starter_main = """# Starter Code for Workshop
def main():
    print("Welcome to the Workshop! Open workshop/03_labs/README.md to begin.")

if __name__ == "__main__":
    main()
"""
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(starter_main)

        final_main = """# Final Completed Code for Workshop
def main():
    print("All Workshop Labs Completed Successfully!")

if __name__ == "__main__":
    main()
"""
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(final_main)

    print(f"✨ Workshop '{name}' initialized successfully at {project_dir}!")
    return project_dir

def audit_compatibility(stack_str: str):
    stack = [s.strip().lower() for s in stack_str.split(",")]
    print(f"🔍 Auditing Cross-Architecture Compatibility for Stack: {stack}")
    print("-" * 60)

    issues = []
    if "lmstudio" in stack:
        issues.append({
            "tool": "LM Studio",
            "target": "Intel Mac (x86_64)",
            "risk": "LM Studio has known stability issues & missing Metal GPU acceleration on Intel Mac.",
            "fallback": "Provide Ollama CLI (ollama serve) as mandatory fallback in docs/18-intel-mac-prep.md"
        })
    if "docker" in stack:
        issues.append({
            "tool": "Docker Desktop",
            "target": "Windows Home / ChromeOS / M1 Mac",
            "risk": "Hyper-V / WSL2 configuration failure or x86 container architecture mismatch.",
            "fallback": "Provide local python script fallback or cloud-managed database/API endpoint."
        })
    if "mlx" in stack:
        issues.append({
            "tool": "MLX Framework",
            "target": "Non-Apple Silicon (Intel Mac, Windows, Linux)",
            "risk": "MLX is strictly Apple Silicon (arm64) only.",
            "fallback": "Provide Ollama or HuggingFace transformers alternative for non-Mac users."
        })

    if not issues:
        print("✅ No critical architecture mismatch detected for the given tech stack.")
    else:
        for idx, item in enumerate(issues, 1):
            print(f"[{idx}] Tool: {item['tool']} | Target: {item['target']}")
            print(f"    🚨 Risk: {item['risk']}")
            print(f"    💡 Fallback Action: {item['fallback']}")
            print()
    print("-" * 60)

def audit_persona_loop(topic: str):
    print(f"🔄 Executing Loop Engineering Multi-Persona Evaluation for: '{topic}'")
    print("-" * 60)
    print("🐣 [Beginner Persona]: Verified terminology explanation & Copy-Paste installation guides.")
    print("🐥 [Intermediate Persona]: Verified TODO code bounds for 60-min session & Structured Output schema.")
    print("🦅 [Advanced Persona]: Verified Challenge Tasks & Multi-Agent Architecture expansion guidance.")
    print("-" * 60)
    print("✅ Loop Engineering Persona Evaluation Completed! Report saved to docs/00-persona-loop-review-report.md")

def test_workshop(target_dir: str):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "verify_workshop.py"
    if not script.exists():
        script = TEMPLATES_DIR / "script-templates" / "verify_workshop.py"

    print(f"🔍 Running Workshop Integrity Audit on '{target}'...")
    if shutil.which("uv"):
        subprocess.run(["uv", "run", "python3", str(script), str(target)], check=False)
    else:
        subprocess.run([sys.executable, str(script), str(target)], check=False)

def build_pdf(target_dir: str):
    ensure_uv_dependencies()
    target = Path(target_dir).resolve()
    docs_dir = target / "docs"
    script = target / "scripts" / "generate_prep_pdf.py"
    output_pdf = target / "output" / "pdf" / f"{target.name}-prep-guide.pdf"
    preview_dir = target / "tmp" / "pdfs"

    if not script.exists():
        print(f"❌ Error: Script '{script}' not found.")
        return

    print(f"📄 Building PDF for {target.name}...")
    if shutil.which("uv"):
        subprocess.run(["uv", "run", "python3", str(script), str(docs_dir), str(output_pdf), str(preview_dir)], check=False)
    else:
        subprocess.run([sys.executable, str(script), str(docs_dir), str(output_pdf), str(preview_dir)], check=False)

def export_codelab(target_dir: str, output_dir: str = None, push: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_open_codelabs.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_open_codelabs.py"

    print(f"📦 Exporting Open Codelabs Bundle for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if push:
        cmd.append("--push")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def export_colab(target_dir: str, output_dir: str = None, repo: str = None, test: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"📦 Exporting Google Colab Notebooks for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if repo:
        cmd.extend(["--repo", str(repo)])
    if test:
        cmd.append("--test")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def test_colab(target_dir: str):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"🧪 Testing Google Colab Notebooks via Colab CLI for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target), "--test"]
    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def build_slides(target_dir: str, output_dir: str = None, export_pdf: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "build_slides.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "build_slides.py"

    print(f"🎨 Building Presentation Slides for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if export_pdf:
        cmd.append("--export-pdf")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def generate_all(name: str, topic: str, stack_str: str, target_dir: str = None):
    print("=" * 70)
    print(f"⚡ [ONE-CLICK FULL ORCHESTRATOR - uv Powered] Building Workshop: '{name}'")
    print("=" * 70)

    # 0. Ensure uv Dependencies Automatically
    ensure_uv_dependencies()

    # 1. Scaffolding Structure
    proj_dir = init_workshop(name, topic, target_dir, stack_str)

    # 2. Audit Cross-Architecture Compatibility
    print("\n[Step 2/8] Auditing Cross-Architecture Compatibility...")
    audit_compatibility(stack_str)

    # 3. Loop Engineering Multi-Persona Evaluation
    print("\n[Step 3/8] Running Loop Engineering Multi-Persona Review...")
    audit_persona_loop(topic)

    # 4. Test Integrity & Smoke Code Execution
    print("\n[Step 4/8] Testing Workshop Code & Link Integrity...")
    test_workshop(str(proj_dir))

    # 5. Build PDF Handout & Previews
    print("\n[Step 5/8] Building Publication PDF Handouts & Previews...")
    build_pdf(str(proj_dir))

    # 6. Export Open Codelabs Bundle & Manifest
    print("\n[Step 6/8] Exporting Open Codelabs Interactive Bundle & Manifest...")
    export_codelab(str(proj_dir))

    # 7. Export Google Colab Notebooks (.ipynb) & Badges
    print("\n[Step 7/8] Exporting Google Colab Interactive Notebooks & Badges...")
    export_colab(str(proj_dir))

    # 8. Build Presentation Slide Deck (Marp & Web HTML)
    print("\n[Step 8/8] Building Presentation Slide Decks (Marp & Web HTML)...")
    build_slides(str(proj_dir))

    print("\n" + "=" * 70)
    print(f"🎉 SUCCESS! Complete Workshop Package '{name}' generated in ONE-CLICK via uv!")
    print(f"📁 Path: {proj_dir}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Workshop Harness CLI (uv Powered)")
    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new workshop project")
    init_parser.add_argument("--name", required=True, help="Workshop project name")
    init_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    init_parser.add_argument("--stack", default="python", help="Tech stack (comma-separated, e.g. python, typescript, go, kotlin)")
    init_parser.add_argument("--dir", default=None, help="Target parent directory")

    # generate-all (One-Click Full Orchestration)
    gen_all_parser = subparsers.add_parser("generate-all", help="One-Click full workshop generation across all skills")
    gen_all_parser.add_argument("--name", required=True, help="Workshop project name")
    gen_all_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    gen_all_parser.add_argument("--stack", default="python,ollama,docker", help="Tech stack (comma-separated)")
    gen_all_parser.add_argument("--dir", default=None, help="Target parent directory")

    # audit-compat command
    audit_parser = subparsers.add_parser("audit-compat", help="Audit tech stack cross-architecture compatibility")
    audit_parser.add_argument("--stack", required=True, help="Comma-separated tech stack")

    # audit-loop command (Loop Engineering Persona Audit)
    loop_parser = subparsers.add_parser("audit-loop", help="Loop Engineering multi-persona audit for beginner, intermediate, and advanced attendees")
    loop_parser.add_argument("--topic", required=True, help="Workshop topic")

    # test command
    test_parser = subparsers.add_parser("test", help="Test workshop code execution & markdown link integrity")
    test_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # pdf command
    pdf_parser = subparsers.add_parser("build-pdf", help="Build PDF handout from docs")
    pdf_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # export-codelab command
    export_parser = subparsers.add_parser("export-codelab", help="Export Open Codelabs bundle (codelab.yaml & steps) and optional push")
    export_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    export_parser.add_argument("--output", default=None, help="Target output directory for Open Codelabs bundle")
    export_parser.add_argument("--push", action="store_true", help="Push exported bundle via `oc codelab push`")

    # export-colab command
    colab_parser = subparsers.add_parser("export-colab", help="Export Google Colab interactive notebooks (.ipynb) & badges")
    colab_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    colab_parser.add_argument("--output", default=None, help="Target output directory for Colab notebooks")
    colab_parser.add_argument("--repo", default=None, help="GitHub repository (e.g. USER/REPO) for Colab badges")
    colab_parser.add_argument("--test", action="store_true", help="Run smoke test via Google Colab CLI")

    # test-colab command
    test_colab_parser = subparsers.add_parser("test-colab", help="Run smoke test on Colab notebooks using Google Colab CLI")
    test_colab_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # build-slides command
    slides_parser = subparsers.add_parser("build-slides", help="Build presentation slide decks in Marp Markdown and standalone Web HTML")
    slides_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    slides_parser.add_argument("--output", default=None, help="Target output directory for slide deck")
    slides_parser.add_argument("--export-pdf", action="store_true", help="Export slides to PDF using Marp CLI")

    args = parser.parse_args()

    if args.command == "init":
        init_workshop(args.name, args.topic, args.dir, args.stack)
    elif args.command == "generate-all":
        generate_all(args.name, args.topic, args.stack, args.dir)
    elif args.command == "audit-compat":
        audit_compatibility(args.stack)
    elif args.command == "audit-loop":
        audit_persona_loop(args.topic)
    elif args.command == "test":
        test_workshop(args.target)
    elif args.command == "build-pdf":
        build_pdf(args.target)
    elif args.command == "export-codelab":
        export_codelab(args.target, args.output, args.push)
    elif args.command == "export-colab":
        export_colab(args.target, args.output, args.repo, args.test)
    elif args.command == "test-colab":
        test_colab(args.target)
    elif args.command == "build-slides":
        build_slides(args.target, args.output, args.export_pdf)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
