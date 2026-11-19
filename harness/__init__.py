# -*- coding: utf-8 -*-
"""
harness - Modular Core Package for Workshop Harness
"""

__version__ = "2026.11.14"

from .auditors import (
    audit_compatibility,
    audit_models,
    audit_persona_loop,
    audit_typography,
    doctor_workshop,
    list_models,
    sanitize_no_em_dash,
)
from .exporters import (
    build_pdf,
    build_slides,
    export_codelab,
    export_colab,
    generate_all,
    generate_from_prompt,
    test_colab,
    test_workshop,
)
from .registry import (
    AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS,
    DEPRECATED_MODEL_REPLACEMENTS,
    HARNESS_ROOT,
    MODEL_REGISTRY,
    TEMPLATES_DIR,
    ensure_uv_dependencies,
)
from .router import _resolve_provider_config, detect_prompt_language, parse_natural_prompt
from .scaffolder import init_workshop

__all__ = [
    "__version__",
    "HARNESS_ROOT",
    "TEMPLATES_DIR",
    "MODEL_REGISTRY",
    "DEPRECATED_MODEL_REPLACEMENTS",
    "AWKWARD_LITERAL_TRANSLATION_REPLACEMENTS",
    "ensure_uv_dependencies",
    "detect_prompt_language",
    "_resolve_provider_config",
    "parse_natural_prompt",
    "list_models",
    "audit_models",
    "sanitize_no_em_dash",
    "audit_typography",
    "audit_compatibility",
    "audit_persona_loop",
    "doctor_workshop",
    "init_workshop",
    "test_workshop",
    "build_pdf",
    "export_codelab",
    "export_colab",
    "test_colab",
    "build_slides",
    "generate_all",
    "generate_from_prompt",
]
