---
name: cross-architecture-checker
description: Audits cross-architecture compatibility across Apple Silicon (arm64), Intel Mac (x86_64), Windows (x86/ARM64), Linux, and ChromeOS. Identifies known risks for tools like LM Studio, Docker, and MLX, and generates a fallback matrix document (docs/00-architecture-compatibility-matrix.md).
---

# Cross-Architecture Checker Skill

## Purpose
Workshop attendees bring a wide variety of hardware platforms (Apple Silicon M1-M4, Intel x86_64 Mac, Windows x86_64 / ARM64, Linux, ChromeOS). This skill performs automated and agentic audits of tech stacks against known architecture constraints, identifying compatibility risks *before* the workshop session and producing mandatory alternative fallback workflows.

---

## Hardware & OS Compatibility Matrix

| Architecture / OS | Primary Acceleration | Known Risks & Constraints | Mandatory Fallback Strategy |
|---|---|---|---|
| **macOS Apple Silicon** (`arm64`) | Metal / Unified Memory | Minimal risks; high performance for local LLMs | Standard Ollama or MLX (`mlx-lm`) acceleration |
| **macOS Intel** (`x86_64`) | CPU-only (No Metal) | LM Studio crashes / freezes; high latency; no Metal support | Force Ollama CLI (`ollama serve`) with quantized 2B/4B models (`gemma4:e2b`) or cloud API |
| **Windows 11 x86_64** | CUDA / DirectML / CPU | PowerShell script execution disabled by policy; WSL2 required for Docker | Provide PowerShell bypass scripts (`Set-ExecutionPolicy -Scope Process Bypass`) and native binary fallbacks |
| **Windows ARM64** (Snapdragon) | NPU / DirectML | x64 emulation performance overhead; Docker driver conflicts | Use native ARM64 Ollama builds or cloud Gemini API |
| **Linux** (Debian/Ubuntu/Arch) | CUDA / ROCm / CPU | No GUI support on headless servers; permission issues with docker socket | Terminal-only commands (`ollama serve &`) and user group additions (`sudo usermod -aG docker $USER`) |
| **ChromeOS** (Linux Container) | Virtualized CPU | Low RAM allocation; no direct GPU pass-through | Use cloud API (Google AI Studio / GCP Gemini) or small 2B quantized models |

---

## Tech Stack Audit Rules

When auditing a workshop tech stack string (e.g. `lmstudio,docker,mlx,python`), the agent must evaluate the following rules:

1. **`lmstudio` in stack**:
   - *Risk*: Intel Mac users will experience severe GUI lag or crashes due to lack of Metal support.
   - *Fix*: Mandate Ollama CLI (`http://localhost:11434`) as an alternative in `docs/00-architecture-compatibility-matrix.md`.
2. **`mlx` / `mlx-lm` in stack**:
   - *Risk*: Strictly restricted to Apple Silicon (`arm64`). Fails instantly on Windows, Linux, and Intel Mac.
   - *Fix*: Provide PyTorch / HuggingFace transformers or Ollama fallbacks for non-Apple Silicon users.
3. **`docker` in stack**:
   - *Risk*: Windows Home users without WSL2 or hypervisor enabled will fail to start Docker Desktop.
   - *Fix*: Provide local native executable setup or cloud sandbox alternatives.
4. **`ollama` in stack**:
   - *Risk*: High RAM model selection (`12B+`) crashes 8GB RAM laptops.
   - *Fix*: Provide model quantization tiers (`gemma4:e2b` for 8GB, `gemma4:e4b` for 16GB, `gemma4:e12b` for 32GB+).

---

## CLI Command Integration

Audit a given tech stack using `harness_cli.py`:

```bash
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"
```

---

## Generated Output Artifacts

1. **`docs/00-architecture-compatibility-matrix.md`**: Complete markdown matrix documenting supported platforms, risks, and fallback instructions for attendees.
2. **`scripts/check_architecture_compat.sh`**: Shell script for macOS/Linux to detect CPU architecture, available RAM, and GPU capabilities.
3. **`scripts/check_architecture_compat.ps1`**: PowerShell script for Windows to audit environment compatibility.
