---
name: cross-architecture-checker
description: Audits cross-architecture compatibility across Apple Silicon (arm64), Intel Mac (x86_64), Windows (x86/ARM64), Linux, and ChromeOS. Identifies known risks for tools like LM Studio, Docker, and MLX, and generates a fallback matrix document (docs/00-architecture-compatibility-matrix.md).
---

# Cross-Architecture Checker Skill

## Purpose
Workshop attendees bring diverse hardware (Apple Silicon, Intel Mac, Windows x86/ARM64, Linux, ChromeOS). This skill audits the selected tech stack for architecture-specific risks and generates a compatibility fallback matrix with mandatory alternative paths.

## Known Risk Matrix

| Architecture / OS | Known Risk | Mandatory Fallback |
|---|---|---|
| macOS Intel (`x86_64`) | LM Studio crashes due to missing Metal GPU acceleration | Use Ollama CLI (`ollama serve`) as primary fallback |
| macOS Apple Silicon (`arm64`) | No known issues; full Metal GPU support | MLX (`mlx-lm`) as optional accelerator |
| Windows x86_64 | PowerShell execution policy restrictions; WSL2 required for Docker | Provide PowerShell bypass script |
| Windows ARM64 (Snapdragon) | Performance degradation under x64 emulation | Use native Ollama ARM64 build |
| Linux / ChromeOS | No GUI support; sandbox container limitations | Use `ollama serve` terminal mode with small models (`e2b`) |

## Output Artifacts
- `docs/00-architecture-compatibility-matrix.md`
- `scripts/check_architecture_compat.sh` (Mac/Linux)
- `scripts/check_architecture_compat.ps1` (Windows)
