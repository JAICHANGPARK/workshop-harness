# Agent Instructions, Developer Terminology & Typography Rules for sample-bwai-workshop

> Topic: **Local RAG with Gemma 4**
> Tech Stack: `python,ollama,lmstudio` | Primary Cloud Model: `gemma-4-26b-a4b-it` | Local Model: `gemma4:e4b`

## Mandatory Rules for AI Coding Agents

1. **Real-World Developer Language & Anti-Translationese Rule (실무 개발자 용어/문법 사용 & 영문 직역·번역투 절대 금지)**:
   - **English (EN)**: Write in clear, idiomatic, direct technical English.
   - **Korean (KO), Japanese (JA), and Chinese (ZH) Requests**: Whenever a user requests documentation, `.md` files, slide decks, setup guides, runbooks, or **code comments** in Korean, Japanese, or Chinese, **NEVER generate awkward English-to-local literal calques or translationese grammar (영문 직역 및 번역투 문장 절대 금지)**. Always write the way local software engineers actually speak and write in production:
     - **Korean (KO) Real-World Developer Language**: Use natural developer vernacular and widely used English/loanword terms as-is (`핸즈온 실습`, `레포지토리`, `스타터 코드`, `정답 코드`, `보일러플레이트`, `스캐폴딩`, `런북`, `스모크 테스트 / 동작 확인`, `폴백`, `Structured Output (JSON 스키마 응답)`, `Tool Calling / Function Calling`, `RAG 파이프라인`, `임베딩`, `양자화`, `Thinking Budget (추론 토큰 한도)`, `멀티 에이전트 오케스트레이션`, `서브 에이전트 라우팅`, `Trajectory Eval (실행 경로 평가)`, `End-to-End (E2E)`, `브레이킹 체인지`, `API 키 보안 점검`). Never output literal English calques or translationese (❌ 직역 금지: "손으로 하는 실험실", "달리는 책", "뼈대 코드", "구조화 출력", "추론 예산", "생각 예산", "궤적 평가", "서브 에이전트 위임", "건전성 검사", "API 키 위생", "종단 간", "파괴적 변경", "본 저장소는 ~를 포함합니다", "당신의 API 키", "~되어집니다", "~하는 것이 가능합니다").
     - **Japanese (JA)**: Use natural Japanese engineer terminology (`ハンズオンラボ`, `スターターコード`, `リファレンス実装`, `ランブック`, `動作確認 / スモークテスト`, `Structured Outputs (構造化出力)`, `Tool Calling`, `Thinking Budget`, `フォールバック`) and natural sentence endings (`〜を設定します`, `〜を実行できます`).
     - **Chinese (ZH)**: Use authentic Chinese developer phrasing (`实战工作坊`, `Starter 初始代码`, `参考实现`, `演练手册`, `冒烟测试`, `Structured Outputs (结构化输出)`, `Tool Calling (工具调用)`, `Thinking Budget (推理预算)`, `回退策略`).
   - **Code Comments & Identifiers**: Keep all SDK symbols, class/function names, and CLI flags in exact English (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`), and write comments in concise, natural developer prose without forcing mechanical `(괄호)` glosses on every obvious loanword.

2. **Typography Rule (No Em Dash in Markdown or Documentation)**:
   - **NEVER generate em dash characters (`\u2014`)** in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks.
   - Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
   - Run `python3 scripts/verify_workshop.py .` to verify zero forbidden em dashes or awkward literal translations exist.

3. **No Emojis in Documentation by Default**:
   - Do not include emojis in generated documentation, slide decks, setup guides, or runbooks unless explicitly requested.

4. **2026 Frontier Model & SDK Currency**:
   - Use verified 2026 SDKs (`google-genai >= 3.0.0`, `anthropic >= 2.8.0`, `openai >= 3.50.0`, `google-adk >= 2.14.0`) and active model tags (`gemma-4-26b-a4b-it`, `gemma-4-31b-it`, `gemini-4-hydrogen`, `gemini-4-carbon`, `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gemma4:e4b`).
   - Never use deprecated `google-generativeai` or retired legacy model tags.

## References
- [Workshop Harness Repository](https://github.com/JAICHANGPARK/workshop-harness)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
