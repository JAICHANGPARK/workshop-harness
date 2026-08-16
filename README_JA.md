![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness (日本語)

[![Official Docs](https://img.shields.io/badge/Official%20Docs-MkDocs-blue.svg)](https://JAICHANGPARK.github.io/workshop-harness/)
[![Landing Page](https://img.shields.io/badge/Landing%20Page-Website-purple.svg)](https://JAICHANGPARK.github.io/workshop-harness/website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.08.16-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

**公式ドキュメント**: [https://JAICHANGPARK.github.io/workshop-harness/](https://JAICHANGPARK.github.io/workshop-harness/)  
**ランディングページ**: [https://JAICHANGPARK.github.io/workshop-harness/website/](https://JAICHANGPARK.github.io/workshop-harness/website/)

---

## 概要

`workshop-harness` は、**Astral uv** を基盤とした、技術ワークショップ（Build with AI、DevFest、コミュニティハンズオンラボ）の主催者、スピーカー、ファシリテーター、TAのための **AIエージェントハーネス、14スキルスイート、およびCLI自動化ツールキット** です。

[AGENTS.md標準仕様](https://agents.md/)に準拠し、**Google Antigravity**、**Gemini CLI**、**Anthropic Claude Code**、**OpenAI Codex / ChatGPT**、**Cursor**、**Aider** など、すべての主要AIエージェントとネイティブに連携します。

---

## ⚡ クイックスタート (uv Powered)

```bash
# 1. リポジトリのクローン
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 14個のエージェントスキルをローカル環境 (~/.gemini/skills/) に自動インストール
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. ワンクリックでワークショップパッケージ全体を自動生成
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 🧩 15種類のエージェントスキル仕様

| # | スキル名 | トリガー / 入力 | 生成物・成果物 | 主な役割 |
|---|---|---|---|---|
| 1 | [`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md) | ワークショップ名・テーマ | `docs/`, `workshop/`, `prompt-pack/`, `scripts/` | 標準的なワークショップリポジトリ構造の生成 |
| 2 | [`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md) | 技術スタック一覧 | `docs/00-architecture-compatibility-matrix.md` | Apple Silicon、Intel Mac、Win、Linuxの互換性診断とフォールバック作成 |
| 3 | [`prerequisite-checker`](skills/prerequisite-checker/SKILL.md) | 事前準備要件 | `gemma4-local-setup-guide.md`, `check_env.sh/ps1` | OS別事前準備ガイドと環境自動検証スクリプトの作成 |
| 4 | [`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md) | 目標・時間 | `03_labs/README.md`, `starter`/`final` コード, プロンプトパック | ステップバイステップLabカリキュラムとコードの作成 |
| 5 | [`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md) | `docs/` ディレクトリ | `output/pdf/*.pdf`, `tmp/pdfs/contact_sheet.png` | ReportLab 기반 出版品質PDFハンドアウトとコンタクトシート生成 |
| 6 | [`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md) | ハードウェア仕様・OS | `docs/troubleshooting.md`, `docs/20-faq.md` | RAM容量別（8G/16G/32G）およびOS別のトラブルシューティングFAQ作成 |
| 7 | [`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md) | セッション時間・TA数 | `RUNBOOK.md` | 進行者・TA用の分単位進行ランブックとキューカード作成 |
| 8 | [`live-debug-assistant`](skills/live-debug-assistant/SKILL.md) | ターミナルエラーログ | 10秒ホットフィックスコマンド, `.env.sample` | 現場エラーログの即時診断およびAPI Keyセキュリティ保護 |
| 9 | [`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md) | テーマ・難易度 | `docs/20-faq.md` / `FAQ.md` | 参加者向け事前FAQ（ハードウェア・ネットワーク・コード）自動生成 |
| 10 | [`workshop-tester`](skills/workshop-tester/SKILL.md) | プロジェクトパス | `verify_workshop.py` 監査レポート | コード実行スモークテストとリンク整合性検証 |
| 11 | [`workshop-web-researcher`](skills/workshop-web-researcher/SKILL.md) | ツール・モデルキーワード | 最新リリースバージョン情報 | Web検索による最新ツール/SDKバージョンのリアルタイム監査 |
| 12 | [`workshop-persona-loop-evaluator`](skills/workshop-persona-loop-evaluator/SKILL.md) | テーマ・カリキュラム | `docs/00-persona-loop-review-report.md` | 初級・中級・上級ペルソナによるループエンジニアリング多角レビュー |
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | プロジェクトパス | `output/open-codelabs/` (`codelab.yaml`), `oc` push | Open Codelabsマニフェスト出力と `oc` CLI/MCP連携発行 |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | プロジェクトパス | `output/colab/` (`*.ipynb`, バッジ), `colab` CLIテスト | Google Colabノートブック(`.ipynb`)変換、バッジ挿入およびColab CLIテスト |
| 15 | [`workshop-slide-generator`](skills/workshop-slide-generator/SKILL.md) | プロジェクトパス | `output/slides/` (`slides.md`, `index.html`), PDF | Marp Markdownおよびランブックと同期したWebスライドの自動生成 |

---

## 🛠️ CLI の使い方 (`harness_cli.py`)

```bash
# 1. 14スキルを一括実行するワンクリック生成
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"

# 2. Google Colab ノートブックとバッジのエクスポート
uv run harness_cli.py export-colab --target my-bwai-workshop --repo "JAICHANGPARK/my-bwai-workshop"

# 3. Google Colab CLI によるヘッドレス動作検証
uv run harness_cli.py test-colab --target my-bwai-workshop

# 4. Open Codelabs マニフェストのエクスポート & プッシュ
uv run harness_cli.py export-codelab --target my-bwai-workshop --push

# 5. クロスアーキテクチャ互換性リスクの監査
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 6. PDF ハンドアウトのビルド
uv run harness_cli.py build-pdf --target my-bwai-workshop
```

---

## ライセンス

[MIT License](LICENSE)
