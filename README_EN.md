# 🚀 Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)

🌐 **Languages**: [🇰🇷 한국어](./README.md) | [🇺🇸 English](./README_EN.md) | [🇯🇵 日本語](./README_JA.md) | [🇨🇳 中文](./README_ZH.md)

**`workshop-harness`** is an **AI Agent Harness & Skill Suite and CLI Automation Toolkit** designed for organizers, speakers, and TAs preparing tech workshops (Build with AI, DevFest, community hands-on labs).

It standardizes the structure and battle-tested workflows from real-world events like Build with AI Seoul (`2026-bwai-seoul`), Golang Korea (`2026-bwai-golang-korea`), Mongo (`2026-bwai-mongo`), and Cloud Pangyo (`2026-bwai-cloud-pangyo`).

---

## 💡 Key Features & 9 Agent Skills Specification

| # | Skill Name | Input / Trigger | Output & Artifacts | Description |
|---|---|---|---|---|
| 1 | **[`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md)** | Workshop name & topic | `docs/`, `workshop/`, `prompt-pack/`, `scripts/` | Scaffolds standard repository structure |
| 2 | **[`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md)** | Tech stack list | `docs/00-architecture-compatibility-matrix.md` | Audits Apple Silicon, Intel Mac, Win, Linux compatibility & fallback paths |
| 3 | **[`prerequisite-checker`](skills/prerequisite-checker/SKILL.md)** | List of prerequisites | `gemma4-local-setup-guide.md`, `check_env.sh/ps1` | Generates OS-specific setup guides & verification scripts |
| 4 | **[`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md)** | Session goal & duration | `03_labs/README.md`, `prompt-pack/`, `starter`/`final` code | Builds step-by-step curriculum, starter vs final code, and prompt packs |
| 5 | **[`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md)** | `docs/` markdown directory | `output/pdf/*.pdf`, `tmp/pdfs/contact_sheet.png` | Builds publication-ready PDF handouts & preview contact sheets via ReportLab |
| 6 | **[`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md)** | Hardware specs & OS | `docs/troubleshooting.md`, `docs/20-faq.md` | Generates troubleshooting matrix by RAM (8G/16G/32G+) and OS |
| 7 | **[`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md)** | Session duration & TAs | `RUNBOOK.md` | Creates minute-by-minute facilitator timeline runbook & cue cards |
| 8 | **[`live-debug-assistant`](skills/live-debug-assistant/SKILL.md)** | Terminal error log | 10-second hotfix command, `.env.sample` | Diagnoses live terminal errors & enforces API Key security protocols |
| 9 | **[`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md)** | Workshop topic & level | `docs/20-faq.md` / `FAQ.md` | Automatically generates attendee FAQ (hardware, network, code) |

---

## 💻 Cross-Architecture Compatibility Matrix

| Architecture / OS | Recommended Tool | Known Risks | Mandatory Fallback Path |
| --- | --- | --- | --- |
| **macOS Intel Mac** (`x86_64`) | **Ollama CLI** (`ollama serve`) | 🚨 **LM Studio lacks GPU acceleration / crashes frequently** | **Must provide Ollama CLI fallback guide** (`docs/18-intel-mac-prep.md`) |
| **macOS Apple Silicon** (`arm64`) | LM Studio / Ollama / MLX | Metal GPU hardware acceleration supported | MLX (`mlx-lm`) optional |
| **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell execution policy restriction, WSL2 for Docker | Provide PowerShell bypass script |
| **Windows ARM64** (Snapdragon) | Ollama CLI (Native) | Performance degradation under x64 emulation | Use Ollama native build |
| **Linux / ChromeOS** | Ollama CLI | No GUI support / Sandbox container | Use `ollama serve` terminal mode & small models (`e2b`) |

---

## 🛠️ CLI Usage (`harness_cli.py`)

```bash
# 1. Initialize a new workshop project
python3 harness_cli.py init --name my-bwai-workshop --topic "Local RAG with Gemma 4"

# 2. Audit tech stack for cross-architecture risks
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. Build PDF handout from markdown docs
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## 📦 Agent Skill Installation

Install all 9 skills to your `~/.gemini/skills` directory:

```bash
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh
```

---

## 📜 License

[MIT License](LICENSE)
