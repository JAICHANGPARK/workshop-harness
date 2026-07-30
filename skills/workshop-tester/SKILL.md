---
name: workshop-tester
description: Runs automated smoke tests on starter and final code, validates markdown document integrity (broken relative paths, missing image links), and generates a test report.
---

# Workshop Tester Skill

## Purpose
Catches broken code, missing files, and dead links **before** the workshop goes live, preventing attendees from hitting preventable errors during the session.

## Test Suites

### 1. Code Smoke Tests
- **Starter code**: Verify `01_starter/` builds and runs without errors (dependencies install, entry point executes)
- **Final code**: Verify `02_final/` produces expected output end-to-end
- **Environment scripts**: Verify `check_env.sh` / `check_env.ps1` execute without errors

### 2. Markdown Link Integrity
- Scan all `.md` files for relative paths (`./`, `../`) and verify target files exist
- Scan for image references (`![](path)`) and verify image files exist
- Scan for URL links and flag any returning HTTP 404

### 3. Template Completeness
- Verify all `TODO:` markers in starter code have corresponding solutions in final code
- Verify lab guide step numbers are sequential and complete

## Output Artifacts
- Test results printed to stdout with pass/fail summary
- Non-zero exit code on any failure for CI/CD integration
