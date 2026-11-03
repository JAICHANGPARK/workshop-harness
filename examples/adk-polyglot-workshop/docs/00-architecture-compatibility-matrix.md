# Attendee Laptop Architecture & OS Compatibility Guide (Compatibility Matrix)

When preparing workshop sessions, always verify the tool recommendations and fallback paths below to accommodate attendees' diverse hardware architectures (Apple Silicon, Intel Mac, Windows x86, Windows ARM64, Linux).

---

## Compatibility & Fallback Matrix

| # | Attendee Environment | Recommended Primary Tool | Known Risks & Constraints | Fallback Path |
| --- | --- | --- | --- | --- |
| 1 | **macOS Apple Silicon** (M1-M4) | LM Studio / Ollama | None (Metal GPU acceleration supported) | MLX (`mlx-lm`) available as optional accelerator |
| 2 | **macOS Intel Mac** (x86_64) | **Ollama CLI** | **LM Studio lacks GPU acceleration / freezing reported** | **Provide Ollama migration guide instead of LM Studio** |
| 3 | **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell script execution restrictions, WSL2 required for Docker | Run `Set-ExecutionPolicy -Scope Process Bypass` |
| 4 | **Windows ARM64** (Snapdragon) | Ollama CLI | Inference speed degradation under x64 emulation | Use Ollama native ARM64 build |
| 5 | **Linux / ChromeOS** | Ollama CLI | No GUI tool support | Use `ollama serve` in terminal mode |

---

## Important Notice for Intel Mac Attendees

> **Critical**: LM Studio frequently fails to enable GPU acceleration or terminates unexpectedly on Intel CPU-based Macs.
> Intel Mac users should prepare with **Ollama instead of LM Studio**.

1. **Install Ollama**: https://ollama.com/download/Ollama-darwin.zip
2. **Pull models in advance**:
   ```bash
   ollama pull gemma4:e4b
   ```
3. **Verify local API host**: Ollama automatically binds to `http://localhost:11434` on startup.

---

## Stack-Specific Architecture & Risk Audit (`adk,polyglot,agents-cli`)

| Tool / Component | Target Environment | Identified Risk | Mandatory Fallback Path |
| :--- | :--- | :--- | :--- |
| **Google Agent Development Kit (ADK & adk web)** | Port 8000 Conflict & Multi-Agent Delegation Loops | Local port 8000 collisions prevent 'adk web' / 'adk api_server' startup; missing 'root_agent' symbol in agent.py breaks discovery. | Ensure top-level orchestrator is named 'root_agent' in agent.py, use 'adk web --port 8080' on port conflict, and assign gemini-3.8-flash to sub_agents. |
| **Google Agents CLI (google-agents-cli)** | Python < 3.11 / Missing uvx or GCP Application Default Credentials | 'uvx google-agents-cli setup' requires Python 3.11+ and Astral uv; 'agents-cli deploy' fails without active GCP ADC credentials. | Install uv first, run 'uvx google-agents-cli setup' (or 'npx skills add google/agents-cli'), and run 'gcloud auth application-default login' before Lab 03. |

