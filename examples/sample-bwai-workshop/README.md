# sample-bwai-workshop

> Topic: Testing Workshop Harness

이 저장소는 **Testing Workshop Harness** 워크숍을 위한 사전 준비 문서와 핸즈온 실습 코드 저장소입니다.

## 🚀 빠른 시작

1. **사전 준비 가이드**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **사전 점검 스크립트 실행**: `./scripts/check_env.sh` (Windows: `.\scripts\check_env.ps1`)
3. **당일 핸즈온**:
   - 실습 순서: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - 실습 코드: [workshop/01_starter](./workshop/01_starter)
   - 정답 코드: [workshop/02_final](./workshop/02_final)

## 📂 저장소 구조

```text
.
├── gemma4-local-setup-guide.md   # 통합 사전 준비 가이드
├── docs/                        # 상세 주제별 가이드 문서
├── workshop/                    # 당일 핸즈온 실습
│   ├── 01_starter/              # 시작 코드
│   ├── 02_final/                # 최종 참고 코드
│   └── 03_labs/                 # Step-by-Step 실습 문서
├── prompt-pack/                 # 핸즈온 프롬프트 팩
├── scripts/                     # 유틸리티 및 빌드 스크립트
└── output/                      # 산출물 (PDF 등)
```
