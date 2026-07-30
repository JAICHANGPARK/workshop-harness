# ==============================================================================
# BWAI Workshop Environment Verification Script (Windows PowerShell)
# ==============================================================================

Write-Host "=== 🔍 BWAI Workshop Environment Checker (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) {
    $ver = python --version
    Write-Host "[OK] Python: $ver" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python is not installed or not in PATH." -ForegroundColor Red
}

# 2. Check uv
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    $uvVer = uv --version
    Write-Host "[OK] uv package manager: $uvVer" -ForegroundColor Green
} else {
    Write-Host "[WARN] uv is not installed. (Install: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`")" -ForegroundColor Yellow
}

# 3. Check Ollama / LM Studio port
try {
    $res = Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Ollama server is running on port 11434." -ForegroundColor Green
} catch {
    try {
        $res2 = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "[OK] LM Studio server is running on port 1234." -ForegroundColor Green
    } catch {
        Write-Host "[WARN] No local LLM server detected on localhost:11434 or localhost:1234." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== Check Completed! ===" -ForegroundColor Cyan
