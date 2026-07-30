---
name: workshop-tester
description: 워크숍 배포 전 starter/final 코드 실행 스모크 테스트, 마크다운 문서 내 상대 경로 및 이미지 링크 유효성(Broken Link) 자동 검증 하네스 스킬
---

# Workshop Tester & Integrity Auditor Skill

## 📌 목적
워크숍 자료를 참가자들에게 공개하기 전, **"starter/final 코드가 실제로 에러 없이 동작하는지"**, **"마크다운 가이드 내 링크나 이미지 경로가 깨진 곳(Broken Link)은 없는지"**를 하네스 차원에서 자동 검증하여 결함을 사전 차단합니다.

---

## 🔍 자동 검증 3대 항목

1. **코드 스모크 테스트 (Code Smoke Test)**:
   - `workshop/01_starter`의 `run.sh` / `run.ps1` 실행 테스트
   - `workshop/02_final`의 `run.sh` / `run.ps1` 실행 테스트 및 반환 코드 0 검증
2. **마크다운 링크 검증 (Markdown Broken Link Audit)**:
   - `docs/` 및 `README.md` 내의 상대 경로 링크(`[text](./docs/01-hardware.md)`)가 실제 존재하는 파일인지 전수 검사
3. **이미지 자산 경로 검증 (Asset Integrity Check)**:
   - `![alt](./assets/screenshot.png)` 내의 이미지 파일 경로 유효성 검사

---

## 🛠️ CLI 사용법 (`harness_cli.py test`)

```bash
# 워크숍 프로젝트의 코드 및 문서 링크 유효성 자동 검증
python3 harness_cli.py test --target my-bwai-workshop
```

**검증 출력 예시:**
```text
🔍 Auditing Workshop Integrity for: my-bwai-workshop
--------------------------------------------------
[OK] Markdown Links: 24/24 links valid.
[OK] Asset Images: 6/6 image paths valid.
[OK] Code Execution: workshop/01_starter -> Passed.
[OK] Code Execution: workshop/02_final -> Passed.
--------------------------------------------------
✨ All Workshop Integrity Checks Passed! Ready for publication.
```
