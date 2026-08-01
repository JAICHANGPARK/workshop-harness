# Hardware & Operating System Environment Setup Guide

This document provides guidance on selecting the appropriate runtime environment based on each attendee's hardware specifications (RAM, CPU/GPU, OS) and API port configurations for workshop sessions.

## Local LLM Server API & Port Specification

When integrating local LLMs into Python, Node.js, or Go applications, verify the correct API endpoint and port number for your runtime tool:

| Runtime Tool | Default Port | Base API URL | OpenAI Compatible Endpoint | Default API Key |
| --- | --- | --- | --- | --- |
| **Ollama** | `11434` | `http://localhost:11434` | `http://localhost:11434/v1` | `ollama` (or any string) |
| **LM Studio** | `1234` | `http://localhost:1234` | `http://localhost:1234/v1` | `lm-studio` (or any string) |

> 💡 **Port Tip**: If `http://localhost:11434/v1` throws `Connection Refused`, check if `ollama serve` is running. If `http://localhost:1234/v1` fails, ensure the "Local Inference Server" is started inside LM Studio's Developer tab.

---

## Recommended Models & Settings by Hardware Tier

| RAM | Recommended Model | Runtime Tool | Notes |
| --- | --- | --- | --- |
| **8GB** | `gemma4:e2b` (or 2B-3B class) | Ollama / LM Studio | Set context length to 2048 or below |
| **16GB** | `gemma4:e4b` (or 7B-9B class) | LM Studio / Ollama | Recommended baseline spec for hands-on labs |
| **32GB+** | `gemma4:26b-a4b` or 31B | LM Studio / Ollama / MLX | Supports advanced pipelines and multi-agent labs |

> **Note**: The 'B' in parameter count stands for Billion (1,000,000,000). This does not correspond 1:1 with file size in GB. Check the actual download size for 4-bit quantized (Q4_K_M) models.

---

## OS-Specific Guides

### 1. Apple Silicon Mac (M1/M2/M3/M4)
- **Recommended Tools**: LM Studio, Ollama, MLX
- Metal GPU acceleration is natively supported, enabling smooth local LLM inference.

### 2. Intel Mac
- **Recommended Tools**: Ollama CLI
- If LM Studio freezes or hangs, use the terminal-based Ollama CLI for CPU/GPU inference as a fallback (`http://localhost:11434`).

### 3. Windows (Windows 10/11)
- **Recommended Tools**: LM Studio (GUI) or Ollama for Windows
- PowerShell execution policy bypass:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- WSL2 (Windows Subsystem for Linux 2) setup is required for Docker/RAG labs.

### 4. Linux / ChromeOS
- **Recommended Tools**: Ollama CLI
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

---

## References

- **Ollama Documentation**: [https://ollama.com](https://ollama.com)
- **LM Studio Developer Portal**: [https://lmstudio.ai](https://lmstudio.ai)
- **Build with AI Seoul Reference**: [https://github.com/JAICHANGPARK/2026-bwai-seoul](https://github.com/JAICHANGPARK/2026-bwai-golang-seoul)
