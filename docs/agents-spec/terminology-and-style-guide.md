# Developer Terminology & Bilingual Technical Term Notation Guide

> Official Documentation, Slide Deck, and Code Comment Authoring Standard for `workshop-harness`

When AI coding agents (**Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**) generate or localize workshop documentation, hands-on lab guides, slide decks, runbooks, or code comments in Korean (KO), Japanese (JA), or Chinese (ZH), they must follow the **Developer-Friendly Terminology & Bilingual Notation Protocol** below.

---

## 1. Core Principles

### A. No Awkward Literal Translations (직역 금지 및 실무 개발자 용어 사용)
- Never translate software engineering or AI/ML terminology word-for-word into unnatural phrases that real-world developers do not use.
- Always use the community-standard developer terminology used in production engineering teams, tech blogs, and developer conferences (Build with AI, DevFest, Google I/O, KotlinConf).

### B. Bilingual Technical Term Notation (기술 용어 영어 원문 병기 원칙)
- When writing technical documentation, headings, tables, or code comments in Korean, Japanese, or Chinese, **always include the original English technical term alongside the developer-friendly localized term**:
  - **Format**: `개발자 친화적 한국어 용어 (English Original Term)` or `English Original Term (개발자 친화적 설명)`
  - **First Mention & Headings**: Always provide the bilingual pair (`한국어 용어 (English Original)`) in section headings, summary tables, and on first mention in each document or lab step.
  - **Code Identifiers & SDK Symbols**: Never translate code symbols, CLI flags, environment variable names, or class/method names (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`, `GEMINI_API_KEY`). Keep them in backticks in their exact original English form.

### C. Clean Typography Rule (No Em Dash `\u2014`)
- Never generate em dash characters (`\u2014`) in any markdown (`.md`) file, slide deck, setup guide, or code comment.
- Use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.

---

## 2. Standard Bilingual Developer Terminology Reference Table (KO / EN / JA / ZH)

| Prohibited Literal Translation (직역 금지 예시) | Approved Korean + English Bilingual Notation (권장 표기: 개발자 용어 + 영어 원문 병기) | Japanese (JA) + English | Chinese (ZH) + English |
| :--- | :--- | :--- | :--- |
| 손으로 하는 실험실 / 실습실 | **핸즈온 랩 (Hands-on Lab)** | ハンズオンラボ (Hands-on Lab) | 动手实验 / 实战工作坊 (Hands-on Lab) |
| 달리는 책 / 운영 수첩 | **런북 (Runbook)** | ランブック (Runbook) | 演练手册 (Runbook) |
| 발판 설치 / 뼈대 공사 | **스캐폴딩 (Scaffolding)** | スキャフォールディング (Scaffolding) | 脚手架 (Scaffolding) |
| 생각 예산 / 사고 한도 | **추론 예산 (Thinking Budget)** | 推論バジェット (Thinking Budget) | 推理预算 (Thinking Budget) |
| 구조화된 출력물 | **구조화 출력 (Structured Outputs / JSON Schema)** | 構造化出力 (Structured Outputs) | 结构化输出 (Structured Outputs) |
| 도구 부르기 / 함수 부르기 | **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)** | ツール呼び出し (Tool Calling) | 工具调用 / 函数调用 (Tool Calling) |
| 검색 증강된 생성 | **검색 증강 생성 (RAG, Retrieval-Augmented Generation)** | 検索拡張生成 (RAG) | 检索增强生成 (RAG) |
| 끼워넣기 벡터 | **임베딩 (Embedding)** | エンベディング (Embedding) | 向量嵌入 (Embedding) |
| 정량화 / 양자 축소 | **양자화 (Quantization, 4-bit / GGUF)** | 量子化 (Quantization) | 量化 (Quantization) |
| 미세 조정하기 | **파인튜닝 (Fine-tuning)** | ファインチューニング (Fine-tuning) | 微调 (Fine-tuning) |
| 다중 대리인 지휘 | **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)** | マルチエージェント・オーケストレーション (Multi-Agent Orchestration) | 多智能体编排 (Multi-Agent Orchestration) |
| 하위 대리인 넘기기 | **서브 에이전트 위임 / 핸드오프 (Sub-Agent Delegation / Handoff)** | サブエージェント委譲 (Sub-Agent Delegation) | 子智能体委派 (Sub-Agent Delegation) |
| 궤도 채점 / 경로 평가 | **궤적 평가 (Trajectory Evaluation)** | トラジェクトリ評価 (Trajectory Evaluation) | 轨迹评估 (Trajectory Evaluation) |
| 연기 시험 | **스모크 테스트 (Smoke Test)** | スモークテスト (Smoke Test) | 冒烟测试 (Smoke Test) |
| 후퇴 경로 / 비상 후퇴 | **폴백 (Fallback / 우회 경로)** | フォールバック (Fallback) | 回退方案 (Fallback) |
| 상투적인 판박이 코드 | **보일러플레이트 코드 (Boilerplate Code)** | ボイラープレート (Boilerplate) | 样板代码 (Boilerplate) |
| 의존성 주사 | **의존성 주입 (Dependency Injection)** | 依存性の注入 (Dependency Injection) | 依赖注入 (Dependency Injection) |
| 차가운 시작 | **콜드 스타트 (Cold Start)** | コールドスタート (Cold Start) | 冷启动 (Cold Start) |
| 기억 장치 넘침 | **메모리 부족 에러 (OOM, Out-Of-Memory)** | メモリ不足エラー (OOM) | 内存溢出错误 (OOM) |

---

## 3. Code Comment & Docstring Guidelines (코드 주석 작성 지침)

When writing comments or docstrings in starter (`01_starter`) and reference solution (`02_final`) code:

1. **Preserve Original English Technical Terms in Parentheses**:
   ```python
   # TODO [Lab 02]: 구조화 출력 (Structured Outputs)을 위해 Pydantic JSON Schema와 추론 예산 (Thinking Budget)을 설정합니다.
   config = types.GenerateContentConfig(
       response_mime_type="application/json",
       response_schema=WorkshopSummary,
       thinking_config=types.ThinkingConfig(thinking_budget=1024),
   )
   ```
2. **Never Translate Code Symbols or API Parameters**:
   - Refer to `root_agent`, `sub_agents`, `FunctionTool`, `InMemoryRunner`, and `GenerateContentConfig` using their exact English identifiers.
3. **Automated Verification**:
   - Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to automatically scan for forbidden em dashes (`\u2014`) and prohibited literal translations.

---

## References

- [AGENTS.md Specification](./agents-md.md)
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
