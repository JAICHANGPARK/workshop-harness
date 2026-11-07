# Developer Terminology, Original Technical Term & Natural Grammar Guide (EN / KO / JA / ZH)

> Official Documentation, Slide Deck, and Code Comment Authoring Standard for `workshop-harness`

When AI coding agents (**Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**) generate workshop documentation, hands-on lab guides, slide decks, runbooks, or code comments:
- **English (`EN`)**: Write in clear, idiomatic English technical prose.
- **Korean (`KO`), Japanese (`JA`), Chinese (`ZH`)**: When requested by a Korean, Japanese, or Chinese user, **never translate English word-for-word (no literal translation or awkward translationese grammar)**. Always use **the original English technical term paired with the actual terminology, expressions, and natural sentence structures used by real-world local software engineers**.

---

## 1. Core Principles (핵심 작성 원칙)

### A. No Awkward Literal Translations (영문 직역 절대 금지)
- Never translate software engineering or AI/ML terminology word-for-word into unnatural phrases that real-world developers do not use.
  - **KO Prohibited**: "손으로 하는 실험실", "달리는 책", "발판 설치", "뼈대 코드", "생각 예산", "도구 부르기", "대리인 개발 키트", "문맥 창문", "부서지는 변경"
  - **JA Prohibited**: 「手で触る実験室」, 「走る本」, 「足場の設置」, 「骨組みコード」, 「思考の予算」, 「道具を呼ぶ」, 「代理人開発キット」, 「煙の試験」, 「後退経路」
  - **ZH Prohibited**: “手把手的实验室”, “奔跑的书”, “骨架代码”, “思考预算”, “工具呼叫”, “代理人开发套件”, “烟雾测试”, “后退路径”, “冰冷启动”
- Always write in the natural vernacular used by production software engineers in tech blogs, GitHub repositories, and developer conferences (Build with AI, DevFest, Google I/O, KotlinConf).

### B. Original Technical Term First + Developer-Friendly Term Notation (기술 용어 원어 우선 표기 및 개발자 용어 병기)
- For technical terms, **use the original English technical term first and append the developer-friendly translation/explanation in parentheses (`English Original Term (개발자 친화적 용어)`)**, or pair natural loanwords used by developers with the original English term:
  - **Korean (KO)**: `Hands-on Lab (핸즈온 랩)`, `Scaffolding (스캐폴딩)`, `Runbook (런북)`, `Starter / Reference Solution (스타터 / 레퍼런스 솔루션 코드)`, `Structured Outputs (구조화 출력)`, `Tool Calling (툴 콜링)`, `Thinking Budget (추론 예산)`, `Trajectory Evaluation (궤적 평가)`, `Fallback (폴백)`
  - **Japanese (JA)**: `Hands-on Lab (ハンズオンラボ)`, `Scaffolding (スキャフォールディング)`, `Runbook (ランブック)`, `Starter / Reference Solution (スターターコード / リファレンス実装)`, `Structured Outputs (構造化出力)`, `Tool Calling (ツール呼び出し)`, `Thinking Budget (推論バジェット)`, `Trajectory Evaluation (トラジェクトリ評価)`, `Fallback (フォールバック)`
  - **Chinese (ZH)**: `Hands-on Lab (实战工作坊 / 动手实验)`, `Scaffolding (脚手架)`, `Runbook (演练手册)`, `Starter / Reference Solution (Starter 初始代码 / 参考实现)`, `Structured Outputs (结构化输出)`, `Tool Calling (工具调用)`, `Thinking Budget (推理预算)`, `Trajectory Evaluation (轨迹评估)`, `Fallback (回退方案)`
  - **Code Identifiers & SDK Symbols**: Never translate code symbols, CLI flags, environment variable names, or class/method names (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`, `GEMINI_API_KEY`). Keep them in backticks in their exact original English form.

### C. Natural Developer Grammar & Anti-Translationese (실무 개발자 문법 및 번역투 문장 금지)
- When generating Korean, Japanese, or Chinese documentation, follow the natural grammar and sentence style of native software engineers rather than English syntactic calques:
  1. **Korean (KO) Developer Grammar**:
     - Avoid awkward double passives (`~되어지다`, `~에 의해 생성되어집니다`), unnatural pronouns (`당신의 API 키`, `그것은 ~를 가집니다`), and verbose translationese (`~하는 것이 가능합니다`).
     - Use concise, active developer prose (`~를 생성합니다`, `~할 수 있습니다`, `환경 변수에 API 키를 설정합니다`) and clean noun-ending (`~생성`, `~검증`) in tables and bullet lists.
  2. **Japanese (JA) Developer Grammar**:
     - Avoid literal English passive/modal calques (`〜によって生成されることができます`, `あなたのAPIキーを設定してください`, `それは〜を持っています`).
     - Use natural Japanese engineering documentation style (`〜を生成します`, `〜が可能です`, `環境変数にAPIキーを設定します`, and concise `体言止め` in tables and summary items).
  3. **Chinese (ZH) Developer Grammar**:
     - Avoid clunky Europeanized translationese (`被通过...所生成`, `去进行一个...的操作`, `你的 API 密钥`).
     - Use crisp, active Chinese technical phrasing (`通过...自动生成`, `配置 API Key`, `执行冒烟测试`).

### D. Clean Typography Rule (No Em Dash `\u2014`)
- Never generate em dash characters (`\u2014`) in any markdown (`.md`) file, slide deck, setup guide, or code comment.
- Use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.

---

## 2. Standard Technical Term & Developer Terminology Reference Table (KO / EN / JA / ZH)

| Prohibited Literal Translation (직역 금지 예시) | Approved Korean (KO) + English | Approved Japanese (JA) + English | Approved Chinese (ZH) + English |
| :--- | :--- | :--- | :--- |
| 손으로 하는 실험실 / 手で触る実験室 / 手把手的实验室 | **Hands-on Lab (핸즈온 랩)** | **Hands-on Lab (ハンズオンラボ)** | **Hands-on Lab (实战工作坊 / 动手实验)** |
| 달리는 책 / 走る本 / 奔跑的书 | **Runbook (런북 / 진행 가이드)** | **Runbook (ランブック)** | **Runbook (演练手册)** |
| 발판 설치 / 足場の設置 / 脚手架安装 | **Scaffolding (스캐폴딩 / 초기 구조 생성)** | **Scaffolding (スキャフォールディング)** | **Scaffolding (脚手架)** |
| 뼈대 코드 / 骨組みコード / 骨架代码 | **Starter / Boilerplate Code (스타터 / 보일러플레이트 코드)** | **Starter / Boilerplate Code (スターターコード / ボイラープレート)** | **Starter / Boilerplate Code (Starter 初始代码 / 样板代码)** |
| 생각 예산 / 思考の予算 / 思考预算 | **Thinking Budget (추론 예산)** | **Thinking Budget (推論バジェット)** | **Thinking Budget (推理预算)** |
| 구조화된 출력물 / 構造化された出力物 / 被结构化的输出物 | **Structured Outputs (구조화 출력 / JSON Schema)** | **Structured Outputs (構造化出力)** | **Structured Outputs (结构化输出)** |
| 도구 부르기 / 道具を呼ぶ / 工具呼叫 | **Tool Calling / Function Calling (툴 콜링 / 함수 호출)** | **Tool Calling (ツール呼び出し)** | **Tool Calling (工具调用 / 函数调用)** |
| 검색 증강된 생성 / 検索増強された生成 / 被检索增强的生成 | **RAG (Retrieval-Augmented Generation, 검색 증강 생성)** | **RAG (検索拡張生成)** | **RAG (检索增强生成)** |
| 끼워넣기 벡터 / 埋め込みベクトル / 嵌入进去的向量 | **Embedding (임베딩)** | **Embedding (エンベディング)** | **Embedding (向量嵌入)** |
| 정량화 / 양자 축소 | **Quantization (양자화, 4-bit / GGUF)** | **Quantization (量子化)** | **Quantization (量化)** |
| 미세 조정하기 / 微調整する / 进行微调操作 | **Fine-tuning (파인튜닝)** | **Fine-tuning (ファインチューニング)** | **Fine-tuning (微调)** |
| 다중 대리인 지휘 / 多重代理人指揮 / 多代理人指挥 | **Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)** | **Multi-Agent Orchestration (マルチエージェント・オーケストレーション)** | **Multi-Agent Orchestration (多智能体编排 / 多 Agent 编排)** |
| 하위 대리인 넘기기 / 下位代理人引き渡し / 下级代理人移交 | **Sub-Agent Delegation (서브 에이전트 위임 / 핸드오프)** | **Sub-Agent Delegation (サブエージェント委譲)** | **Sub-Agent Delegation (子 Agent 委派)** |
| 대리인 개발 키트 / 代理人開発キット / 代理人开发套件 | **ADK (Agent Development Kit, 에이전트 개발 키트)** | **ADK (Agent Development Kit)** | **ADK (Agent 开发套件)** |
| 궤도 채점 / 軌道採点 / 轨道打分 | **Trajectory Evaluation (궤적 평가)** | **Trajectory Evaluation (トラジェクトリ評価)** | **Trajectory Evaluation (轨迹评估)** |
| 연기 시험 / 煙の試験 / 烟雾测试 | **Smoke Test (스모크 테스트)** | **Smoke Test (スモークテスト)** | **Smoke Test (冒烟测试)** |
| 후퇴 경로 / 後退経路 / 后退路径 | **Fallback (폴백 / 우회 경로)** | **Fallback (フォールバック)** | **Fallback (回退方案)** |
| 의존성 주사 / 依存性注射 / 依赖注射 | **Dependency Injection (의존성 주입)** | **Dependency Injection (依存性の注入)** | **Dependency Injection (依赖注入)** |
| 차가운 시작 / 冷たい開始 / 冰冷启动 | **Cold Start (콜드 스타트)** | **Cold Start (コールドスタート)** | **Cold Start (冷启动)** |
| 기억 장치 넘침 / 記憶装置あふれ / 内存满溢 | **OOM (Out-Of-Memory, 메모리 부족 에러)** | **OOM (メモリ不足エラー)** | **OOM (内存溢出错误)** |
| 부서지는 변경 / 壊れる変更 / 破碎性变更 | **Breaking Changes (브레이킹 체인지 / 호환성 변경)** | **Breaking Changes (破壊的変更)** | **Breaking Changes (破坏性变更)** |
| 속도 제한 걸림 / 速度制限 / 速度限制 | **Rate Limit (레이트 리밋 / 호출 할당량 제한)** | **Rate Limit (レート制限)** | **Rate Limit (速率限制)** |
| 맥락 창문 / 文脈の窓 / 语境窗户 | **Context Window (컨텍스트 윈도우)** | **Context Window (コンテキストウィンドウ)** | **Context Window (上下文窗口)** |
| 체제 지시문 / 体制指示文 / 体制指示文 | **System Instruction (시스템 프롬프트)** | **System Instruction (システムプロンプト)** | **System Instruction (系统提示词)** |
| 인간 고리 안 / 人間を輪の中に / 人在环路里 | **Human-in-the-Loop (HITL, 사용자 승인 체크포인트)** | **Human-in-the-Loop (HITL)** | **Human-in-the-Loop (人机协同审批)** |

---

## 3. Grammar & Sentence Style Comparison (번역투 문법 vs 실무 개발자 문법 예시)

| Language | Awkward Translationese Grammar (지양: 번역투 문장) | Natural Developer Grammar (권장: 실무 개발자 문장) |
| :--- | :--- | :--- |
| **Korean (KO)** | "당신의 `GEMINI_API_KEY`가 설정되어져 있는지 확인하는 것이 가능합니다." | "`.env` 파일에 `GEMINI_API_KEY` 환경 변수가 정상적으로 설정되었는지 확인합니다." |
| **Korean (KO)** | "이 도구는 손으로 하는 실험실을 위한 뼈대 코드를 생성해 줍니다." | "이 CLI는 Hands-on Lab (핸즈온 랩)을 위한 Starter Code (스타터 코드)를 자동 생성합니다." |
| **Japanese (JA)** | "あなたのAPIキーによってモデルが呼び出されることができます。" | "`GEMINI_API_KEY` を設定してモデル API を呼び出します。" |
| **Japanese (JA)** | "このスクリプトは骨組みコードと走る本を作ります。" | "このスクリプトは Starter Code (スターターコード) と Runbook (ランブック) を自動生成します。" |
| **Chinese (ZH)** | "你的 API 密钥可以被用来去进行一个模型的呼叫操作。" | "配置 `GEMINI_API_KEY` 环境变量以调用模型 API。" |
| **Chinese (ZH)** | "自动生成手把手的实验室的骨架代码与奔跑的书。" | "自动生成 Hands-on Lab (实战工作坊) 的 Starter 初始代码与 Runbook (演练手册)。" |

---

## 4. Code Comment & Docstring Guidelines (코드 주석 작성 지침)

When writing comments or docstrings in starter (`01_starter`) and reference solution (`02_final`) code:

1. **Use Original English Technical Terms + Developer-Friendly Explanation**:
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
   - Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to automatically scan for forbidden em dashes (`\u2014`), prohibited literal translations, and awkward translationese expressions across KO, JA, and ZH.

---

## References

- [AGENTS.md Specification](./agents-md.md)
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
