#!/usr/bin/env python3
"""
harness_cli.py - Workshop Harness Command Line Tool
BWAI 및 기술 워크숍 프로젝트 생성을 자동화하고 사전 준비물, 아키텍처 호환성, 커리큘럼, 런북, 하네스 검증, PDF 핸드아웃 생성을 총괄하는 CLI
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

HARNESS_ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = HARNESS_ROOT / "templates"

def init_workshop(name: str, topic: str, target_dir: str = None):
    project_dir = Path(target_dir) / name if target_dir else Path.cwd() / name
    print(f"🚀 Initializing new workshop project: '{name}' at {project_dir}")

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

    # 3. Copy PDF Generator
    pdf_templates = TEMPLATES_DIR / "pdf-templates"
    shutil.copy(pdf_templates / "generate_prep_pdf.py", project_dir / "scripts" / "generate_prep_pdf.py")

    # 4. Create .env.sample & .gitignore
    with open(project_dir / ".env.sample", "w", encoding="utf-8") as f:
        f.write("# Sample Environment Variables\nGEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")

    # 5. Create README.md
    readme_content = f"""# {name}

> Topic: {topic}

이 저장소는 **{topic}** 워크숍을 위한 사전 준비 문서와 핸즈온 실습 코드 저장소입니다.

## 🚀 빠른 시작

1. **사전 준비 가이드**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **노트북 아키텍처 호환성 점검**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **사전 환경 점검 스크립트 실행**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **당일 핸즈온**:
   - 실습 순서: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - 실습 코드: [workshop/01_starter](./workshop/01_starter)
   - 정답 코드: [workshop/02_final](./workshop/02_final)
5. **발표자 & TA 진행 런북**: [RUNBOOK.md](./RUNBOOK.md)

## 📂 저장소 구조

```text
.
├── RUNBOOK.md                    # 발표자 및 TA 전용 진행 런북
├── gemma4-local-setup-guide.md   # 통합 사전 준비 가이드
├── docs/                        # 상세 주제별 및 아키텍처 호환성 가이드 문서
│   └── 00-architecture-compatibility-matrix.md
├── workshop/                    # 당일 핸즈온 실습
│   ├── 01_starter/              # 시작 코드
│   ├── 02_final/                # 최종 참고 코드
│   └── 03_labs/                 # Step-by-Step 실습 문서
├── prompt-pack/                 # 핸즈온 프롬프트 팩
├── scripts/                     # 크로스 아키텍처 점검 및 오프라인 번들링 스크립트
└── output/                      # 산출물 (PDF 등)
```

## 🔗 참고 (References)
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
"""
    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 6. Starter main.py
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

def test_workshop(target_dir: str):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "verify_workshop.py"
    if not script.exists():
        script = TEMPLATES_DIR / "script-templates" / "verify_workshop.py"

    print(f"🔍 Running Workshop Integrity Audit on '{target}'...")
    os.system(f"python3 '{script}' '{target}'")

def build_pdf(target_dir: str):
    target = Path(target_dir).resolve()
    docs_dir = target / "docs"
    script = target / "scripts" / "generate_prep_pdf.py"
    output_pdf = target / "output" / "pdf" / f"{target.name}-prep-guide.pdf"
    preview_dir = target / "tmp" / "pdfs"

    if not script.exists():
        print(f"❌ Error: Script '{script}' not found.")
        return

    print(f"📄 Building PDF for {target.name}...")
    os.system(f"python3 '{script}' '{docs_dir}' '{output_pdf}' '{preview_dir}'")

def generate_all(name: str, topic: str, stack_str: str, target_dir: str = None):
    print("=" * 70)
    print(f"⚡ [ONE-CLICK FULL ORCHESTRATOR] Building Complete Workshop: '{name}'")
    print("=" * 70)

    # 1. Scaffolding Structure
    proj_dir = init_workshop(name, topic, target_dir)

    # 2. Audit Cross-Architecture Compatibility
    print("\n[Step 2/5] Auditing Cross-Architecture Compatibility...")
    audit_compatibility(stack_str)

    # 3. Test Integrity & Smoke Code Execution
    print("\n[Step 3/5] Testing Workshop Code & Link Integrity...")
    test_workshop(str(proj_dir))

    # 4. Build PDF Handout & Previews
    print("\n[Step 4/5] Building Publication PDF Handouts & Previews...")
    build_pdf(str(proj_dir))

    print("\n" + "=" * 70)
    print(f"🎉 SUCCESS! Complete Workshop Package '{name}' generated in ONE-CLICK!")
    print(f"📁 Path: {proj_dir}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Workshop Harness CLI")
    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new workshop project")
    init_parser.add_argument("--name", required=True, help="Workshop project name")
    init_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    init_parser.add_argument("--dir", default=None, help="Target parent directory")

    # generate-all (One-Click Full Orchestration)
    gen_all_parser = subparsers.add_parser("generate-all", help="One-Click full workshop generation across all 11 skills")
    gen_all_parser.add_argument("--name", required=True, help="Workshop project name")
    gen_all_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    gen_all_parser.add_argument("--stack", default="python,ollama,docker", help="Tech stack (comma-separated)")
    gen_all_parser.add_argument("--dir", default=None, help="Target parent directory")

    # audit-compat command
    audit_parser = subparsers.add_parser("audit-compat", help="Audit tech stack cross-architecture compatibility")
    audit_parser.add_argument("--stack", required=True, help="Comma-separated tech stack")

    # test command
    test_parser = subparsers.add_parser("test", help="Test workshop code execution & markdown link integrity")
    test_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # pdf command
    pdf_parser = subparsers.add_parser("build-pdf", help="Build PDF handout from docs")
    pdf_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    args = parser.parse_args()

    if args.command == "init":
        init_workshop(args.name, args.topic, args.dir)
    elif args.command == "generate-all":
        generate_all(args.name, args.topic, args.stack, args.dir)
    elif args.command == "audit-compat":
        audit_compatibility(args.stack)
    elif args.command == "test":
        test_workshop(args.target)
    elif args.command == "build-pdf":
        build_pdf(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
