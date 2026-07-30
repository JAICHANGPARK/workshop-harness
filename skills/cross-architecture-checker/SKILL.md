---
name: cross-architecture-checker
description: 다양한 참석자 노트북 아키텍처(Apple Silicon arm64, Intel Mac x86_64, Windows x86/ARM64, Linux, ChromeOS)와 도구(LM Studio, Ollama, Docker, MLX 등) 간 호환성 이슈를 점검하고 대체 경로(Fallback Matrix)를 진단/생성하는 스킬
---

# Cross Architecture & OS Compatibility Checker Skill

## 📌 목적
워크숍 참석자마다 보유한 노트북 아키텍처(Apple Silicon M1~M4, Intel x86_64 Mac, Windows Intel/AMD, Windows Snapdragon ARM64, Linux, ChromeOS)가 상이합니다.
특정 도구(예: LM Studio)를 메인 도구로 지정하더라도 **Intel Mac 등 특정 환경에서 동작하지 않거나 호환성 에러가 발생하는 리스크를 사전 진단하고, 자동 대안(Fallback) 경로 및 환경 검증 스크립트**를 구성합니다.

---

## 💻 칩셋 아키텍처 & OS별 도구 호환성 검증 표준 (Compatibility Matrix)

| 아키텍처 / OS | 추천 메인 도구 | 주의사항 & 알려진 제약 (Known Issues) | 필수 대체 경로 (Fallback) |
| --- | --- | --- | --- |
| **macOS Apple Silicon** (M1~M4, arm64) | LM Studio / Ollama | Metal GPU 가속 원활, 최상의 환경 | MLX (`mlx-lm`) 추가 활용 가능 |
| **macOS Intel Mac** (x86_64) | **Ollama CLI** (`ollama serve`) | ⚠️ **LM Studio 호환성 이슈 발생 빈번** (Metal 가속 미지원, CPU 과열/다운 현상) | **LM Studio 대신 Ollama 기준 가이드 필수 제공** |
| **Windows x86_64** (Intel/AMD) | LM Studio / Ollama | PowerShell 실행 정책 제약, Docker 시 WSL2 필수 | PowerShell Bypass 스크립트, Ollama CLI |
| **Windows ARM64** (Snapdragon X) | Ollama (arm64 / x64 emu) | x64 에뮬레이션 시 추론 속도 저하 | Ollama Native build 또는 Cloud API 대체 |
| **Linux x86_64 / arm64** | Ollama CLI | GUI 미지원, 터미널 기반 동작 | `curl -fsSL https://ollama.com/install.sh \| sh` |
| **ChromeOS (Linux Container)** | Ollama CLI | Crostini 가상화 샌드박스 내부 실행, RAM 제한 | 소형 모델(`e2b` 2B~3B) 및 CPU 추론 전용 |

---

## 🔍 워크숍 준비 시 아키텍처 점검 체크리스트 (Audit Checklist)

### 1. 메인 도구 지정 시 위험 요소 오디팅
- **LM Studio를 메인 도구로 정한 경우**:
  - 🚨 **위험**: Intel Mac 참석자는 LM Studio 실행 중 멈춤/오류가 자주 발생함.
  - ✅ **대응**: `docs/18-intel-mac-prep.md` 문서를 마련하고, Intel Mac 사용자는 `Ollama`를 다운로드하여 `http://localhost:11434` 포트로 접속하도록 분기 가이드 추가.
- **Docker Desktop을 필수로 지정한 경우**:
  - 🚨 **위험**: Windows Home Edition 참가자의 Hyper-V / WSL2 미설치, ChromeOS / M1 Mac의 x86 container 호환 문제.
  - ✅ **대응**: Native 실행용 Python fallback script 또는 Cloud Atlas/Managed 서비스 대안 주소 준비.
- **Python 패키지 (C/C++ 빌드 포함된 패키지)**:
  - 🚨 **위험**: Windows x86에서 `torch` / `cxx` 컴파일 에러, Apple Silicon에서 `x86_64` wheels 설치 에러.
  - ✅ **대응**: 순수 Python 패키지 또는 사전 빌드된 휠(`uv`) 기반 설치 검증.

---

## 🛠️ 크로스 아키텍처 자동 감지 스크립트 (`check_architecture_compat.sh` / `.ps1`)

참석자가 실행하면 자신의 노트북 아키텍처와 OS를 감지하여 알맞은 도구를 추천해주는 스크립트 기능입니다.

### macOS / Linux 아키텍처 감지 (`check_architecture_compat.sh`)
```bash
#!/usr/bin/env bash
OS_TYPE="$(uname -s)"
ARCH_TYPE="$(uname -m)"

echo "=== 💻 Laptop Architecture & OS Auditor ==="
echo "OS: $OS_TYPE | Architecture: $ARCH_TYPE"

if [ "$OS_TYPE" = "Darwin" ]; then
    if [ "$ARCH_TYPE" = "arm64" ]; then
        echo "✅ System: Apple Silicon Mac (M-Series)"
        echo "👉 Recommended Tool: LM Studio or Ollama (Metal Acceleration Enabled)"
    elif [ "$ARCH_TYPE" = "x86_64" ]; then
        echo "⚠️ System: Intel Mac"
        echo "👉 WARNING: LM Studio may have stability issues on Intel Mac."
        echo "👉 Recommended Tool: Ollama CLI (ollama serve)"
    fi
elif [ "$OS_TYPE" = "Linux" ]; then
    echo "✅ System: Linux ($ARCH_TYPE)"
    echo "👉 Recommended Tool: Ollama CLI"
fi
```

### Windows 아키텍처 감지 (`check_architecture_compat.ps1`)
```powershell
$arch = $env:PROCESSOR_ARCHITECTURE
Write-Host "=== 💻 Laptop Architecture & OS Auditor (Windows) ===" -ForegroundColor Cyan
Write-Host "Architecture: $arch"

if ($arch -eq "AMD64") {
    Write-Host "✅ System: Windows x64 (Intel/AMD)" -ForegroundColor Green
    Write-Host "👉 Recommended Tool: LM Studio (GUI) or Ollama for Windows" -ForegroundColor Green
    Write-Host "⚠️ Note: Enable WSL2 if Docker is required." -ForegroundColor Yellow
} elseif ($arch -eq "ARM64") {
    Write-Host "⚠️ System: Windows ARM64 (Snapdragon)" -ForegroundColor Yellow
    Write-Host "👉 Recommended Tool: Ollama CLI" -ForegroundColor Green
}
```

---

## 🚀 하네스 CLI 통합 사용법 (`harness_cli.py audit-compat`)

```bash
# 워크숍 호환성 위험 요소 및 대체 경로 진단
python3 harness_cli.py audit-compat --stack "lmstudio,python,docker"
```

출력 예시:
```text
🔍 Auditing Tech Stack: ['lmstudio', 'python', 'docker']
--------------------------------------------------
[!] Warning: 'lmstudio' selected. Intel Mac users WILL experience issues.
    -> Action: Include Ollama fallback guide for Intel Mac.
[!] Warning: 'docker' selected. Windows Home & ChromeOS users may fail container boot.
    -> Action: Provide local non-docker alternative script.
--------------------------------------------------
✅ Fallback Matrix Generated in docs/00-architecture-compatibility-matrix.md
```
