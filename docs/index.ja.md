# Workshop Harness (日本語)

> **AIエージェントハーネス、21スキルスイート & CLI自動化ツールキット**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-21%20Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.10.31-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

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

# 2. 21スキルを自動インストール (~/.gemini/skills/)
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. ワンクリックでフルパッケージ生成 (デフォルトモデル: gemini-3.8-flash)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 21のエージェントスキル一覧

- `workshop-scaffolder`: リポジトリの標準構造スキャフォールディング
- `cross-architecture-checker`: チップセット・OS互換性診断およびFallback作成 (`docs/18-intel-mac-prep.md`)
- `prerequisite-checker`: OS別事前準備ガイドと環境チェック用スクリプト生成
- `hands-on-curriculum-builder`: ステップバイステップLabガイドとコード生成
- `pdf-handout-generator`: ReportLab基盤のPDFハンドアウトとコンタクトシート生成
- `workshop-troubleshooter`: RAM容量別・OS別トラブルシューティングFAQ自動作成
- `workshop-runbook-generator`: 分単位の進行タイムラインランブック (`RUNBOOK.md`) 作成
- `live-debug-assistant`: 現場エラーの10秒ホットフィックスとAPI Keyセキュリティ保護
- `workshop-faq-generator`: 参加者FAQ自動作成 (`docs/20-faq.md`)
- `workshop-tester`: コード実行スモークテスト、2026モデル最新性監査、リンク検証
- `workshop-web-researcher`: 2026最新SDK/AIモデルバージョンのリアルタイムWeb調査
- `workshop-persona-loop-evaluator`: 非開発者・初級・中級・シニア4ペルソナによるループエンジニアリングレビュー
- `open-codelabs-integrator`: Open Codelabsマニフェスト出力 (`codelab.yaml`) & `oc` push
- `colab-workshop-integrator`: Google Colabノートブック(`.ipynb`)変換、バッジ挿入およびColab CLIテスト
- `workshop-slide-generator`: Google Slides `.pptx`、Marp MarkdownおよびWeb発表スライド自動生成
- `adk-workshop-builder`: 公式5言語（Python, Go, Java, Kotlin, TypeScript, Polyglot）Google ADKマルチエージェントラボ生成
- `eli5-concept-explainer`: 3段階ELI5物理アナロジーとメンタルモデル解説 (`docs/eli5-concept-cheat-sheet.md`)
- `android-workshop-builder`: Jetpack Compose Material 3、`com.google.genai`、`android` CLIベースのAndroid GenAIラボ生成
- `flutter-workshop-builder`: Flutter 3.x、`google_generative_ai`およびFlutter Webフォールバック対応クロスプラットフォームラボ生成
- `a2ui-workshop-builder`: A2UI宣言型JSONストリーミングおよびFlutter `genui`動的UIサーフェスラボ生成
- `agents-cli-workshop-builder`: Google Agents CLI (`google-agents-cli`) と7公式スキルによるADLCラボ生成
