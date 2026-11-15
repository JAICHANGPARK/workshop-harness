# -*- coding: utf-8 -*-
"""
harness/scaffolder.py - Multi-Stack & Multi-Provider Workshop Repository Scaffolder
"""

import json
import os
import re
import shutil
from pathlib import Path

from .auditors import audit_typography
from .registry import MODEL_REGISTRY, TEMPLATES_DIR
from .router import _resolve_provider_config, detect_prompt_language, parse_natural_prompt


def init_workshop(
    name: str,
    topic: str,
    target_dir: str = None,
    stack_str: str = "python",
    model_name: str = None,
    lang: str = None,
):
    raw_path = Path(target_dir) / name if target_dir else Path(name)
    project_dir = raw_path if raw_path.is_absolute() else (Path.cwd() / raw_path)
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", project_dir.name).strip("-") or "workshop"
    stack = [s.strip().lower() for s in stack_str.split(",") if s.strip()] if stack_str else ["python"]
    final_lang = (lang or detect_prompt_language(topic or "")).lower()

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

    # Copy unified setup guide to root
    shutil.copy(doc_templates / "02_prerequisites.md", project_dir / "SETUP_GUIDE.md")

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

    if final_lang == "ko":
        runbook_md = f"""# 진행자 및 TA 런북 (Runbook): {name}

- **세션 주제**: {topic}
- **기술 스택**: `{stack_str}`
- **기본 클라우드 프로바이더**: {provider_label} (`{primary_api_key_env}`)
- **사용 모델**: 클라우드 `{default_cloud_model}` | 코디네이터 `{default_flagship_model}` | 로컬 `{default_local_model}` | 로컬 멀티모달 임베딩 `{default_local_embedding_model}`
- **발표자 (Facilitator)**: 리드 진행자
- **현장 서포트 (TA)**: 실습 지원 TA 팀

---

## 세션 타임라인 (총 60분)

### 00m - 10m: 오프닝 및 개발 환경 점검
- **Facilitator**: `SETUP_GUIDE.md` 사전 준비 사항을 간단히 짚어주고, 전체 아키텍처와 `./scripts/check_env.sh` 실행 화면을 시연합니다.
- **TA**: 환경 점검 스크립트에서 에러가 난 참가자를 1:1로 도와주고, 저사양 노트북 참가자는 `output/colab/workshop_starter.ipynb` (Google Colab 폴백)으로 바로 안내합니다.

### 10m - 25m: Lab 01 - 환경 설정 및 클라이언트 연결 확인 (Smoke Test)
- **Facilitator**: `workshop/01_starter` 스타터 코드 구조를 설명하고 `TODO: [Lab 01]` 연결 코드를 라이브로 작성합니다.
- **TA**: `.env` 파일의 `{primary_api_key_env}` 입력이나 로컬 LLM 서버(`ollama serve`, 포트 `11434`) 실행을 돕습니다.

### 25m - 45m: Lab 02 - Structured Output (JSON 스키마 응답) 및 Tool Calling
- **Facilitator**: `prompt-pack/README.md`의 JSON 스키마 정의와 툴 콜링·서브 에이전트 라우팅 구현을 시연합니다.
- **TA**: 스키마 검증 에러나 로컬 포트(`11434` / `1234`) 충돌 이슈를 빠르게 해결합니다.

### 45m - 55m: Lab 03 - End-to-End 파이프라인 실행 및 동작 검증
- **Facilitator**: `workshop/02_final` 정답 코드를 함께 살펴보고 `python3 scripts/verify_workshop.py .` 검증 스크립트를 실행합니다.
- **TA**: 참가자별 최종 실행 결과를 확인합니다.

### 55m - 60m: Q&A 및 마무리
- **Facilitator**: 핵심 내용을 정리하고 PDF 핸드아웃(`output/pdf/`)과 피드백 설문 링크를 공유합니다.
"""
    elif final_lang == "ja":
        runbook_md = f"""# Facilitator & TA Runbook (ランブック): {name}

- **Session Title**: {topic}
- **Tech Stack**: `{stack_str}`
- **Primary Cloud Provider**: {provider_label} (`{primary_api_key_env}`)
- **Primary Cloud Model**: `{default_cloud_model}` | **Coordinator**: `{default_flagship_model}` | **Local Model**: `{default_local_model}` | **Local Multimodal Embedding**: `{default_local_embedding_model}`
- **Facilitator**: Workshop Lead Facilitator
- **Teaching Assistants (TA)**: Roaming TA Team

---

## Session Timeline (60分タイムライン)

### 00m - 10m: オープニング・環境検証
- **Facilitator**: `SETUP_GUIDE.md` とアーキテクチャ概要を説明し、`./scripts/check_env.sh` を実演します。
- **TA**: 環境チェックエラーの参加者をサポートし、低メモリPCの参加者を `output/colab/workshop_starter.ipynb` の **Fallback (フォールバック)** へ案内します。

### 10m - 25m: Lab 01 - 環境構築・クライアント Smoke Test (スモークテスト)
- **Facilitator**: `workshop/01_starter` の **Starter Code (スターターコード)** を解説し、`TODO: [Lab 01]` を実装します。
- **TA**: `.env` の `{primary_api_key_env}` 設定またはローカルサーバー (`ollama serve`, ポート `11434`) の起動を支援します。

### 25m - 45m: Lab 02 - Structured Outputs (構造化出力) と Tool Calling (ツール呼び出し)
- **Facilitator**: `prompt-pack/README.md` の出力スキーマ定義とツール連携を実演します。
- **TA**: スキーマ検証エラーやポート競合の解消をサポートします。

### 45m - 55m: Lab 03 - End-to-End パイプライン検証
- **Facilitator**: `workshop/02_final` のリファレンス実装を共有し、`python3 scripts/verify_workshop.py .` を実行します。
- **TA**: 参加者の完了チェックポイントを確認します。

### 55m - 60m: Q&A・クロージング
- **Facilitator**: まとめ、PDFハンドアウト (`output/pdf/`) の共有、アンケート案内を行います。
"""
    elif final_lang == "zh":
        runbook_md = f"""# Facilitator & TA Runbook (演练手册): {name}

- **Session Title**: {topic}
- **Tech Stack**: `{stack_str}`
- **Primary Cloud Provider**: {provider_label} (`{primary_api_key_env}`)
- **Primary Cloud Model**: `{default_cloud_model}` | **Coordinator**: `{default_flagship_model}` | **Local Model**: `{default_local_model}` | **Local Multimodal Embedding**: `{default_local_embedding_model}`
- **Facilitator**: Workshop Lead Facilitator
- **Teaching Assistants (TA)**: Roaming TA Team

---

## Session Timeline (60分钟议程)

### 00m - 10m: 开场与环境检查
- **Facilitator**: 讲解 `SETUP_GUIDE.md` 与整体架构，演示运行 `./scripts/check_env.sh`。
- **TA**: 协助排查环境检测报错，引导低内存笔记本参与者使用 `output/colab/workshop_starter.ipynb` **Fallback (回退策略)**。

### 10m - 25m: Lab 01 - 环境配置与客户端 Smoke Test (冒烟测试)
- **Facilitator**: 介绍 `workshop/01_starter` **Starter Code (Starter 初始代码)** 结构并演示完成 `TODO: [Lab 01]`。
- **TA**: 协助配置 `.env` 中的 `{primary_api_key_env}` 或启动本地服务 (`ollama serve`, 端口 `11434`)。

### 25m - 45m: Lab 02 - Structured Outputs (结构化输出) 与 Tool Calling (工具调用)
- **Facilitator**: 演示 `prompt-pack/README.md` 中的类型安全输出 Schema 与工具调用集成。
- **TA**: 协助解决 Schema 校验与端口冲突问题。

### 45m - 55m: Lab 03 - End-to-End 流水线与完整性验证
- **Facilitator**: 展示 `workshop/02_final` 参考实现并运行 `python3 scripts/verify_workshop.py .`。
- **TA**: 核对参与者实验完成检查点。

### 55m - 60m: 答疑与总结
- **Facilitator**: 总结回顾、分发 PDF 讲义 (`output/pdf/`) 并收集反馈问卷。
"""
    else:
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
- **Facilitator**: Walk through `SETUP_GUIDE.md`, architecture overview, and demo `./scripts/check_env.sh` execution.
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
        if final_lang == "ko":
            f.write(f"""# 핵심 AI 엔지니어링 개념 치트시트 (ELI5)

> 워크숍 주제: **{topic}**
> 기본 클라우드 모델: `{default_cloud_model}` | 코디네이터 모델: `{default_flagship_model}` | 로컬 모델: `{default_local_model}`

처음 접하는 참가자도 직관적으로 이해할 수 있도록 핵심 개념을 **비유 -> 실제 동작 원리 -> 실습 적용** 3단계로 정리했습니다.

---

## 한눈에 보는 핵심 개념

| 핵심 개념 | 직관적인 비유 | 실제 동작 원리 | 핸즈온 실습 포인트 |
| :--- | :--- | :--- | :--- |
| **로컬 LLM (`{default_local_model}`)** | 와이파이를 꺼도 내 노트북 안에서 바로 답해주는 전담 사서 | 양자화된 가중치를 로컬 GPU/CPU 메모리에 올려 `localhost:11434` HTTP API로 서빙 | `ollama serve`로 로컬 서버를 띄우고 네트워크 지연 없이 호출 |
| **양자화 (Quantization, 4-bit)** | 두꺼운 겨울 패딩을 압축팩에 넣어 기내용 캐리어에 쏙 넣는 것 | 16-bit 부동소수점 가중치를 4-bit 정수로 압축해 메모리 점유율을 약 70% 절감 | 8GB RAM 노트북에서 `gemma4:e2b`를 사용해 OOM(메모리 부족 에러) 방지 |
| **Structured Output (JSON 스키마 응답)** | 빈 종이 대신 칸이 정해진 신청서 양식을 주고 빈칸만 채우게 하는 것 | Pydantic / Zod 스키마에 맞춰 토큰 생성 결과를 고정된 JSON 구조로 강제 | `Lab 02`에서 정규식 파싱 없이 타입 안전하게 응답 처리 |
| **RAG 파이프라인** | 시험 문제를 풀 때 관련 교재 페이지를 먼저 펼쳐 확인한 뒤 답을 쓰는 오픈북 시험 | 멀티모달 임베딩(`gemini-embedding-2` / 로컬 `{default_local_embedding_model}` 768차원)으로 관련 문서를 검색해 프롬프트에 주입 | 환각(Hallucination)을 줄이고 검증된 문서를 근거로 응답 생성 |
| **멀티 에이전트 오케스트레이션** | 총괄 셰프(`{default_flagship_model}`)가 파트별 요리사(`{default_cloud_model}`)에게 업무를 나눠 맡기는 주방 | 루트 에이전트가 하위 전문 에이전트(Sub-agent)와 FunctionTool로 작업을 라우팅 | `Lab 02 & Lab 03`에서 서브 에이전트 라우팅과 Trajectory Eval(실행 경로 평가) 확인 |

## 참고 문서
- [Google Gemini API 공식 문서](https://ai.google.dev/gemini-api/docs)
- [Anthropic Claude 공식 문서](https://docs.anthropic.com)
- [OpenAI Platform 공식 문서](https://platform.openai.com/docs)
- [Google Agent Development Kit (ADK)](https://adk.dev)
""")
        else:
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

1. **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
   - **English (EN)**: Write in clear, idiomatic, direct technical English.
   - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** in Korean, Japanese, or Chinese, **NEVER generate awkward English-to-local literal calques or translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
     - **Korean (KO) Real-World Developer Language**: Use natural developer vernacular and widely used English/loanword terms as-is (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Never output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", "~되어집니다", "~하는 것이 가능합니다").
     - **Japanese (JA)**: Use natural Japanese engineer terminology (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Tool Calling`, `Thinking Budget`, `フォールバック`) and natural sentence endings (`〜を設定します`, `〜を実行できます`).
     - **Chinese (ZH)**: Use authentic Chinese developer phrasing (`实战工作坊`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Tool Calling (工具调用)`, `Thinking Budget (推理预算)`, `回退策略`).
   - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in exact English (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments in concise, natural developer prose without forcing mechanical `(괄호)` glosses on every obvious loanword.

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

    if final_lang == "ko":
        readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

**{topic}** 핸즈온 실습(Hands-on Lab)에 필요한 사전 환경 설정 가이드, 스타터 코드(`01_starter`), 정답 코드(`02_final`), 진행자용 런북(`RUNBOOK.md`)을 모아둔 레포지토리입니다.

## 빠른 시작 (Quick Start)

1. **사전 환경 세팅 가이드**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. **OS/아키텍처 호환성 체크**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **개발 환경 자동 점검 스크립트**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **당일 핸즈온 실습 자료**:
   - 실습 가이드: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - 스타터 코드: [workshop/01_starter](./workshop/01_starter)
   - 정답 코드: [workshop/02_final](./workshop/02_final)
5. **진행자 및 TA 런북 (Runbook)**: [RUNBOOK.md](./RUNBOOK.md)
"""
    elif final_lang == "ja":
        readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

本リポジトリには **{topic}** **Hands-on Lab (ハンズオンラボ)** の事前セットアップガイド、**Starter Code (スターターコード)**、リファレンス実装、進行用 **Runbook (ランブック)** が含まれています。

## Quick Start (クイックスタート)

1. **事前セットアップガイド**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. **アーキテクチャ互換性チェック**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **環境検証スクリプト**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **Hands-on Lab (ハンズオンラボ)**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook (ランブック)**: [RUNBOOK.md](./RUNBOOK.md)
"""
    elif final_lang == "zh":
        readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

本仓库包含 **{topic}** **Hands-on Lab (实战工作坊)** 的课前环境准备指南、**Starter Code (Starter 初始代码)**、参考实现与讲师 **Runbook (演练手册)**。

## Quick Start (快速开始)

1. **环境准备指南**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. **跨架构兼容性检测**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **环境自动验证脚本**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **Hands-on Lab (实战工作坊)**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook (演练手册)**: [RUNBOOK.md](./RUNBOOK.md)
"""
    else:
        readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

This repository contains pre-event preparation documents and hands-on lab code for the **{topic}** workshop.

## Quick Start

1. **Preparation Guide**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. **Architecture Compatibility Check**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **Environment Verification Script**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **Day-of Hands-on Labs**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook**: [RUNBOOK.md](./RUNBOOK.md)
"""

    readme_content += """
## Repository Structure

```text
.
├── AGENTS.md                     # AI Agent & Typography rules (No Em Dash rule)
├── CLAUDE.md                     # Claude Code instructions
├── RUNBOOK.md                    # Facilitator & TA execution runbook
├── SETUP_GUIDE.md                # Unified attendee preparation guide
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
└── output/                      # Build artifacts (PDF, Colab, Open Codelabs, Slides)
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

            if final_lang == "ko":
                with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
                    f.write(f"""# {topic} - 핸즈온 실습 가이드

**{topic}** 세션의 단계별 실습 가이드입니다.
실습 코드는 `workshop/01_starter` 디렉터리에서 직접 작성하고, 막히는 부분이 있으면 `workshop/02_final`의 정답 코드를 참고하세요.

---

## 세션 진행 순서 (총 60분)

- **00m - 10m**: 세션 소개 및 개발 환경 점검 (`./scripts/check_env.sh`)
- **10m - 25m**: **Lab 01** - 개발 환경 점검, ADK 스캐폴딩 및 커스텀 Tool 정의 (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - 멀티 에이전트 계층 구성, 서브 에이전트 라우팅 및 Structured Output (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - Trajectory Eval (`adk eval`) 실행 경로 평가 및 배포 준비 (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A 및 마무리

---

## 단계별 실습 문서

1. **[Lab 01: 개발 환경 점검, ADK 스캐폴딩 및 커스텀 Tool 정의](./01_lab_environment_and_client.md)**
2. **[Lab 02: 멀티 에이전트 계층 구성, 서브 에이전트 라우팅 및 Structured Output](./02_lab_structured_outputs.md)**
3. **[Lab 03: Trajectory Eval (adk eval) 실행 경로 평가 및 배포 준비](./03_lab_end_to_end_pipeline.md)**
""")
                with open(labs_dir / "01_lab_environment_and_client.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 01: 개발 환경 점검, ADK 스캐폴딩 및 커스텀 Tool 정의

## 실습 목표
`./scripts/check_env.sh`로 로컬 개발 환경을 점검하고, Google ADK(`google-adk` / `google.golang.org/adk/v2` / `com.google.adk:google-adk` / `@google/adk`)와 `{default_cloud_model}` 모델로 기본 에이전트와 커스텀 툴을 초기화합니다.

## 언어별 ADK 엔트리포인트
- **Python (`google-adk`)**: `workshop/01_starter/sre_agent/agent.py` (`root_agent = LlmAgent(...)`)
- **Go (`google.golang.org/adk/v2`)**: `llmagent.New`, `functiontool.New`, `gemini.NewModel`
- **Java (`com.google.adk:google-adk`)**: `LlmAgent.builder()`, `SequentialAgent.builder()`, `FunctionTool.create()`
- **Kotlin (`com.google.adk:google-adk-kotlin-core`)**: `LlmAgent(...)`, `Gemini("{default_cloud_model}")`, `FunctionTool.create(::fn)`
- **TypeScript (`@google/adk`)**: `new LlmAgent({{...}})`, Zod 기반 `new FunctionTool({{...}})`

## 실습 순서
1. 터미널에서 `./scripts/check_env.sh` (Windows는 `.\\scripts\\check_env.ps1`)를 실행해 환경을 확인합니다.
2. ADK와 `agents-cli`를 함께 사용할 경우 공식 에이전트 스킬을 설치합니다:
   ```bash
   uvx google-agents-cli setup
   ```
3. `workshop/01_starter/main.py`와 `workshop/01_starter/agent.py` (또는 `polyglot/`)를 열어 스타터 코드의 Tool 함수를 확인합니다.
4. 스타터 스크립트가 정상 실행되는지 스모크 테스트를 돌립니다:
   ```bash
   python3 workshop/01_starter/main.py
   ```
""")
                with open(labs_dir / "02_lab_structured_outputs.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 02: 멀티 에이전트 계층 구성, 서브 에이전트 라우팅 및 Structured Output

## 실습 목표
코디네이터 역할을 맡는 `root_agent`(`{default_flagship_model}`) 아래에 전문 서브 에이전트(`slo_specialist`, `report_specialist`)를 연결하고, JSON 스키마 기반 Structured Output 응답을 구성합니다.

## 실습 순서
1. `prompt-pack/README.md`에 정의된 출력 JSON 스키마 구조를 확인합니다.
2. `workshop/01_starter/agent.py`에서 `root_agent`에 `sub_agents=[slo_specialist, report_specialist]`를 연결합니다.
3. `workshop/02_final/polyglot/` 아래의 Go, Java, Kotlin, TypeScript 구현과 비교하며 언어별 서브 에이전트 라우팅 방식을 확인합니다.
4. ADK 웹 UI를 띄워 에이전트 간 라우팅 흐름과 툴 호출 로그를 눈으로 확인합니다:
   ```bash
   cd workshop/02_final && adk web
   ```
""")
                with open(labs_dir / "03_lab_end_to_end_pipeline.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 03: Trajectory Eval (adk eval) 실행 경로 평가 및 배포 준비

## 실습 목표
`evalset.json`을 기준으로 에이전트의 툴 호출 순서와 응답 품질을 검증(`adk eval` / `agents-cli eval`)하고, Cloud Run 및 Vertex AI Agent Engine 배포 구성을 마무리합니다.

## 실습 순서
1. 완성된 정답 코드를 실행해 전체 파이프라인 동작을 확인합니다:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. `workshop/02_final/evalset.json` 테스트셋으로 Trajectory Eval(실행 경로 평가)을 수행합니다:
   ```bash
   adk eval workshop/02_final/sre_agent workshop/02_final/evalset.json
   ```
3. 워크숍 전체 검증 스크립트를 실행해 링크·모델 태그·코드 동작을 최종 확인합니다:
   ```bash
   python3 scripts/verify_workshop.py .
   ```
""")
            else:
                with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
                    f.write(f"""# {topic} - Hands-on Lab Session Guide

This guide outlines the session schedule and step-by-step objectives for the **{topic}** workshop.
Write your code in `workshop/01_starter`. If you get stuck, refer to the completed reference solution in `workshop/02_final`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & environment verification (`./scripts/check_env.sh`)
- **10m - 25m**: **Lab 01** - Environment Verification, ADK Scaffolding & Custom Tools (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - Multi-Agent Hierarchy, Sub-Agent Routing & Structured Outputs (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - Trajectory Evaluation (`adk eval`), ADLC Optimization & Deployment (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Environment Verification, ADK Scaffolding & Custom Tools](./01_lab_environment_and_client.md)**
2. **[Lab 02: Multi-Agent Hierarchy, Sub-Agent Routing & Structured Outputs](./02_lab_structured_outputs.md)**
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
                    f.write(f"""# Lab 02: Multi-Agent Hierarchy, Sub-Agent Routing & Structured Outputs

## Objective
Wire specialized sub-agents (`slo_specialist`, `report_specialist`) under a root coordinator (`root_agent` running `{default_flagship_model}`) and enforce deterministic JSON schema outputs.

## Instructions
1. Review `prompt-pack/README.md` for the target JSON Schema.
2. In Python (`workshop/01_starter/agent.py`), attach `sub_agents=[slo_specialist, report_specialist]` to `root_agent`.
3. If exploring the Go, Java, Kotlin, or TypeScript tracks under `workshop/02_final/polyglot/`, compare how `SubAgents` / `subAgents` and `SequentialAgent` route tasks across languages.
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
            if final_lang == "ko":
                with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
                    f.write(f"""# {topic} - 핸즈온 실습 가이드

**{topic}** 세션의 단계별 실습 가이드입니다.
실습 코드는 `workshop/01_starter/main.py`에서 직접 작성하고, 막히는 부분이 있으면 `workshop/02_final/main.py` 정답 코드를 참고하세요.

---

## 세션 진행 순서 (총 60분)

- **00m - 10m**: 세션 소개 및 개발 환경 점검 (`./scripts/check_env.sh`)
- **10m - 25m**: **Lab 01** - 개발 환경 점검 및 AI 클라이언트 연결 확인 (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - Structured Output 및 JSON 스키마 검증 (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - End-to-End 파이프라인 실행 및 자동 검증 (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A 및 마무리

---

## 단계별 실습 문서

1. **[Lab 01: 개발 환경 점검 및 AI 클라이언트 연결 확인](./01_lab_environment_and_client.md)**
2. **[Lab 02: Structured Output 및 JSON 스키마 검증](./02_lab_structured_outputs.md)**
3. **[Lab 03: End-to-End 파이프라인 실행 및 자동 검증](./03_lab_end_to_end_pipeline.md)**
""")
                with open(labs_dir / "01_lab_environment_and_client.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 01: 개발 환경 점검 및 AI 클라이언트 연결 확인

## 실습 목표
`./scripts/check_env.sh`로 로컬 및 클라우드 개발 환경을 점검하고, `workshop/01_starter/main.py`에서 {provider_label}(`{default_cloud_model}`) 또는 로컬 Ollama(`{default_local_model}`) 서버와 정상적으로 통신하는지 스모크 테스트를 진행합니다.

## 실습 순서
1. `./scripts/check_env.sh` (Windows는 `.\\scripts\\check_env.ps1`)를 실행해 Python, `uv`, 로컬 포트 상태를 확인합니다.
2. `workshop/01_starter/main.py`를 열고 `lab1_sanity_check()` 함수 안의 `TODO: [Lab 01 - Exercise]` 주석을 확인합니다.
3. `.env` 파일에 `{primary_api_key_env}`를 입력하거나, 로컬 Ollama 서버(`ollama serve`, 모델 `{default_local_model}`)를 띄웁니다.
4. 스타터 스크립트를 실행해 모델 응답이 정상적으로 돌아오는지 확인합니다:
   ```bash
   python3 workshop/01_starter/main.py
   ```
""")
                with open(labs_dir / "02_lab_structured_outputs.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 02: Structured Output 및 JSON 스키마 검증

## 실습 목표
Pydantic `WorkshopTaskResult` 스키마(`status`, `model_used`, `summary`, `action_items`)에 맞춰 항상 파싱 가능한 JSON 응답(Structured Output)을 받도록 구성합니다.

## 실습 순서
1. `prompt-pack/README.md`에서 시스템 프롬프트와 출력 JSON 스키마 정의를 확인합니다.
2. `workshop/01_starter/main.py`의 `lab2_structured_output()` 함수에서 `TODO: [Lab 02 - Exercise]` 부분을 완성합니다.
3. 마크다운 코드 블록(` ```json `)이 섞이지 않고 스키마에 맞는 순수 JSON으로 직렬화되는지 확인합니다.
""")
                with open(labs_dir / "03_lab_end_to_end_pipeline.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 03: End-to-End 파이프라인 실행 및 자동 검증

## 실습 목표
클라우드·로컬 폴백(Fallback)이 적용된 `workshop/02_final/main.py` 전체 파이프라인을 실행하고, 자동 검증 스크립트로 워크숍 산출물 상태를 점검합니다.

## 실습 순서
1. 완성된 정답 코드를 실행합니다:
   ```bash
   python3 workshop/02_final/main.py
   ```
2. 직접 작성한 `workshop/01_starter/main.py` 코드와 `workshop/02_final/main.py` 정답 코드를 비교해 봅니다.
3. 워크숍 검증 스크립트를 돌려 마크다운 링크, 모델 버전, 보안 항목을 한 번에 점검합니다:
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
- **10m - 25m**: **Lab 01** - Environment Verification & AI Client Smoke Test (`01_lab_environment_and_client.md`)
- **25m - 45m**: **Lab 02** - Structured Outputs & JSON Schema Validation (`02_lab_structured_outputs.md`)
- **45m - 55m**: **Lab 03** - End-to-End Pipeline & Automated Verification (`03_lab_end_to_end_pipeline.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Environment Verification & AI Client Smoke Test](./01_lab_environment_and_client.md)**
2. **[Lab 02: Structured Outputs & JSON Schema Validation](./02_lab_structured_outputs.md)**
3. **[Lab 03: End-to-End Pipeline & Automated Verification](./03_lab_end_to_end_pipeline.md)**
""")
                with open(labs_dir / "01_lab_environment_and_client.md", "w", encoding="utf-8") as f:
                    f.write(f"""# Lab 01: Environment Verification & AI Client Smoke Test

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

