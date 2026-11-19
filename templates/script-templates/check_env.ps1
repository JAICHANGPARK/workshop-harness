# ==============================================================================
# Workshop Environment Verification Script (Windows PowerShell)
# ==============================================================================

$FailCount = 0
$WarnCount = 0

Write-Host "=== Workshop Environment Checker (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# 0. Show workshop manifest summary if workshop.json is present
$WorkshopStack = @()
if (Test-Path "workshop.json") {
    try {
        $manifest = Get-Content "workshop.json" -Raw | ConvertFrom-Json
        $WorkshopStack = @($manifest.stack)
        Write-Host "[INFO] Manifest: $($manifest.name) | Stack: $($WorkshopStack -join ',') | Cloud: $($manifest.models.cloud)" -ForegroundColor Green
    } catch {}
}

# 1. System RAM & Gemma 4 Tier Recommendation
try {
    $ramBytes = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory
    $ramGB = [math]::Floor($ramBytes / 1GB)
    if ($ramGB -lt 12) {
        Write-Host "[OK] System RAM: ${ramGB}GB -> Recommended local tier: 8GB (gemma4:e2b + embeddinggemma-2:270m, or Google Colab)" -ForegroundColor Yellow
    } elseif ($ramGB -lt 24) {
        Write-Host "[OK] System RAM: ${ramGB}GB -> Recommended local tier: 16GB (gemma4:e4b / gemma4:12b + embeddinggemma-2)" -ForegroundColor Green
    } else {
        Write-Host "[OK] System RAM: ${ramGB}GB -> Recommended local tier: 32GB+ (gemma4:26b / gemma4:31b + embeddinggemma-2)" -ForegroundColor Green
    }
} catch {}

# 2. Free Disk Space Check
try {
    $drive = (Get-Location).Drive
    $freeGB = [math]::Floor($drive.Free / 1GB)
    if ($freeGB -lt 10) {
        Write-Host "[WARN] Low Disk Space: ${freeGB}GB free (< 10GB recommended for local models / SDKs)" -ForegroundColor Yellow
        $WarnCount++
    } else {
        Write-Host "[OK] Disk Space: ${freeGB}GB available" -ForegroundColor Green
    }
} catch {}

# 3. Check Python
$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) {
    $ver = python --version
    Write-Host "[OK] Python: $ver" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python is not installed or not in PATH." -ForegroundColor Red
    $FailCount++
}

# 4. Check uv
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    $uvVer = uv --version
    Write-Host "[OK] uv package manager: $uvVer" -ForegroundColor Green
} else {
    Write-Host "[WARN] uv is not installed. (Install: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`")" -ForegroundColor Yellow
    $WarnCount++
}

# 5. Check Ollama / LM Studio port
try {
    $res = Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Ollama server is running on port 11434." -ForegroundColor Green
} catch {
    try {
        $res2 = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "[OK] LM Studio server is running on port 1234." -ForegroundColor Green
    } catch {
        Write-Host "[WARN] No local LLM server detected on localhost:11434 or localhost:1234." -ForegroundColor Yellow
        $WarnCount++
    }
}

# 6. Check Node.js (Optional unless TypeScript stack)
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCmd) {
    Write-Host "[OK] Node.js: $(node --version)" -ForegroundColor Green
} elseif ($WorkshopStack -contains "typescript" -or $WorkshopStack -contains "ts" -or $WorkshopStack -contains "node") {
    Write-Host "[FAIL] Node.js is required for this TypeScript workshop." -ForegroundColor Red
    $FailCount++
}

# 7. Check Flutter & Dart (Optional unless Flutter stack)
$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue
if ($flutterCmd) {
    $flVer = flutter --version | Select-Object -First 1
    Write-Host "[OK] Flutter SDK: $flVer" -ForegroundColor Green
} elseif ($WorkshopStack -contains "flutter" -or $WorkshopStack -contains "genui" -or $WorkshopStack -contains "a2ui") {
    Write-Host "[FAIL] Flutter SDK is required for this Flutter/GenUI workshop." -ForegroundColor Red
    $FailCount++
} else {
    Write-Host "[INFO] Flutter SDK not detected (Required only for Flutter/GenUI/A2UI labs)." -ForegroundColor DarkGray
}

# 8. Check Java & Android CLI
$javaCmd = Get-Command java -ErrorAction SilentlyContinue
if ($javaCmd) {
    $jVer = java -version 2>&1 | Select-Object -First 1
    Write-Host "[OK] Java Runtime: $jVer" -ForegroundColor Green
} elseif ($WorkshopStack -contains "android" -or $WorkshopStack -contains "java") {
    Write-Host "[FAIL] Java JDK is required for this Android/Java workshop." -ForegroundColor Red
    $FailCount++
}

$androidCmd = Get-Command android -ErrorAction SilentlyContinue
if ($androidCmd) {
    Write-Host "[OK] Google Android CLI found." -ForegroundColor Green
}

# 9. Check Google ADK CLI & Google Agents CLI
if (Get-Command adk -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Google ADK CLI (adk) found." -ForegroundColor Green
}
if (Get-Command agents-cli -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Google Agents CLI (agents-cli) found." -ForegroundColor Green
}

# 10. Check Go
$goCmd = Get-Command go -ErrorAction SilentlyContinue
if ($goCmd) {
    Write-Host "[OK] Go Toolchain: $(go version)" -ForegroundColor Green
} elseif ($WorkshopStack -contains "go" -or $WorkshopStack -contains "golang") {
    Write-Host "[FAIL] Go toolchain is required for this Go workshop." -ForegroundColor Red
    $FailCount++
}

# 11. Check Cloud AI Provider API Keys (Gemini / Anthropic Claude / OpenAI)
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim().Trim('"'))
        }
    }
}
$foundCloudKey = $false
if ($env:GEMINI_API_KEY -and $env:GEMINI_API_KEY -ne "YOUR_GEMINI_API_KEY_HERE") {
    Write-Host "[OK] GEMINI_API_KEY: configured" -ForegroundColor Green
    $foundCloudKey = $true
}
if ($env:ANTHROPIC_API_KEY -and $env:ANTHROPIC_API_KEY -ne "YOUR_ANTHROPIC_API_KEY_HERE") {
    Write-Host "[OK] ANTHROPIC_API_KEY: configured" -ForegroundColor Green
    $foundCloudKey = $true
}
if ($env:OPENAI_API_KEY -and $env:OPENAI_API_KEY -ne "YOUR_OPENAI_API_KEY_HERE") {
    Write-Host "[OK] OPENAI_API_KEY: configured" -ForegroundColor Green
    $foundCloudKey = $true
}
if (-not $foundCloudKey) {
    Write-Host "[INFO] No cloud API key detected in env/.env (Set GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY if running cloud labs)." -ForegroundColor DarkGray
}

Write-Host ""
if ($FailCount -gt 0) {
    Write-Host "=== Environment Check FAILED ($FailCount error(s), $WarnCount warning(s)) ===" -ForegroundColor Red
    exit 1
} else {
    Write-Host "=== Environment Check PASSED (0 errors, $WarnCount warning(s)) ===" -ForegroundColor Green
    exit 0
}
