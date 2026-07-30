# 하드웨어 및 운영체제 환경 설정 가이드

본 문서에서는 워크숍 진행을 위해 각 참가자의 장비 사양(RAM, CPU/GPU, OS)에 알맞은 실행 환경 선택 기준을 안내합니다.

## 💻 장비 사양별 권장 모델 및 설정

| RAM 메모리 | 권장 모델 선택 | 실행 도구 추천 | 비고 |
| --- | --- | --- | --- |
| **8GB** | `gemma4:e2b` (또는 2B~3B 급) | Ollama / LM Studio | 컨텍스트 길이를 2048 이하로 설정 권장 |
| **16GB** | `gemma4:e4b` (또는 7B~9B 급) | LM Studio / Ollama | 기본 핸즈온 권장 스펙 |
| **32GB+** | `gemma4:26b-a4b` 또는 31B | LM Studio / Ollama / MLX | 고성능 파이프라인 및 멀티에이전트 실습 가능 |

> 💡 **참고**: 파라미터 수의 'B'는 Billion(10억 개)을 의미하며, 파일 용량(GB)과 1:1로 대응하지 않습니다. 4-bit 양자화(Q4_K_M) 모델 기준 다운로드 용량을 확인하세요.

---

## 🖥️ 운영체제(OS)별 가이드

### 1. Apple Silicon Mac (M1/M2/M3/M4)
- **추천 도구**: LM Studio, Ollama, MLX
- Metal GPU 가속이 기본 지원되므로 원활한 로컬 LLM 추론이 가능합니다.

### 2. Intel Mac
- **추천 도구**: Ollama CLI
- LM Studio 실행 중 멈춤 현상이 발생할 경우, 터미널 기반의 Ollama CLI를 사용하여 CPU/GPU 추론을 수행하세요.

### 3. Windows (Windows 10/11)
- **추천 도구**: LM Studio (GUI) 또는 Ollama for Windows
- PowerShell 명령어 실행 정책 변경:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- Docker/RAG 실습 시 WSL2 (Windows Subsystem for Linux 2) 설정 필수.

### 4. Linux / ChromeOS
- **추천 도구**: Ollama CLI
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

---

## 🔗 참고 (References)

- **Ollama Documentation**: [https://ollama.com](https://ollama.com)
- **LM Studio Developer Portal**: [https://lmstudio.ai](https://lmstudio.ai)
- **Build with AI Seoul Reference**: [https://github.com/JAICHANGPARK/2026-bwai-seoul](https://github.com/JAICHANGPARK/2026-bwai-seoul)
