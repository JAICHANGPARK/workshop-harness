---
name: workshop-tester
description: Runs automated smoke tests on starter and final code, validates markdown document integrity (broken relative paths, missing image links), and generates a test report.
---

# Workshop Tester Skill

## Purpose
Catches broken code, missing files, broken markdown relative links, missing images, and dead HTTP URLs **before** the workshop goes live. Prevents attendees from running into preventable setup errors or dead links during live sessions.

---

## 3-Stage Automated Test Pipeline

```text
[Stage 1: Code Smoke Test] -> [Stage 2: Markdown Link & Image Integrity Audit] -> [Stage 3: TODO Alignment Audit]
```

### Stage 1: Code Smoke Tests
- **`01_starter/` Verification**: Verify dependencies install cleanly and entry point (`main.py` / `run.sh`) executes without syntax or import errors.
- **`02_final/` Verification**: Run reference solution end-to-end and confirm expected terminal output and non-zero exit codes.
- **Environment Scripts**: Run `scripts/check_env.sh` and `scripts/check_architecture_compat.sh` to ensure execution without errors.

### Stage 2: Markdown Link & Image Integrity Audit
- Scan all `.md` files in `docs/`, `workshop/`, and repository root for relative file links (`[text](./path/to/file.md)`).
- Verify that every referenced target file exists on disk.
- Scan for embedded image links (`![caption](images/pic.png)`) and confirm image files exist in specified paths.
- Flag dead external HTTP URLs (404 / 500 errors).

### Stage 3: Starter vs Final TODO Alignment Audit
- Scan `workshop/01_starter/` for all `# TODO: [Lab N]` markers.
- Verify that every marked TODO item has a corresponding completed solution in `workshop/02_final/`.

---

## CLI Command Integration

Run the full integrity audit suite via `harness_cli.py`:

```bash
uv run harness_cli.py test --target my-bwai-workshop
```

---

## Output Artifact & CI Integration

- **Output**: Detailed pass/fail test report printed to stdout with explicit error line numbers and broken file paths.
- **Exit Code**: Returns `0` on 100% pass; returns `1` on any broken link or code failure for CI/CD workflow enforcement.

---

## Typography & Documentation Rule (No Em Dash)

- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks.
- **Approved Punctuation**: Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify and enforce zero em dashes across all generated markdown files.
