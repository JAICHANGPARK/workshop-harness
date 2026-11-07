# Developer Terminology & Original Technical Term Notation Guide

> Official Documentation, Slide Deck, and Code Comment Authoring Standard for `workshop-harness`

When AI coding agents (**Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**) generate or localize workshop documentation, hands-on lab guides, slide decks, runbooks, or code comments in Korean (KO), Japanese (JA), or Chinese (ZH), they must follow the **Original Technical Term First & Real-World Developer Terminology Protocol** below.

---

## 1. Core Principles (핵심 작성 원칙)

### A. No Awkward Literal Translations (영문 직역 절대 금지)
- Never translate software engineering or AI/ML terminology word-for-word into unnatural phrases that real-world developers do not use (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경").
- Always write in the natural vernacular used by production software engineers in tech blogs, GitHub repositories, and developer conferences (Build with AI, DevFest, Google I/O, KotlinConf).

### B. Original Technical Term First + Developer-Friendly Term Notation (기술 용어 원어 우선 표기 및 개발자 용어 병기)
- For technical terms, **use the original English technical term first and append the developer-friendly translation/explanation in parentheses (`English Original Term (개발자 친화적 용어)`)**, or pair natural loanwords used by developers with the original English term (`개발자 용어 (English Original Term)`):
  - **Preferred Format 1 (Technical Term First)**: `Structured Outputs (구조화 출력)`, `Thinking Budget (추론 예산)`, `Trajectory Evaluation (궤적 평가)`, `Sub-Agent Delegation (서브 에이전트 위임)`, `RAG (Retrieval-Augmented Generation, 검색 증강 생성)`, `Human-in-the-Loop (HITL, 사용자 승인 체크포인트)`, `Context Window (컨텍스트 윈도우)`
  - **Preferred Format 2 (Established Developer Loanword + Original)**: `핸즈온 랩 (Hands-on Lab)`, `스캐폴딩 (Scaffolding)`, `런북 (Runbook)`, `툴 콜링 (Tool Calling)`, `임베딩 (Embedding)`, `양자화 (Quantization)`, `파인튜닝 (Fine-tuning)`, `폴백 (Fallback)`, `스모크 테스트 (Smoke Test)`, `보일러플레이트 코드 (Boilerplate Code)`
  - **Code Identifiers & SDK Symbols**: Never translate code symbols, CLI flags, environment variable names, or class/method names (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`, `GEMINI_API_KEY`). Keep them in backticks in their exact original English form.

### C. Clean Typography Rule (No Em Dash `\u2014`)
- Never generate em dash characters (`\u2014`) in any markdown (`.md`) file, slide deck, setup guide, or code comment.
- Use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.

---

## 2. Standard Technical Term & Developer Terminology Reference Table (KO / EN / JA / ZH)

| Prohibited Literal Translation (직역 금지 예시) | Approved Original + Developer Terminology (권장 표기: 원어 + 실무 개발자 용어 병기) | Japanese (JA) | Chinese (ZH) |
| :--- | :--- | :--- | :--- |
| 손으로 하는 실험실 / 실습실 | **Hands-on Lab (핸즈온 랩)** | Hands-on Lab (ハンズオンラボ) | Hands-on Lab (实战工作坊 / 动手实验) |
| 달리는 책 / 운영 수첩 | **Runbook (런북 / 진행 가이드)** | Runbook (ランブック) | Runbook (演练手册) |
| 발판 설치 / 뼈대 공사 | **Scaffolding (스캐폴딩 / 초기 구조 생성)** | Scaffolding (スキャフォールディング) | Scaffolding (脚手架) |
| 뼈대 코드 / 상투적인 판박이 코드 | **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)** | Starter / Boilerplate Code (ボイラープレート) | Starter / Boilerplate Code (样板代码) |
| 생각 예산 / 사고 예산 | **Thinking Budget (추론 예산)** | Thinking Budget (推論バジェット) | Thinking Budget (推理预算) |
| 구조화된 출력물 | **Structured Outputs (구조화 출력 / JSON Schema)** | Structured Outputs (構造化出力) | Structured Outputs (结构化输出) |
| 도구 부르기 / 함수 부르기 | **Tool Calling / Function Calling (툴 콜링 / 함수 호출)** | Tool Calling (ツール呼び出し) | Tool Calling (工具调用 / 函数调用) |
| 검색 증강된 생성 | **RAG (Retrieval-Augmented Generation, 검색 증강 생성)** | RAG (検索拡張生成) | RAG (检索增强生成) |
| 끼워넣기 벡터 | **Embedding (임베딩)** | Embedding (エンベディング) | Embedding (向量嵌入) |
| 정량화 / 양자 축소 | **Quantization (양자화, 4-bit / GGUF)** | Quantization (量子化) | Quantization (量化) |
| 미세 조정하기 | **Fine-tuning (파인튜닝)** | Fine-tuning (ファインチューニング) | Fine-tuning (微调) |
| 다중 대리인 지휘 | **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)** | Multi-Agent Orchestration (マルチエージェント・オーケストレーション) | Multi-Agent Orchestration (多智能体编排) |
| 하위 대리인 넘기기 | **Sub-Agent Delegation (서브 에이전트 위임 / 핸드오프)** | Sub-Agent Delegation (サブエージェント委譲) | Sub-Agent Delegation (子智能体委派) |
| 대리인 개발 키트 | **ADK (Agent Development Kit, 에이전트 개발 키트)** | ADK (Agent Development Kit) | ADK (智能体开发套件) |
| 궤도 채점 / 경로 채점 | **Trajectory Evaluation (궤적 평가)** | Trajectory Evaluation (トラジェクトリ評価) | Trajectory Evaluation (轨迹评估) |
| 연기 시험 | **Smoke Test (스모크 테스트)** | Smoke Test (スモークテスト) | Smoke Test (冒烟测试) |
| 후퇴 경로 / 비상 후퇴 | **Fallback (폴백 / 우회 경로)** | Fallback (フォールバック) | Fallback (回退方案) |
| 의존성 주사 | **Dependency Injection (의존성 주입)** | Dependency Injection (依存性の注入) | Dependency Injection (依赖注入) |
| 차가운 시작 | **Cold Start (콜드 스타트)** | Cold Start (コールドスタート) | Cold Start (冷启动) |
| 기억 장치 넘침 | **OOM (Out-Of-Memory, 메모리 부족 에러)** | OOM (メモリ不足エラー) | OOM (内存溢出错误) |
| 부서지는 변경 / 깨지는 변경 | **Breaking Changes (브레이킹 체인지 / 호환성 변경)** | Breaking Changes (破壊的変更) | Breaking Changes (破坏性变更) |
| 속도 제한 걸림 | **Rate Limit (레이트 리밋 / 호출 할당량 제한)** | Rate Limit (レート制限) | Rate Limit (速率限制) |
| 맥락 창문 / 문맥 창문 | **Context Window (컨텍스트 윈도우)** | Context Window (コンテキストウィンドウ) | Context Window (上下文窗口) |
| 체제 지시문 | **System Instruction (시스템 프롬프트)** | System Instruction (システムプロンプト) | System Instruction (系统提示词) |
| 인간 고리 안 / 사람을 루프에 | **Human-in-the-Loop (HITL, 사용자 승인 체크포인트)** | Human-in-the-Loop (HITL) | Human-in-the-Loop (人机协同审批) |
| 기술 조교 | **TA (Teaching Assistant, 실습 코치 / 퍼실리테이터)** | TA (ティーチングアシスタント) | TA (助教) |
| 저장소 복제 | **리포지토리 클론 (Repository Clone)** | リポジトリのクローン (Repository Clone) | 克隆仓库 (Repository Clone) |

---

## 3. Code Comment & Docstring Guidelines (코드 주석 작성 지침)

When writing comments or docstrings in starter (`01_starter`) and reference solution (`02_final`) code:

1. **Use Original English Technical Terms + Developer-Friendly Korean Explanation**:
   ```python
   # TODO [Lab 02]: Structured Outputs (구조화 출력)을 위해 Pydantic JSON Schema와 Thinking Budget (추론 예산)을 설정합니다.
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
