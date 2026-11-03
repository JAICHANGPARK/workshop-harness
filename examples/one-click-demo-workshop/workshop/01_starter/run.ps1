Write-Host "[INFO] Starting Workshop Application..." -ForegroundColor Green
if (Test-Path "..\..\.venv\Scripts\python.exe") {
    & "..\..\.venv\Scripts\python.exe" main.py
} elseif (Test-Path ".venv\Scripts\python.exe") {
    & ".venv\Scripts\python.exe" main.py
} else {
    python main.py
}
