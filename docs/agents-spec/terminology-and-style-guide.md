# Real-World Developer Language & Anti-Translationese Guide (EN / KO / JA / ZH)

> Official Documentation, Lab Guide, Slide Deck, and Code Comment Authoring Standard for `workshop-harness`

When AI coding agents (**Google Antigravity**, **Gemini CLI**, **Anthropic Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**) generate workshop documentation, hands-on lab guides, slide decks, runbooks, or code comments:
- **English (`EN`)**: Write in clear, idiomatic, direct technical English.
- **Korean (`KO`), Japanese (`JA`), Chinese (`ZH`)**: **Never generate awkward literal translations from English (영문 직역 절대 금지) or stiff translationese grammar (번역투 문장 금지).** Write in the exact everyday vernacular, vocabulary, and sentence rhythm that real software engineers actually use in Slack, GitHub PRs, tech blogs, and developer conferences (Build with AI, DevFest, Google I/O, KotlinConf).

---

## 1. Core Principles (핵심 작성 원칙)

### A. Never Generate Awkward English-to-Local Calques (영문 직역 절대 금지)
LLMs frequently translate idiomatic English engineering expressions into stiff Sino-Korean/Kanji calques that **no real developer says in practice**. Both exaggerated word-for-word literals and subtle calques are strictly prohibited:
- **KO Prohibited (직역 금지)**:
  - Exaggerated literals: ❌ `"손으로 하는 실험실"`, ❌ `"달리는 책"`, ❌ `"발판 설치"`, ❌ `"뼈대 코드"`, ❌ `"생각 예산"`, ❌ `"도구 부르기"`, ❌ `"대리인 개발 키트"`, ❌ `"연기 테스트"`
  - Subtle English calques LLMs often emit: ❌ `"구조화 출력"` / `"구조화된 출력물"`, ❌ `"추론 예산"`, ❌ `"궤적 평가"`, ❌ `"서브 에이전트 위임"`, ❌ `"건전성 검사"` (literal of *sanity check*), ❌ `"API 키 위생"` (literal of *API key hygiene*), ❌ `"종단 간"` (literal of *end-to-end*), ❌ `"파괴적 변경"` / `"부서지는 변경"` (literal of *breaking changes*), ❌ `"인간 루프"` (literal of *human-in-the-loop*), ❌ `"박스를 벗어나자마자"` (*out-of-the-box*), ❌ `"일급 시민"` (*first-class citizen*), ❌ `"본 저장소는 ~를 포함합니다"` (*This repository contains...*)
- **JA Prohibited (직역 금지)**: ❌ 「手で触る実験室」, ❌ 「走る本」, ❌ 「骨組みコード」, ❌ 「思考の予算」, ❌ 「健全性検査」, ❌ 「煙の試験」, ❌ 「後退経路」
- **ZH Prohibited (직역 금지)**: ❌ “手把手的实验室”, ❌ “奔跑的书”, ❌ “骨架代码”, ❌ “思考预算”, ❌ “健全性检查”, ❌ “烟雾测试”, ❌ “后退路径”

### B. Use Terms That Real Developers Actually Speak & Write (실무 개발자가 실제로 쓰는 표현 사용)
1. **Do NOT force mechanical `English (한국어)` parenthetical echoes on every obvious loanword**:
   - Repeating `Starter Code (스타터 코드)`, `Lab Guide (실습 가이드)`, `Quick Start (빠른 시작)` on every line feels robotic and translated.
   - Instead, write loanwords and developer terms naturally (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트`, `폴백`), and keep English terms in English where Korean developers naturally use English (`Structured Output`, `Tool Calling`, `Function Calling`, `RAG`, `End-to-End (E2E)`), adding a concise developer explanation in parentheses **only when introducing a concept** (e.g., `Structured Output (JSON 스키마 응답)`, `Thinking Budget (추론 토큰 한도)`, `Trajectory Eval (실행 경로 평가)`).
2. **Code Identifiers & SDK Symbols**:
   - Never translate code symbols, CLI flags, environment variable names, or class/method names (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`, `GEMINI_API_KEY`). Keep them in backticks in exact English.

### C. Natural Developer Sentence Grammar (번역투 문장 금지)
1. **Korean (KO) Developer Prose**:
   - Avoid double passives (❌ `~되어집니다` -> ✅ `~됩니다`), verbose nominalizations (❌ `~하는 것이 가능합니다` -> ✅ `~할 수 있습니다`), unnatural second-person pronouns (❌ `당신의 API 키` -> ✅ `.env 파일의 API 키`), inanimate `가지다` calques (❌ `에이전트는 2개의 도구를 가집니다` -> ✅ `에이전트에 툴 2개를 연결합니다`), and stiff bureaucratic verbs (❌ `본 저장소는 ~를 포함합니다`, `서버 기동을 지원합니다` -> ✅ `~를 모아둔 레포지토리입니다`, `로컬 서버를 띄웁니다`).
2. **Japanese (JA) Developer Prose**:
   - Avoid literal passive/modal calques (❌ `〜によって生成されることができます`, `あなたのAPIキー`). Use natural Japanese engineer phrasing (`〜を生成します`, `環境変数にAPIキーを設定します`).
3. **Chinese (ZH) Developer Prose**:
   - Avoid Europeanized translationese (❌ `被通过...所生成`, `你的 API 密钥`). Use concise active phrasing (`配置 API Key`, `启动本地服务`, `运行冒烟测试`).

### D. Clean Typography Rule (No Em Dash `\u2014`)
- Never generate em dash characters (`\u2014`) in any markdown (`.md`) file, slide deck, setup guide, or code comment.
- Use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.

---

## 2. Real-World Developer Terminology Mapping (KO / EN / JA / ZH)

| English Source Term | Awkward Literal Calque (직역 금지 ❌) | Real-World Korean Developer Term (실무 권장 ✅) | Japanese (JA) | Chinese (ZH) |
| :--- | :--- | :--- | :--- | :--- |
| Hands-on Lab | 손으로 하는 실험실 | **핸즈온 실습** / **핸즈온 랩** | **ハンズオンラボ** | **实战工作坊 / 动手实验** |
| Repository | 본 저장소 | **레포지토리** | **リポジトリ** | **代码仓库** |
| Starter / Solution Code | 뼈대 코드 / 레퍼런스 해답 | **스타터 코드 (`01_starter`)** / **정답 코드 (`02_final`)** | **スターターコード / リファレンス実装** | **Starter 初始代码 / 参考实现** |
| Scaffolding | 발판 설치 / 뼈대 공사 | **스캐폴딩 (초기 프로젝트 세팅)** | **スキャフォールディング** | **脚手架** |
| Runbook | 달리는 책 | **런북 (`RUNBOOK.md`)** | **ランブック (進行ガイド)** | **演练手册** |
| Sanity Check / Smoke Test | 건전성 검사 / 연기 시험 | **동작 확인** / **연결 확인** / **스모크 테스트** | **動作確認 / スモークテスト** | **连通性验证 / 冒烟测试** |
| API Key Hygiene | API 키 위생 | **API 키 보안 점검** / **시크릿 유출 점검** | **APIキーのセキュリティ管理** | **API Key 安全检查** |
| Structured Outputs | 구조화 출력 / 구조화된 출력물 | **Structured Output (JSON 스키마 응답)** | **Structured Outputs (構造化出力)** | **Structured Outputs (结构化输出)** |
| Tool / Function Calling | 도구 부르기 / 함수 부르기 | **Tool Calling** / **Function Calling** / **툴 콜링** | **Tool Calling (ツール呼び出し)** | **Tool Calling (工具调用)** |
| RAG | 검색 증강된 생성 | **RAG** / **RAG 파이프라인** | **RAG パイプライン** | **RAG 检索增强流水线** |
| Thinking Budget | 생각 예산 / 추론 예산 | **Thinking Budget (추론 토큰 한도)** | **Thinking Budget (推論トークン上限)** | **Thinking Budget (推理 Token 上限)** |
| Sub-Agent Delegation | 하위 대리인 넘기기 / 서브 에이전트 위임 | **서브 에이전트 라우팅** / **Sub-agent 호출** | **サブエージェントへのルーティング** | **子 Agent 路由分发** |
| Trajectory Evaluation | 궤적 평가 / 궤도 채점 | **Trajectory Eval (실행 경로 평가)** | **Trajectory Eval (実行経路評価)** | **Trajectory Eval (执行轨迹评估)** |
| End-to-End (E2E) | 종단 간 / 끝에서 끝까지 | **End-to-End (E2E)** / **전체 파이프라인** | **End-to-End (E2E)** | **端到端 (E2E)** |
| Fallback | 후퇴 경로 / 대체 작동 | **폴백 (Fallback)** / **우회 경로** | **フォールバック** | **Fallback (回退方案)** |
| Breaking Changes | 파괴적 변경 / 부서지는 변경 | **브레이킹 체인지 (하위 호환성 변경)** | **破壊的変更 (Breaking Changes)** | **破坏性变更 (Breaking Changes)** |
| Human-in-the-Loop | 인간 고리 안 / 인간 루프 | **Human-in-the-Loop (사용자 승인 단계)** | **Human-in-the-Loop (承認ステップ)** | **Human-in-the-Loop (人工审批节点)** |
| Out-of-the-box | 박스를 벗어나자마자 | **별도 설정 없이 바로** | **追加設定なしですぐに** | **开箱即用** |

---

## 3. Translationese vs Real Developer Prose (번역투 vs 현업 개발자 문장 비교)

| Language | Awkward Translationese (지양 ❌) | Natural Developer Prose (권장 ✅) |
| :--- | :--- | :--- |
| **Korean (KO)** | "본 저장소는 구조화 출력과 궤적 평가를 위한 스타터 코드를 포함합니다." | "Pydantic 기반 Structured Output과 `adk eval` 실행 경로 평가 예제를 담은 핸즈온 레포지토리입니다." |
| **Korean (KO)** | "당신의 `GEMINI_API_KEY`가 설정되어져 있는지 건전성 검사를 수행하는 것이 가능합니다." | "`.env` 파일에 `GEMINI_API_KEY`가 제대로 들어갔는지 스모크 테스트로 바로 확인합니다." |
| **Korean (KO)** | "로컬 서버 기동을 지원하며 추론 예산을 가집니다." | "`ollama serve`로 로컬 서버를 띄우고 `thinking_budget`(추론 토큰 한도)을 설정합니다." |
| **Japanese (JA)** | "あなたのAPIキーによって健全性検査が実行されることができます。" | "`.env` に `GEMINI_API_KEY` を設定し、動作確認スクリプトを実行します。" |
| **Chinese (ZH)** | "你的 API 密钥可以被用来进行健全性检查。" | "在 `.env` 中配置 `GEMINI_API_KEY`，运行冒烟测试确认连通性。" |

---

## 4. Code Comment Guidelines (코드 주석 작성 지침)

```python
# TODO [Lab 02]: Pydantic 스키마 기반 Structured Output과 thinking_budget(추론 토큰 한도)을 설정합니다.
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=WorkshopTaskResult,
    thinking_config=types.ThinkingConfig(thinking_budget=1024),
)
```

- Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to automatically catch and fix forbidden em dashes (`\u2014`), literal English calques, and translationese patterns.

---

## References

- [AGENTS.md Specification](./agents-md.md)
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
