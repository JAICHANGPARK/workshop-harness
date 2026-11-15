---
name: agents-cli-workshop-builder
description: Builds end-to-end Agent Development Lifecycle (ADLC) workshops using Google Agents CLI (google-agents-cli / google/agents-cli) and its 7 official AI coding agent skills (workflow, adk-code, scaffold, eval, deploy, publish, observability). Automates scaffolding, synthetic eval dataset generation, LLM-as-a-Judge optimization loops, Cloud Run / Vertex AI Agent Runtime deployment, Gemini Enterprise registry publishing, and Cloud Trace observability labs.
---

# Google Agents CLI (`google-agents-cli`) Workshop Builder Skill

## Purpose

Automates the end-to-end creation of technical hands-on workshops centered on **`google-agents-cli` (`google/agents-cli`)** and the complete **Agent Development Lifecycle (ADLC)** on Google Cloud and the Gemini Enterprise Agent Platform. This skill teaches attendees how to combine **`agents-cli` CLI commands** with its **7 built-in AI coding assistant skills** (for Antigravity, Gemini CLI, Claude Code, Codex, and Cursor) to take an ADK agent from initial scaffolding to automated evaluation, cloud deployment, enterprise registry publication, and production telemetry.

> Pre-Flight Web Research Protocol:
> Before generating workshop materials, execute live web searches to verify the latest `google-agents-cli` release (`google-agents-cli>=1.4.1`, `uvx google-agents-cli setup`, `npx skills add google/agents-cli`), ADK compatibility (`google-adk>=2.14.0`), and current Gemini model tags (`gemini-4-carbon`, `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`).

---

## Core Architecture: How `agents-cli` Bridges ADK & Coding Agents

- **ADK (`google-adk`)**: The code-first runtime framework that defines `root_agent`, `LlmAgent`, `sub_agents`, tools, callbacks, and session state.
- **`agents-cli` (`google-agents-cli`)**: The unified lifecycle CLI and skill suite that wraps ADK projects with production scaffolding, synthetic evaluation pipelines, managed deployment, enterprise governance, and OpenTelemetry / Cloud Trace observability.

```mermaid
flowchart LR
    Setup["1. Setup & Skills<br>uvx google-agents-cli setup"] --> Scaffold["2. Scaffold<br>agents-cli create / enhance"]
    Scaffold --> Code["3. ADK Code<br>root_agent + Tools + Callbacks"]
    Code --> Eval["4. Evaluate & Optimize<br>agents-cli eval synthesize/run/grade/optimize"]
    Eval --> Deploy["5. Deploy<br>agents-cli deploy (Agent Runtime / Cloud Run / GKE)"]
    Deploy --> Publish["6. Publish & Observe<br>Gemini Enterprise Registry + Cloud Trace"]
```

---

## The 7 Official `google-agents-cli` Coding Assistant Skills

When attendees run `uvx google-agents-cli setup` or `npx skills add google/agents-cli`, their AI coding assistant gains 7 specialized domain skills:

| Skill Identifier | Lifecycle Stage | Primary Capability & Workshop Role |
|---|---|---|
| **`google-agents-cli-workflow`** | End-to-End ADLC | Guides full agent lifecycle sequencing, code preservation rules, and 2026 Gemini model selection (`gemini-4-carbon` vs `gemini-4-hydrogen` / `gemini-3.8-flash`) |
| **`google-agents-cli-scaffold`** | Project Initialization | Executes `agents-cli create <name>`, `enhance`, and `upgrade` from `adk-samples` or custom templates |
| **`google-agents-cli-adk-code`** | Core Implementation | Enforces idiomatic ADK Python patterns (`root_agent`, `LlmAgent`, `sub_agents`, `FunctionTool`, `MCPToolset`, session state, callbacks) |
| **`google-agents-cli-eval`** | Quality & Optimization | Automates dataset synthesis (`eval dataset synthesize`), execution (`eval run`), LLM-as-a-Judge grading (`eval grade`), failure analysis (`eval analyze`), and prompt optimization (`eval optimize`) |
| **`google-agents-cli-deploy`** | Cloud Deployment | Automates containerization, Secret Manager bindings, CI/CD generation, and deployment to Vertex AI Agent Runtime, Cloud Run, or GKE |
| **`google-agents-cli-publish`** | Enterprise Governance | Registers deployed agents into the **Gemini Enterprise** agent registry for organization-wide discovery and IAM access control |
| **`google-agents-cli-observability`** | Production Telemetry | Configures Google Cloud Trace, Cloud Logging, OpenTelemetry exporters, and latency/token dashboards |

---

## Complete CLI Command Reference (`agents-cli`)

### 1. Environment & Skill Setup
```bash
# One-command CLI + AI Coding Agent Skills installation (requires Python 3.11+ and uv)
uvx google-agents-cli setup

# Alternative: Install the 7 skills directly into any AI coding agent via npx
npx skills add google/agents-cli
```

### 2. Project Scaffolding (`create` / `scaffold`)
```bash
# Scaffold a new production-ready ADK agent project
agents-cli create sreswarm-agent

# Enhance an existing ADK directory with deployment, eval, and observability manifests
agents-cli scaffold enhance --target ./sreswarm-agent
```

### 3. Evaluation & Optimization Loop (`eval`)
```bash
# Step 1: Synthesize golden evaluation scenarios from agent instructions and tool schemas
agents-cli eval dataset synthesize --agent ./sreswarm-agent --count 20 --output ./evals/golden_dataset.json

# Step 2: Execute agent runs across the evaluation dataset
agents-cli eval run --agent ./sreswarm-agent --dataset ./evals/golden_dataset.json

# Step 3: Grade trajectories and final responses using LLM-as-a-Judge rubrics
agents-cli eval grade --results ./evals/latest_run.json

# Step 4: Analyze failure clusters and auto-optimize system instructions
agents-cli eval analyze --results ./evals/latest_run.json
agents-cli eval optimize --agent ./sreswarm-agent --results ./evals/latest_run.json
```

### 4. Managed Deployment, Publishing & Observability (`deploy` / `publish`)
```bash
# Deploy to Vertex AI Agent Runtime (or --target cloud-run / --target gke)
agents-cli deploy --agent ./sreswarm-agent --target agent-runtime --project $GOOGLE_CLOUD_PROJECT --region us-central1

# Publish the deployed agent to Gemini Enterprise Registry
agents-cli publish --agent ./sreswarm-agent --registry gemini-enterprise
```

---

## 3-Stage Hands-on Lab Curriculum

```mermaid
flowchart TD
    Lab1["Lab 01: Skill Injection & ADK Project Scaffolding (20 min)<br>Run uvx google-agents-cli setup, scaffold project via agents-cli create, verify in adk web"]
    Lab2["Lab 02: Synthetic Eval Generation & Prompt Optimization Loop (35 min)<br>Synthesize golden test cases, run LLM-as-a-Judge grading, execute agents-cli eval optimize"]
    Lab3["Lab 03: Cloud Deployment, Enterprise Publishing & Cloud Trace (30 min)<br>Enhance project with observability, deploy to Agent Runtime / Cloud Run, publish to Gemini Enterprise"]

    Lab1 --> Lab2 --> Lab3
```

---

## Starter & Final Code Templates for `agents-cli` Workshops

### Starter Template (`workshop/01_starter.py`)
```python
"""
Workshop Starter: Google Agents CLI (google-agents-cli) & ADK Lifecycle Lab
Prerequisites:
  1. uvx google-agents-cli setup
  2. uv add google-adk google-genai pydantic
"""
import os
from google.adk.agents import LlmAgent


def lookup_service_slo(service_name: str) -> dict:
    """Returns target SLO latency and error budget for a production microservice.

    Args:
        service_name: Name of the microservice (e.g., 'checkout-api', 'auth-service').
    """
    slo_catalog = {
        "checkout-api": {"target_p99_ms": 250, "error_budget_remaining_pct": 42.0, "tier": "critical"},
        "auth-service": {"target_p99_ms": 120, "error_budget_remaining_pct": 88.5, "tier": "critical"},
    }
    return slo_catalog.get(
        service_name,
        {"target_p99_ms": 500, "error_budget_remaining_pct": 100.0, "tier": "standard"},
    )


# TODO (Lab 1): Define a specialist LlmAgent named 'slo_auditor' using model 'gemini-4-hydrogen'
# and bind lookup_service_slo in tools=[...].

# TODO (Lab 2): Define 'root_agent' using model 'gemini-4-carbon' and delegate SLO checks
# to 'slo_auditor' so `adk web` and `agents-cli eval run` can evaluate tool trajectories.
root_agent = LlmAgent(
    name="sre_lifecycle_coordinator",
    model="gemini-4-hydrogen",
    description="Starter SRE agent awaiting sub-agent delegation and tool binding.",
    instruction="Answer user questions about service SLOs.",
    tools=[lookup_service_slo],
)

if __name__ == "__main__":
    print(f"[Starter Ready] Loaded root_agent='{root_agent.name}' (model={root_agent.model})")
    print("Next steps:")
    print("  1. Launch interactive Dev UI: adk web")
    print("  2. Synthesize eval dataset : agents-cli eval dataset synthesize")
```

### Final Reference Solution (`workshop/02_final.py`)
```python
"""
Workshop Final Solution: Google Agents CLI (google-agents-cli) & ADK Lifecycle Lab
Verified for:
  - `adk web` / `adk run`
  - `agents-cli eval dataset synthesize` -> `eval run` -> `eval grade` -> `eval optimize`
  - `agents-cli deploy --target agent-runtime`
"""
import os
from google.adk.agents import LlmAgent


def lookup_service_slo(service_name: str) -> dict:
    """Returns target SLO latency and error budget for a production microservice.

    Args:
        service_name: Name of the microservice (e.g., 'checkout-api', 'auth-service').
    """
    slo_catalog = {
        "checkout-api": {"target_p99_ms": 250, "error_budget_remaining_pct": 42.0, "tier": "critical"},
        "auth-service": {"target_p99_ms": 120, "error_budget_remaining_pct": 88.5, "tier": "critical"},
    }
    return slo_catalog.get(
        service_name,
        {"target_p99_ms": 500, "error_budget_remaining_pct": 100.0, "tier": "standard"},
    )


def check_deployment_readiness(service_name: str, current_p99_ms: int) -> dict:
    """Evaluates whether a microservice passes its release gate against its SLO target.

    Args:
        service_name: Name of the microservice being deployed.
        current_p99_ms: Measured P99 latency in milliseconds from staging benchmarks.
    """
    slo = lookup_service_slo(service_name)
    passed = current_p99_ms <= slo["target_p99_ms"] and slo["error_budget_remaining_pct"] > 10.0
    return {
        "service_name": service_name,
        "current_p99_ms": current_p99_ms,
        "target_p99_ms": slo["target_p99_ms"],
        "error_budget_remaining_pct": slo["error_budget_remaining_pct"],
        "release_gate_passed": passed,
        "recommendation": "APPROVE_DEPLOY" if passed else "BLOCK_AND_ROLLBACK",
    }


slo_auditor = LlmAgent(
    name="slo_auditor",
    model="gemini-4-hydrogen",
    description="Audits microservice SLO targets, P99 latency thresholds, and release readiness gates.",
    instruction=(
        "Always call lookup_service_slo first to inspect the service tier and error budget, "
        "then call check_deployment_readiness when given a staging P99 latency measurement."
    ),
    tools=[lookup_service_slo, check_deployment_readiness],
)

release_reporter = LlmAgent(
    name="release_reporter",
    model="gemini-4-hydrogen",
    description="Formats release gate decisions into structured deployment readiness reports.",
    instruction=(
        "Produce a structured release gate summary containing Service Name, P99 Comparison, "
        "Error Budget Status, and Final Gate Decision (APPROVE_DEPLOY or BLOCK_AND_ROLLBACK)."
    ),
)

root_agent = LlmAgent(
    name="sre_lifecycle_coordinator",
    model="gemini-4-carbon",
    description="Root ADLC coordinator that orchestrates SLO auditing and deployment gate reporting.",
    instruction=(
        "You govern production release gates. "
        "1. Delegate SLO and latency verification to 'slo_auditor'. "
        "2. Delegate the final structured release decision report to 'release_reporter'."
    ),
    sub_agents=[slo_auditor, release_reporter],
)

if __name__ == "__main__":
    gate_check = check_deployment_readiness("checkout-api", 210)
    print(f"[Final Verified] root_agent='{root_agent.name}' (model={root_agent.model})")
    print(f"Sub-agents registered: {[a.name for a in root_agent.sub_agents]}")
    print(f"Sample Release Gate Verification: {gate_check}")
```

---

## Troubleshooting & Hotfix Matrix (`agents-cli`)

| Error Signature | Root Cause | Instant Hotfix / Action |
|---|---|---|
| `uvx: command not found` | Astral `uv` package manager not installed | Run `curl -LsSf https://astral.sh/uv/install.sh \| sh` (macOS/Linux) or `winget install astral-sh.uv` (Windows) |
| `DefaultCredentialsError: Could not automatically determine credentials` | GCP Application Default Credentials not configured for `deploy` / Cloud Trace | Run `gcloud auth application-default login` and `gcloud config set project <PROJECT_ID>` |
| `EvalTrajectoryMismatchError` | Agent skipped a required tool call during `agents-cli eval grade` | Run `agents-cli eval optimize` or tighten sub-agent `description` and `instruction` fields |
| `PermissionDenied: 403 Vertex AI Agent Engine API` | Required GCP APIs not enabled in target project | Run `gcloud services enable aiplatform.googleapis.com run.googleapis.com cloudtrace.googleapis.com` |

---

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never generate awkward literal translations from English or stiff translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
    - **Korean (KO)**: Use natural developer vernacular (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Do NOT repeat mechanical `Starter Code (스타터 코드)` echoes on every line, and NEVER output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", `~되어집니다`, `~하는 것이 가능합니다`).
    - **Japanese (JA)**: Use natural Japanese engineer terms (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Thinking Budget`, `フォールバック`; Never ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」; write in natural engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: Use authentic Chinese developer terms (`实战工作坊`, `脚手架`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Thinking Budget (推理预算)`, `回退策略`; Never ❌ 「手把手的实验室」, ❌ 「奔跑的书」, ❌ 「骨架代码」, ❌ 「思考预算」, ❌ 「健全性检查」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and write comments in concise, natural developer language.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
