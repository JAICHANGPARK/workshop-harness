---
name: prerequisite-checker
description: OS별(macOS Apple Silicon/Intel, Windows PowerShell/WSL2, Linux, ChromeOS) 사전 준비 가이드 문서 작성 및 자동 점검 스크립트(check_env.sh, check_env.ps1) 생성을 담당하는 스킬
---

# Prerequisite Checker Skill

## 📌 목적
참가자들이 워크숍 당일 현장에서 네트워크나 환경 문제로 막히지 않도록, 행사 전에 본인의 컴퓨터 사양 및 필수 소프트웨어(Ollama, LM Studio, Docker, Python uv, Go, Dart/Flutter 등)를 사전 설치하고 점검할 수 있는 가이드와 자동화 스크립트를 제공합니다.

## 🎯 주요 기능 및 역할

1. **통합 사전 준비 가이드 (`gemma4-local-setup-guide.md` / `prerequisites.md`) 생성**:
   - 하드웨어 메모리 사양별 모델 선택 기준 제시:
     - `8GB RAM`: `gemma4:e2b` (경량 모델)
     - `16GB RAM`: `gemma4:e4b` (기본 모델)
     - `32GB+ RAM`: `gemma4:26b-a4b` 또는 `31b`
   - OS별 설치 안내:
     - **Windows**: PowerShell, WSL2, Docker VMM 설정
     - **Apple Silicon Mac**: LM Studio / Ollama / MLX
     - **Intel Mac**: LM Studio 실행 이슈가 있을 시 Ollama 우선 권장
     - **ChromeOS / Linux**: Ollama CLI 기준 안내

2. **현장 네트워크 부하 방지를 위한 사전 다운로드 명령 생성**:
   - Ollama 모델 다운로드: `ollama pull gemma4:e4b`
   - Python 패키지 동기화: `uv sync`
   - HuggingFace 임베딩 캐싱: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('voyageai/voyage-4-nano')"`
   - Local Atlas / Docker 이미지 사전 pull: `atlas local setup local-rag`

3. **자동 검증 스크립트 (`scripts/check_env.sh`, `scripts/check_env.ps1`) 생성**:
   - Python 버전 (3.9+), `uv` 설치 여부
   - Docker daemon 동작 여부
   - Ollama / LM Studio local port (11434, 1234) 리스닝 여부
   - 사용 가능 RAM 및 디스크 용량 (최소 10GB 이상 여부)

## 📋 검증 스크립트 템플릿 사용법

### macOS / Linux (`check_env.sh`)
```bash
#!/usr/bin/env bash
echo "=== 🔍 BWAI Workshop Environment Checker ==="
# 1. Python & uv check
if command -v uv &> /dev/null; then
    echo "[OK] uv is installed: $(uv --version)"
else
    echo "[WARN] uv is not installed. Please install via: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# 2. Ollama check
if curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "[OK] Ollama server is running on localhost:11434"
else
    echo "[WARN] Ollama server is not running."
fi

# 3. Model check
if command -v ollama &> /dev/null; then
    models=$(ollama list)
    echo "[INFO] Installed Ollama models:"
    echo "$models"
fi
```

### Windows (`check_env.ps1`)
```powershell
Write-Host "=== 🔍 BWAI Workshop Environment Checker (Windows) ===" -ForegroundColor Cyan

# 1. Python & uv check
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    Write-Host "[OK] uv is installed: $(uv --version)" -ForegroundColor Green
} else {
    Write-Host "[WARN] uv is not installed." -ForegroundColor Yellow
}

# 2. Ollama port check
try {
    $res = Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 2
    Write-Host "[OK] Ollama server is running on localhost:11434" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Ollama server is not running." -ForegroundColor Yellow
}
```
