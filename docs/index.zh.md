# Workshop Harness (中文)

> **AI Agent 编排框架、21 项技能套件与 CLI 自动化工具包**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-21%20Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.10.31-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

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

# 2. 自动安装 21 项技能 (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. 一键生成完整工作坊包 (默认模型: gemini-3.8-flash)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 21 项 Agent 技能索引

- `workshop-scaffolder`: 自动化标准仓库结构脚手架
- `cross-architecture-checker`: 芯片与 OS 兼容性诊断及替代方案 (`docs/18-intel-mac-prep.md`)
- `prerequisite-checker`: 准备工作指南与环境自动检查脚本生成
- `hands-on-curriculum-builder`: 循序渐进 Lab 指南与骨架/参考代码生成
- `pdf-handout-generator`: 基于 ReportLab 的出版级 PDF 讲义与缩略图生成
- `workshop-troubleshooter`: 按内存规格与系统构建排错矩阵与 FAQ
- `workshop-runbook-generator`: 按分钟规划的讲师与助教演练手册 (`RUNBOOK.md`)
- `live-debug-assistant`: 现场终端错误 10 秒热修复与 API Key 安全防泄漏
- `workshop-faq-generator`: 参会者 FAQ 自动生成 (`docs/20-faq.md`)
- `workshop-tester`: 代码运行冒烟测试、2026 模型标签审计与链接有效性验证
- `workshop-web-researcher`: 2026 最新 SDK 与模型标签实时网络审计
- `workshop-persona-loop-evaluator`: 零基础/初级/中级/资深工程师 4 类角色画像循环工程审查
- `open-codelabs-integrator`: Open Codelabs Bundle (`codelab.yaml`) 导出与 `oc` push 部署
- `colab-workshop-integrator`: Google Colab 笔记本(`.ipynb`)转换、徽章生成与 Colab CLI 测试
- `workshop-slide-generator`: Google Slides `.pptx`、Marp Markdown 幻灯片与交互式网页演示生成
- `adk-workshop-builder`: 官方 5 大语言 (Python, Go, Java, Kotlin, TypeScript, Polyglot) Google ADK 多 Agent 实战工作坊构建
- `eli5-concept-explainer`: 3 层 ELI5 物理类比与心智模型图谱 (`docs/eli5-concept-cheat-sheet.md`)
- `android-workshop-builder`: 基于 Jetpack Compose Material 3、`com.google.genai` 与 `android` CLI 的 Android GenAI 工作坊构建
- `flutter-workshop-builder`: 基于 Flutter 3.x、`google_generative_ai` 与 Flutter Web 零安装回退的跨平台工作坊构建
- `a2ui-workshop-builder`: 基于 A2UI 声明式 JSON 流与 Flutter `genui` 的动态界面工作坊构建
- `agents-cli-workshop-builder`: 基于 Google Agents CLI (`google-agents-cli`) 及 7 项官方技能的 ADLC 全生命周期工作坊构建
