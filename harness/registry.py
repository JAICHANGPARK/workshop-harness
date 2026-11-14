# -*- coding: utf-8 -*-
"""
harness/registry.py - Verified 2026 Model Registry, Deprecation Map & Bilingual Terminology Rules
"""

import shutil
import subprocess
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parent.parent
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
    "gemma-2-2b-it": "gemma-4-e2b-it",
    "gemma-2-9b-it": "gemma-4-12b-it",
    "gemma-2-27b-it": "gemma-4-26b-a4b-it",
    "gemma-3-4b-it": "gemma-4-e4b-it",
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


def ensure_uv_dependencies():
    """Ensure reportlab, pymupdf, pillow, python-pptx are installed automatically via uv or pip."""
    try:
        import reportlab  # noqa: F401
        import fitz  # noqa: F401
        import PIL  # noqa: F401
        import pptx  # noqa: F401
    except ImportError:
        print("📦 Installing required dependencies automatically via uv/pip...")
        if shutil.which("uv"):
            subprocess.run(["uv", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)
