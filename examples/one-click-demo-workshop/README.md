# one-click-demo-workshop

> Topic: Flutter and Gemma 4 AI Agent

이 저장소는 **Flutter and Gemma 4 AI Agent** 워크숍을 위한 사전 준비 문서와 핸즈온 실습 코드 저장소입니다.

## 🚀 빠른 시작

1. **사전 준비 가이드**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **노트북 아키텍처 호환성 점검**: `./scripts/check_architecture_compat.sh` (Windows: `.\scripts\check_architecture_compat.ps1`)
3. **사전 환경 점검 스크립트 실행**: `./scripts/check_env.sh` (Windows: `.\scripts\check_env.ps1`)
4. **당일 핸즈온**:
   - 실습 순서: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - 실습 코드: [workshop/01_starter](./workshop/01_starter)
   - 정답 코드: [workshop/02_final](./workshop/02_final)
5. **발표자 & TA 진행 런북**: [RUNBOOK.md](./RUNBOOK.md)

## 📂 저장소 구조

```text
.
├── RUNBOOK.md                    # 발표자 및 TA 전용 진행 런북
├── gemma4-local-setup-guide.md   # 통합 사전 준비 가이드
├── docs/                        # 상세 주제별 및 아키텍처 호환성 가이드 문서
│   └── 00-architecture-compatibility-matrix.md
├── workshop/                    # 당일 핸즈온 실습
│   ├── 01_starter/              # 시작 코드
│   ├── 02_final/                # 최종 참고 코드
│   └── 03_labs/                 # Step-by-Step 실습 문서
├── prompt-pack/                 # 핸즈온 프롬프트 팩
├── scripts/                     # 크로스 아키텍처 점검 및 오프라인 번들링 스크립트
└── output/                      # 산출물 (PDF 등)
```

## 🔗 참고 (References)
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
