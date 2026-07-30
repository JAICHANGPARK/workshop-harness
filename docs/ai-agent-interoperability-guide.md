# 🤖 AI Agent Interoperability Guide (AGENTS.md Standard)

`workshop-harness`는 **[AGENTS.md 표준 명세](https://agents.md/)**를 준수하여 **Google Antigravity, Gemini CLI, Anthropic Claude (Claude Code CLI / Desktop), OpenAI Codex (ChatGPT / Aider), Cursor / Windsurf** 등 모든 AI 코딩 에이전트 및 LLM 환경에서 100% 동일하게 호환되도록 설계되었습니다.

---

## 🛠️ 표준 명세 & 도구별 활용 방법

### 1. `AGENTS.md` 표준 지침 (Standard Specification)
- 프로젝트 루트의 [`AGENTS.md`](../AGENTS.md) 파일은 [AGENTS.md 표준 명세](https://agents.md/)에 따라 에이전트의 역할, 명령어, 스킬 구조를 명시합니다.
- Cursor, Windsurf, Aider, Codex, Claude 등 모든 오픈 에이전트가 루트의 `AGENTS.md`를 표준 콘텍스트로 인지합니다.

---

### 2. Anthropic Claude (Claude Code CLI & Claude Desktop)
- **Claude Code CLI**:
  - 프로젝트 루트의 [`CLAUDE.md`](../CLAUDE.md) 및 [`AGENTS.md`](../AGENTS.md) 가이드를 참조합니다.
  - Claude Code에서 아래처럼 자연어로 명령하세요:
    > *"skills/cross-architecture-checker/SKILL.md 규칙에 따라 Intel Mac과 Windows 참석자를 위한 호환성 우회 가이드를 docs/00-architecture-compatibility-matrix.md에 작성해줘."*

---

### 3. OpenAI Codex, ChatGPT & Aider
- **Codex / ChatGPT / Aider**:
  - 루트의 [`AGENTS.md`](../AGENTS.md) 지침을 참조합니다.
  - `python3 harness_cli.py generate-all` 명령을 직접 터미널에서 실행하거나 `skills/` 디렉토리의 `SKILL.md` 문서 규칙을 수용합니다.

---

### 4. CLI 도구 직접 실행 (모든 에이전트 공통)
- 에이전트가 어떤 LLM 모델(Claude 3.5 Sonnet, GPT-4o, Gemini 2.0 등)이든 관계없이 터미널 실행 권한이 있다면 아래 명령어를 통해 모든 기능을 실행할 수 있습니다:
  ```bash
  python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
  ```

---

## 🔗 참고 (References)

- **AGENTS.md Open Specification**: [https://agents.md/](https://agents.md/)
- **Claude Code Documentation**: [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- **Google Antigravity Guide**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
