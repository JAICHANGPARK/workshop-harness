# Cross-Architecture Compatibility Matrix

Participants bring a wide variety of hardware architectures to workshops. Workshop Harness audits technology stack risks prior to the session and provides mandatory fallback paths.

---

## Hardware Chipset & OS Matrix

| Architecture / OS | Recommended Tool | Known Risks | Mandatory Fallback Path |
| --- | --- | --- | --- |
| **macOS Intel Mac** (`x86_64`) | Ollama CLI (`ollama serve`) | LM Studio GPU acceleration unavailable / crashes frequently | Must provide Ollama CLI fallback guide (`docs/18-intel-mac-prep.md`) |
| **macOS Apple Silicon** (`arm64`) | LM Studio / Ollama / MLX | Full Metal GPU hardware acceleration supported | MLX (`mlx-lm`) optional |
| **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell execution policy restriction, WSL2 required for Docker | Provide PowerShell bypass script |
| **Windows ARM64** (Snapdragon) | Ollama CLI (Native build) | Performance degradation under x64 emulation | Use Ollama native build |
| **Linux / ChromeOS** | Ollama CLI | No GUI support / Sandbox container | Use `ollama serve` terminal mode & small models |

---

## Automated Architecture Detection (`check_architecture_compat`)

Workshop Harness embeds architecture detection scripts inside every generated workshop project:

- **macOS / Linux**: `./scripts/check_architecture_compat.sh`
- **Windows**: `.\scripts\check_architecture_compat.ps1`
