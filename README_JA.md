![Workshop Harness Banner](./assets/workshop_harness_banner.jpg)

# Workshop Harness (日本語)

[![Official Docs](https://img.shields.io/badge/Official%20Docs-MkDocs-blue.svg)](https://JAICHANGPARK.github.io/workshop-harness/)
[![Landing Page](https://img.shields.io/badge/Landing%20Page-Website-purple.svg)](https://JAICHANGPARK.github.io/workshop-harness/website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv Powered](https://img.shields.io/badge/python%20package%20manager-uv-de1f88.svg)](https://astral.sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity Skills](https://img.shields.io/badge/Antigravity-21%20Agent%20Skills-purple.svg)](https://github.com/JAICHANGPARK)
[![Release](https://img.shields.io/badge/release-v2026.10.31-green.svg)](https://github.com/JAICHANGPARK/workshop-harness/releases)

Languages: [English](./README.md) | [Korean](./README_KR.md) | [Japanese](./README_JA.md) | [Chinese](./README_ZH.md)

**公式ドキュメント**: [https://JAICHANGPARK.github.io/workshop-harness/](https://JAICHANGPARK.github.io/workshop-harness/)  
**ランディングページ**: [https://JAICHANGPARK.github.io/workshop-harness/website/](https://JAICHANGPARK.github.io/workshop-harness/website/)

---

## 概要

`workshop-harness` は、**Astral uv** を基盤とした、技術ワークショップ（Build with AI、DevFest、コミュニティハンズオンラボ）の主催者、スピーカー、ファシリテーター、TAのための **AIエージェントハーネス、21スキルスイート、およびCLI自動化ツールキット** です。

[AGENTS.md標準仕様](https://agents.md/)に準拠し、**Google Antigravity**、**Gemini CLI**、**Anthropic Claude Code**、**OpenAI Codex / ChatGPT**、**Cursor**、**Aider** など、すべての主要AIコーディングエージェントとネイティブに連携します。

---

## クイックスタート (uv Powered)

```bash
# 1. リポジトリのクローン
git clone https://github.com/JAICHANGPARK/workshop-harness.git
cd workshop-harness

# 2. 21個のエージェントスキルをローカル環境 (~/.gemini/skills/ 等) に自動インストール
chmod +x scripts/install_skills.sh
./scripts/install_skills.sh

# 3. ワンクリックでワークショップパッケージ全体を自動生成 (デフォルトモデル: gemini-3.8-flash)
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker"
```

---

## 定量的生産性 & ファシリテーター ROI

| 指標 (Metrics) | 従来の手動準備 | Workshop Harness 導入後 | 改善効果 | 主な牽引スキル |
| :--- | :--- | :--- | :--- | :--- |
| **ファシリテーター準備時間** | **20.0 時間 (2.5日)** | **5.0 時間 (0.5日)** | **75% 時間短縮 (4倍高速化)** | `generate-all` |
| **TA 1人あたりの参加者対応数** | **1 : 6 名** | **1 : 25~30 名** | **対応キャパシティ 4~5倍向上** | `live-debug-assistant` |
| **ライブデバッグ MTTR** | **18 分 / 件** | **0.5 分 (30秒) / 件** | **36倍高速な障害復旧** | `live-debug-assistant` |
| **ライブセッション遅延時間** | **平均 35 分** | **3 分以内** | **進行遅延 91.4% 削減** | `cross-architecture-checker` |
| **1開催あたりの削減工数** | 100% ベースライン | **15 時間削減** | **約 2 日分の工数を節約** | 全 21 スキル |

---

## 21種類のエージェントスキル仕様

| # | スキル名 | トリガー / 入力 | 生成物・成果物 | 主な役割 |
|---|---|---|---|---|
| 1 | [`workshop-scaffolder`](skills/workshop-scaffolder/SKILL.md) | ワークショップ名・テーマ | `docs/`, `workshop/`, `prompt-pack/`, `scripts/` | 標準的なワークショップリポジトリ構造のスキャフォールディング |
| 2 | [`cross-architecture-checker`](skills/cross-architecture-checker/SKILL.md) | 技術スタック一覧 | `docs/00-architecture-compatibility-matrix.md` | Apple Silicon、Intel Mac、Win、Linuxの互換性診断とフォールバック作成 |
| 3 | [`prerequisite-checker`](skills/prerequisite-checker/SKILL.md) | 事前準備要件 | `gemma4-local-setup-guide.md`, `check_env.sh/ps1` | OS別事前準備ガイドと環境自動検証スクリプトの作成 |
| 4 | [`hands-on-curriculum-builder`](skills/hands-on-curriculum-builder/SKILL.md) | 目標・時間 | `03_labs/README.md`, `starter`/`final` コード, プロンプトパック | ステップバイステップハンズオンカリキュラムとコードの作成 |
| 5 | [`pdf-handout-generator`](skills/pdf-handout-generator/SKILL.md) | `docs/` ディレクトリ | `output/pdf/*.pdf`, `tmp/pdfs/contact_sheet.png` | ReportLabベースの出版品質PDFハンドアウトとコンタクトシート生成 |
| 6 | [`workshop-troubleshooter`](skills/workshop-troubleshooter/SKILL.md) | ハードウェア仕様・OS | `docs/troubleshooting.md`, `docs/20-faq.md` | RAM容量別（8G/16G/32G）およびOS別のトラブルシューティングFAQ作成 |
| 7 | [`workshop-runbook-generator`](skills/workshop-runbook-generator/SKILL.md) | セッション時間・TA数 | `RUNBOOK.md` | 進行者・TA用の分単位進行ランブックとキューカード作成 |
| 8 | [`live-debug-assistant`](skills/live-debug-assistant/SKILL.md) | ターミナルエラーログ | 10秒ホットフィックスコマンド, `.env.sample` | 現場エラーログの即時診断およびAPI Keyセキュリティ保護 |
| 9 | [`workshop-faq-generator`](skills/workshop-faq-generator/SKILL.md) | テーマ・難易度 | `docs/20-faq.md` / `FAQ.md` | 参加者向け事前FAQ（ハードウェア・ネットワーク・コード）自動生成 |
| 10 | [`workshop-tester`](skills/workshop-tester/SKILL.md) | プロジェクトパス | `verify_workshop.py` 監査レポート | コード実行スモークテスト、2026モデル最新性およびリンク整合性検証 |
| 11 | [`workshop-web-researcher`](skills/workshop-web-researcher/SKILL.md) | ツール・モデルキーワード | 最新リリースバージョン情報 | Web検索による2026最新ツール/SDKバージョンのリアルタイム監査 |
| 12 | [`workshop-persona-loop-evaluator`](skills/workshop-persona-loop-evaluator/SKILL.md) | テーマ・カリキュラム | `docs/00-persona-loop-review-report.md` | 非開発者・初級・中級・シニア4ペルソナによるループエンジニアリングレビュー |
| 13 | [`open-codelabs-integrator`](skills/open-codelabs-integrator/SKILL.md) | プロジェクトパス | `output/open-codelabs/` (`codelab.yaml`), `oc` push | Open Codelabsマニフェスト出力と `oc` CLI/MCP連携発行 |
| 14 | [`colab-workshop-integrator`](skills/colab-workshop-integrator/SKILL.md) | プロジェクトパス | `output/colab/` (`*.ipynb`, バッジ), `colab` CLIテスト | Google Colabノートブック(`.ipynb`)変換、バッジ挿入およびColab CLIテスト |
| 15 | [`workshop-slide-generator`](skills/workshop-slide-generator/SKILL.md) | プロジェクトパス | `output/slides/` (`slides.md`, `index.html`, `.pptx`), PDF | Google Slides `.pptx`、Marp MarkdownおよびWebスライドの自動生成 |
| 16 | [`adk-workshop-builder`](skills/adk-workshop-builder/SKILL.md) | ADKテーマ・言語トラック | `root_agent` LlmAgent & サブエージェント、`evalset.json` | 公式5言語（Python, Go, Java, Kotlin, TypeScript, Polyglot）Google ADKハンズオン生成 |
| 17 | [`eli5-concept-explainer`](skills/eli5-concept-explainer/SKILL.md) | 技術概念・エラー | 3段階ELI5比喩とメンタルモデル (`docs/eli5-concept-cheat-sheet.md`) | 複雑なAI概念とエラーを初心者向けのアナロジーで解説 |
| 18 | [`android-workshop-builder`](skills/android-workshop-builder/SKILL.md) | Androidテーマ | Jetpack Compose + Google GenAI Kotlin SDK | Jetpack Compose Material 3および`android` CLIベースのAndroid GenAIラボ生成 |
| 19 | [`flutter-workshop-builder`](skills/flutter-workshop-builder/SKILL.md) | Flutterテーマ | Flutter 3.x + `google_generative_ai` | クロスプラットフォームFlutter GenAIラボおよびFlutter Webフォールバック生成 |
| 20 | [`a2ui-workshop-builder`](skills/a2ui-workshop-builder/SKILL.md) | A2UI / GenUIテーマ | `genui` + `WidgetCatalog` + `SurfaceController` | A2UI宣言型JSONストリーミングおよびFlutter GenUI動的UIラボ生成 |
| 21 | [`agents-cli-workshop-builder`](skills/agents-cli-workshop-builder/SKILL.md) | ADLC & `google-agents-cli` | 7公式ADLCスキル、評価データセット、Cloud Runデプロイ | Google Agents CLI (`google/agents-cli`) によるエージェント開発ライフサイクル(ADLC)ラボ生成 |

---

## クロスアーキテクチャ互換性マトリクス

| アーキテクチャ / OS | 推奨メインツール | 既知のリスク | 必須フォールバック経路 |
| --- | --- | --- | --- |
| macOS Intel Mac (`x86_64`) | Ollama CLI (`ollama serve`) | LM StudioのGPUアクセラレーション非対応・フリーズ発生 | Ollama CLI移行ガイド (`docs/18-intel-mac-prep.md`) を提供 |
| macOS Apple Silicon (`arm64`) | LM Studio / Ollama / MLX | Metal GPUハードウェアアクセラレーション完全対応 | MLX (`mlx-lm`) オプション対応 |
| Windows x86_64 (Intel/AMD) | LM Studio / Ollama | PowerShell実行ポリシー制限、Docker利用時のWSL2要件 | PowerShell Bypassスクリプト (`check_env.ps1`) を提供 |
| Windows ARM64 (Snapdragon) | Ollama CLI (Native) | x64エミュレーション時の推論速度低下 | Ollama ARM64ネイティブビルドを使用 |
| Linux / ChromeOS | Ollama CLI | GUI非対応 / コンテナサンドボックス制限 | `ollama serve` ターミナルモードおよび軽量モデル (`gemma4:e2b`) を使用 |
| Universal / Web | Flutter Web (`-d chrome`) | エミュレータのメモリ不足・仮想化非対応 | FlutterおよびA2UI/GenUIハンズオンのゼロインストール即時実行フォールバック |

---

## CLI の使い方 (`harness_cli.py`)

```bash
# 1. 21スキルを一括実行するワンクリック生成
uv run harness_cli.py generate-all --name "my-bwai-workshop" --topic "Local RAG with Gemma 4" --stack "python,ollama,docker" --model "gemini-3.8-flash"

# 2. 2026 Frontier & Open-Weight モデル一覧表示、旧モデルタグ自動アップグレード、および Markdown Em Dash(\u2014) 自動サニタイズ
uv run harness_cli.py list-models
uv run harness_cli.py audit-models --target my-bwai-workshop --fix
uv run harness_cli.py audit-typography --target my-bwai-workshop --fix

# 3. 公式5言語 Google ADK & Google Agents CLI ハンズオン初期化 (Python, Go, Java, Kotlin, TypeScript, Polyglot)
uv run harness_cli.py init --name "adk-python-lab" --topic "Multi-Agent ADLC with Google ADK and agents-cli" --stack "python,adk,agents-cli"
uv run harness_cli.py init --name "adk-go-lab" --topic "Go Multi-Agent Systems with Google ADK" --stack "go,adk"
uv run harness_cli.py init --name "adk-java-lab" --topic "Java 21 Enterprise Agents with Google ADK" --stack "java,adk"
uv run harness_cli.py init --name "adk-kotlin-lab" --topic "Kotlin Multi-Agent Systems with Google ADK" --stack "kotlin,adk"
uv run harness_cli.py init --name "adk-ts-lab" --topic "TypeScript Multi-Agent Systems with Google ADK" --stack "typescript,adk"
uv run harness_cli.py init --name "adk-polyglot-lab" --topic "Polyglot Multi-Language Google ADK Workshop" --stack "adk,polyglot,agents-cli"

# 4. Android Jetpack Compose GenAI & Flutter GenUI / A2UI ハンズオン初期化
uv run harness_cli.py init --name "android-gemini-lab" --topic "Android GenAI with Jetpack Compose" --stack "android"
uv run harness_cli.py init --name "flutter-genui-lab" --topic "Generative UI with Flutter and A2UI" --stack "flutter,genui,a2ui"

# 5. クロスアーキテクチャ互換性監査 & 4ペルソナループエンジニアリング評価
uv run harness_cli.py audit-compat --stack "adk,agents-cli,android,flutter,genui,docker,gemini-live"
uv run harness_cli.py audit-loop --topic "Local RAG with Gemma 4" --target my-bwai-workshop

# 6. コードスモークテスト、PDFハンドアウト、スライド、Colab、Open Codelabs出力
uv run harness_cli.py test --target my-bwai-workshop
uv run harness_cli.py build-pdf --target my-bwai-workshop
uv run harness_cli.py build-slides --target my-bwai-workshop
uv run harness_cli.py export-colab --target my-bwai-workshop --repo "JAICHANGPARK/my-bwai-workshop"
uv run harness_cli.py export-codelab --target my-bwai-workshop --push
```

---

## ライセンス

[MIT License](LICENSE)
