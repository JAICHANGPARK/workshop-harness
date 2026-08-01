# Cross-Architecture Checker Skill

The **Cross-Architecture Checker** skill ([`skills/cross-architecture-checker/SKILL.md`](file:///Users/jaichang/Documents/GitHub/workshop-harness/skills/cross-architecture-checker/SKILL.md)) audits tech stack hardware risks across participant laptops (Apple Silicon, Intel Mac, Windows, Linux) and generates mandatory fallback guides.

---

## Primary Roles

1. **Chipset & OS Risk Auditing**:
   - `LM Studio`: Missing Metal GPU acceleration & freeze risk on Intel Macs → Mandatory `Ollama CLI` fallback guide in `docs/18-intel-mac-prep.md`.
   - `Docker Desktop`: WSL2 / Hyper-V configuration failures on Windows Home → Local Python script fallback.
   - `MLX`: Strictly Apple Silicon (arm64) only → HuggingFace or Ollama fallback for Non-Mac users.
2. **Automated Architecture Selector Scripts**:
   - Generates `check_architecture_compat.sh` and `check_architecture_compat.ps1` in the target workshop scripts directory.

---

## CLI Usage Example

```bash
uv run harness_cli.py audit-compat --stack "lmstudio,docker,mlx"
```
