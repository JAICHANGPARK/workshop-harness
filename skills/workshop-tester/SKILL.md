---
name: workshop-tester
description: Runs automated smoke tests on starter and final code, validates markdown document integrity (broken relative paths, missing image links), and generates a test report.
---

# Workshop Tester Skill

## Purpose
Catches broken code, missing files, broken markdown relative links, missing images, and dead HTTP URLs **before** the workshop goes live. Prevents attendees from running into preventable setup errors or dead links during live sessions.

---

## 3-Stage Automated Test Pipeline

```text
[Stage 1: Code Smoke Test] -> [Stage 2: Markdown Link & Image Integrity Audit] -> [Stage 3: TODO Alignment Audit]
```

### Stage 1: Code Smoke Tests
- **`01_starter/` Verification**: Verify dependencies install cleanly and entry point (`main.py` / `run.sh`) executes without syntax or import errors.
- **`02_final/` Verification**: Run reference solution end-to-end and confirm expected terminal output and non-zero exit codes.
- **Environment Scripts**: Run `scripts/check_env.sh` and `scripts/check_architecture_compat.sh` to ensure execution without errors.

### Stage 2: Markdown Link & Image Integrity Audit
- Scan all `.md` files in `docs/`, `workshop/`, and repository root for relative file links (`[text](./path/to/file.md)`).
- Verify that every referenced target file exists on disk.
- Scan for embedded image links (`![caption](images/pic.png)`) and confirm image files exist in specified paths.
- Flag dead external HTTP URLs (404 / 500 errors).

### Stage 3: Starter vs Final TODO Alignment Audit
- Scan `workshop/01_starter/` for all `# TODO: [Lab N]` markers.
- Verify that every marked TODO item has a corresponding completed solution in `workshop/02_final/`.

---

## CLI Command Integration

Run the full integrity audit suite via `harness_cli.py`:

```bash
uv run harness_cli.py test --target my-bwai-workshop
```

---

## Output Artifact & CI Integration

- **Output**: Detailed pass/fail test report printed to stdout with explicit error line numbers and broken file paths.
- **Exit Code**: Returns `0` on 100% pass; returns `1` on any broken link or code failure for CI/CD workflow enforcement.

---

## Typography, Developer Terminology & Bilingual Notation Rules

- **Developer-Friendly Terminology & English Original Notation (영어 원문 병기 & 직역 금지)**:
  - Never use awkward literal translations (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기").
  - Always use developer-friendly terminology commonly used by real-world software engineers AND include the original English technical term in parentheses (`개발자 친화적 용어 (English Original)`), such as:
    - **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**, **스모크 테스트 (Smoke Test)**, **보일러플레이트 코드 (Boilerplate Code)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
