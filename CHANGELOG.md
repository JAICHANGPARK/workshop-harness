# Changelog

All notable changes to the **Workshop Harness** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2026.07.30] - 2026-07-30

### Added
- **9 Specialized Agent Skills**:
  - `workshop-scaffolder`: Scaffolds standard repository structure (`docs/`, `workshop/`, `prompt-pack/`, `scripts/`).
  - `cross-architecture-checker`: Audits chipset (Apple Silicon, Intel Mac, Windows, Linux) compatibility and generates fallback paths.
  - `prerequisite-checker`: Generates OS-specific setup guides and `check_env.sh/ps1` scripts.
  - `hands-on-curriculum-builder`: Builds step-by-step labs, `starter` vs `final` code, and prompt packs.
  - `pdf-handout-generator`: Builds publication-ready PDF handouts and contact sheet previews via ReportLab and PyMuPDF.
  - `workshop-troubleshooter`: Generates troubleshooting matrices by RAM specs (8G/16G/32G+) and OS.
  - `workshop-runbook-generator`: Creates minute-by-minute facilitator timeline runbooks and cue cards (`RUNBOOK.md`).
  - `live-debug-assistant`: Diagnoses live terminal errors with 10-second hotfixes and enforces API Key security protocols.
  - `workshop-faq-generator`: Generates attendee FAQs for hardware, network, and code questions (`FAQ.md`).
- **Cross-Architecture Auditor CLI**:
  - Added `harness_cli.py audit-compat --stack "lmstudio,docker,mlx"` command for pre-session risk auditing.
- **Offline Asset Bundler**:
  - Added `scripts/bundle_offline_assets.sh` script to package pip wheels for emergency network outages.
- **Skill Installer**:
  - Added `scripts/install_skills.sh` for one-click installation to `~/.gemini/skills`.
- **Multilingual README Support**:
  - Added English (`README.md`), Korean (`README_KR.md`), Japanese (`README_JA.md`), and Chinese (`README_ZH.md`).

### Changed
- Standardized default primary `README.md` to English with clean, professional, emoji-free markdown styling.

### Security
- Enforced API Key protection protocol with `.env.sample` templates and `.gitignore` rules.
