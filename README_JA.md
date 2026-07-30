# Workshop Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

`workshop-harness` は、Build with AI (BWAI)、DevFest、コミュニティハンズオンなどを準備する主催者、発表者、TAのためのAIエージェントハーネス＆スキル（Skills）集およびCLI自動化ツールキットです。

---

## 全9種類のエージェントスキル仕様

| # | スキル名 | 説明 |
|---|---|---|
| 1 | [`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md) | 標準的なワークショップリポジトリ構造の生成 |
| 2 | [`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md) | Intel Mac、Apple Silicon、Windows、Linuxの互換性診断と回避策の作成 |
| 3 | [`prerequisite-checker`](skills/prerequisite-checker/SKILL.md) | OS別事前準備ガイドと環境自動検証スクリプトの作成 |
| 4 | [`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md) | `starter` vs `final` コード、Labsガイド、プロンプトパックの構築 |
| 5 | [`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md) | マークダウン文書から出版品質のPDFハンドアウトとプレビュー画像を自動生成 |
| 6 | [`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md) | RAM容量別（8G/16G/32G）およびOS別のトラブルシューティングマトリックス作成 |
| 7 | [`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md) | 進行者・TA用の分単位進行ランブック（`RUNBOOK.md`）作成 |
| 8 | [`live-debug-assistant`](skills/live-debug-assistant/SKILL.md) | 現場エラーログの10秒緊急診断およびAPI Keyセキュリティガイド |
| 9 | [`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md) | 参加者向けの事前FAQ（ハードウェア・ネットワーク・コード）自動生成 |

---

## CLI の使い方 (`harness_cli.py`)

```bash
# 1. 新しいワークショッププロジェクトの初期化
python3 harness_cli.py init --name my-bwai-workshop --topic "Local RAG with Gemma 4"

# 2. クロスアーキテクチャ互換性リスクの監査
python3 harness_cli.py audit-compat --stack "lmstudio,docker,mlx"

# 3. PDFハンドアウトのビルド
python3 harness_cli.py build-pdf --target my-bwai-workshop
```

---

## ライセンス

[MIT License](LICENSE)
