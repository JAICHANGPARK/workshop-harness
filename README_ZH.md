# 🚀 Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)

🌐 **Languages**: [🇰🇷 한국어](./README.md) | [🇺🇸 English](./README_EN.md) | [🇯🇵 日本語](./README_JA.md) | [🇨🇳 中文](./README_ZH.md)

**`workshop-harness`** 是一个专为 **Build with AI (BWAI)**、DevFest 和社区 Hands-on 工作坊的组织者、讲师和 TA 打造的 **AI Agent 工具链与技能（Skills）集合**。

---

## 💡 全套 9 个 Agent 技能说明 (Skill Specification)

| # | 技能名称 | 描述 |
|---|---|---|
| 1 | **[`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md)** | 自动脚手架生成标准工作坊仓库结构 |
| 2 | **[`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md)** | **诊断 Apple Silicon, Intel Mac, Windows, Linux 的架构兼容性与替代方案** |
| 3 | **[`prerequisite-checker`](skills/prerequisite-checker/SKILL.md)** | 生成各 OS 预备指南及环境自动检测脚本 |
| 4 | **[`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md)** | 构建 `starter` 与 `final` 代码、Lab 指南和 Prompt Pack |
| 5 | **[`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md)** | 将 Markdown 自动合成为高清 PDF 手册及预览 Contact Sheet |
| 6 | **[`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md)** | 按内存 (8G/16G/32G) 及 OS 构建排错矩阵和 FAQ |
| 7 | **[`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md)** | **生成讲师与 TA 专用的分秒级 Runbook (`RUNBOOK.md`)** |
| 8 | **[`live-debug-assistant`](skills/live-debug-assistant/SKILL.md)** | **现场终端错误 10 秒快速诊断与 API Key 安全规范** |
| 9 | **[`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md)** | **自动生成参会者常见问题解答 (`FAQ.md`)** |

---

## 🛠️ CLI 使用说明 (`harness_cli.py`)

```bash
# 1. 初始化新工作坊项目
python3 harness_cli.py init --name my-bwai-workshop --topic "Local RAG with Gemma 4"

# 2. 审计技术栈跨架构兼容性
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. 构建 PDF 讲义
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## 📜 许可证

[MIT License](LICENSE)
