# 🤖 AI Agent & LLM Interoperability Guide (Claude, Codex, Antigravity, Cursor)

`workshop-harness`는 **Google Antigravity, Gemini CLI**뿐만 아니라 **Anthropic Claude (Claude Code CLI / Claude Desktop), OpenAI Codex (ChatGPT / Aider), Cursor / Windsurf** 등 도구에 제약 없이 모든 AI 코딩 에이전트 및 LLM 시스템에서 100% 동일하게 활용할 수 있도록 설계되었습니다.

---

## 🛠️ 도구별 연동 및 사용 방법

### 1. Anthropic Claude (Claude Code CLI & Claude Desktop)
- **Claude Code CLI**:
  - 프로젝트 루트의 [`CLAUDE.md`](../CLAUDE.md) 가이드를 자동으로 읽어들입니다.
  - Claude Code에서 아래처럼 자연어로 명령하세요:
    > *"skills/cross-architecture-checker/SKILL.md 규칙에 따라 Intel Mac과 Windows 참석자를 위한 호환성 우회 가이드를 docs/00-architecture-compatibility-matrix.md에 작성해줘."*
- **Claude Desktop / Web Interface**:
  - `skills/` 폴더 내 원하는 `SKILL.md` 파일 내용과 `templates/doc-templates/`의 템플릿을 붙여넣은 뒤 생성을 요청합니다.

---

### 2. OpenAI Codex, ChatGPT & Aider
- **Codex / ChatGPT**:
  - 프로젝트 루트의 [`CODEX.md`](../CODEX.md) 또는 [`AGENTS.md`](../AGENTS.md) 지침을 참조합니다.
  - CLI 도구를 직접 터미널에서 실행하도록 명령하거나, Custom Instructions에 `skills/` 하위 규칙을 포함시킵니다:
    > *"harness_cli.py generate-all 명령어로 Flutter AI 워크숍 패키지를 원클릭 생성해줘."*
- **Aider**:
  - `aider --read skills/workshop-scaffolder/SKILL.md` 구문으로 스킬 규칙을 로드하여 실행합니다.

---

### 3. Cursor & Windsurf IDE
- **Cursor Agent**:
  - `.cursorrules` 파일에 `AGENTS.md` 또는 `skills/` 하위 `SKILL.md` 스펙을 참조하도록 설정되어 있습니다.
- **CLI 직접 실행 (모든 에이전트 공통)**:
  - 에이전트가 어떤 모델(Claude 3.5 Sonnet, GPT-4o 등)이든 관계없이 터미널 명령어 실행 권한이 있다면 아래 명령어를 통해 모든 기능을 실행할 수 있습니다:
    ```bash
    python3 harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
    ```

---

## 🔗 참고 (References)

- **Claude Code Documentation**: [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- **OpenAI Codex & API Docs**: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- **Google Antigravity Guide**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
