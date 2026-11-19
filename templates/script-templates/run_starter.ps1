$ErrorActionPreference = "Stop"
Write-Host "[INFO] Starting Workshop Application..." -ForegroundColor Green

if (Test-Path "main.py") {
    if (Test-Path "..\..\.venv\Scripts\python.exe") {
        & "..\..\.venv\Scripts\python.exe" main.py @args
    } elseif (Test-Path ".venv\Scripts\python.exe") {
        & ".venv\Scripts\python.exe" main.py @args
    } elseif (Get-Command uv -ErrorAction SilentlyContinue) {
        uv run --project ..\.. python main.py @args
    } else {
        python main.py @args
    }
} elseif (Test-Path "package.json") {
    npm start -- @args
} elseif (Test-Path "go.mod") {
    go run . @args
} elseif (Test-Path "pubspec.yaml") {
    flutter run -d chrome @args
} elseif (Test-Path "gradlew.bat") {
    .\gradlew.bat assembleDebug @args
} else {
    Write-Host "[FAIL] No recognized workshop entrypoint found (main.py, package.json, go.mod, pubspec.yaml, gradlew.bat)." -ForegroundColor Red
    exit 1
}
