# 💻 참가자 노트북 아키텍처 & OS 호환성 가이드 (Compatibility Matrix)

워크숍 세션 준비 시 참석자들의 다양한 노트북 하드웨어 아키텍처(Apple Silicon, Intel Mac, Windows x86, Windows ARM64, Linux)에 맞춰 아래의 도구 권장 사항 및 대체 경로(Fallback)를 반드시 확인해 주세요.

---

## 📊 호환성 & 대체 경로 요약표 (Fallback Matrix)

| 구분 | 참석자 환경 | 권장 메인 도구 | 알려진 위험 & 제약 사항 | 대체 경로 (Fallback Path) |
| --- | --- | --- | --- | --- |
| 1 | **macOS Apple Silicon** (M1~M4) | LM Studio / Ollama | 없음 (Metal GPU 최적화 지원) | MLX (`mlx-lm`) 추가 사용 가능 |
| 2 | **macOS Intel Mac** (x86_64) | **Ollama CLI** | 🚨 **LM Studio 가속 미지원 / 멈춤 현상 발생** | **LM Studio 대신 Ollama로 전환 가이드 제공** |
| 3 | **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell 스크립트 실행 제한, Docker 시 WSL2 필요 | `Set-ExecutionPolicy -Scope Process Bypass` 실행 |
| 4 | **Windows ARM64** (Snapdragon) | Ollama CLI | x64 에뮬레이션 시 추론 속도 저하 | Ollama Native build 사용 |
| 5 | **Linux / ChromeOS** | Ollama CLI | GUI 설치 미지원 | `ollama serve` 터미널 모드 사용 |

---

## 🚨 Intel Mac 참석자 필독 안내

> **중요**: LM Studio는 Intel CPU 기반 Mac에서 GPU 가속이 작동하지 않거나 프로그램이 비정상적으로 종료되는 사례가 자주 보고됩니다.  
> Intel Mac 사용자는 **LM Studio 대신 Ollama**를 기준으로 사전 준비를 진행하세요.

1. **Ollama 설치**: https://ollama.com/download/Ollama-darwin.zip
2. **모델 받아두기**:
   ```bash
   ollama pull gemma4:e4b
   ```
3. **로컬 API 호스트 확인**: Ollama 실행 시 `http://localhost:11434` 포트로 자동 연동됩니다.
