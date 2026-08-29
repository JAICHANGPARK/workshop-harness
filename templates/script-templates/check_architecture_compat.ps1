# ==============================================================================
# Cross-Architecture & OS Environment Auditor Script (Windows PowerShell)
# ==============================================================================

Write-Host "=== 💻 Laptop Architecture & OS Auditor (Windows) ===" -ForegroundColor Cyan

$arch = $env:PROCESSOR_ARCHITECTURE
$os = (Get-CimInstance Win32_OperatingSystem).Caption

Write-Host "Detected OS: $os"
Write-Host "Detected Architecture: $arch"
Write-Host "--------------------------------------------------" -ForegroundColor Gray

if ($arch -eq "AMD64") {
    Write-Host "[RECOMMENDED] Windows x64 (Intel/AMD)" -ForegroundColor Green
    Write-Host "  - LLM Runtime: LM Studio (GUI) or Ollama for Windows" -ForegroundColor White
    Write-Host "  - Android Labs: Ensure Windows Hypervisor / AEHD driver is enabled" -ForegroundColor White
    Write-Host "  - Flutter/GenUI Labs: Use Flutter Web (flutter run -d chrome) for fastest execution" -ForegroundColor White
    Write-Host "  - Note: If workshop requires Docker, ensure WSL2 is enabled." -ForegroundColor Yellow
} elseif ($arch -eq "ARM64") {
    Write-Host "[ATTENTION] Windows ARM64 (Snapdragon X)" -ForegroundColor Yellow
    Write-Host "  - LLM Runtime: Ollama CLI (Native ARM64 build recommended)" -ForegroundColor White
    Write-Host "  - Android Labs: Use ARM64 AVD image or physical USB device" -ForegroundColor White
    Write-Host "  - Flutter/GenUI Labs: Use Flutter Web target" -ForegroundColor White
} else {
    Write-Host "[WARN] Unknown Architecture: $arch" -ForegroundColor Red
}

Write-Host "--------------------------------------------------" -ForegroundColor Gray

