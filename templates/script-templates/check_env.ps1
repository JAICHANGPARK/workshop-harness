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

# 4. Check Flutter & Dart (Optional for Mobile Labs)
$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue
if ($flutterCmd) {
    $flVer = flutter --version | Select-Object -First 1
    Write-Host "[OK] Flutter SDK: $flVer" -ForegroundColor Green
    Write-Host "     -> Tip: Discover bundled AI skills via: dart run skills@ get" -ForegroundColor Green
} else {
    Write-Host "[INFO] Flutter SDK not detected in PATH (Required only for Flutter/GenUI/A2UI labs)." -ForegroundColor DarkGray
}

# 5. Check Java & Android SDK (Optional for Android Labs)
$javaCmd = Get-Command java -ErrorAction SilentlyContinue
if ($javaCmd) {
    $jVer = java -version 2>&1 | Select-Object -First 1
    Write-Host "[OK] Java Runtime: $jVer" -ForegroundColor Green
} else {
    Write-Host "[INFO] Java JDK not detected in PATH (Required for Android/Compose labs)." -ForegroundColor DarkGray
}

$adbCmd = Get-Command adb -ErrorAction SilentlyContinue
if ($adbCmd) {
    Write-Host "[OK] Android Debug Bridge (adb) found." -ForegroundColor Green
}

# 6. Check Google Android CLI & Skills (Optional for Android Labs)
$androidCmd = Get-Command android -ErrorAction SilentlyContinue
if ($androidCmd) {
    Write-Host "[OK] Google Android CLI found." -ForegroundColor Green
} else {
    Write-Host "[INFO] Google Android CLI not detected. (Install: curl.exe -fsSL https://dl.google.com/android/cli/latest/windows_x86_64/install.cmd -o `"$env:TEMP\i.cmd`"; & `"$env:TEMP\i.cmd`")" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "=== Check Completed! ===" -ForegroundColor Cyan


