# Workshop Harness (日本語)

> **AIエージェントハーネス、14スキルスイート & CLI自動化ツールキット**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v2026.08.16-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

---

## 概要

**Workshop Harness**は、ハンズオンワークショップ（Build with AI、DevFest、コミュニティハンズオン）を開催する主催者、スピーカー、ファシリテーター、TAのためのワンクリックAIエージェントオーケストレーションツールキットです。

[AGENTS.md標準仕様](https://agents.md/)に準拠し、**Google Antigravity**、**Gemini CLI**、**Anthropic Claude Code**、**OpenAI Codex / ChatGPT**、**Cursor**、**Aider**など、すべてのAIコーディングエージェントと完全に互換性があります。

---

## Quickstart Guide

```bash
# 1. リポジトリをクローン
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 14スキルを自動インストール (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. ワンクリックでフルパッケージ生成
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 14のエージェントスキル一覧

- `workshop-scaffolder`: リポジトリの標準構造スキャフォールディング
- `cross-architecture-checker`: チップセット・OS互換性診断およびFallback作成
- `prerequisite-checker`: 事前準備ガイドの自動生成
- `hands-on-curriculum-builder`: ステップバイステップLabガイドとコード生成
- `pdf-handout-generator`: ReportLab基盤のPDFハンドアウト生成
- `workshop-troubleshooter`: トラブルシューティングFAQ自動作成
- `workshop-runbook-generator`: 分単位の進行タイムラインランブック作成
- `live-debug-assistant`: 現場エラーの10秒ホットフィックス
- `workshop-faq-generator`: 参加者FAQ自動作成
- `workshop-tester`: コード実行スモークテストとリンク検証
- `workshop-web-researcher`: 最新SDKバージョンと変更点のリアルタイム調査
- `workshop-persona-loop-evaluator`: 初級・中級・上級ペルソナレビュー
- `open-codelabs-integrator`: Open Codelabsマニフェスト出力 & `oc` push
- `colab-workshop-integrator`: Google Colabノートブック(`.ipynb`)変換、バッジ挿入およびColab CLIテスト
