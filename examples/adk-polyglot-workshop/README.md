# adk-polyglot-workshop

> Topic: Multi-Language Google ADK & Agents CLI ADLC Workshop
> Tech Stack: python,adk,agents-cli,polyglot

This repository contains pre-event preparation documents and hands-on lab code for the **Multi-Language Google ADK & Agents CLI ADLC Workshop** workshop.

## Quick Start

1. **Preparation Guide**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **Architecture Compatibility Check**: `./scripts/check_architecture_compat.sh` (Windows: `.\scripts\check_architecture_compat.ps1`)
3. **Environment Verification Script**: `./scripts/check_env.sh` (Windows: `.\scripts\check_env.ps1`)
4. **Day-of Hands-on Labs**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook**: [RUNBOOK.md](./RUNBOOK.md)

## Repository Structure

```text
.
├── AGENTS.md                     # AI Agent & Typography rules (No Em Dash rule)
├── CLAUDE.md                     # Claude Code instructions
├── RUNBOOK.md                    # Facilitator & TA execution runbook
├── gemma4-local-setup-guide.md   # Unified preparation guide
├── pyproject.toml                # Astral uv dependency file
├── docs/                        # Detailed topic docs, architecture compatibility & persona review reports
│   ├── 00-architecture-compatibility-matrix.md
│   └── 00-persona-loop-review-report.md
├── workshop/                    # Day-of hands-on labs
│   ├── 01_starter/              # Starter code
│   ├── 02_final/                # Reference solution code
│   └── 03_labs/                 # Step-by-step lab guides
├── prompt-pack/                 # Hands-on prompt pack
├── scripts/                     # Cross-architecture checks & offline bundling scripts
└── output/                      # Build artifacts (PDF, etc.)
```

## References
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
