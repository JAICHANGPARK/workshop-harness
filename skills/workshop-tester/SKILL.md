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

## Typography, Developer Terminology & Natural Multilingual Grammar Rules

- **Original Technical Term First, Real-World Developer Terminology & Natural Grammar (기술 용어 원어 우선 표기, 실무 개발자 용어/문법 사용 & 직역·번역투 금지)**:
  - **English (EN)**: Write in clear, idiomatic, direct technical English.
  - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slides, runbooks, or code comments in Korean, Japanese, or Chinese, **never use awkward word-for-word literal translations or unnatural translationese grammar (번역투 문법, 不自然な直訳調, 生硬的机翻腔)**.
  - **Use the original English technical term first and append the developer-friendly term in parentheses (`English Original (개발자 친화적 용어)`), and write in natural sentence grammar used by local software engineers**:
    - **Korean (KO)**: **Hands-on Lab (핸즈온 랩)**, **Scaffolding (스캐폴딩)**, **Runbook (런북)**, **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)**, **Prompt Engineering (프롬프트 엔지니어링)**, **Structured Outputs (구조화 출력 / JSON Schema)**, **Tool Calling / Function Calling (툴 콜링 / 함수 호출)**, **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**, **Embedding (임베딩)**, **Quantization (양자화)**, **Thinking Budget (추론 예산)**, **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)**, **Sub-Agent Delegation (서브 에이전트 위임)**, **Trajectory Evaluation (궤적 평가)**, **Dependency Injection (의존성 주입)**, **Fallback (폴백)**, **Smoke Test (스모크 테스트)**, **Breaking Changes (브레이킹 체인지)**. Never use awkward literals ("손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트") or double passives (`~되어집니다` -> `~됩니다`).
    - **Japanese (JA)**: 「Hands-on Lab (ハンズオンラボ)」, 「Scaffolding (スキャフォールディング)」, 「Starter / Boilerplate Code (スターターコード)」, 「Structured Outputs (構造化出力)」, 「Thinking Budget (推論バジェット)」, 「Runbook (ランブック)」, 「Smoke Test (スモークテスト)」 (Never 「手で触る実験室」, 「走る本」, 「骨組みコード」, 「思考の予算」; write in natural Japanese engineer style `〜を設定します`, `〜を実行できます`).
    - **Chinese (ZH)**: 「Hands-on Lab (实战工作坊)」, 「Scaffolding (脚手架)」, 「Starter / Boilerplate Code (Starter 初始代码 / 样板代码)」, 「Structured Outputs (结构化输出)」, 「Thinking Budget (推理预算)」, 「Runbook (演练手册)」, 「Smoke Test (冒烟测试)」 (Never 「手把手的实验室」, 「奔跑的书」, 「骨架代码」, 「思考预算」; write in concise Chinese developer phrasing).
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.
