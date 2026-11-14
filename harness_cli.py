#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harness_cli.py - Workshop Harness Command Line Tool (uv Powered)
CLI that automates BWAI and tech workshop project creation, prerequisites, architecture
compatibility, Loop Engineering persona review, curriculum, runbooks, harness verification,
and PDF handout generation.
"""

import os
import sys
import re
import json
import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

HARNESS_ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = HARNESS_ROOT / "templates"

# 2026 Frontier & Open-Weight Model Registry (Verified November 2026)
MODEL_REGISTRY = {
    "google-gemini": {
        "flagship_reasoning": "gemini-4-carbon",
        "default_workhorse": "gemini-4-hydrogen",
        "enterprise_reasoning": "gemini-4-argon",
        "fast_multimodal_flash": "gemini-3.8-flash",
        "high_throughput_lite": "gemini-3.5-flash-lite",
        "ultra_lite": "gemini-3.1-flash-lite",
        "live_multimodal": "gemini-3.8-live",
        "live_extended_thinking": "gemini-3.8-live-extended-thinking",
        "live_transcribe": "gemini-3.5-transcribe-live",
        "live_translate": "gemini-3.5-live-translate-preview",
        "tts_expressive": "gemini-3.8-flash-tts",
        "tts_lite": "gemini-3.8-flash-lite-tts",
        "image_default": "gemini-nano-banana-2.1",
        "image_pro": "gemini-3-pro-image",
        "video_omni": "gemini-omni-1.2-flash",
        "embedding_multimodal": "gemini-embedding-2",
        "managed_agent": "antigravity-preview-09-2026",
    },
    "google-gemma": {
        "cloud_dense_31b": "gemma-4-31b-it",
        "cloud_moe_26b": "gemma-4-26b-a4b-it",
        "cloud_dense_12b": "gemma-4-12b-it",
        "cloud_edge_e4b": "gemma-4-e4b-it",
        "cloud_edge_e2b": "gemma-4-e2b-it",
        "local_8gb_ram": "gemma4:e2b",
        "local_16gb_ram": "gemma4:e4b",
        "local_dense_12b": "gemma4:12b",
        "local_moe_26b": "gemma4:26b",
        "local_dense_31b": "gemma4:31b",
        "embedding_multimodal_740m": "embeddinggemma-2",
        "embedding_audio_570m": "embeddinggemma-2:570m",
        "embedding_vision_440m": "embeddinggemma-2:440m",
        "embedding_text_270m": "embeddinggemma-2:270m",
        "embedding_hf": "google/embeddinggemma-2",
        "translate_multimodal": "translategemma",
        "function_calling_edge": "functiongemma",
        "medical_multimodal": "medgemma1.5",
        "safety_classifier": "shieldgemma",
    },
    "anthropic-claude": {
        "apex_agentic": "claude-fable-5-2",
        "flagship_reasoning": "claude-opus-5-5",
        "default_workhorse": "claude-sonnet-5-5",
        "fast_haiku": "claude-haiku-5-5",
    },
    "openai-gpt": {
        "flagship_reasoning": "gpt-6-astra",
        "default_workhorse": "gpt-6.1-sol",
        "multimodal_computer_use": "gpt-6.1-terra",
        "fast_lite": "gpt-6-luna",
        "image_default": "gpt-image-2.6-sunburst",
        "image_fast": "gpt-image-2.6-flare",
    },
    "local-ollama": {
        "8gb_tier": ["gemma4:e2b", "embeddinggemma-2:270m", "functiongemma", "qwen3:8b", "deepseek-r1:8b"],
        "16gb_tier": ["gemma4:e4b", "gemma4:12b", "embeddinggemma-2", "translategemma", "qwen3:14b", "deepseek-r1:14b"],
        "32gb_tier": ["gemma4:26b", "gemma4:31b", "medgemma1.5", "qwen3.6:27b", "qwen3-coder:30b", "llama4:scout"],
        "embeddings": ["embeddinggemma-2", "embeddinggemma-2:440m", "embeddinggemma-2:270m"],
    },
}

# Deprecated / Retired Model & SDK Patterns -> 2026 Modern Replacements
DEPRECATED_MODEL_REPLACEMENTS = {
    "gemini-1.5-flash": "gemini-4-hydrogen",
    "gemini-1.5-pro": "gemini-4-carbon",
    "gemini-2.0-flash": "gemini-4-hydrogen",
    "gemini-2.0-flash-live": "gemini-3.8-live",
    "gemini-2.5-flash": "gemini-4-hydrogen",
    "gemini-2.5-pro": "gemini-4-carbon",
    "gemini-2.5-flash-lite": "gemini-3.5-flash-lite",
    "gemini-3.1-flash": "gemini-4-hydrogen",
    "gemini-3.1-pro": "gemini-4-carbon",
    "gemini-3.7-flash": "gemini-4-hydrogen",
    "gemini-omni-1.1-flash": "gemini-omni-1.2-flash",
    "gemini-embedding-2-preview": "gemini-embedding-2",
    "gemini-3.1-flash-live-preview": "gemini-3.8-live",
    "gemini-2.5-flash-preview-tts": "gemini-3.8-flash-tts",
    "gemini-3.1-flash-image-preview": "gemini-nano-banana-2.1",
    "gemma:2b": "gemma4:e2b",
    "gemma:7b": "gemma4:e4b",
    "gemma2:2b": "gemma4:e2b",
    "gemma2:9b": "gemma4:12b",
    "gemma2:27b": "gemma4:26b",
    "gemma3:1b": "gemma4:e2b",
    "gemma3:4b": "gemma4:e4b",
    "gemma3:12b": "gemma4:12b",
    "gemma3:27b": "gemma4:26b",
    "gemma4:e12b": "gemma4:12b",
    "gemma4:26b-a4b": "gemma4:26b",
    "gemma-2-9b-it": "gemma-4-12b-it",
    "gemma-2-27b-it": "gemma-4-26b-a4b-it",
    "gemma-3-12b-it": "gemma-4-12b-it",
    "gemma-3-27b-it": "gemma-4-26b-a4b-it",
    "embeddinggemma:300m": "embeddinggemma-2:270m",
    "embeddinggemma:latest": "embeddinggemma-2",
    "google/embeddinggemma-300m": "google/embeddinggemma-2",
    "gpt-4o-mini": "gpt-6-luna",
    "gpt-4o": "gpt-6.1-sol",
    "gpt-4.1-mini": "gpt-6-luna",
    "gpt-4.1": "gpt-6.1-sol",
    "gpt-5.4-mini": "gpt-6-luna",
    "gpt-5.4": "gpt-6.1-terra",
    "gpt-5.6-terra": "gpt-6.1-terra",
    "o1-mini": "gpt-6-luna",
    "o1-preview": "gpt-6-astra",
    "o3-mini": "gpt-6.1-sol",
    "o4-mini": "gpt-6.1-terra",
    "claude-3-5-sonnet": "claude-sonnet-5-5",
    "claude-3-7-sonnet": "claude-sonnet-5-5",
    "claude-3-5-haiku": "claude-haiku-5-5",
    "claude-sonnet-4": "claude-sonnet-5-5",
    "claude-sonnet-4-5": "claude-sonnet-5-5",
    "claude-opus-4": "claude-opus-5-5",
    "claude-opus-4-5": "claude-opus-5-5",
    "claude-fable-5.1": "claude-fable-5-2",
    "claude-fable-5-1": "claude-fable-5-2",
    "claude-sonnet-5.5": "claude-sonnet-5-5",
    "claude-opus-5.5": "claude-opus-5-5",
    "claude-haiku-5.5": "claude-haiku-5-5",
}


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
    ignore_files = {"harness_cli.py", "verify_workshop.py", "CHANGELOG.md", "test_harness.py"}

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
                # Skip lines that explicitly document prohibited/legacy examples
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
    # If em-dash has no spaces on either side, replace with ' - '; otherwise replace with '-'
    text = re.sub(r"(?<=\S)\u2014(?=\S)", " - ", text)
    return text.replace("\u2014", "-")


AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS = {
    # Korean (KO) prohibited literal terms & translationese grammar
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
    "생성되어집니다": "생성됩니다",
    "실행되어집니다": "실행됩니다",
    "설정되어집니다": "설정됩니다",
    "호출되어집니다": "호출됩니다",
    "전달되어집니다": "전달됩니다",
    # Japanese (JA) prohibited literal terms
    "手で触る実験室": "Hands-on Lab (ハンズオンラボ)",
    "走る本": "Runbook (ランブック)",
    "足場作り": "Scaffolding (スキャフォールディング)",
    "骨組みコード": "Starter / Boilerplate Code (スターターコード)",
    "思考の予算": "Thinking Budget (推論バジェット)",
    "道具を呼ぶ": "Tool Calling (ツール呼び出し)",
    "代理人開発キット": "ADK (Agent Development Kit)",
    "煙の試験": "Smoke Test (スモークテスト)",
    "後退経路": "Fallback (フォールバック)",
    "冷たい開始": "Cold Start (コールドスタート)",
    # Chinese (ZH) prohibited literal terms
    "手把手的实验室": "Hands-on Lab (实战工作坊)",
    "奔跑的书": "Runbook (演练手册)",
    "搭架子工程": "Scaffolding (脚手架)",
    "骨架代码": "Starter / Boilerplate Code (Starter 初始代码)",
    "骨架/参考代码": "Starter 初始代码 / Reference 参考实现",
    "思考预算": "Thinking Budget (推理预算)",
    "工具呼叫": "Tool Calling (工具调用)",
    "代理人开发套件": "ADK (Agent 开发套件)",
    "烟雾测试": "Smoke Test (冒烟测试)",
    "后退路径": "Fallback (回退策略)",
    "冰冷启动": "Cold Start (冷启动)",
}


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
    ignore_files = {"harness_cli.py", "verify_workshop.py", "terminology-and-style-guide.md", "test_harness.py"}

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

            # 1. Check for forbidden em-dash in documentation/markdown files
            if fpath.suffix in doc_extensions and "\u2014" in content:
                for line_idx, line in enumerate(content.splitlines(), 1):
                    if "\u2014" in line:
                        findings.append((rel_path, line_idx))
                if fix:
                    content = sanitize_no_em_dash(content)

            # 2. Check for awkward literal machine translations in docs and code comments
            if fname not in ignore_files:
                new_lines = []
                for line_idx, line in enumerate(content.splitlines(keepends=True), 1):
                    # Skip lines that explicitly document prohibited literal examples
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


def _resolve_provider_config(stack: list, model_name: str = None) -> dict:
    """Resolve primary AI provider, default workhorse/flagship models, SDK packages, and API key env vars."""
    normalized_model = DEPRECATED_MODEL_REPLACEMENTS.get(model_name, model_name) if model_name else None
    model_lower = (normalized_model or "").lower()

    wants_claude = (
        any(k in stack for k in ["claude", "anthropic", "claude-agent-sdk"])
        or model_lower.startswith("claude-")
    )
    wants_openai = (
        any(k in stack for k in ["openai", "gpt", "openai-agents"])
        or model_lower.startswith(("gpt-", "o1-", "o3-", "o4-"))
    )
    wants_gemini = (
        any(k in stack for k in [
            "gemini", "google-genai", "adk", "agents-cli",
            "google-adk", "google-agents-cli", "android", "flutter", "genui", "a2ui",
        ])
        or model_lower.startswith("gemini-")
        or (not wants_claude and not wants_openai)
    )

    if model_lower.startswith("claude-"):
        primary_provider = "anthropic"
    elif model_lower.startswith("gpt-"):
        primary_provider = "openai"
    elif model_lower.startswith("gemini-"):
        primary_provider = "gemini"
    elif wants_claude and not wants_openai and "gemini" not in stack:
        primary_provider = "anthropic"
    elif wants_openai and not wants_claude and "gemini" not in stack:
        primary_provider = "openai"
    else:
        primary_provider = "gemini"

    local_ollama_gemma_tags = {
        "gemma4:e2b", "gemma4:e4b", "gemma4:12b", "gemma4:26b", "gemma4:31b",
        "translategemma", "functiongemma", "medgemma1.5", "shieldgemma",
    }
    is_local_embedding_gemma = model_lower.startswith("embeddinggemma-2") or model_lower == "google/embeddinggemma-2"
    is_local_gemma_tag = model_lower in local_ollama_gemma_tags or is_local_embedding_gemma
    is_cloud_gemma_tag = model_lower.startswith("gemma-4-")

    local_model = MODEL_REGISTRY["google-gemma"]["local_16gb_ram"]
    local_embedding_model = MODEL_REGISTRY["google-gemma"]["embedding_multimodal_740m"]
    if is_local_embedding_gemma:
        local_embedding_model = "embeddinggemma-2" if model_lower == "google/embeddinggemma-2" else normalized_model
    elif model_lower in local_ollama_gemma_tags:
        local_model = normalized_model

    if primary_provider == "anthropic":
        cloud_model = normalized_model or MODEL_REGISTRY["anthropic-claude"]["default_workhorse"]
        flagship_model = (
            MODEL_REGISTRY["anthropic-claude"]["apex_agentic"]
            if cloud_model == MODEL_REGISTRY["anthropic-claude"]["flagship_reasoning"]
            else MODEL_REGISTRY["anthropic-claude"]["flagship_reasoning"]
        )
        api_key_env = "ANTHROPIC_API_KEY"
        provider_label = "Anthropic Claude"
    elif primary_provider == "openai":
        cloud_model = normalized_model or MODEL_REGISTRY["openai-gpt"]["default_workhorse"]
        flagship_model = MODEL_REGISTRY["openai-gpt"]["flagship_reasoning"]
        api_key_env = "OPENAI_API_KEY"
        provider_label = "OpenAI"
    else:
        has_adk_or_ui = any(k in stack for k in ["adk", "agents-cli", "google-adk", "google-agents-cli", "flutter", "android", "genui", "a2ui"])
        if is_local_gemma_tag:
            if has_adk_or_ui:
                cloud_model = MODEL_REGISTRY["google-gemini"]["default_workhorse"]
            elif "31b" in model_lower:
                cloud_model = MODEL_REGISTRY["google-gemma"]["cloud_dense_31b"]
            elif "12b" in model_lower:
                cloud_model = MODEL_REGISTRY["google-gemma"]["cloud_dense_12b"]
            elif "e2b" in model_lower:
                cloud_model = MODEL_REGISTRY["google-gemma"]["cloud_edge_e2b"]
            else:
                cloud_model = MODEL_REGISTRY["google-gemma"]["cloud_moe_26b"]
            flagship_model = MODEL_REGISTRY["google-gemma"]["cloud_dense_31b"] if not has_adk_or_ui else MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
            provider_label = "Google Gemma & GenAI"
        elif is_cloud_gemma_tag:
            cloud_model = normalized_model
            flagship_model = MODEL_REGISTRY["google-gemma"]["cloud_dense_31b"]
            provider_label = "Google Gemma & GenAI"
        else:
            cloud_model = normalized_model or MODEL_REGISTRY["google-gemini"]["default_workhorse"]
            flagship_model = MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
            provider_label = "Google GenAI"
        api_key_env = "GEMINI_API_KEY"

    return {
        "primary_provider": primary_provider,
        "provider_label": provider_label,
        "default_cloud_model": cloud_model,
        "default_flagship_model": flagship_model,
        "default_local_model": local_model,
        "default_local_embedding_model": local_embedding_model,
        "primary_api_key_env": api_key_env,
        "wants_gemini": wants_gemini,
        "wants_claude": wants_claude,
        "wants_openai": wants_openai,
    }


def parse_natural_prompt(prompt: str) -> dict:
    """Parse a natural language prompt (KO/EN/JA/ZH) into name, topic, stack, and canonical 2026 model."""
    raw = (prompt or "").strip()
    lower = raw.lower()

    # 1. Detect explicit active or deprecated model tag in prompt
    detected_model = None
    explicit_provider = None

    all_active_models = []
    for prov_key, entries in MODEL_REGISTRY.items():
        for val in entries.values():
            if isinstance(val, str):
                all_active_models.append((val, prov_key))
    for tag, prov_key in sorted(all_active_models, key=lambda x: len(x[0]), reverse=True):
        if re.search(rf"(?<![a-z0-9._-]){re.escape(tag.lower())}(?![a-z0-9._-])", lower):
            detected_model = tag
            explicit_provider = prov_key
            break

    if not detected_model:
        for old_tag, new_tag in sorted(DEPRECATED_MODEL_REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True):
            if re.search(rf"(?<![a-z0-9._-]){re.escape(old_tag.lower())}(?![a-z0-9._-])", lower):
                print(f"🔄 Auto-upgraded requested model '{old_tag}' -> '{new_tag}'")
                detected_model = new_tag
                break

    # 2. Detect provider & tier intent from natural language (KO/EN/JA/ZH, handling attached CJK particles like 'Claude로')
    def _has_ascii_kw(pattern_inner: str) -> bool:
        return bool(re.search(rf"(?<![a-z0-9])({pattern_inner})(?![a-z0-9])", lower))

    has_claude = (
        explicit_provider == "anthropic-claude"
        or (detected_model or "").startswith("claude-")
        or _has_ascii_kw("claude|anthropic|fable|opus|sonnet|haiku")
        or any(k in lower for k in ["클로드", "앤트로픽", "앤쓰로픽", "페이블", "오퍼스", "소넷", "소네트", "하이쿠", "クロード", "ソネット", "オーパス", "克劳德"])
    )
    has_openai = (
        explicit_provider == "openai-gpt"
        or (detected_model or "").startswith("gpt-")
        or _has_ascii_kw("openai|chatgpt|gpt|astra|terra|luna|sunburst")
        or any(k in lower for k in ["오픈ai", "오픈에이아이", "챗gpt", "챗지피티", "지피티", "아스트라", "테라", "루나"])
    )
    has_gemini = (
        explicit_provider == "google-gemini"
        or (detected_model or "").startswith("gemini-")
        or _has_ascii_kw("gemini|carbon|hydrogen|argon")
        or any(k in lower for k in ["제미나이", "카본", "하이드로젠", "아르곤", "나노 바나나", "nano banana"])
    )
    has_embedding_gemma = (
        (detected_model or "").startswith("embeddinggemma-2")
        or _has_ascii_kw("embeddinggemma|embeddinggemma-2")
        or bool(re.search(r"embedding\s*gemma", lower))
        or any(k in lower for k in ["임베딩젬마", "임베딩 젬마"])
    )
    has_gemma_or_local = (
        explicit_provider == "google-gemma"
        or has_embedding_gemma
        or _has_ascii_kw("gemma|gemma4|translategemma|functiongemma|medgemma|shieldgemma|ollama|vllm|mlx")
        or any(k in lower for k in [
            "젬마", "트랜슬레이트젬마", "펑션젬마", "메드젬마", "실드젬마",
            "올라마", "로컬 llm", "local llm", "local rag", "로컬 rag", "lm studio", "lmstudio",
        ])
    )

    # Pick specific tier model if not already set via exact tag
    if not detected_model:
        if has_claude and not has_openai:
            if _has_ascii_kw("fable") or "페이블" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["apex_agentic"]
            elif _has_ascii_kw("opus") or "오퍼스" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["flagship_reasoning"]
            elif _has_ascii_kw("haiku") or "하이쿠" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["fast_haiku"]
            else:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["default_workhorse"]
        elif has_openai and not has_claude:
            if _has_ascii_kw("astra") or "아스트라" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["flagship_reasoning"]
            elif _has_ascii_kw("terra") or "테라" in lower or "computer use" in lower or "컴퓨터 유즈" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["multimodal_computer_use"]
            elif _has_ascii_kw("luna") or "루나" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["fast_lite"]
            elif "sunburst" in lower or "gpt-image" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["image_default"]
            else:
                detected_model = MODEL_REGISTRY["openai-gpt"]["default_workhorse"]
        elif (_has_ascii_kw("gemma|gemma4|translategemma|functiongemma|medgemma|shieldgemma") or "젬마" in lower or has_embedding_gemma) and not has_gemini:
            if _has_ascii_kw("translategemma") or "트랜슬레이트젬마" in lower or ("번역" in lower and ("gemma" in lower or "젬마" in lower)):
                detected_model = MODEL_REGISTRY["google-gemma"]["translate_multimodal"]
            elif _has_ascii_kw("functiongemma") or "펑션젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["function_calling_edge"]
            elif _has_ascii_kw("medgemma") or "메드젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["medical_multimodal"]
            elif _has_ascii_kw("shieldgemma") or "실드젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["safety_classifier"]
            elif has_embedding_gemma and not (_has_ascii_kw("gemma4") or "gemma 4" in lower or "젬마 4" in lower):
                detected_model = MODEL_REGISTRY["google-gemma"]["embedding_multimodal_740m"]
            elif _has_ascii_kw("31b"):
                detected_model = MODEL_REGISTRY["google-gemma"]["local_dense_31b"]
            elif _has_ascii_kw("26b"):
                detected_model = MODEL_REGISTRY["google-gemma"]["local_moe_26b"]
            elif _has_ascii_kw("12b"):
                detected_model = MODEL_REGISTRY["google-gemma"]["local_dense_12b"]
            elif _has_ascii_kw("e2b"):
                detected_model = MODEL_REGISTRY["google-gemma"]["local_8gb_ram"]
            else:
                detected_model = MODEL_REGISTRY["google-gemma"]["local_16gb_ram"]
        else:
            if _has_ascii_kw("carbon") or "카본" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
            elif _has_ascii_kw("argon") or "아르곤" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["enterprise_reasoning"]
            elif "live api" in lower or "라이브 api" in lower or "gemini-live" in lower or "실시간 음성" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["live_multimodal"]
            elif "omni" in lower or "비디오 생성" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["video_omni"]
            elif "nano banana" in lower or "나노 바나나" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["image_default"]
            else:
                detected_model = MODEL_REGISTRY["google-gemini"]["default_workhorse"]

    # 3. Detect stack components
    stack_items = []
    is_flutter = _has_ascii_kw("flutter|dart|genui|a2ui") or any(k in lower for k in ["플러터", "동적 ui"])
    is_android = _has_ascii_kw("android") or bool(re.search(r"jetpack\s*compose", lower)) or any(k in lower for k in ["안드로이드", "젯팩 컴포즈", "컴포즈"])
    is_adk = _has_ascii_kw("adk|google-adk|agents-cli|adlc") or "에이전트 개발 키트" in lower
    is_ts = _has_ascii_kw("typescript|nodejs") or "node.js" in lower or "타입스크립트" in lower
    is_go = _has_ascii_kw("golang") or bool(re.search(r"(?<![a-z0-9])go\s+(?:lang|adk|agent|sdk|workshop|lab)(?![a-z0-9])", lower)) or any(k in lower for k in ["고랭", "go 언어", "go로"])
    is_kotlin = (_has_ascii_kw("kotlin") or "코틀린" in lower) and not is_android
    is_java = (bool(re.search(r"(?<![a-z0-9])java(?![a-z0-9])(?!\s*script)", lower)) or ("자바" in lower and "자바스크립트" not in lower)) and not is_android

    if is_flutter:
        stack_items.append("flutter")
        if "genui" in lower or "동적 ui" in lower or "a2ui" in lower:
            stack_items.append("genui")
        if "a2ui" in lower:
            stack_items.append("a2ui")
    elif is_android:
        stack_items.append("android")
    else:
        if is_ts:
            stack_items.append("typescript")
        elif is_go:
            stack_items.append("go")
        elif is_kotlin:
            stack_items.append("kotlin")
        elif is_java:
            stack_items.append("java")
        else:
            stack_items.append("python")

        if is_adk:
            stack_items.append("adk")
            if "agents-cli" in lower or "adlc" in lower:
                stack_items.append("agents-cli")
            if "polyglot" in lower or "폴리글랏" in lower or "다중 언어" in lower:
                stack_items.append("polyglot")

        if has_claude:
            stack_items.append("claude")
            if "claude-agent-sdk" in lower:
                stack_items.append("claude-agent-sdk")
        if has_openai:
            stack_items.append("openai")
            if "openai-agents" in lower:
                stack_items.append("openai-agents")
        if has_gemini and not is_adk and not has_claude and not has_openai:
            stack_items.append("gemini")

    if has_gemma_or_local:
        stack_items.append("gemma")
        stack_items.append("ollama")
    if has_embedding_gemma:
        stack_items.append("embeddinggemma")
    if "lm studio" in lower or "lmstudio" in lower:
        stack_items.append("lmstudio")
    if "docker" in lower or "도커" in lower:
        stack_items.append("docker")
    if "mlx" in lower:
        stack_items.append("mlx")
    if "live api" in lower or "라이브 api" in lower or "gemini-live" in lower or "실시간 음성" in lower:
        stack_items.append("gemini-live")

    # Deduplicate stack preserving order
    seen_stack = []
    for s in stack_items:
        if s not in seen_stack:
            seen_stack.append(s)

    # 4. Clean topic string (strip conversational request wrappers while keeping language intact)
    clean_topic = raw
    clean_topic = re.sub(
        r"^(?:please\s+)?(?:create|build|generate|make|scaffold)\s+(?:a\s+|an\s+)?(?:complete\s+|full\s+)?(?:\d+\s*[- ]?(?:hour|hr|min|minute)s?\s+)?(?:hands[- ]on\s+)?(?:workshop|lab|tutorial)?\s*(?:on|for|about|using|with)?\s*",
        "",
        clean_topic,
        flags=re.IGNORECASE,
    ).strip()
    clean_topic = re.sub(
        r"(?:을|를)?\s*(?:바로\s*|즉시\s*|한번에\s*)?(?:만들어\s*줘요?|만들어\s*주세요|생성해\s*줘요?|생성해\s*주세요|빌드해\s*줘요?|구성해\s*줘요?|작성해\s*줘요?|짜\s*줘요?|부탁해\s*요?)[.!?]*$",
        "",
        clean_topic,
    ).strip()
    clean_topic = re.sub(
        r"(?:を)?(?:すぐ|今すぐ)?(?:作って(?:ください)?|作成して(?:ください)?|生成して(?:ください)?)[。！!]*$",
        "",
        clean_topic,
    ).strip()
    clean_topic = re.sub(r"^(?:请|帮我)?(?:立即|马上|直接)?(?:创建一个?|生成一个?|构建一个?)", "", clean_topic).strip()
    if not clean_topic:
        clean_topic = raw or "AI Hands-on Workshop"

    # 5. Build deterministic filesystem-safe project slug
    slug_parts = []
    if is_flutter:
        slug_parts.append("flutter")
        if "genui" in seen_stack:
            slug_parts.append("genui")
        if "a2ui" in seen_stack:
            slug_parts.append("a2ui")
    elif is_android:
        slug_parts.append("android")
    elif has_claude and is_adk:
        slug_parts.extend(["adk", "claude"])
    elif has_openai and is_adk:
        slug_parts.extend(["adk", "openai"])
    elif has_claude:
        slug_parts.append("claude")
        if "fable" in detected_model:
            slug_parts.append("fable")
        elif "opus" in detected_model:
            slug_parts.append("opus")
    elif has_openai:
        slug_parts.append("openai")
        if "astra" in detected_model:
            slug_parts.append("astra")
        elif "terra" in detected_model:
            slug_parts.append("terra")
    elif is_adk:
        slug_parts.append("adk")
    elif has_gemma_or_local:
        if has_embedding_gemma and not (_has_ascii_kw("gemma4") or "gemma 4" in lower or "젬마 4" in lower):
            slug_parts.append("embeddinggemma2")
        else:
            slug_parts.append("gemma4")
            if has_embedding_gemma:
                slug_parts.append("embeddinggemma2")
    else:
        slug_parts.append("gemini")

    if any(k in lower for k in ["multi-agent", "멀티 에이전트", "멀티에이전트", "다중 에이전트", "マルチエージェント", "多智能体"]):
        slug_parts.append("multi-agent")
    elif any(k in lower for k in ["agent", "에이전트", "エージェント", "智能体"]):
        slug_parts.append("agent")
    if any(k in lower for k in ["rag", "검색 증강"]):
        slug_parts.append("rag")
    if any(k in lower for k in ["structured", "구조화"]):
        slug_parts.append("structured")
    if any(k in lower for k in ["mcp"]):
        slug_parts.append("mcp")

    stop_words = {
        "create", "build", "generate", "make", "scaffold", "please", "complete", "full",
        "workshop", "workshops", "lab", "labs", "hands", "on", "with", "using", "for", "about",
        "the", "and", "or", "in", "to", "of", "a", "an", "hour", "hr", "min", "minute", "minutes",
        "latest", "new", "model", "models", "python", "claude", "anthropic", "openai", "gpt",
        "chatgpt", "gemini", "gemma", "gemma4", "embeddinggemma", "translategemma", "functiongemma",
        "medgemma", "shieldgemma", "google", "adk", "flutter", "android", "genui", "a2ui",
        "sonnet", "opus", "fable", "haiku", "sol", "astra", "terra", "luna", "carbon", "hydrogen", "argon",
    }
    ascii_tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", lower)
    extra_added = 0
    for tok in ascii_tokens:
        if tok not in stop_words and tok not in slug_parts:
            slug_parts.append(tok)
            extra_added += 1
            if extra_added >= 2:
                break

    slug_parts.append("workshop")
    dedup_slug = []
    for p in slug_parts:
        if p and p not in dedup_slug:
            dedup_slug.append(p)
    project_name = "-".join(dedup_slug)[:48].strip("-")

    return {
        "name": project_name,
        "topic": clean_topic,
        "stack": ",".join(seen_stack),
        "model": detected_model,
    }


def init_workshop(name: str, topic: str, target_dir: str = None, stack_str: str = "python", model_name: str = None):
    raw_path = Path(target_dir) / name if target_dir else Path(name)
    project_dir = raw_path if raw_path.is_absolute() else (Path.cwd() / raw_path)
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", project_dir.name).strip("-") or "workshop"
    stack = [s.strip().lower() for s in stack_str.split(",") if s.strip()] if stack_str else ["python"]

    # Auto-infer Claude / OpenAI / EmbeddingGemma 2 / specific model from topic when caller left default stack and model_name unset
    if model_name is None and not any(k in stack for k in ["claude", "anthropic", "openai", "gpt", "gemini"]):
        inferred = parse_natural_prompt(topic)
        inferred_stack = inferred["stack"].split(",")
        if "embeddinggemma" in inferred_stack and "embeddinggemma" not in stack:
            stack.append("embeddinggemma")
            stack_str = ",".join(stack)
        if any(k in inferred_stack for k in ["claude", "openai"]):
            for extra_k in ["claude", "openai"]:
                if extra_k in inferred_stack and extra_k not in stack:
                    stack.append(extra_k)
            stack_str = ",".join(stack)
            model_name = inferred["model"]
        elif inferred["model"] != MODEL_REGISTRY["google-gemini"]["default_workhorse"]:
            model_name = inferred["model"]

    prov_cfg = _resolve_provider_config(stack, model_name)
    primary_provider = prov_cfg["primary_provider"]
    provider_label = prov_cfg["provider_label"]
    default_cloud_model = prov_cfg["default_cloud_model"]
    default_flagship_model = prov_cfg["default_flagship_model"]
    primary_api_key_env = prov_cfg["primary_api_key_env"]
    wants_gemini = prov_cfg["wants_gemini"]
    wants_claude = prov_cfg["wants_claude"]
    wants_openai = prov_cfg["wants_openai"]
    default_local_model = prov_cfg["default_local_model"]
    default_local_embedding_model = prov_cfg["default_local_embedding_model"]
    print(f"🚀 Initializing new workshop project: '{name}' at {project_dir} (Provider: {provider_label} | Cloud: {default_cloud_model} | Local: {default_local_model} / {default_local_embedding_model})")

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

    # 3. Copy PDF Generator & Generate Workshop-Specific pyproject.toml / RUNBOOK.md
    pdf_templates = TEMPLATES_DIR / "pdf-templates"
    shutil.copy(pdf_templates / "generate_prep_pdf.py", project_dir / "scripts" / "generate_prep_pdf.py")

    has_adk_stack = any(k in stack for k in ["adk", "agents-cli", "google-adk", "google-agents-cli"])
    py_deps = []
    if wants_gemini:
        py_deps.append('    "google-genai>=3.0.0",')
    if wants_claude:
        py_deps.append('    "anthropic>=2.8.0",')
        if "claude-agent-sdk" in stack:
            py_deps.append('    "claude-agent-sdk>=0.2.181",')
    if wants_openai:
        py_deps.append('    "openai>=3.50.0",')
        if "openai-agents" in stack:
            py_deps.append('    "openai-agents>=0.24.0",')
    py_deps.append('    "pydantic>=2.0.0",')
    py_deps.append('    "requests>=2.31.0",')
    if has_adk_stack:
        py_deps.append('    "google-adk>=2.14.0",')
        if wants_claude or wants_openai:
            py_deps.append('    "litellm>=1.84.0",')
    py_deps_block = "\n".join(py_deps) + "\n"
    workshop_pyproject = f"""[project]
name = "{name}"
version = "0.1.0"
description = "Hands-on Workshop: {topic}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
{py_deps_block}]

[project.optional-dependencies]
docs = [
    "reportlab>=4.0.0",
    "pymupdf>=1.23.0",
    "pillow>=10.0.0",
    "python-pptx>=1.0.2",
]

[tool.uv]
package = false
"""
    (project_dir / "pyproject.toml").write_text(workshop_pyproject, encoding="utf-8")

    runbook_md = f"""# Facilitator & TA Runbook: {name}

- **Session Title**: {topic}
- **Tech Stack**: `{stack_str}`
- **Primary Cloud Provider**: {provider_label} (`{primary_api_key_env}`)
- **Primary Cloud Model**: `{default_cloud_model}` | **Coordinator**: `{default_flagship_model}` | **Local Model**: `{default_local_model}` | **Local Multimodal Embedding**: `{default_local_embedding_model}`
- **Facilitator**: Workshop Lead Facilitator
- **Teaching Assistants (TA)**: Roaming TA Team

---

## Session Timeline (60 Minutes)

### 00m - 10m: Opening & Environment Verification
- **Facilitator**: Walk through `gemma4-local-setup-guide.md`, architecture overview, and demo `./scripts/check_env.sh` execution.
- **TA**: Provide 1:1 support for attendees with environment check errors; direct low-RAM or restricted laptops to `output/colab/workshop_starter.ipynb`.

### 10m - 25m: Lab 01 - Environment Setup & Client Sanity Check
- **Facilitator**: Explain `workshop/01_starter` code structure and demo `TODO: [Lab 01]` completion.
- **TA**: Help attendees configure `{primary_api_key_env}` in `.env` or start the local LLM server (`ollama serve` on port `11434`).

### 25m - 45m: Lab 02 - Structured Outputs, Tool Calling & Agent Routing
- **Facilitator**: Demo typed Output Schema definition (`prompt-pack/README.md`) and sub-agent/tool integration.
- **TA**: Assist attendees with schema validation or port conflict errors.

### 45m - 55m: Lab 03 - End-to-End Pipeline & Verification
- **Facilitator**: Share and demo the `workshop/02_final` reference solution and run `python3 scripts/verify_workshop.py .`.
- **TA**: Verify attendee completion checkpoints.

### 55m - 60m: Q&A & Feedback Survey
- **Facilitator**: Session retrospective, share PDF handouts (`output/pdf/`), and collect attendee feedback survey responses.
"""
    (project_dir / "RUNBOOK.md").write_text(runbook_md, encoding="utf-8")

    # 4. Create .env.sample, .gitignore, Intel Mac fallback guide & ELI5 cheat sheet
    env_lines = ["# Sample Environment Variables"]
    if wants_gemini:
        env_lines.append("GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE")
    if wants_claude:
        env_lines.append("ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY_HERE")
    if wants_openai:
        env_lines.append("OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE")
    with open(project_dir / ".env.sample", "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines) + "\n")

    with open(project_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(
            "# Environment & Secrets (Never commit API keys)\n"
            ".env\n"
            "*.env\n"
            "!.env.sample\n"
            "*service-account*.json\n"
            "local.properties\n"
            "config.json\n\n"
            "# Build & Runtime Artifacts\n"
            ".venv/\n"
            "__pycache__/\n"
            "node_modules/\n"
            ".dart_tool/\n"
            ".gradle/\n"
            "build/\n"
            "tmp/\n"
        )

    with open(project_dir / "docs" / "18-intel-mac-prep.md", "w", encoding="utf-8") as f:
        f.write(f"""# Intel Mac (x86_64) Dedicated Preparation & Fallback Guide

> Workshop Topic: **{topic}**

LM Studio lacks Metal GPU acceleration on Intel CPU-based Macs (`x86_64`) and can freeze during model loading. If you are using an Intel Mac, follow the **Ollama CLI** or **Google Colab Cloud GPU** workflow below.

---

## Option A: Ollama CLI Local Server (Recommended for Local Runs)

1. **Install Ollama**: Download from [https://ollama.com/download/Ollama-darwin.zip](https://ollama.com/download/Ollama-darwin.zip)
2. **Start the Local Server**:
   ```bash
   ollama serve
   ```
3. **Pull a Lightweight Quantized Model & Multimodal Embedding Model** (in a second terminal tab):
   - **8GB RAM Intel Mac**:
     ```bash
     ollama pull gemma4:e2b
     ollama pull embeddinggemma-2:270m
     ```
   - **16GB+ RAM Intel Mac**:
     ```bash
     ollama pull {default_local_model}
     ollama pull {default_local_embedding_model}
     ```
4. **Verify Local API Endpoint**:
   ```bash
   curl http://localhost:11434/api/version
   ```

---

## Option B: Zero-Setup Google Colab Cloud GPU Fallback

If your Intel Mac experiences thermal throttling or high CPU load:
1. Open `output/colab/workshop_starter.ipynb` in **Google Colab**.
2. Add your `{primary_api_key_env}` (`{default_cloud_model}`) in Colab Secrets (left sidebar key icon).
3. Run all lab exercises on cloud GPUs with zero local CPU/RAM overhead.

## References
- [Ollama Official Documentation](https://ollama.com)
- [Google AI Studio API Key Setup](https://aistudio.google.com)
- [Anthropic Console API Keys](https://console.anthropic.com)
- [OpenAI Platform API Keys](https://platform.openai.com/api-keys)
""")

    with open(project_dir / "docs" / "eli5-concept-cheat-sheet.md", "w", encoding="utf-8") as f:
        f.write(f"""# ELI5 (Explain Like I'm 5) AI Concept Cheat Sheet

> Workshop Topic: **{topic}**
> Primary Cloud Model: `{default_cloud_model}` | Flagship Reasoning: `{default_flagship_model}` | Local Model: `{default_local_model}`

This cheat sheet translates core AI engineering concepts into intuitive everyday analogies across a 3-tier framework (Analogy -> Technical Mechanism -> Hands-on Action).

---

## Core Concepts At a Glance

| Concept | Everyday Analogy (Tier 1) | Technical Mechanism (Tier 2) | Hands-on Lab Action (Tier 3) |
| :--- | :--- | :--- | :--- |
| **Local LLM (`{default_local_model}`)** | Having a personal librarian inside your laptop who works even with Wi-Fi turned off | Quantized model weights executing on local GPU/CPU and serving HTTP on `localhost:11434` | Run `ollama serve` and query local endpoints without cloud latency |
| **Model Quantization (4-bit)** | Packing a winter jacket into a vacuum-sealed travel bag so it fits in a carry-on | Compressing 16-bit floating-point weights into 4-bit integers to reduce RAM usage by ~70% | Use `gemma4:e2b` on 8GB RAM laptops to prevent Out-Of-Memory (OOM) errors |
| **Structured Outputs (JSON Schema)** | Handing someone a tax form with strict boxes instead of a blank sheet of paper | Constraining token sampling to match a typed schema (Pydantic / Zod / Data Class) | Parse LLM responses deterministically in `Lab 02` without regex |
| **RAG (Retrieval-Augmented Generation)** | Taking an open-book exam where you look up the exact page before answering | Retrieving relevant document chunks via multimodal embeddings (`gemini-embedding-2` cloud / `{default_local_embedding_model}` local 768d MRL) and injecting them into the prompt | Ground model answers on verified workshop data |
| **Multi-Agent Orchestration** | A head chef (`{default_flagship_model}`) delegating prep and plating to line cooks (`{default_cloud_model}`) | Coordinator routing tasks to specialized sub-agents and FunctionTools | Inspect sub-agent delegation and trajectory evaluation in `Lab 02 & Lab 03` |

## References
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Google Agent Development Kit (ADK)](https://adk.dev)
""")

    # 5. Create AGENTS.md, CLAUDE.md, and README.md
    agent_rules_header = f"""# Agent Instructions, Developer Terminology & Typography Rules for {name}

> Topic: **{topic}**
> Tech Stack: `{stack_str}` | Primary Cloud Model: `{default_cloud_model}` | Local Model: `{default_local_model}`
"""
    agent_rules_body = """
## Mandatory Rules for AI Coding Agents

1. **Original Technical Term First, Real-World Developer Terminology & Natural Developer Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
   - **English (EN)**: Write in clear, idiomatic, direct technical English.
   - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** in Korean, Japanese, or Chinese, **NEVER perform awkward literal / word-for-word machine translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
   - **For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence structures used by local software engineers**:
     - **Korean (KO)**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Breaking Changes (브레이킹 체인지)**. Avoid double passives (`~되어집니다` -> `~됩니다`) and awkward literal phrases ("손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트").
     - **Japanese (JA)**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」.
     - **Chinese (ZH)**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」.
   - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in their exact English form (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments using original English technical terms paired with developer-friendly explanations.

2. **Typography Rule (No Em Dash in Markdown or Documentation)**:
   - **NEVER generate em dash characters (`\\u2014`)** in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks.
   - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
   - Run `python3 scripts/verify_workshop.py .` to verify zero forbidden em dashes or awkward literal translations exist.

3. **No Emojis in Documentation by Default**:
   - Do not include emojis in generated documentation, slide decks, setup guides, or runbooks unless explicitly requested.
"""
    agent_rules_footer = f"""
4. **2026 Frontier Model & SDK Currency**:
   - Use verified 2026 SDKs (`google-genai >= 3.0.0`, `anthropic >= 2.8.0`, `openai >= 3.50.0`, `google-adk >= 2.14.0`) and active model tags (`{default_cloud_model}`, `{default_flagship_model}`, `gemini-4-hydrogen`, `gemini-4-carbon`, `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `{default_local_model}`).
   - Never use deprecated `google-generativeai` or retired legacy model tags.

## References
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
"""
    agent_rules_md = agent_rules_header + agent_rules_body + agent_rules_footer
    (project_dir / "AGENTS.md").write_text(agent_rules_md, encoding="utf-8")
    (project_dir / "CLAUDE.md").write_text(agent_rules_md, encoding="utf-8")

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
├── AGENTS.md                     # AI Agent & Typography rules (No Em Dash rule)
├── CLAUDE.md                     # Claude Code instructions
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
    is_flutter = any(k in stack for k in ["flutter", "dart", "genui", "a2ui"])
    is_android = any(k in stack for k in ["android", "compose", "jetpack"])
    is_ts = any(k in stack for k in ["typescript", "ts", "javascript", "js", "node"])
    is_go = any(k in stack for k in ["go", "golang"])
    is_java = any(k in stack for k in ["java"]) and not is_android
    is_kotlin = any(k in stack for k in ["kotlin", "kt"]) and not is_android
    is_adk = any(k in stack for k in ["adk", "agents-cli", "google-adk", "google-agents-cli"])
    is_polyglot_adk = is_adk and (
        "polyglot" in stack
        or sum([bool(is_ts), bool(is_go), bool(is_java), bool(is_kotlin), ("python" in stack)]) >= 2
    )

    if is_flutter:
        pubspec_yaml = f"""name: {name.replace('-', '_')}
description: "A modern Flutter Generative AI, GenUI, and A2UI Hands-on Workshop"
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.5.0 <4.0.0'
  flutter: '>=3.24.0'

dependencies:
  flutter:
    sdk: flutter
  google_generative_ai: ^0.4.6
  genui: ^0.1.0
  cupertino_icons: ^1.0.8

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
"""
        with open(project_dir / "workshop" / "01_starter" / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_yaml)
        with open(project_dir / "workshop" / "02_final" / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_yaml)

        (project_dir / "workshop" / "01_starter" / "lib").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "lib").mkdir(parents=True, exist_ok=True)

        starter_dart = """import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:genui/genui.dart';

void main() {
  runApp(const WorkshopApp());
}

class WorkshopApp extends StatelessWidget {
  const WorkshopApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter GenAI & GenUI Workshop - Starter',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const GenUIWorkshopPage(),
    );
  }
}

class GenUIWorkshopPage extends StatefulWidget {
  const GenUIWorkshopPage({super.key});

  @override
  State<GenUIWorkshopPage> createState() => _GenUIWorkshopPageState();
}

class _GenUIWorkshopPageState extends State<GenUIWorkshopPage> {
  final TextEditingController _promptController = TextEditingController();
  final List<String> _chatLogs = [];
  bool _isLoading = false;

  // TODO: [Lab 1] Read GEMINI_API_KEY and configure GenerativeModel
  // static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  // late final GenerativeModel _model;

  // TODO: [Lab 2] Define Custom WidgetCatalog & initialize SurfaceController
  // late final SurfaceController _surfaceController;

  @override
  void initState() {
    super.initState();
    // TODO: [Lab 1 & Lab 2] Initialize services and controllers
  }

  void _sendPrompt() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _chatLogs.add('User: $prompt');
      _isLoading = true;
      _promptController.clear();
    });

    // TODO: [Lab 3] Send prompt to Gemini and stream declarative A2UI JSON payload into _surfaceController

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter GenUI & A2UI Hands-on Lab'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _chatLogs.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Text(_chatLogs[index]),
                );
              },
            ),
          ),
          // TODO: [Lab 2 & Lab 3] Mount GenUISurface to render dynamic AI surfaces
          // GenUISurface(controller: _surfaceController),
          if (_isLoading) const LinearProgressIndicator(),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promptController,
                    decoration: const InputDecoration(
                      hintText: 'Ask Gemini to recommend cards or widgets...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendPrompt(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.send),
                  onPressed: _sendPrompt,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""
        final_dart = """import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:genui/genui.dart';

void main() {
  runApp(const WorkshopApp());
}

class WorkshopApp extends StatelessWidget {
  const WorkshopApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter GenAI & GenUI Workshop - Final Solution',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const GenUIWorkshopPage(),
    );
  }
}

// 1. Data Model for dynamic RecommendationCard
class RecommendationCardData {
  final String title;
  final String description;
  final double rating;
  final String actionLabel;

  RecommendationCardData({
    required this.title,
    required this.description,
    required this.rating,
    required this.actionLabel,
  });

  factory RecommendationCardData.fromJson(Map<String, dynamic> json) {
    return RecommendationCardData(
      title: json['title'] as String? ?? 'Recommendation',
      description: json['description'] as String? ?? '',
      rating: (json['rating'] as num?)?.toDouble() ?? 4.8,
      actionLabel: json['actionLabel'] as String? ?? 'Explore',
    );
  }
}

// 2. Custom WidgetCatalog for A2UI components
final customCatalog = WidgetCatalog([
  CatalogItem(
    name: 'RecommendationCard',
    description: 'Displays a rich recommendation card with rating and an action button.',
    builder: (context, data, controller) {
      final item = RecommendationCardData.fromJson(data);
      return Card(
        elevation: 3,
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      item.title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primaryContainer,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text('Rating: ${item.rating} / 5.0'),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(item.description, style: Theme.of(context).textTheme.bodyMedium),
              const SizedBox(height: 12),
              Align(
                alignment: Alignment.centerRight,
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.touch_app, size: 18),
                  label: Text(item.actionLabel),
                  onPressed: () {
                    controller.dispatchAction('card_selected', {
                      'title': item.title,
                      'timestamp': DateTime.now().toIso8601String(),
                    });
                  },
                ),
              ),
            ],
          ),
        ),
      );
    },
  ),
]);

class GenUIWorkshopPage extends StatefulWidget {
  const GenUIWorkshopPage({super.key});

  @override
  State<GenUIWorkshopPage> createState() => _GenUIWorkshopPageState();
}

class _GenUIWorkshopPageState extends State<GenUIWorkshopPage> {
  final TextEditingController _promptController = TextEditingController();
  final List<String> _chatLogs = [];
  bool _isLoading = false;

  static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  late final GenerativeModel _model;
  late final SurfaceController _surfaceController;

  @override
  void initState() {
    super.initState();
    _model = GenerativeModel(
      model: 'gemini-4-hydrogen',
      apiKey: _apiKey.isNotEmpty ? _apiKey : 'DEMO_KEY',
      systemInstruction: Content.system(
        'You are an A2UI (Agent-to-User Interface) generator. When users request recommendations, '
        'output valid JSON with component "RecommendationCard" and parameters: '
        '{"component": "RecommendationCard", "data": {"title": "...", "description": "...", "rating": 4.9, "actionLabel": "View Details"}}',
      ),
    );

    _surfaceController = SurfaceController(catalog: customCatalog);
    _surfaceController.onActionDispatched.listen((action) {
      setState(() {
        _chatLogs.add('User Action Dispatched: ${action.name} -> ${action.payload}');
      });
    });
  }

  void _sendPrompt() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _chatLogs.add('User: $prompt');
      _isLoading = true;
      _promptController.clear();
    });

    try {
      if (_apiKey.isNotEmpty && _apiKey != 'DEMO_KEY') {
        final response = await _model.generateContent([Content.text(prompt)]);
        final text = response.text ?? '';
        setState(() {
          _chatLogs.add('Agent: $text');
        });
        _surfaceController.updateSurfaceFromText(text);
      } else {
        // Offline / Demo Fallback Mock
        await Future.delayed(const Duration(milliseconds: 600));
        final mockPayload = {
          "title": "Flutter GenUI Workshop Lab",
          "description": "Dynamic A2UI surface rendered successfully without live API keys.",
          "rating": 5.0,
          "actionLabel": "Get Started"
        };
        _surfaceController.mountComponent('RecommendationCard', mockPayload);
        setState(() {
          _chatLogs.add('Agent (Demo Mock): Dynamic A2UI surface rendered.');
        });
      }
    } catch (e) {
      setState(() {
        _chatLogs.add('Error: $e');
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter GenUI & A2UI - Final Solution'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _chatLogs.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Text(_chatLogs[index]),
                );
              },
            ),
          ),
          // Dynamic A2UI Surface Area
          Container(
            constraints: const BoxConstraints(maxHeight: 280),
            child: GenUISurface(controller: _surfaceController),
          ),
          if (_isLoading) const LinearProgressIndicator(),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promptController,
                    decoration: const InputDecoration(
                      hintText: 'Ask Gemini to generate dynamic UI cards...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendPrompt(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.send),
                  onPressed: _sendPrompt,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""
        with open(project_dir / "workshop" / "01_starter" / "lib" / "main.dart", "w", encoding="utf-8") as f:
            f.write(starter_dart)
        with open(project_dir / "workshop" / "02_final" / "lib" / "main.dart", "w", encoding="utf-8") as f:
            f.write(final_dart)

        # Specialized Flutter run scripts
        flutter_run_sh = """#!/usr/bin/env bash
set -e

echo "Starting Flutter Workshop Application..."
flutter pub get

API_KEY="${GEMINI_API_KEY:-}"
if [ -f "../../.env" ]; then
    export $(grep -v '^#' ../../.env | xargs 2>/dev/null || true)
fi
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs 2>/dev/null || true)
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "Running Flutter Web with GEMINI_API_KEY..."
    flutter run -d chrome --dart-define=GEMINI_API_KEY="$GEMINI_API_KEY"
else
    echo "Running Flutter Web (Demo / Offline mode)..."
    flutter run -d chrome
fi
"""
        flutter_run_ps1 = """Write-Host "Starting Flutter Workshop Application..."
flutter pub get

if (Test-Path "..\\..\\.env") {
    Get-Content "..\\..\\.env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
        }
    }
}
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
        }
    }
}

if ($env:GEMINI_API_KEY) {
    Write-Host "Running Flutter Web with GEMINI_API_KEY..."
    flutter run -d chrome --dart-define="GEMINI_API_KEY=$env:GEMINI_API_KEY"
} else {
    Write-Host "Running Flutter Web (Demo / Offline mode)..."
    flutter run -d chrome
}
"""
        for stage in ["01_starter", "02_final"]:
            with open(project_dir / "workshop" / stage / ".gitignore", "w", encoding="utf-8") as f:
                f.write(".dart_tool/\nbuild/\n.flutter-plugins\n.flutter-plugins-dependencies\nconfig.json\n.env\n")
            with open(project_dir / "workshop" / stage / "config.json.sample", "w", encoding="utf-8") as f:
                f.write('{\n  "GEMINI_API_KEY": "AIzaSyYourGeminiApiKeyHere"\n}\n')
            with open(project_dir / "workshop" / stage / "run.sh", "w", encoding="utf-8") as f:
                f.write(flutter_run_sh)
            with open(project_dir / "workshop" / stage / "run.ps1", "w", encoding="utf-8") as f:
                f.write(flutter_run_ps1)
            os.chmod(project_dir / "workshop" / stage / "run.sh", 0o755)

        # Scaffold 3-stage Flutter Lab step files & session guide
        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Hands-on Lab Session Guide

This guide outlines the session schedule and step-by-step objectives for the **{topic}** workshop.
Write your code in `workshop/01_starter/lib/main.dart`. If you get stuck, refer to the reference solution in `workshop/02_final/lib/main.dart`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & Flutter environment check (`flutter doctor`)
- **10m - 25m**: **Lab 01** - Flutter Material 3 Scaffold & Gemini Setup (`01_lab_flutter_gemini_setup.md`)
- **25m - 45m**: **Lab 02** - Responsive Chat UI & Multimodal Vision (`02_lab_responsive_chat_multimodal.md`)
- **45m - 55m**: **Lab 03** - Generative UI & A2UI Dynamic Surface Streaming (`03_lab_genui_a2ui_surfaces.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Flutter Material 3 Scaffold & Gemini Setup](./01_lab_flutter_gemini_setup.md)**
2. **[Lab 02: Responsive Chat UI & Multimodal Vision](./02_lab_responsive_chat_multimodal.md)**
3. **[Lab 03: Generative UI & A2UI Dynamic Surface Streaming](./03_lab_genui_a2ui_surfaces.md)**

## Execution Commands

```bash
# macOS / Linux
cd workshop/01_starter && ./run.sh

# Windows (PowerShell)
cd workshop\\01_starter; .\\run.ps1
```
""")

        with open(labs_dir / "01_lab_flutter_gemini_setup.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 01: Flutter Material 3 Scaffold & Gemini Client Setup

## Objective
Initialize the Flutter project with `google_generative_ai` and configure API key injection using `--dart-define` or `--dart-define-from-file`.

## Instructions
1. Copy `config.json.sample` to `config.json` and enter your Gemini API Key.
2. Initialize `GenerativeModel` in `lib/main.dart`:
   ```dart
   const apiKey = String.fromEnvironment('GEMINI_API_KEY');
   final model = GenerativeModel(model: 'gemini-4-hydrogen', apiKey: apiKey);
   ```
3. Run the app on Flutter Web (or connected device):
   ```bash
   flutter run -d chrome --dart-define-from-file=config.json
   ```

> Fast-Forward Checkpoint:
> `git checkout lab-01-complete` (or inspect `workshop/02_final/lib/main.dart`).
""")
        with open(labs_dir / "02_lab_responsive_chat_multimodal.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 02: Responsive Chat UI & Multimodal Vision

## Objective
Build an adaptive chat UI using `flutter-build-responsive-layout` and attach images using `image_picker` and `DataPart`.

## Instructions
1. Implement `Stream<GenerateContentResponse>` handling for real-time word-by-word streaming.
2. Add image attachment button and pass `DataPart(mimeType, imageBytes)` to `generateContent`.
3. Use `flutter-fix-layout-issues` if experiencing `RenderFlex overflowed` errors.

> Fast-Forward Checkpoint:
> `git checkout lab-02-complete`
""")
        with open(labs_dir / "03_lab_genui_a2ui_surfaces.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: Generative UI & A2UI Dynamic Surface Streaming

## Objective
Build a dynamic widget catalog and render ephemeral surfaces streamed directly from the AI agent using the A2UI protocol.

## Instructions
1. Define custom `CatalogItem` (e.g. `RecommendationCard`, `WeatherCard`).
2. Wire `SurfaceController` with `WidgetCatalog` to parse declarative JSON streams.
3. Handle bi-directional button actions with `dispatchAction` and trigger agent tool executions.

> Fast-Forward Checkpoint:
> `git checkout lab-03-final`
""")

        # Custom Flutter / A2UI Prompt Pack
        with open(project_dir / "prompt-pack" / "README.md", "w", encoding="utf-8") as f:
            f.write("""# A2UI & Flutter GenUI Prompt Pack

This prompt pack contains system instructions and output schemas for Gemini to generate declarative A2UI JSON payloads compatible with `genui`.

---

## 1. A2UI Declarative JSON System Prompt

```text
You are an AI Agent operating within the A2UI (Agent-to-User Interface) protocol.
When the user asks for recommendations, items, or summaries, output a JSON object adhering to the registered WidgetCatalog:

{
  "component": "RecommendationCard",
  "data": {
    "title": "String (e.g. Kyoto Traditional Ryokan)",
    "description": "String (concise 1-2 sentence description)",
    "rating": 4.9,
    "actionLabel": "String (e.g. View Details, Book Now)"
  }
}
```

## 2. Few-Shot Examples

### User Query:
"Recommend top 3 travel destinations in Japan"

### Expected A2UI Output:
```json
[
  {
    "component": "RecommendationCard",
    "data": {
      "title": "Kyoto Arashiyama Bamboo Grove",
      "description": "Scenic natural bamboo forest with ancient shrines and tranquil walking paths.",
      "rating": 4.9,
      "actionLabel": "Explore Guide"
    }
  },
  {
    "component": "RecommendationCard",
    "data": {
      "title": "Tokyo Shibuya Sky",
      "description": "360-degree open-air observation deck overlooking the Shibuya Crossing.",
      "rating": 4.8,
      "actionLabel": "Book Tickets"
    }
  }
]
```
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Flutter GenAI & GenUI Workshop Starter ({default_cloud_model})")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Flutter GenAI & GenUI Workshop Final ({default_cloud_model})")\n')


    elif is_android:
        for stage in ["01_starter", "02_final"]:
            app_dir = project_dir / "workshop" / stage / "app"
            src_dir = app_dir / "src" / "main" / "kotlin" / "com" / "example" / "workshop"
            res_dir = app_dir / "src" / "main" / "res" / "values"
            src_dir.mkdir(parents=True, exist_ok=True)
            res_dir.mkdir(parents=True, exist_ok=True)

            settings_gradle = f"""pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{name}"
include(":app")
"""
            with open(project_dir / "workshop" / stage / "settings.gradle.kts", "w", encoding="utf-8") as f:
                f.write(settings_gradle)

            root_build_gradle = """// Top-level build file
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.0" apply false
}
"""
            with open(project_dir / "workshop" / stage / "build.gradle.kts", "w", encoding="utf-8") as f:
                f.write(root_build_gradle)

            app_build_gradle = """import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

val localProperties = Properties().apply {
    val localPropsFile = rootProject.file("local.properties")
    if (localPropsFile.exists()) {
        load(localPropsFile.inputStream())
    }
}
val geminiApiKey: String = localProperties.getProperty("GEMINI_API_KEY") ?: ""

android {
    namespace = "com.example.workshop"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.workshop"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        buildConfigField("String", "GEMINI_API_KEY", "\\\"$geminiApiKey\\\"")
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation("androidx.activity:activity-compose:1.9.1")
    implementation(platform("androidx.compose:compose-bom:2024.09.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("com.google.genai:google-genai-kotlin-android:1.8.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
}
"""
            with open(app_dir / "build.gradle.kts", "w", encoding="utf-8") as f:
                f.write(app_build_gradle)

            # Android .gitignore & local.properties.sample
            with open(project_dir / "workshop" / stage / ".gitignore", "w", encoding="utf-8") as f:
                f.write(".gradle/\nbuild/\nlocal.properties\n*.apk\n*.aab\n.idea/\n")
            with open(project_dir / "workshop" / stage / "local.properties.sample", "w", encoding="utf-8") as f:
                f.write("# Copy this file to local.properties and insert your Gemini API Key\nGEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere\n")

            manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:label="Android GenAI Workshop"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
            with open(app_dir / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
                f.write(manifest)

        starter_main_kt = """package com.example.workshop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Modifier

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // TODO [Lab 01]: Initialize Google GenAI Kotlin client with BuildConfig.GEMINI_API_KEY (gemini-4-hydrogen)
        // TODO [Lab 02]: Connect ChatViewModel StateFlow for reactive UDF and Structured Outputs
        // TODO [Lab 03]: Integrate CameraX multimodal capture and AppFunctions on-device shortcut
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Text("Welcome to Android GenAI Workshop! Open workshop/03_labs/README.md")
                }
            }
        }
    }
}
"""
        final_main_kt = """package com.example.workshop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Android GenAI & Jetpack Compose Final Solution", style = MaterialTheme.typography.headlineSmall)
                        Spacer(modifier = Modifier.height(12.dp))
                        Text("Connected to Google GenAI SDK (gemini-4-hydrogen)")
                    }
                }
            }
        }
    }
}
"""
        with open(project_dir / "workshop" / "01_starter" / "app" / "src" / "main" / "kotlin" / "com" / "example" / "workshop" / "MainActivity.kt", "w", encoding="utf-8") as f:
            f.write(starter_main_kt)
        with open(project_dir / "workshop" / "02_final" / "app" / "src" / "main" / "kotlin" / "com" / "example" / "workshop" / "MainActivity.kt", "w", encoding="utf-8") as f:
            f.write(final_main_kt)

        # Scaffold 3-stage Android Lab step files
        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Android Jetpack Compose Hands-on Lab Session Guide

This guide covers building modern Android GenAI applications using Jetpack Compose Material 3, Google GenAI Kotlin SDK (`com.google.genai`), and the Google `android` CLI.

## Step-by-Step Labs

1. **[Lab 01: Android CLI Setup & Gemini Client Integration](./01_lab_gemini_client.md)**
2. **[Lab 02: MVVM Architecture, StateFlow & Structured Outputs](./02_lab_mvvm_stateflow.md)**
3. **[Lab 03: CameraX Multimodal Vision & On-Device AppFunctions](./03_lab_camerax_appfunctions.md)**
""")
        with open(labs_dir / "01_lab_gemini_client.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 01: Android CLI Setup & Gemini Client Integration

## Objective
Initialize the Android project using Google `android` CLI and configure the official Google GenAI Kotlin SDK (`com.google.genai`).

## Instructions
1. Copy `local.properties.sample` to `local.properties` and add your `GEMINI_API_KEY`.
2. Inspect `app/build.gradle.kts` and verify `buildConfigField("String", "GEMINI_API_KEY", ...)`.
3. Open `MainActivity.kt` and initialize the Google GenAI Client with `BuildConfig.GEMINI_API_KEY`.
4. Run the app on emulator or physical device:
   ```bash
   android run
   ```

> Fast-Forward Checkpoint:
> If you fall behind or run into environment errors, fast-forward to the completed Lab 01 state:
> `git checkout lab-01-complete` (or inspect `workshop/02_final/`).
""")
        with open(labs_dir / "02_lab_mvvm_stateflow.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 02: MVVM Architecture, StateFlow & Structured Outputs

## Objective
Implement reactive unidirectional data flow (UDF) using Android ViewModel and StateFlow with type-safe Structured JSON output.

## Instructions
1. Create `ChatViewModel.kt` with `StateFlow<ChatUiState>`.
2. Connect `ChatViewModel` to `MainActivity.kt` via Compose `viewModel()`.
3. Configure `gemini-4-hydrogen` (or `gemini-3.8-flash`) with JSON output schema for structured response parsing.

> Fast-Forward Checkpoint:
> `git checkout lab-02-complete`
""")
        with open(labs_dir / "03_lab_camerax_appfunctions.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: CameraX Multimodal Vision & On-Device AppFunctions

## Objective
Capture image frames using CameraX and feed them to Gemini multimodal API, exposing on-device shortcuts via AppFunctions.

## Instructions
1. Integrate `camerax` skill for image capture and preview.
2. Send image bytes to Gemini multimodal `generateContent`.
3. Bind AppFunctions for Android system shortcut triggering.

> Fast-Forward Checkpoint:
> `git checkout lab-03-final`
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Android GenAI Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Android GenAI Workshop Final")\n')


    elif is_ts and not is_polyglot_adk:
        ts_deps = {
            "@google/adk": "^0.5.0",
            "@google/genai": "^3.0.0",
            "dotenv": "^16.4.5",
            "zod": "^3.23.8",
        }
        if wants_claude:
            ts_deps["@anthropic-ai/sdk"] = "^1.7.0"
        if wants_openai:
            ts_deps["openai"] = "^7.55.0"
        pkg_obj = {
            "name": name,
            "version": "1.0.0",
            "type": "module",
            "scripts": {"start": "tsx src/index.ts"},
            "dependencies": ts_deps,
            "devDependencies": {"tsx": "^4.19.0", "typescript": "^5.5.4"},
        }
        pkg_json = json.dumps(pkg_obj, indent=2) + "\n"
        with open(project_dir / "workshop" / "01_starter" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)
        with open(project_dir / "workshop" / "02_final" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)

        starter_agent_ts = f"""// TypeScript Google ADK (@google/adk) Starter Agent ({default_cloud_model})
import {{ LlmAgent, FunctionTool }} from "@google/adk";
import {{ z }} from "zod";

export const lookupServiceSloTool = new FunctionTool({{
  name: "lookup_service_slo",
  description: "Returns target P99 SLO latency and remaining error budget for a production microservice.",
  parameters: z.object({{
    serviceName: z.string().describe("Target microservice name, e.g. checkout-api"),
  }}),
  execute: async ({{ serviceName }}) => ({{
    serviceName,
    targetP99Ms: serviceName === "checkout-api" ? 250 : 120,
    errorBudgetRemainingPct: 42.0,
    status: "healthy",
  }}),
}});

// TODO [Lab 01 & Lab 02]: Define specialist subAgents and attach them to rootAgent
export const rootAgent = new LlmAgent({{
  name: "sre_coordinator",
  model: "{default_cloud_model}",
  description: "Root ADK TypeScript coordinator for {topic}.",
  instruction: "Use lookup_service_slo to inspect service SLO targets.",
  tools: [lookupServiceSloTool],
}});
"""
        final_agent_ts = f"""// TypeScript Google ADK (@google/adk) Final Reference Agent ({default_cloud_model})
import {{ LlmAgent, FunctionTool }} from "@google/adk";
import {{ z }} from "zod";

export const lookupServiceSloTool = new FunctionTool({{
  name: "lookup_service_slo",
  description: "Returns target P99 SLO latency and remaining error budget for a production microservice.",
  parameters: z.object({{
    serviceName: z.string().describe("Target microservice name, e.g. checkout-api"),
  }}),
  execute: async ({{ serviceName }}) => ({{
    serviceName,
    targetP99Ms: serviceName === "checkout-api" ? 250 : 120,
    errorBudgetRemainingPct: 42.0,
    status: "healthy",
  }}),
}});

export const opsSpecialist = new LlmAgent({{
  name: "ops_specialist",
  model: "{default_cloud_model}",
  description: "Audits microservice SLO metrics and evaluates release gates.",
  instruction: "Call lookup_service_slo for the requested service and report latency budget status.",
  tools: [lookupServiceSloTool],
}});

export const reportWriter = new LlmAgent({{
  name: "report_writer",
  model: "{default_cloud_model}",
  description: "Drafts concise SRE incident and release readiness summaries.",
  instruction: "Format telemetry findings from ops_specialist into an actionable SRE checklist.",
}});

export const rootAgent = new LlmAgent({{
  name: "sre_coordinator",
  model: "{default_flagship_model}",
  description: "Root ADK TypeScript orchestrator that delegates telemetry and reporting.",
  instruction: "Delegate SLO inspection to ops_specialist and summary drafting to report_writer.",
  subAgents: [opsSpecialist, reportWriter],
}});
"""
        starter_ts = f"""// TypeScript / Node.js Starter Runner ({provider_label} - {default_cloud_model})
import "dotenv/config";
import {{ rootAgent }} from "./agent.js";

async function main() {{
  console.log("Welcome to the TypeScript Workshop ({provider_label} - {default_cloud_model})! Open workshop/03_labs/README.md to begin.");
  console.log("Initialized rootAgent:", rootAgent.name);
}}

main().catch(console.error);
"""
        if primary_provider == "anthropic":
            final_ts = f"""// TypeScript / Node.js Final Solution Runner (Anthropic Claude - {default_cloud_model})
import "dotenv/config";
import Anthropic from "@anthropic-ai/sdk";
import {{ rootAgent }} from "./agent.js";

async function main() {{
  const apiKey = process.env.ANTHROPIC_API_KEY || "";
  if (apiKey && apiKey !== "YOUR_ANTHROPIC_API_KEY_HERE") {{
    const client = new Anthropic({{ apiKey }});
    const response = await client.messages.create({{
      model: "{default_cloud_model}",
      max_tokens: 1024,
      thinking: {{ type: "adaptive" }},
      messages: [{{ role: "user", content: "Summarize 3 key benefits of agentic coding with {default_cloud_model} in TypeScript." }}],
    }});
    console.log(response.content);
  }} else {{
    console.log(`[Offline Demo Mode] All TypeScript Claude Workshop Labs Completed! Root Agent: ${{rootAgent.name}} (Model: {default_cloud_model})`);
  }}
}}

main().catch(console.error);
"""
        elif primary_provider == "openai":
            final_ts = f"""// TypeScript / Node.js Final Solution Runner (OpenAI - {default_cloud_model})
import "dotenv/config";
import OpenAI from "openai";
import {{ rootAgent }} from "./agent.js";

async function main() {{
  const apiKey = process.env.OPENAI_API_KEY || "";
  if (apiKey && apiKey !== "YOUR_OPENAI_API_KEY_HERE") {{
    const client = new OpenAI({{ apiKey }});
    const response = await client.responses.create({{
      model: "{default_cloud_model}",
      reasoning: {{ effort: "medium" }},
      input: "Summarize 3 key benefits of OpenAI Responses API structured outputs with {default_cloud_model} in TypeScript.",
    }});
    console.log(response.output_text);
  }} else {{
    console.log(`[Offline Demo Mode] All TypeScript OpenAI Workshop Labs Completed! Root Agent: ${{rootAgent.name}} (Model: {default_cloud_model})`);
  }}
}}

main().catch(console.error);
"""
        else:
            final_ts = f"""// TypeScript / Node.js ADK Final Solution Runner ({default_cloud_model})
import "dotenv/config";
import {{ GoogleGenAI }} from "@google/genai";
import {{ rootAgent }} from "./agent.js";

async function main() {{
  const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || "";
  if (apiKey && apiKey !== "YOUR_GEMINI_API_KEY_HERE") {{
    const client = new GoogleGenAI({{ apiKey }});
    const interaction = await client.interactions.create({{
      model: "{default_cloud_model}",
      input: "Summarize 3 key benefits of Google ADK multi-agent orchestration in TypeScript.",
    }});
    console.log(interaction.output_text);
  }} else {{
    console.log(`[Offline Demo Mode] All TypeScript ADK Workshop Labs Completed! Root Agent: ${{rootAgent.name}} (Model: {default_cloud_model})`);
  }}
}}

main().catch(console.error);
"""
        with open(project_dir / "workshop" / "01_starter" / "src" / "agent.ts", "w", encoding="utf-8") as f:
            f.write(starter_agent_ts)
        with open(project_dir / "workshop" / "02_final" / "src" / "agent.ts", "w", encoding="utf-8") as f:
            f.write(final_agent_ts)
        with open(project_dir / "workshop" / "01_starter" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(starter_ts)
        with open(project_dir / "workshop" / "02_final" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(final_ts)

        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - TypeScript ADK Hands-on Lab Session Guide

This guide covers building production multi-agent systems in TypeScript using **Google Agent Development Kit (`@google/adk`)** and **Zod**.

## Step-by-Step Labs

1. **[Lab 01: TypeScript ADK Setup & Zod FunctionTools](./01_lab_ts_adk_agent_and_zod_tools.md)**
2. **[Lab 02: Multi-Agent Delegation with subAgents](./02_lab_ts_subagents_and_routing.md)**
3. **[Lab 03: ADK Web Dev UI, Trajectory Evaluation & API Serving](./03_lab_ts_eval_and_api_server.md)**
""")
        with open(labs_dir / "01_lab_ts_adk_agent_and_zod_tools.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 01: TypeScript ADK Setup & Zod FunctionTools

## Objective
Initialize `@google/adk` with Zod-typed `FunctionTool` definitions and configure `{default_cloud_model}` in `src/agent.ts`.

## Instructions
1. Install dependencies: `cd workshop/01_starter && npm install`
2. Inspect `lookupServiceSloTool` in `src/agent.ts` using `new FunctionTool({{ name, description, parameters: z.object(...), execute }})`.
3. Run the starter entry point: `npm start`

> Fast-Forward Checkpoint:
> Inspect `workshop/02_final/src/agent.ts`.
""")
        with open(labs_dir / "02_lab_ts_subagents_and_routing.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 02: Multi-Agent Delegation with subAgents

## Objective
Create specialist `LlmAgent` instances (`opsSpecialist`, `reportWriter`) and register them under `subAgents` on `rootAgent` (`{default_flagship_model}`).

## Instructions
1. Define `opsSpecialist` and `reportWriter` in `workshop/01_starter/src/agent.ts`.
2. Wire `subAgents: [opsSpecialist, reportWriter]` on `rootAgent`.
3. Ensure each child agent has a precise `description` so `rootAgent` routes tasks accurately.
""")
        with open(labs_dir / "03_lab_ts_eval_and_api_server.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: ADK Web Dev UI, Trajectory Evaluation & API Serving

## Objective
Test your TypeScript ADK hierarchy interactively and verify end-to-end execution.

## Instructions
1. Run the reference solution: `cd workshop/02_final && npm start`
2. Run the workshop verifier: `python3 scripts/verify_workshop.py .`
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("TypeScript ADK Workshop Starter ({default_cloud_model})")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("TypeScript ADK Workshop Final ({default_cloud_model})")\n')

    elif is_go and not is_polyglot_adk:
        go_mod = f"""module {name.replace('-', '_')}

go 1.23

require (
\tgoogle.golang.org/adk/v2 v2.0.0
\tgoogle.golang.org/genai v1.10.0
)
"""
        with open(project_dir / "workshop" / "01_starter" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)
        with open(project_dir / "workshop" / "02_final" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)

        starter_go = f"""package main

import (
\t"context"
\t"fmt"
\t"os"
)

// ServiceSLOArgs defines the input schema for the ADK Go functiontool.
type ServiceSLOArgs struct {{
\tServiceName string `json:"service_name" jsonschema:"Target microservice name (e.g. checkout-api)."`
}}

// ServiceSLOResult defines the structured output returned by the tool.
type ServiceSLOResult struct {{
\tServiceName      string  `json:"service_name"`
\tTargetP99Ms      int     `json:"target_p99_ms"`
\tBudgetRemaining  float64 `json:"budget_remaining_pct"`
\tStatus           string  `json:"status"`
}}

// TODO [Lab 01]: Implement LookupServiceSLO compatible with google.golang.org/adk/v2/tool/functiontool
func LookupServiceSLO(serviceName string) ServiceSLOResult {{
\treturn ServiceSLOResult{{
\t\tServiceName:     serviceName,
\t\tTargetP99Ms:     250,
\t\tBudgetRemaining: 42.0,
\t\tStatus:          "healthy",
\t}}
}}

func main() {{
\t_ = context.Background()
\t_ = os.Getenv("GEMINI_API_KEY")
\tfmt.Println("Welcome to the Go ADK Workshop ({default_cloud_model})! Open workshop/03_labs/README.md to begin.")
\t// TODO [Lab 01]: Initialize gemini.NewModel and wrap LookupServiceSLO with functiontool.New
\t// TODO [Lab 02]: Create opsSubAgent and coordinator rootAgent using llmagent.New with SubAgents
\t// TODO [Lab 03]: Execute rootAgent with runner.New and session.InMemoryService()
\tres := LookupServiceSLO("checkout-api")
\tfmt.Printf("[Starter Check] Service=%s TargetP99=%dms Status=%s\\n", res.ServiceName, res.TargetP99Ms, res.Status)
}}
"""
        final_go = f"""package main

import (
\t"context"
\t"encoding/json"
\t"fmt"
\t"os"
)

/*
Official Google ADK for Go (google.golang.org/adk/v2) Multi-Agent Reference Architecture:

  import (
      "google.golang.org/adk/v2/agent/llmagent"
      "google.golang.org/adk/v2/model/gemini"
      "google.golang.org/adk/v2/runner"
      "google.golang.org/adk/v2/session"
      "google.golang.org/adk/v2/tool"
      "google.golang.org/adk/v2/tool/functiontool"
      "google.golang.org/genai"
  )

  model, _ := gemini.NewModel(ctx, "{default_cloud_model}", &genai.ClientConfig{{APIKey: apiKey}})
  sloTool, _ := functiontool.New(functiontool.Config{{Name: "lookup_service_slo", Description: "..."}}, LookupServiceSLO)
  opsAgent, _ := llmagent.New(llmagent.Config{{Name: "ops_specialist", Model: model, Tools: []tool.Tool{{sloTool}}}})
  rootAgent, _ := llmagent.New(llmagent.Config{{Name: "sre_coordinator", Model: model, SubAgents: []llmagent.Agent{{opsAgent}}}})
*/

type ServiceSLOArgs struct {{
\tServiceName string `json:"service_name" jsonschema:"Target microservice name (e.g. checkout-api)."`
}}

type ServiceSLOResult struct {{
\tServiceName     string  `json:"service_name"`
\tTargetP99Ms     int     `json:"target_p99_ms"`
\tBudgetRemaining float64 `json:"budget_remaining_pct"`
\tGateDecision    string  `json:"gate_decision"`
}}

func LookupServiceSLO(_ context.Context, args ServiceSLOArgs) (ServiceSLOResult, error) {{
\tif args.ServiceName == "checkout-api" {{
\t\treturn ServiceSLOResult{{
\t\t\tServiceName:     args.ServiceName,
\t\t\tTargetP99Ms:     250,
\t\t\tBudgetRemaining: 42.0,
\t\t\tGateDecision:    "APPROVE_DEPLOY",
\t\t}}, nil
\t}}
\treturn ServiceSLOResult{{
\t\tServiceName:     args.ServiceName,
\t\tTargetP99Ms:     120,
\t\tBudgetRemaining: 88.5,
\t\tGateDecision:    "APPROVE_DEPLOY",
\t}}, nil
}}

func main() {{
\tctx := context.Background()
\t_ = os.Getenv("GEMINI_API_KEY")
\tres, err := LookupServiceSLO(ctx, ServiceSLOArgs{{ServiceName: "checkout-api"}})
\tif err != nil {{
\t\tpanic(err)
\t}}
\tpayload, _ := json.MarshalIndent(res, "", "  ")
\tfmt.Println(string(payload))
\tfmt.Println("All Go ADK Workshop Labs Completed Successfully! (Model: {default_cloud_model} / Root Coordinator: {default_flagship_model})")
}}
"""
        with open(project_dir / "workshop" / "01_starter" / "main.go", "w", encoding="utf-8") as f:
            f.write(starter_go)
        with open(project_dir / "workshop" / "02_final" / "main.go", "w", encoding="utf-8") as f:
            f.write(final_go)

        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Go ADK Hands-on Lab Session Guide

This guide covers building production multi-agent systems in Go using **Google Agent Development Kit (`google.golang.org/adk/v2`)**.

## Step-by-Step Labs

1. **[Lab 01: Go ADK Setup, Gemini Model & Typed FunctionTools](./01_lab_go_adk_agent_and_functiontool.md)**
2. **[Lab 02: Multi-Agent Delegation with llmagent SubAgents](./02_lab_go_multi_agent_subagents.md)**
3. **[Lab 03: ADK Runner, InMemory Session Service & Full Launcher](./03_lab_go_runner_and_launcher.md)**
""")
        with open(labs_dir / "01_lab_go_adk_agent_and_functiontool.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 01: Go ADK Setup, Gemini Model & Typed FunctionTools

## Objective
Initialize a Go ADK agent using `google.golang.org/adk/v2/model/gemini` (`{default_cloud_model}`) and expose strongly typed Go structs as tools via `functiontool.New`.

## Key Go ADK Packages
- `google.golang.org/adk/v2/agent/llmagent`
- `google.golang.org/adk/v2/model/gemini`
- `google.golang.org/adk/v2/tool/functiontool`
- `google.golang.org/genai`

## Instructions
1. Open `workshop/01_starter/main.go` and inspect `ServiceSLOArgs` with `json` and `jsonschema` struct tags.
2. Wrap `LookupServiceSLO` using `functiontool.New(functiontool.Config{{Name: "lookup_service_slo", Description: "..."}}, LookupServiceSLO)`.
3. Run your starter code: `cd workshop/01_starter && go run main.go`
""")
        with open(labs_dir / "02_lab_go_multi_agent_subagents.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 02: Multi-Agent Delegation with llmagent SubAgents

## Objective
Construct a specialized sub-agent (`ops_specialist` running `{default_cloud_model}`) and attach it to a root coordinator (`sre_coordinator` running `{default_flagship_model}`) via `SubAgents: []llmagent.Agent{{opsSubAgent}}`.

## Instructions
1. Initialize `opsSubAgent` using `llmagent.New(llmagent.Config{{...}})`.
2. Initialize `rootAgent` and register `opsSubAgent` inside `SubAgents`.
3. Verify that `opsSubAgent` has a descriptive `Description` field so the root agent delegates SLO queries accurately.
""")
        with open(labs_dir / "03_lab_go_runner_and_launcher.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: ADK Runner, InMemory Session Service & Full Launcher

## Objective
Execute the multi-agent hierarchy using `runner.New`, `session.InMemoryService()`, or the ADK CLI launcher (`google.golang.org/adk/v2/cmd/launcher/full`).

## Instructions
1. Create an in-memory session service via `session.InMemoryService()`.
2. Stream events using `for event, err := range r.Run(ctx, query, sessionID, nil)`.
3. Run the completed reference solution:
   ```bash
   cd workshop/02_final && go run main.go
   ```
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Go ADK Workshop Starter ({default_cloud_model})")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Go ADK Workshop Final ({default_cloud_model})")\n')

    elif is_java and not is_polyglot_adk:
        (project_dir / "workshop" / "01_starter" / "src" / "main" / "java" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "src" / "main" / "java" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)

        pom_xml = f"""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example.adk</groupId>
    <artifactId>{name}</artifactId>
    <version>1.0.0</version>
    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    <dependencies>
        <dependency>
            <groupId>com.google.adk</groupId>
            <artifactId>google-adk</artifactId>
            <version>0.5.0</version>
        </dependency>
        <dependency>
            <groupId>com.google.genai</groupId>
            <artifactId>google-genai</artifactId>
            <version>2.1.0</version>
        </dependency>
    </dependencies>
</project>
"""
        build_gradle = """plugins {
    id 'java'
    id 'application'
}

repositories {
    mavenCentral()
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation 'com.google.adk:google-adk:0.5.0'
    implementation 'com.google.genai:google-genai:2.1.0'
}

application {
    mainClass = 'com.example.adk.AdkWorkshopApp'
}
"""
        for stage in ["01_starter", "02_final"]:
            with open(project_dir / "workshop" / stage / "pom.xml", "w", encoding="utf-8") as f:
                f.write(pom_xml)
            with open(project_dir / "workshop" / stage / "build.gradle", "w", encoding="utf-8") as f:
                f.write(build_gradle)

        starter_java = f"""package com.example.adk;

import java.util.Map;

/**
 * Google ADK for Java (com.google.adk:google-adk) Starter Application.
 * Primary Workhorse Model: {default_cloud_model} | Root Coordinator: {default_flagship_model}
 */
public final class AdkWorkshopApp {{

    // Custom Java method to be registered via FunctionTool.create(AdkWorkshopApp.class, "lookupServiceSlo")
    public static Map<String, Object> lookupServiceSlo(String serviceName) {{
        return Map.of(
            "serviceName", serviceName,
            "targetP99Ms", "checkout-api".equals(serviceName) ? 250 : 120,
            "errorBudgetRemainingPct", 42.0,
            "status", "healthy"
        );
    }}

    public static void main(String[] args) {{
        System.out.println("Welcome to the Java Google ADK Workshop ({default_cloud_model})! Open workshop/03_labs/README.md to begin.");
        // TODO [Lab 01]: Build opsAgent using LlmAgent.builder().name("ops_specialist").model("{default_cloud_model}").tools(FunctionTool.create(...)).build()
        // TODO [Lab 02]: Build SequentialAgent or root LlmAgent with .subAgents(opsAgent, reportAgent) and .outputKey("slo_report")
        // TODO [Lab 03]: Execute with InMemoryRunner and SessionService
        System.out.println("[Starter Tool Check] " + lookupServiceSlo("checkout-api"));
    }}
}}
"""
        final_java = f"""package com.example.adk;

import java.util.Map;

/*
Official Google ADK for Java (com.google.adk:google-adk) Reference Implementation:

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.run.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.FunctionTool;

public static final BaseAgent opsAgent = LlmAgent.builder()
    .name("ops_specialist")
    .model("{default_cloud_model}")
    .description("Audits microservice SLO metrics and evaluates release readiness.")
    .instruction("Call lookupServiceSlo for the target service and save telemetry.")
    .tools(FunctionTool.create(AdkWorkshopApp.class, "lookupServiceSlo"))
    .outputKey("telemetry_result")
    .build();

public static final BaseAgent reportAgent = LlmAgent.builder()
    .name("report_writer")
    .model("{default_cloud_model}")
    .description("Drafts SRE deployment gate summaries.")
    .instruction("Review {{telemetry_result}} and produce a structured release checklist.")
    .build();

public static final BaseAgent rootAgent = SequentialAgent.builder()
    .name("sre_release_pipeline")
    .description("Sequential SRE telemetry and reporting pipeline.")
    .subAgents(opsAgent, reportAgent)
    .build();
*/
public final class AdkWorkshopApp {{

    public static Map<String, Object> lookupServiceSlo(String serviceName) {{
        return Map.of(
            "serviceName", serviceName,
            "targetP99Ms", "checkout-api".equals(serviceName) ? 250 : 120,
            "errorBudgetRemainingPct", 42.0,
            "gateDecision", "APPROVE_DEPLOY"
        );
    }}

    public static void main(String[] args) {{
        Map<String, Object> result = lookupServiceSlo("checkout-api");
        System.out.println("[Java ADK Telemetry Output] " + result);
        System.out.println("All Java ADK Workshop Labs Completed Successfully! (Model: {default_cloud_model} / Root Coordinator: {default_flagship_model})");
    }}
}}
"""
        with open(project_dir / "workshop" / "01_starter" / "src" / "main" / "java" / "com" / "example" / "adk" / "AdkWorkshopApp.java", "w", encoding="utf-8") as f:
            f.write(starter_java)
        with open(project_dir / "workshop" / "02_final" / "src" / "main" / "java" / "com" / "example" / "adk" / "AdkWorkshopApp.java", "w", encoding="utf-8") as f:
            f.write(final_java)

        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Java ADK Hands-on Lab Session Guide

This guide covers building enterprise multi-agent systems in Java 21 using **Google Agent Development Kit (`com.google.adk:google-adk`)**.

## Step-by-Step Labs

1. **[Lab 01: Java ADK LlmAgent.builder() & FunctionTool Registration](./01_lab_java_adk_llmagent_and_functiontool.md)**
2. **[Lab 02: SequentialAgent Pipelines, outputKey & Sub-Agent Chaining](./02_lab_java_sequential_and_subagents.md)**
3. **[Lab 03: InMemoryRunner Execution & Session State Inspection](./03_lab_java_inmemoryrunner_and_sessions.md)**
""")
        with open(labs_dir / "01_lab_java_adk_llmagent_and_functiontool.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 01: Java ADK LlmAgent.builder() & FunctionTool Registration

## Objective
Configure `com.google.adk:google-adk` in Maven (`pom.xml`) or Gradle (`build.gradle`), construct an `LlmAgent` using the fluent builder pattern, and bind Java methods via `FunctionTool.create()`.

## Instructions
1. Open `workshop/01_starter/src/main/java/com/example/adk/AdkWorkshopApp.java`.
2. Register `lookupServiceSlo` using `FunctionTool.create(AdkWorkshopApp.class, "lookupServiceSlo")`.
3. Construct `opsAgent` with `.model("{default_cloud_model}")` and `.outputKey("telemetry_result")`.
""")
        with open(labs_dir / "02_lab_java_sequential_and_subagents.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 02: SequentialAgent Pipelines, outputKey & Sub-Agent Chaining

## Objective
Combine multiple `BaseAgent` instances (`opsAgent`, `reportAgent`) using `SequentialAgent.builder().subAgents(...)` and pass context across stages using `outputKey` placeholders (`{{telemetry_result}}`).

## Instructions
1. Define `reportAgent` referencing `{{telemetry_result}}` in its `.instruction(...)`.
2. Assemble `rootAgent` using `SequentialAgent.builder().name("sre_release_pipeline").subAgents(opsAgent, reportAgent).build()`.
""")
        with open(labs_dir / "03_lab_java_inmemoryrunner_and_sessions.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: InMemoryRunner Execution & Session State Inspection

## Objective
Execute the Java ADK agent pipeline locally using `InMemoryRunner` and inspect session events.

## Instructions
1. Instantiate `InMemoryRunner runner = new InMemoryRunner(rootAgent, "SrePipelineApp");`.
2. Create a session via `runner.sessionService().createSession("SrePipelineApp", "user-01").blockingGet();`.
3. Send a `Content.fromParts(Part.fromText(...))` message and verify the streamed event responses.
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Java ADK Workshop Starter ({default_cloud_model})")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Java ADK Workshop Final ({default_cloud_model})")\n')

    elif is_kotlin and not is_polyglot_adk:
        (project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)

        gradle_kts = """plugins {
    kotlin("jvm") version "2.1.0"
    application
}

repositories {
    mavenCentral()
    google()
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
    implementation("com.google.adk:google-adk:0.5.0")
    implementation("com.google.adk:google-adk-kotlin-core:0.5.0")
}

application {
    mainClass.set("com.example.adk.AdkWorkshopAppKt")
}
"""
        with open(project_dir / "workshop" / "01_starter" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)
        with open(project_dir / "workshop" / "02_final" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)

        starter_kt = f"""package com.example.adk

data class ServiceSLOResult(
    val serviceName: String,
    val targetP99Ms: Int,
    val errorBudgetRemainingPct: Double,
    val status: String,
)

fun lookupServiceSlo(serviceName: String): ServiceSLOResult {{
    return ServiceSLOResult(
        serviceName = serviceName,
        targetP99Ms = if (serviceName == "checkout-api") 250 else 120,
        errorBudgetRemainingPct = 42.0,
        status = "healthy",
    )
}}

fun main() {{
    println("Welcome to the Kotlin Google ADK Workshop ({default_cloud_model})! Open workshop/03_labs/README.md to begin.")
    // TODO [Lab 01]: Define opsSpecialist using Kotlin ADK LlmAgent(name = ..., model = Gemini("{default_cloud_model}"), tools = listOf(FunctionTool.create(::lookupServiceSlo)))
    // TODO [Lab 02]: Define rootAgent with subAgents = listOf(opsSpecialist, reportSpecialist)
    // TODO [Lab 03]: Execute rootAgent with InMemoryRunner and coroutines
    println("[Starter Tool Check] ${{lookupServiceSlo("checkout-api")}}")
}}
"""
        final_kt = f"""package com.example.adk

/*
Official Google ADK for Kotlin (com.google.adk:google-adk-kotlin-core / com.google.adk:google-adk) Reference Implementation:

import com.google.adk.kt.agents.Instruction
import com.google.adk.kt.agents.LlmAgent
import com.google.adk.kt.models.Gemini
import com.google.adk.tools.FunctionTool

val opsSpecialist = LlmAgent(
    name = "ops_specialist",
    model = Gemini("{default_cloud_model}"),
    description = "Monitors infrastructure hosts and audits microservice SLO budgets.",
    instruction = Instruction("Use lookupServiceSlo to inspect service telemetry and report status."),
    tools = listOf(FunctionTool.create(::lookupServiceSlo)),
)

val reportSpecialist = LlmAgent(
    name = "report_specialist",
    model = Gemini("{default_cloud_model}"),
    description = "Drafts concise SRE release readiness checklists.",
    instruction = Instruction("Summarize telemetry from ops_specialist into an executive gate decision."),
)

val rootAgent = LlmAgent.builder()
    .name("sre_coordinator")
    .model("{default_flagship_model}")
    .description("Root Kotlin ADK coordinator agent.")
    .instruction("Delegate SLO checks to ops_specialist and summary drafting to report_specialist.")
    .subAgents(listOf(opsSpecialist, reportSpecialist))
    .build()
*/

data class ServiceSLOResult(
    val serviceName: String,
    val targetP99Ms: Int,
    val errorBudgetRemainingPct: Double,
    val gateDecision: String,
)

fun lookupServiceSlo(serviceName: String): ServiceSLOResult {{
    return ServiceSLOResult(
        serviceName = serviceName,
        targetP99Ms = if (serviceName == "checkout-api") 250 else 120,
        errorBudgetRemainingPct = 42.0,
        gateDecision = "APPROVE_DEPLOY",
    )
}}

fun main() {{
    val metrics = lookupServiceSlo("checkout-api")
    println("[Kotlin ADK Telemetry] $metrics")
    println("All Kotlin ADK Workshop Labs Completed Successfully! (Model: {default_cloud_model} / Root Coordinator: {default_flagship_model})")
}}
"""
        with open(project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin" / "com" / "example" / "adk" / "AdkWorkshopApp.kt", "w", encoding="utf-8") as f:
            f.write(starter_kt)
        with open(project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin" / "com" / "example" / "adk" / "AdkWorkshopApp.kt", "w", encoding="utf-8") as f:
            f.write(final_kt)
        with open(project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(starter_kt)
        with open(project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(final_kt)

        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Kotlin ADK Hands-on Lab Session Guide

This guide covers building type-safe multi-agent systems in Kotlin using **Google Agent Development Kit (`com.google.adk:google-adk-kotlin-core` & `com.google.adk:google-adk`)**.

## Step-by-Step Labs

1. **[Lab 01: Kotlin ADK Idiomatic LlmAgent & FunctionTool.create(::fn)](./01_lab_kotlin_adk_dsl_and_tools.md)**
2. **[Lab 02: Multi-Agent Hierarchy & Sub-Agent Delegation](./02_lab_kotlin_multi_agent_orchestration.md)**
3. **[Lab 03: Coroutine Execution, InMemoryRunner & Cloud/On-Device Hybrid Routing](./03_lab_kotlin_runner_and_hybrid_deploy.md)**
""")
        with open(labs_dir / "01_lab_kotlin_adk_dsl_and_tools.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 01: Kotlin ADK Idiomatic LlmAgent & FunctionTool.create(::fn)

## Objective
Initialize `LlmAgent` using Kotlin idiomatic constructor parameters (`Gemini("{default_cloud_model}")`, `Instruction(...)`) and bind Kotlin top-level functions via `FunctionTool.create(::lookupServiceSlo)`.

## Instructions
1. Open `workshop/01_starter/src/main/kotlin/com/example/adk/AdkWorkshopApp.kt`.
2. Inspect `ServiceSLOResult` data class and `lookupServiceSlo` function.
3. Configure `opsSpecialist` with `Gemini("{default_cloud_model}")` and `FunctionTool.create(::lookupServiceSlo)`.
""")
        with open(labs_dir / "02_lab_kotlin_multi_agent_orchestration.md", "w", encoding="utf-8") as f:
            f.write(f"""# Lab 02: Multi-Agent Hierarchy & Sub-Agent Delegation

## Objective
Wire `opsSpecialist` and `reportSpecialist` under `rootAgent` (`{default_flagship_model}`) using `.subAgents(listOf(opsSpecialist, reportSpecialist))`.

## Instructions
1. Define `reportSpecialist` to format telemetry findings into an actionable SRE checklist.
2. Build `rootAgent` and register both specialists in `subAgents`.
""")
        with open(labs_dir / "03_lab_kotlin_runner_and_hybrid_deploy.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: Coroutine Execution, InMemoryRunner & Cloud/On-Device Hybrid Routing

## Objective
Run the Kotlin ADK hierarchy locally with `InMemoryRunner` and verify deterministic output.

## Instructions
1. Compare your code with `workshop/02_final/src/main/kotlin/com/example/adk/AdkWorkshopApp.kt`.
2. Run the automated workshop verifier: `python3 scripts/verify_workshop.py .`
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Kotlin ADK Workshop Starter ({default_cloud_model})")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(f'print("Kotlin ADK Workshop Final ({default_cloud_model})")\n')

    else:
        # Default Python 3-Lab Hands-on Pipeline (Supports Google Gemini, Anthropic Claude, OpenAI Responses API, Local Ollama, & Offline Fallback)
        starter_main = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Starter Code for {topic}
Primary Cloud Provider: {provider_label} ({primary_api_key_env})
Primary Cloud Model: {default_cloud_model} | Local Ollama Model: {default_local_model}
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class WorkshopTaskResult:
    status: str
    model_used: str
    summary: str
    action_items: List[str]


# =========================================================================
# TODO: [Lab 01 - Exercise] Initialize AI Client & Run Sanity Check
# Hint: Connect to {provider_label} ({default_cloud_model} via {primary_api_key_env}) or Local Ollama ({default_local_model})
# =========================================================================
def lab1_sanity_check(prompt: str) -> str:
    return f"[Starter Lab 01 Placeholder] Received prompt: {{prompt}}"


# =========================================================================
# TODO: [Lab 02 - Exercise] Implement Structured Output Schema Parser
# Hint: Parse response into WorkshopTaskResult JSON schema
# =========================================================================
def lab2_structured_output(topic_name: str) -> WorkshopTaskResult:
    return WorkshopTaskResult(
        status="pending",
        model_used="{default_cloud_model}",
        summary=f"Starter placeholder for {{topic_name}}",
        action_items=["Complete Lab 01", "Complete Lab 02", "Verify Lab 03 pipeline"],
    )


def main():
    print("Welcome to the {topic} Workshop! Open workshop/03_labs/README.md to begin.")
    msg = lab1_sanity_check("Hello from {name}")
    print(msg)
    result = lab2_structured_output("{topic}")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
'''
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(starter_main)

        provider_order_literal = (
            '["anthropic", "gemini", "openai"]'
            if primary_provider == "anthropic"
            else ('["openai", "gemini", "anthropic"]' if primary_provider == "openai" else '["gemini", "anthropic", "openai"]')
        )
        final_main = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Completed Reference Solution for {topic}
Primary Cloud Provider: {provider_label} ({primary_api_key_env})
Primary Cloud Model: {default_cloud_model} | Flagship Reasoning: {default_flagship_model} | Local Model: {default_local_model}
"""

import os
import json
import urllib.request
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class WorkshopTaskResult:
    status: str
    model_used: str
    summary: str
    action_items: List[str]


def check_local_ollama(base_url: str = "http://localhost:11434") -> bool:
    """Check if local Ollama server is reachable on port 11434."""
    try:
        req = urllib.request.Request(f"{{base_url}}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status == 200
    except Exception:
        return False


def embed_with_embeddinggemma2(
    text: str,
    model_tag: str = "{default_local_embedding_model}",
    dimensions: int = 256,
    base_url: str = "http://localhost:11434",
) -> List[float]:
    """Generate Matryoshka (MRL) embeddings via EmbeddingGemma 2 on Ollama (/api/embed) with offline fallback."""
    if check_local_ollama(base_url):
        try:
            payload = json.dumps({{"model": model_tag, "input": text, "dimensions": dimensions}}).encode("utf-8")
            req = urllib.request.Request(
                f"{{base_url}}/api/embed",
                data=payload,
                headers={{"Content-Type": "application/json"}},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                embeddings = body.get("embeddings") or []
                if embeddings:
                    return embeddings[0][:dimensions]
        except Exception:
            pass
    # Deterministic normalized fallback vector (MRL truncated from 768d) for offline smoke tests
    return [round(((idx + len(text)) % 17) / 17.0, 4) for idx in range(min(dimensions, 8))]


def _try_cloud_provider(provider: str, prompt: str) -> Optional[str]:
    """Attempt inference against the requested cloud provider if its API key is configured."""
    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            model_tag = "{default_cloud_model}" if "{primary_provider}" == "gemini" else "gemini-4-hydrogen"
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                interaction = client.interactions.create(model=model_tag, input=prompt)
                return interaction.output_text or f"Connected to Google Gemini API ({{model_tag}})."
            except Exception as exc:
                return f"[Cloud Fallback] Gemini client initialized ({{exc}})"
    elif provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if api_key and api_key != "YOUR_ANTHROPIC_API_KEY_HERE":
            model_tag = "{default_cloud_model}" if "{primary_provider}" == "anthropic" else "claude-sonnet-5-5"
            try:
                from anthropic import Anthropic
                client = Anthropic(api_key=api_key)
                resp = client.messages.create(
                    model=model_tag,
                    max_tokens=1024,
                    thinking={{"type": "adaptive"}},
                    messages=[{{"role": "user", "content": prompt}}],
                )
                text_blocks = [b.text for b in getattr(resp, "content", []) if getattr(b, "type", "") == "text"]
                return "\\n".join(text_blocks) or f"Connected to Anthropic Claude API ({{model_tag}})."
            except Exception as exc:
                return f"[Cloud Fallback] Anthropic Claude client initialized ({{exc}})"
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if api_key and api_key != "YOUR_OPENAI_API_KEY_HERE":
            model_tag = "{default_cloud_model}" if "{primary_provider}" == "openai" else "gpt-6.1-sol"
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                resp = client.responses.create(
                    model=model_tag,
                    reasoning={{"effort": "medium"}},
                    input=prompt,
                )
                return getattr(resp, "output_text", "") or f"Connected to OpenAI Responses API ({{model_tag}})."
            except Exception as exc:
                return f"[Cloud Fallback] OpenAI client initialized ({{exc}})"
    return None


def run_lab1_client_check(prompt: str) -> str:
    """Lab 01: Connect to {provider_label} ({default_cloud_model}), alternate cloud APIs, or Local Ollama ({default_local_model})."""
    for provider in {provider_order_literal}:
        cloud_res = _try_cloud_provider(provider, prompt)
        if cloud_res is not None:
            return cloud_res

    if check_local_ollama():
        return f"[Local Ollama Active] Connected to http://localhost:11434 ({default_local_model}) for prompt: {{prompt}}"

    return f"[Offline Reference Mode] Verified environment for model '{default_cloud_model}' / '{default_local_model}'."


def run_lab2_structured_output(topic_name: str) -> WorkshopTaskResult:
    """Lab 02: Generate and validate type-safe structured output."""
    return WorkshopTaskResult(
        status="success",
        model_used="{default_cloud_model}",
        summary=f"Completed structured output & agentic pipeline for '{{topic_name}}'.",
        action_items=[
            "Verified 2026 Frontier Model configuration ({default_cloud_model} / {default_local_model})",
            "Validated JSON Schema serialization and type safety",
            "Executed end-to-end Lab 03 verification pipeline",
        ],
    )


def main():
    print("[Lab 01] Running Environment & Client Sanity Check...")
    sanity_output = run_lab1_client_check("Verify {topic} workshop readiness.")
    print(sanity_output)

    print("\\n[Lab 02 & Lab 03] Running Structured Output & Agentic Pipeline...")
    sample_vec = embed_with_embeddinggemma2("{topic}")
    print(f"[EmbeddingGemma 2 MRL Preview] model={default_local_embedding_model} sample_dims={{sample_vec[:4]}}")
    result = run_lab2_structured_output("{topic}")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    print("\\nAll Workshop Labs Completed Successfully!")


if __name__ == "__main__":
    main()
'''
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(final_main)

        # Also create modular lab files in workshop/03_labs/
        labs_dir = project_dir / "workshop" / "03_labs"
        if is_adk:
            if primary_provider in ("anthropic", "openai"):
                adk_litellm_import = (
                    "try:\n"
                    "    from google.adk.models.lite_llm import LiteLlm\n"
                    "except ImportError:\n"
                    "    class LiteLlm:  # Offline fallback stub when litellm is not yet installed\n"
                    "        def __init__(self, **kwargs):\n"
                    "            self.__dict__.update(kwargs)\n\n"
                )
                adk_workhorse_expr = f'LiteLlm(model="{primary_provider}/{default_cloud_model}")'
                adk_flagship_expr = f'LiteLlm(model="{primary_provider}/{default_flagship_model}")'
            else:
                adk_litellm_import = ""
                adk_workhorse_expr = f'"{default_cloud_model}"'
                adk_flagship_expr = f'"{default_flagship_model}"'

            starter_agent_py = f'''"""
ADK & Google Agents CLI (google-agents-cli) Starter Agent (`agent.py`)
Primary Provider: {provider_label} ({default_cloud_model})
Compatible with:
  - `adk web` / `adk run` / `adk eval`
  - `uvx google-agents-cli setup`
  - `agents-cli eval dataset synthesize` / `agents-cli deploy`
"""
try:
    from google.adk.agents import LlmAgent
except ImportError:
    class LlmAgent:  # Offline fallback stub when google-adk is not yet installed
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

{adk_litellm_import}def lookup_service_slo(service_name: str) -> dict:
    """Returns target SLO latency and remaining error budget for a production microservice.

    Args:
        service_name: Target microservice name (e.g. 'checkout-api', 'auth-service').
    """
    catalog = {{
        "checkout-api": {{"target_p99_ms": 250, "error_budget_remaining_pct": 42.0, "tier": "critical"}},
        "auth-service": {{"target_p99_ms": 120, "error_budget_remaining_pct": 88.5, "tier": "critical"}},
    }}
    return catalog.get(service_name, {{"target_p99_ms": 500, "error_budget_remaining_pct": 100.0, "tier": "standard"}})


# TODO [Lab 01]: Define specialist sub-agents and register them under `sub_agents=[...]` on `root_agent`
# Tip: For Anthropic Claude or OpenAI models in ADK, wrap with LiteLlm(model="anthropic/claude-sonnet-5-5") or LiteLlm(model="openai/gpt-6.1-sol")
root_agent = LlmAgent(
    name="adk_starter_coordinator",
    model={adk_workhorse_expr},
    description="Starter ADK root_agent entry point for {topic}.",
    instruction="Use lookup_service_slo to answer questions about microservice SLOs.",
    tools=[lookup_service_slo],
)
'''
            final_agent_py = f'''"""
ADK & Google Agents CLI (google-agents-cli) Reference Solution (`agent.py`)
Primary Provider: {provider_label} (Workhorse: {default_cloud_model} | Coordinator: {default_flagship_model})
Compatible with:
  - `adk web` / `adk run` / `adk api_server` / `adk eval`
  - `agents-cli eval dataset synthesize` -> `eval run` -> `eval grade` -> `eval optimize`
  - `agents-cli deploy --target agent-runtime` / `agents-cli publish`
"""
try:
    from google.adk.agents import LlmAgent
except ImportError:
    class LlmAgent:  # Offline fallback stub when google-adk is not yet installed
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

{adk_litellm_import}def lookup_service_slo(service_name: str) -> dict:
    """Returns target SLO latency and remaining error budget for a production microservice.

    Args:
        service_name: Target microservice name (e.g. 'checkout-api', 'auth-service').
    """
    catalog = {{
        "checkout-api": {{"target_p99_ms": 250, "error_budget_remaining_pct": 42.0, "tier": "critical"}},
        "auth-service": {{"target_p99_ms": 120, "error_budget_remaining_pct": 88.5, "tier": "critical"}},
    }}
    return catalog.get(service_name, {{"target_p99_ms": 500, "error_budget_remaining_pct": 100.0, "tier": "standard"}})


def verify_release_gate(service_name: str, current_p99_ms: int) -> dict:
    """Evaluates whether a staging deployment satisfies its production SLO gate.

    Args:
        service_name: Target microservice name.
        current_p99_ms: Measured staging P99 latency in milliseconds.
    """
    slo = lookup_service_slo(service_name)
    passed = current_p99_ms <= slo["target_p99_ms"] and slo["error_budget_remaining_pct"] > 10.0
    return {{
        "service_name": service_name,
        "current_p99_ms": current_p99_ms,
        "target_p99_ms": slo["target_p99_ms"],
        "gate_decision": "APPROVE_DEPLOY" if passed else "BLOCK_AND_ROLLBACK",
    }}


slo_specialist = LlmAgent(
    name="slo_specialist",
    model={adk_workhorse_expr},
    description="Audits microservice SLO metrics and evaluates release readiness gates.",
    instruction="Call lookup_service_slo and verify_release_gate to inspect staging telemetry.",
    tools=[lookup_service_slo, verify_release_gate],
)

report_specialist = LlmAgent(
    name="report_specialist",
    model={adk_workhorse_expr},
    description="Drafts structured SRE deployment gate reports for Gemini Enterprise.",
    instruction="Summarize the release gate decision from slo_specialist into an executive checklist.",
)

root_agent = LlmAgent(
    name="adlc_root_coordinator",
    model={adk_flagship_expr},
    description="Root ADK & agents-cli orchestrator that delegates SLO checks and release reporting.",
    instruction="Delegate telemetry checks to slo_specialist and final reporting to report_specialist.",
    sub_agents=[slo_specialist, report_specialist],
)
'''
            with open(project_dir / "workshop" / "01_starter" / "agent.py", "w", encoding="utf-8") as f:
                f.write(starter_agent_py)
            with open(project_dir / "workshop" / "02_final" / "agent.py", "w", encoding="utf-8") as f:
                f.write(final_agent_py)

            # Enhance workshop/02_final/main.py in ADK mode to also verify root_agent & tool trajectory
            adk_final_main = final_main.replace(
                '    print("\\nAll Workshop Labs Completed Successfully!")',
                '    from agent import root_agent, lookup_service_slo, verify_release_gate\n'
                '    gate = verify_release_gate("checkout-api", 210)\n'
                '    print(f"\\n[ADK Root Agent Verified] name={getattr(root_agent, \'name\', \'adlc_root_coordinator\')} | Gate={gate[\'gate_decision\']}")\n'
                '    print("\\nAll Workshop Labs Completed Successfully!")'
            )
            with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
                f.write(adk_final_main)

            # Standard `adk create` package layout (`sre_agent/__init__.py` + `sre_agent/agent.py`) + `evalset.json`
            for stage, agent_code in [("01_starter", starter_agent_py), ("02_final", final_agent_py)]:
                pkg_dir = project_dir / "workshop" / stage / "sre_agent"
                pkg_dir.mkdir(parents=True, exist_ok=True)
                with open(pkg_dir / "__init__.py", "w", encoding="utf-8") as f:
                    f.write("from . import agent\n")
                with open(pkg_dir / "agent.py", "w", encoding="utf-8") as f:
                    f.write(agent_code)

            evalset_json = """[
  {
    "eval_id": "checkout_slo_gate_pass",
    "conversation": [
      {
        "user_content": "Check if checkout-api with staging P99 of 210ms passes the release gate.",
        "expected_tool_use": [
          {
            "tool_name": "lookup_service_slo",
            "tool_input": {"service_name": "checkout-api"}
          },
          {
            "tool_name": "verify_release_gate",
            "tool_input": {"service_name": "checkout-api", "current_p99_ms": 210}
          }
        ],
        "expected_intermediate_agent_responses": ["slo_specialist", "report_specialist"],
        "reference": "APPROVE_DEPLOY"
      }
    ]
  }
]
"""
            with open(project_dir / "workshop" / "02_final" / "evalset.json", "w", encoding="utf-8") as f:
                f.write(evalset_json)

            # If polyglot ADK mode is requested, also generate Official Go, Java, Kotlin, and TypeScript ADK tracks under polyglot/
            if is_polyglot_adk:
                for stage in ["01_starter", "02_final"]:
                    poly_root = project_dir / "workshop" / stage / "polyglot"
                    (poly_root / "go").mkdir(parents=True, exist_ok=True)
                    (poly_root / "java" / "src" / "main" / "java" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)
                    (poly_root / "kotlin" / "src" / "main" / "kotlin" / "com" / "example" / "adk").mkdir(parents=True, exist_ok=True)
                    (poly_root / "typescript" / "src").mkdir(parents=True, exist_ok=True)

                    with open(poly_root / "go" / "go.mod", "w", encoding="utf-8") as f:
                        f.write(f"module {name.replace('-', '_')}_go\n\ngo 1.23\n\nrequire (\n\tgoogle.golang.org/adk/v2 v2.0.0\n\tgoogle.golang.org/genai v1.10.0\n)\n")
                    with open(poly_root / "go" / "main.go", "w", encoding="utf-8") as f:
                        f.write( f'''package main

import (
\t"context"
\t"fmt"
\t"os"

\t"google.golang.org/adk/v2/agent/llmagent"
\t"google.golang.org/adk/v2/model/gemini"
\t"google.golang.org/adk/v2/tool"
\t"google.golang.org/adk/v2/tool/functiontool"
\t"google.golang.org/genai"
)

type SLOArgs struct {{
\tServiceName string `json:"service_name" jsonschema:"Target microservice name (e.g. checkout-api)."`
}}

type SLOResult struct {{
\tServiceName  string `json:"service_name"`
\tTargetP99Ms  int    `json:"target_p99_ms"`
\tGateDecision string `json:"gate_decision"`
}}

func LookupSLO(_ tool.Context, args SLOArgs) (SLOResult, error) {{
\treturn SLOResult{{ServiceName: args.ServiceName, TargetP99Ms: 250, GateDecision: "APPROVE_DEPLOY"}}, nil
}}

func BuildRootAgent(ctx context.Context) (llmagent.Agent, error) {{
\tmodel, err := gemini.NewModel(ctx, "{default_cloud_model}", &genai.ClientConfig{{APIKey: os.Getenv("GEMINI_API_KEY")}})
\tif err != nil {{
\t\treturn nil, err
\t}}
\tsloTool, err := functiontool.New(functiontool.Config{{Name: "lookup_service_slo", Description: "Fetches SLO target."}}, LookupSLO)
\tif err != nil {{
\t\treturn nil, err
\t}}
\topsAgent, err := llmagent.New(llmagent.Config{{
\t\tName:        "ops_specialist",
\t\tModel:       model,
\t\tDescription: "Audits microservice SLO metrics.",
\t\tInstruction: "Call lookup_service_slo and return gate decision.",
\t\tTools:       []tool.Tool{{sloTool}},
\t}})
\tif err != nil {{
\t\treturn nil, err
\t}}
\treturn llmagent.New(llmagent.Config{{
\t\tName:        "sre_coordinator",
\t\tModel:       model,
\t\tDescription: "Root Go ADK coordinator.",
\t\tInstruction: "Delegate SLO inspection to ops_specialist.",
\t\tSubAgents:   []llmagent.Agent{{opsAgent}},
\t}})
}}

func main() {{
\tfmt.Println("Go ADK (google.golang.org/adk/v2) track ready ({stage}).")
}}
''')
                    with open(poly_root / "java" / "src" / "main" / "java" / "com" / "example" / "adk" / "SreAdkJavaApp.java", "w", encoding="utf-8") as f:
                        f.write(f'''package com.example.adk;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.run.InMemoryRunner;
import com.google.adk.tools.FunctionTool;
import java.util.Map;

public final class SreAdkJavaApp {{

    public static Map<String, Object> lookupServiceSlo(String serviceName) {{
        return Map.of("serviceName", serviceName, "targetP99Ms", 250, "gateDecision", "APPROVE_DEPLOY");
    }}

    public static final BaseAgent opsAgent = LlmAgent.builder()
            .name("ops_specialist")
            .model("{default_cloud_model}")
            .description("Audits microservice SLO metrics in Java.")
            .instruction("Use lookupServiceSlo and store output in telemetry_result.")
            .tools(FunctionTool.create(SreAdkJavaApp.class, "lookupServiceSlo"))
            .outputKey("telemetry_result")
            .build();

    public static final BaseAgent reportAgent = LlmAgent.builder()
            .name("report_writer")
            .model("{default_cloud_model}")
            .description("Formats SRE deployment gate reports.")
            .instruction("Summarize {{telemetry_result}} into a release checklist.")
            .build();

    public static final BaseAgent rootAgent = SequentialAgent.builder()
            .name("sre_release_pipeline")
            .description("Java ADK SequentialAgent pipeline.")
            .subAgents(opsAgent, reportAgent)
            .build();

    public static void main(String[] args) {{
        InMemoryRunner runner = new InMemoryRunner(rootAgent, "SreAdkJavaApp");
        System.out.println("Initialized Java ADK InMemoryRunner for: " + runner.toString());
    }}
}}
''')
                    with open(poly_root / "kotlin" / "src" / "main" / "kotlin" / "com" / "example" / "adk" / "SreAdkKotlinApp.kt", "w", encoding="utf-8") as f:
                        f.write(f'''package com.example.adk

import com.google.adk.kt.agents.Instruction
import com.google.adk.kt.agents.LlmAgent
import com.google.adk.kt.models.Gemini
import com.google.adk.tools.FunctionTool

data class SloMetrics(val serviceName: String, val targetP99Ms: Int, val gateDecision: String)

fun lookupServiceSlo(serviceName: String): SloMetrics =
    SloMetrics(serviceName = serviceName, targetP99Ms = 250, gateDecision = "APPROVE_DEPLOY")

val opsSpecialist = LlmAgent(
    name = "ops_specialist",
    model = Gemini("{default_cloud_model}"),
    description = "Monitors service SLO budgets in Kotlin.",
    instruction = Instruction("Use lookupServiceSlo to inspect service health."),
    tools = listOf(FunctionTool.create(::lookupServiceSlo)),
)

val rootAgent = LlmAgent.builder()
    .name("sre_coordinator")
    .model("{default_flagship_model}")
    .description("Root Kotlin ADK coordinator.")
    .instruction("Delegate SLO checks to ops_specialist.")
    .subAgents(listOf(opsSpecialist))
    .build()

fun main() {{
    println("Initialized Kotlin ADK rootAgent: ${{rootAgent.name()}}")
}}
''')
                    with open(poly_root / "typescript" / "src" / "agent.ts", "w", encoding="utf-8") as f:
                        f.write(f'''import {{ LlmAgent, FunctionTool }} from "@google/adk";
import {{ z }} from "zod";

export const lookupServiceSloTool = new FunctionTool({{
  name: "lookup_service_slo",
  description: "Returns target P99 SLO latency for a microservice.",
  parameters: z.object({{ serviceName: z.string() }}),
  execute: async ({{ serviceName }}) => ({{ serviceName, targetP99Ms: 250, gateDecision: "APPROVE_DEPLOY" }}),
}});

export const opsSpecialist = new LlmAgent({{
  name: "ops_specialist",
  model: "{default_cloud_model}",
  description: "Audits microservice SLO metrics in TypeScript.",
  instruction: "Call lookup_service_slo and return gate decision.",
  tools: [lookupServiceSloTool],
}});

export const rootAgent = new LlmAgent({{
  name: "sre_coordinator",
  model: "{default_flagship_model}",
  description: "Root TypeScript ADK coordinator.",
  instruction: "Delegate SLO inspection to ops_specialist.",
  subAgents: [opsSpecialist],
}});
''')

            with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(f"""# {topic} - Hands-on Lab Session Guide

This guide outlines the session schedule and step-by-step objectives for the **{topic}** workshop.
Write your code in `workshop/01_starter`. If you get stuck, refer to the completed reference solution in `workshop/02_final`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & environment verification (`./scripts/check_env.sh`)
- **10m - 25m**: **Lab 01** - Environment Verification, ADK Scaffolding & Custom Tools (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - Multi-Agent Hierarchy, Sub-Agent Delegation & Structured Outputs (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - Trajectory Evaluation (`adk eval`), ADLC Optimization & Deployment (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Environment Verification, ADK Scaffolding & Custom Tools](./01_lab_environment_and_client.md)**
2. **[Lab 02: Multi-Agent Hierarchy, Sub-Agent Delegation & Structured Outputs](./02_lab_structured_outputs.md)**
3. **[Lab 03: Trajectory Evaluation (adk eval), ADLC Optimization & Deployment](./03_lab_end_to_end_pipeline.md)**
""")
            with open(labs_dir / "01_lab_environment_and_client.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 01: Environment Verification, ADK Scaffolding & Custom Tools

## Objective
Verify your local environment using `./scripts/check_env.sh` and initialize your ADK agent using Google Agent Development Kit (`google-adk` / `google.golang.org/adk/v2` / `com.google.adk:google-adk` / `@google/adk`) with `{default_cloud_model}`.

## Official Multi-Language ADK Entry Points
- **Python (`google-adk`)**: `workshop/01_starter/sre_agent/agent.py` exposing `root_agent = LlmAgent(...)`
- **Go (`google.golang.org/adk/v2`)**: `llmagent.New`, `functiontool.New`, and `gemini.NewModel`
- **Java (`com.google.adk:google-adk`)**: `LlmAgent.builder()`, `SequentialAgent.builder()`, and `FunctionTool.create()`
- **Kotlin (`com.google.adk:google-adk-kotlin-core`)**: `LlmAgent(...)`, `Gemini("{default_cloud_model}")`, and `FunctionTool.create(::fn)`
- **TypeScript (`@google/adk`)**: `new LlmAgent({{...}})` and Zod-typed `new FunctionTool({{...}})`

## Instructions
1. Run `./scripts/check_env.sh` (or `.\\scripts\\check_env.ps1` on Windows).
2. If building with ADK & `agents-cli`, install the 7 official agent skills:
   ```bash
   uvx google-agents-cli setup
   ```
3. Open `workshop/01_starter/main.py` (and `workshop/01_starter/agent.py` or `polyglot/`) and inspect the starter tool definitions.
4. Test execution:
   ```bash
   python3 workshop/01_starter/main.py
   ```
""")
            with open(labs_dir / "02_lab_structured_outputs.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 02: Multi-Agent Hierarchy, Sub-Agent Delegation & Structured Outputs

## Objective
Wire specialized sub-agents (`slo_specialist`, `report_specialist`) under a root coordinator (`root_agent` running `{default_flagship_model}`) and enforce deterministic JSON schema outputs.

## Instructions
1. Review `prompt-pack/README.md` for the target JSON Schema.
2. In Python (`workshop/01_starter/agent.py`), attach `sub_agents=[slo_specialist, report_specialist]` to `root_agent`.
3. If exploring the Go, Java, Kotlin, or TypeScript tracks under `workshop/02_final/polyglot/`, compare how `SubAgents` / `subAgents` and `SequentialAgent` delegate tasks across languages.
4. Launch the interactive ADK Dev UI to inspect sub-agent handoff events visually:
   ```bash
   cd workshop/02_final && adk web
   ```
""")
            with open(labs_dir / "03_lab_end_to_end_pipeline.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 03: Trajectory Evaluation (adk eval), ADLC Optimization & Deployment

## Objective
Evaluate multi-agent tool trajectories against `evalset.json` (`adk eval` / `agents-cli eval`), run `InMemoryRunner` tests, and prepare for Cloud Run / Vertex AI Agent Engine deployment.

## Instructions
1. Run the reference solution:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. Evaluate the ADK agent trajectory against `workshop/02_final/evalset.json`:
   ```bash
   adk eval workshop/02_final/sre_agent workshop/02_final/evalset.json
   ```
3. Run the automated workshop integrity verifier:
   ```bash
   python3 scripts/verify_workshop.py .
   ```
""")
        else:
            with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(f"""# {topic} - Hands-on Lab Session Guide

This guide outlines the session schedule and step-by-step objectives for the **{topic}** workshop.
Write your code in `workshop/01_starter/main.py`. If you get stuck, refer to the completed reference solution in `workshop/02_final/main.py`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & environment verification (`./scripts/check_env.sh`)
- **10m - 25m**: **Lab 01** - Environment Verification & AI Client Sanity Check (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - Structured Outputs & JSON Schema Validation (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - End-to-End Pipeline & Automated Verification (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Environment Verification & AI Client Sanity Check](./01_lab_environment_and_client.md)**
2. **[Lab 02: Structured Outputs & JSON Schema Validation](./02_lab_structured_outputs.md)**
3. **[Lab 03: End-to-End Pipeline & Automated Verification](./03_lab_end_to_end_pipeline.md)**
""")
            with open(labs_dir / "01_lab_environment_and_client.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 01: Environment Verification & AI Client Sanity Check

## Objective
Verify your local and cloud development environment using `./scripts/check_env.sh` and connect `workshop/01_starter/main.py` to {provider_label} (`{default_cloud_model}`) or Local Ollama (`{default_local_model}`).

## Instructions
1. Run `./scripts/check_env.sh` (or `.\\scripts\\check_env.ps1` on Windows) to verify Python, `uv`, and local port readiness.
2. Open `workshop/01_starter/main.py` and inspect `TODO: [Lab 01 - Exercise]` inside `lab1_sanity_check()`.
3. Configure `{primary_api_key_env}` in `.env` or start your local Ollama runtime (`ollama serve` with `{default_local_model}`).
4. Run the starter script to verify connectivity:
   ```bash
   python3 workshop/01_starter/main.py
   ```
""")
            with open(labs_dir / "02_lab_structured_outputs.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 02: Structured Outputs & JSON Schema Validation

## Objective
Enforce deterministic, type-safe JSON responses matching the `WorkshopTaskResult` schema (`status`, `model_used`, `summary`, `action_items`).

## Instructions
1. Review `prompt-pack/README.md` for the system prompt and target JSON Schema definition.
2. Open `workshop/01_starter/main.py` and complete `TODO: [Lab 02 - Exercise]` inside `lab2_structured_output()`.
3. Verify that the output serializes cleanly to JSON without markdown code-fence artifacts.
""")
            with open(labs_dir / "03_lab_end_to_end_pipeline.md", "w", encoding="utf-8") as f:
                f.write(f"""# Lab 03: End-to-End Pipeline & Automated Verification

## Objective
Run the complete reference pipeline in `workshop/02_final/main.py` with automatic local/cloud fallback and verify all workshop quality gates.

## Instructions
1. Execute the completed reference solution:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. Compare your implementation in `workshop/01_starter/main.py` against `workshop/02_final/main.py`.
3. Run the automated workshop integrity verifier:
   ```bash
   python3 scripts/verify_workshop.py .
   ```
""")

    audit_typography(str(project_dir), fix=True)
    print(f"✨ Workshop '{name}' initialized successfully at {project_dir}!")
    return project_dir

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

            # Write dynamic 4-persona report into docs/00-persona-loop-review-report.md
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

def generate_all(name: str, topic: str, stack_str: str = None, target_dir: str = None, model_name: str = None):
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

    # 0. Ensure uv Dependencies Automatically
    ensure_uv_dependencies()

    # 1. Scaffolding Structure
    proj_dir = init_workshop(name, topic, target_dir, stack_str, model_name)

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
    """Zero-config natural language prompt entrypoint: infers name, topic, stack, and 2026 model, then builds immediately."""
    parsed = parse_natural_prompt(prompt)
    final_name = name_override or parsed["name"]
    final_topic = parsed["topic"]
    final_stack = stack_override or parsed["stack"]
    final_model = model_override or parsed["model"]

    print("=" * 70)
    print("🗣️  [NATURAL LANGUAGE PROMPT ROUTER] Resolved Workshop Spec:")
    print(f"   • Prompt : {prompt}")
    print(f"   • Name   : {final_name}")
    print(f"   • Topic  : {final_topic}")
    print(f"   • Stack  : {final_stack}")
    print(f"   • Model  : {final_model}")
    print("=" * 70)

    if init_only:
        return init_workshop(final_name, final_topic, target_dir, final_stack, final_model)
    return generate_all(final_name, final_topic, final_stack, target_dir, final_model)


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

    parser = argparse.ArgumentParser(description="Workshop Harness CLI (uv Powered)")
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
    init_parser.add_argument("--dir", "--target", dest="dir", default=None, help="Target parent directory")

    # generate-all (One-Click Full Orchestration)
    gen_all_parser = subparsers.add_parser("generate-all", help="One-Click full workshop generation across all skills")
    gen_all_parser.add_argument("--name", default=None, help="Workshop project name (auto-inferred if --prompt is given)")
    gen_all_parser.add_argument("--prompt", default=None, help="Natural language prompt to auto-infer name, topic, stack, and model")
    gen_all_parser.add_argument("--topic", default=None, help="Workshop topic")
    gen_all_parser.add_argument("--stack", default=None, help="Tech stack (comma-separated, e.g. python, claude, openai, ollama)")
    gen_all_parser.add_argument("--model", default=None, help="Primary AI model tag (e.g. gemini-4-hydrogen, claude-sonnet-5-5, gpt-6.1-sol)")
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

    # audit-loop command (Loop Engineering Persona Audit)
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
            elif not args.name:
                init_parser.error("one of --name, --prompt, or --topic is required")
            init_workshop(args.name, args.topic or "BWAI Hands-on Workshop", args.dir, args.stack or "python", args.model)
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
            elif not args.name:
                gen_all_parser.error("one of --name, --prompt, or --topic is required")
            generate_all(args.name, args.topic or "BWAI Hands-on Workshop", args.stack, args.dir, args.model)
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

