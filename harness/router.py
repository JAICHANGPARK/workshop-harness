# -*- coding: utf-8 -*-
"""
harness/router.py - Natural Language Prompt Parser, Language Detector & Multi-Provider Resolver
"""

import re

from .registry import DEPRECATED_MODEL_REPLACEMENTS, MODEL_REGISTRY


def detect_prompt_language(text: str) -> str:
    """Detect user request language ('ko', 'ja', 'zh', or 'en') from natural language input."""
    s = text or ""
    if re.search(r"[\uac00-\ud7a3]", s):
        return "ko"
    if re.search(r"[\u3040-\u30ff]", s):
        return "ja"
    if re.search(r"[\u4e00-\u9fff]", s):
        return "zh"
    return "en"


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
        or model_lower.startswith("gpt-")
    )
    wants_adk = any(k in stack for k in ["adk", "agents-cli", "google-adk", "google-agents-cli"])
    wants_gemini = (
        any(k in stack for k in ["gemini", "google", "vertex", "flutter", "android", "genui", "a2ui", "gemini-live"])
        or model_lower.startswith("gemini-")
        or wants_adk
        or (not wants_claude and not wants_openai)
    )

    local_model = MODEL_REGISTRY["google-gemma"]["local_16gb_ram"]
    local_embedding_model = MODEL_REGISTRY["google-gemma"]["embedding_multimodal_740m"]

    gemma_local_tags = {
        MODEL_REGISTRY["google-gemma"]["local_8gb_ram"],
        MODEL_REGISTRY["google-gemma"]["local_16gb_ram"],
        MODEL_REGISTRY["google-gemma"]["local_dense_12b"],
        MODEL_REGISTRY["google-gemma"]["local_moe_26b"],
        MODEL_REGISTRY["google-gemma"]["local_dense_31b"],
        MODEL_REGISTRY["google-gemma"]["translate_multimodal"],
        MODEL_REGISTRY["google-gemma"]["function_calling_edge"],
        MODEL_REGISTRY["google-gemma"]["medical_multimodal"],
        MODEL_REGISTRY["google-gemma"]["safety_classifier"],
    }
    gemma_embedding_tags = {
        MODEL_REGISTRY["google-gemma"]["embedding_multimodal_740m"],
        MODEL_REGISTRY["google-gemma"]["embedding_audio_570m"],
        MODEL_REGISTRY["google-gemma"]["embedding_vision_440m"],
        MODEL_REGISTRY["google-gemma"]["embedding_text_270m"],
        MODEL_REGISTRY["google-gemma"]["embedding_hf"],
    }

    if normalized_model in gemma_local_tags or model_lower.startswith("gemma4:"):
        local_model = normalized_model
    elif normalized_model in gemma_embedding_tags or model_lower.startswith("embeddinggemma-2"):
        local_embedding_model = (
            "embeddinggemma-2" if normalized_model == "google/embeddinggemma-2" else normalized_model
        )

    if wants_claude and not (model_lower.startswith("gpt-") or model_lower.startswith("gemini-")):
        primary_provider = "anthropic"
        cloud_model = (
            normalized_model
            if (normalized_model and model_lower.startswith("claude-"))
            else MODEL_REGISTRY["anthropic-claude"]["default_workhorse"]
        )
        flagship_model = (
            MODEL_REGISTRY["anthropic-claude"]["apex_agentic"]
            if cloud_model == MODEL_REGISTRY["anthropic-claude"]["apex_agentic"]
            else MODEL_REGISTRY["anthropic-claude"]["flagship_reasoning"]
        )
        api_key_env = "ANTHROPIC_API_KEY"
        provider_label = "Anthropic Claude"
    elif wants_openai and not model_lower.startswith("gemini-"):
        primary_provider = "openai"
        cloud_model = (
            normalized_model
            if (normalized_model and model_lower.startswith("gpt-"))
            else MODEL_REGISTRY["openai-gpt"]["default_workhorse"]
        )
        flagship_model = MODEL_REGISTRY["openai-gpt"]["flagship_reasoning"]
        api_key_env = "OPENAI_API_KEY"
        provider_label = "OpenAI"
    else:
        primary_provider = "gemini"
        if normalized_model and model_lower.startswith("gemma-4-"):
            cloud_model = normalized_model
            flagship_model = MODEL_REGISTRY["google-gemma"]["cloud_dense_31b"]
            provider_label = "Google Gemma & GenAI"
        elif (
            normalized_model in gemma_local_tags
            or normalized_model in gemma_embedding_tags
            or model_lower.startswith("gemma4:")
            or model_lower.startswith("embeddinggemma-2")
        ):
            cloud_model = MODEL_REGISTRY["google-gemma"]["cloud_moe_26b"]
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
    """Parse a natural language prompt (KO/EN/JA/ZH) into name, topic, stack, canonical 2026 model, and lang."""
    raw = (prompt or "").strip()
    lower = raw.lower()
    detected_lang = detect_prompt_language(raw)

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

    # 2. Detect provider & tier intent from natural language (KO/EN/JA/ZH, handling attached CJK particles)
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
        or _has_ascii_kw("gemini|carbon|neon|hydrogen|argon")
        or any(k in lower for k in ["제미나이", "카본", "네온", "하이드로젠", "아르곤", "나노 바나나", "nano banana", "ネオン"])
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
            "젬마", "트랜슬레이트젬마", "트랜슬레이트 젬마", "펑션젬마", "펑션 젬마", "메드젬마", "메드 젬마",
            "실드젬마", "올라마", "로컬 llm", "온디바이스", "lm studio", "lmstudio",
        ])
    )

    if not detected_model:
        if has_claude:
            if _has_ascii_kw("fable") or "페이블" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["apex_agentic"]
            elif _has_ascii_kw("opus") or "오퍼스" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["flagship_reasoning"]
            elif _has_ascii_kw("haiku") or "하이쿠" in lower:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["fast_haiku"]
            else:
                detected_model = MODEL_REGISTRY["anthropic-claude"]["default_workhorse"]
        elif has_openai:
            if _has_ascii_kw("astra") or "아스트라" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["flagship_reasoning"]
            elif _has_ascii_kw("terra") or "테라" in lower or "computer use" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["multimodal_computer_use"]
            elif _has_ascii_kw("luna") or "루나" in lower:
                detected_model = MODEL_REGISTRY["openai-gpt"]["fast_lite"]
            elif _has_ascii_kw("sunburst"):
                detected_model = MODEL_REGISTRY["openai-gpt"]["image_default"]
            else:
                detected_model = MODEL_REGISTRY["openai-gpt"]["default_workhorse"]
        elif has_gemma_or_local and not has_gemini:
            if _has_ascii_kw("translategemma") or "translate gemma" in lower or "트랜슬레이트" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["translate_multimodal"]
            elif _has_ascii_kw("functiongemma") or "function gemma" in lower or "펑션젬마" in lower or "펑션 젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["function_calling_edge"]
            elif _has_ascii_kw("medgemma") or "med gemma" in lower or "메드젬마" in lower or "메드 젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["medical_multimodal"]
            elif _has_ascii_kw("shieldgemma") or "shield gemma" in lower or "실드젬마" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["safety_classifier"]
            elif has_embedding_gemma and not (
                _has_ascii_kw("gemma4|31b|26b|12b|e4b|e2b")
                or "gemma 4" in lower
                or "젬마 4" in lower
                or "젬마4" in lower
            ):
                if "270m" in lower or "8gb" in lower:
                    detected_model = MODEL_REGISTRY["google-gemma"]["embedding_text_270m"]
                elif "440m" in lower:
                    detected_model = MODEL_REGISTRY["google-gemma"]["embedding_vision_440m"]
                elif "570m" in lower:
                    detected_model = MODEL_REGISTRY["google-gemma"]["embedding_audio_570m"]
                else:
                    detected_model = MODEL_REGISTRY["google-gemma"]["embedding_multimodal_740m"]
            elif "31b" in lower:
                detected_model = (
                    MODEL_REGISTRY["google-gemma"]["local_dense_31b"]
                    if ("ollama" in lower or "올라마" in lower or "로컬" in lower or "local" in lower)
                    else MODEL_REGISTRY["google-gemma"]["cloud_dense_31b"]
                )
            elif "26b" in lower or "moe" in lower:
                detected_model = (
                    MODEL_REGISTRY["google-gemma"]["local_moe_26b"]
                    if ("ollama" in lower or "올라마" in lower or "로컬" in lower or "local" in lower)
                    else MODEL_REGISTRY["google-gemma"]["cloud_moe_26b"]
                )
            elif "12b" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["local_dense_12b"]
            elif "e2b" in lower or "2b" in lower or "8gb" in lower:
                detected_model = MODEL_REGISTRY["google-gemma"]["local_8gb_ram"]
            else:
                detected_model = MODEL_REGISTRY["google-gemma"]["local_16gb_ram"]
        else:
            if _has_ascii_kw("carbon") or "카본" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["flagship_reasoning"]
            elif _has_ascii_kw("neon") or "네온" in lower or "ネオン" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["mid_tier_reasoning"]
            elif _has_ascii_kw("argon") or "아르곤" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["enterprise_reasoning"]
            elif "live" in lower or "라이브" in lower or "음성" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["live_multimodal"]
            elif "nano banana" in lower or "나노 바나나" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["image_default"]
            elif "3.8" in lower:
                detected_model = MODEL_REGISTRY["google-gemini"]["fast_multimodal_flash"]
            else:
                detected_model = MODEL_REGISTRY["google-gemini"]["default_workhorse"]

    # 3. Detect framework, language & platform stack
    stack_items = []
    is_flutter = any(k in lower for k in ["flutter", "플러터", "dart", "genui", "a2ui"])
    is_android = any(k in lower for k in ["android", "안드로이드", "jetpack compose", "컴포즈"])
    is_ts = bool(re.search(r"(?<![a-z0-9])(typescript|ts|node\.?js|javascript|nextjs|next\.js)(?![a-z0-9])", lower)) or any(
        k in lower for k in ["타입스크립트", "노드"]
    )
    is_go = bool(re.search(r"(?<![a-z0-9])(golang|go\s+adk|go\s+sdk)(?![a-z0-9])", lower)) or any(
        k in lower for k in ["고랭", "go언어", "go 언어"]
    )
    is_java = bool(re.search(r"(?<![a-z0-9])java(?![a-z0-9])", lower)) or "자바" in lower
    is_kotlin = (bool(re.search(r"(?<![a-z0-9])kotlin(?![a-z0-9])", lower)) or "코틀린" in lower) and not is_android
    is_adk = bool(re.search(r"(?<![a-z0-9])(adk|google-adk|agents-cli|google-agents-cli)(?![a-z0-9])", lower)) or any(
        k in lower for k in ["에이전트 개발 키트"]
    )

    if is_flutter:
        stack_items.append("flutter")
        if "genui" in lower or "생성형 ui" in lower or "동적 ui" in lower:
            stack_items.append("genui")
        if "a2ui" in lower:
            stack_items.append("a2ui")
    elif is_android:
        stack_items.append("android")
    else:
        if is_ts and not is_adk:
            stack_items.append("typescript")
        elif is_go and not is_adk:
            stack_items.append("go")
        else:
            stack_items.append("python")

        if is_adk:
            stack_items.append("adk")
            if "agents-cli" in lower or "adlc" in lower:
                stack_items.append("agents-cli")
            if any(k in lower for k in ["polyglot", "폴리글랏", "다중 언어"]) or sum([is_ts, is_go, is_java, is_kotlin]) >= 1:
                stack_items.append("polyglot")
        if has_claude:
            stack_items.append("claude")
            if "claude-agent-sdk" in lower or "agent sdk" in lower:
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

    seen_stack = []
    for s in stack_items:
        if s not in seen_stack:
            seen_stack.append(s)

    # 4. Clean topic string
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
        "sonnet", "opus", "fable", "haiku", "sol", "astra", "terra", "luna", "carbon", "neon", "hydrogen", "argon",
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
        "lang": detected_lang,
    }
