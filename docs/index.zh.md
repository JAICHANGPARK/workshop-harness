# Workshop Harness (中文)

> **AI Agent 编排框架、15 项技能套件与 CLI 自动化工具包**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v2026.08.16-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

---

## 项目概述

**Workshop Harness** 是专为技术工作坊（Build with AI、DevFest、社区开发者实验室）组织者、讲师和助教（TA）打造的一键式 AI Agent 编排工具包。

遵循 [AGENTS.md 开放规范](https://agents.md/)，该工具包与 **Google Antigravity**、**Gemini CLI**、**Anthropic Claude Code**、**OpenAI Codex / ChatGPT**、**Cursor** 及 **Aider** 等所有 AI 编程 Agent 原生兼容。

---

## Quickstart Guide

```bash
# 1. 克隆仓库
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 自动安装 15 项技能 (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. 一键生成完整工作坊包
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 15 项 Agent 技能索引

- `workshop-scaffolder`: 自动化标准仓库结构脚手架
- `cross-architecture-checker`: 芯片与 OS 兼容性诊断及替代方案 (Fallback)
- `prerequisite-checker`: 准备工作指南与环境检查脚本生成
- `hands-on-curriculum-builder`: 循序渐进 Lab 指南与代码生成
- `pdf-handout-generator`: 基于 ReportLab 的 PDF 手册生成
- `workshop-troubleshooter`: 常见问题故障排除FAQ
- `workshop-runbook-generator`: 按分钟规划的讲师与助教 Runbook
- `live-debug-assistant`: 现场终端错误 10 秒热修复
- `workshop-faq-generator`: 参会者 FAQ 自动生成
- `workshop-tester`: 代码运行烟雾测试与链接有效性审计
- `workshop-web-researcher`: 最新 SDK 版本及破坏性更新实时 Web 审计
- `workshop-persona-loop-evaluator`: 初级/中级/高级画像多视角审查
- `open-codelabs-integrator`: Open Codelabs Bundle 导出与 `oc` push 部署
- `colab-workshop-integrator`: Google Colab 笔记本(`.ipynb`)转换、徽章生成与 Colab CLI 测试
- `workshop-slide-generator`: Marp Markdown 幻灯片与交互式网页演示生成
