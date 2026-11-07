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

- **Original Technical Term First & Real-World Developer Terminology (기술 용어 원어 우선 표기, 실무 개발자 용어 사용 & 직역 금지)**:
  - Never use awkward literal translations of English terms (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
  - For technical terms, use the original English term first and append the developer-friendly translation in parentheses (`English Original (개발자 친화적 용어)`), or pair established developer vernacular with the English original, such as:
    - **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
