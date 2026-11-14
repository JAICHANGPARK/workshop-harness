#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harness_cli.py - Workshop Harness Command Line Entrypoint (uv Powered)
Delegates to the modular `harness` package (`registry`, `router`, `scaffolder`, `auditors`, `exporters`)
while re-exporting all public APIs for seamless backward compatibility.
"""

import argparse
import sys

from harness import (
    AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS,
    DEPRECATED_MODEL_REPLACEMENTS,
    HARNESS_ROOT,
    MODEL_REGISTRY,
    TEMPLATES_DIR,
    __version__,
    _resolve_provider_config,
    audit_compatibility,
    audit_models,
    audit_persona_loop,
    audit_typography,
    build_pdf,
    build_slides,
    detect_prompt_language,
    ensure_uv_dependencies,
    export_codelab,
    export_colab,
    generate_all,
    generate_from_prompt,
    init_workshop,
    list_models,
    parse_natural_prompt,
    sanitize_no_em_dash,
    test_colab,
    test_workshop,
)


def main():
    known_commands = {
        "prompt", "from-prompt", "init", "generate-all", "list-models",
        "audit-models", "audit-typography", "audit-compat", "audit-loop",
        "test", "build-pdf", "export-codelab", "export-colab", "test-colab", "build-slides",
    }
    # Allow direct bare natural language invocation: `python3 harness_cli.py "Claude 최신 모델로 워크숍 만들어줘"`
    if len(sys.argv) > 1 and sys.argv[1] not in known_commands and not sys.argv[1].startswith("-"):
        raw_prompt = " ".join(sys.argv[1:]).strip()
        generate_from_prompt(raw_prompt)
        return

    parser = argparse.ArgumentParser(description=f"Workshop Harness CLI v{__version__} (uv Powered)")
    subparsers = parser.add_subparsers(dest="command")

    # prompt / from-prompt command (Zero-Config Natural Language One-Shot Generator)
    prompt_parser = subparsers.add_parser(
        "prompt",
        aliases=["from-prompt"],
        help="Instantly generate a complete workshop directly from a natural language prompt (KO/EN/JA/ZH)",
    )
    prompt_parser.add_argument("prompt_text", nargs="+", help="Natural language prompt describing the workshop")
    prompt_parser.add_argument("--dir", "--target", dest="dir", default=None, help="Target parent directory")
    prompt_parser.add_argument("--name", default=None, help="Optional project slug override")
    prompt_parser.add_argument("--stack", default=None, help="Optional comma-separated stack override")
    prompt_parser.add_argument("--model", default=None, help="Optional AI model override")
    prompt_parser.add_argument("--init-only", action="store_true", help="Only scaffold repository without PDF/Colab/Slides build")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new workshop project")
    init_parser.add_argument("--name", default=None, help="Workshop project name (auto-inferred if --prompt is given)")
    init_parser.add_argument("--prompt", default=None, help="Natural language prompt to auto-infer name, topic, stack, and model")
    init_parser.add_argument("--topic", default=None, help="Workshop topic")
    init_parser.add_argument("--stack", default=None, help="Tech stack (comma-separated, e.g. python, claude, openai, adk, typescript, go)")
    init_parser.add_argument("--model", default=None, help="Primary AI model tag (e.g. gemini-4-hydrogen, claude-sonnet-5-5, claude-fable-5-2, gpt-6.1-sol)")
    init_parser.add_argument("--lang", default=None, help="Documentation language override (en, ko, ja, zh)")
    init_parser.add_argument("--dir", "--target", dest="dir", default=None, help="Target parent directory")

    # generate-all (One-Click Full Orchestration)
    gen_all_parser = subparsers.add_parser("generate-all", help="One-Click full workshop generation across all skills")
    gen_all_parser.add_argument("--name", default=None, help="Workshop project name (auto-inferred if --prompt is given)")
    gen_all_parser.add_argument("--prompt", default=None, help="Natural language prompt to auto-infer name, topic, stack, and model")
    gen_all_parser.add_argument("--topic", default=None, help="Workshop topic")
    gen_all_parser.add_argument("--stack", default=None, help="Tech stack (comma-separated, e.g. python, claude, openai, ollama)")
    gen_all_parser.add_argument("--model", default=None, help="Primary AI model tag (e.g. gemini-4-hydrogen, claude-sonnet-5-5, gpt-6.1-sol)")
    gen_all_parser.add_argument("--lang", default=None, help="Documentation language override (en, ko, ja, zh)")
    gen_all_parser.add_argument("--dir", "--target", dest="dir", default=None, help="Target parent directory")

    # list-models command
    models_parser = subparsers.add_parser("list-models", help="Display verified 2026 Frontier & Open-Weight Model Catalog")
    models_parser.add_argument("--provider", default=None, help="Filter by provider (e.g. gemini, gemma, claude, openai, ollama)")

    # audit-models command
    audit_models_parser = subparsers.add_parser("audit-models", help="Audit and auto-upgrade deprecated model tags and legacy SDK imports")
    audit_models_parser.add_argument("--target", default=".", help="Path to workshop or harness directory")
    audit_models_parser.add_argument("--fix", action="store_true", help="Automatically replace deprecated model tags with 2026 equivalents")

    # audit-typography command
    audit_typo_parser = subparsers.add_parser("audit-typography", help="Audit and auto-remove forbidden em dashes (\\u2014) in markdown and documentation files")
    audit_typo_parser.add_argument("--target", default=".", help="Path to workshop or harness directory")
    audit_typo_parser.add_argument("--fix", action="store_true", help="Automatically replace em dashes with standard hyphens ('-')")

    # audit-compat command
    audit_parser = subparsers.add_parser("audit-compat", help="Audit tech stack cross-architecture compatibility")
    audit_parser.add_argument("--stack", required=True, help="Comma-separated tech stack")
    audit_parser.add_argument("--target", default=None, help="Optional workshop directory")

    # audit-loop command
    loop_parser = subparsers.add_parser("audit-loop", help="Loop Engineering 4-persona audit for non-coder, novice, intermediate, and senior attendees")
    loop_parser.add_argument("--topic", required=True, help="Workshop topic")
    loop_parser.add_argument("--target", default=None, help="Optional workshop directory to inspect and write report")

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

    if args.command in ("prompt", "from-prompt"):
        raw_prompt = " ".join(args.prompt_text).strip()
        generate_from_prompt(
            raw_prompt,
            target_dir=args.dir,
            init_only=args.init_only,
            name_override=args.name,
            stack_override=args.stack,
            model_override=args.model,
        )
    elif args.command == "init":
        if args.prompt:
            generate_from_prompt(
                args.prompt,
                target_dir=args.dir,
                init_only=True,
                name_override=args.name,
                stack_override=args.stack,
                model_override=args.model,
            )
        else:
            if not args.name and args.topic:
                parsed = parse_natural_prompt(args.topic)
                args.name = parsed["name"]
                args.stack = args.stack or parsed["stack"]
                args.model = args.model or parsed["model"]
                args.lang = args.lang or parsed["lang"]
            elif not args.name:
                init_parser.error("one of --name, --prompt, or --topic is required")
            init_workshop(args.name, args.topic or "BWAI Hands-on Workshop", args.dir, args.stack or "python", args.model, lang=args.lang)
    elif args.command == "generate-all":
        if args.prompt:
            generate_from_prompt(
                args.prompt,
                target_dir=args.dir,
                init_only=False,
                name_override=args.name,
                stack_override=args.stack,
                model_override=args.model,
            )
        else:
            if not args.name and args.topic:
                parsed = parse_natural_prompt(args.topic)
                args.name = parsed["name"]
                args.stack = args.stack or parsed["stack"]
                args.model = args.model or parsed["model"]
                args.lang = args.lang or parsed["lang"]
            elif not args.name:
                gen_all_parser.error("one of --name, --prompt, or --topic is required")
            generate_all(args.name, args.topic or "BWAI Hands-on Workshop", args.stack, args.dir, args.model, lang=args.lang)
    elif args.command == "list-models":
        list_models(args.provider)
    elif args.command == "audit-models":
        if not audit_models(args.target, args.fix):
            sys.exit(1)
    elif args.command == "audit-typography":
        if not audit_typography(args.target, args.fix):
            sys.exit(1)
    elif args.command == "audit-compat":
        audit_compatibility(args.stack, args.target)
    elif args.command == "audit-loop":
        audit_persona_loop(args.topic, args.target)
    elif args.command == "test":
        if not test_workshop(args.target):
            sys.exit(1)
    elif args.command == "build-pdf":
        if not build_pdf(args.target):
            sys.exit(1)
    elif args.command == "export-codelab":
        if not export_codelab(args.target, args.output, args.push):
            sys.exit(1)
    elif args.command == "export-colab":
        if not export_colab(args.target, args.output, args.repo, args.test):
            sys.exit(1)
    elif args.command == "test-colab":
        if not test_colab(args.target):
            sys.exit(1)
    elif args.command == "build-slides":
        if not build_slides(args.target, args.output, args.export_pdf):
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
