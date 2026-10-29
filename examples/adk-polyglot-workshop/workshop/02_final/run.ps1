Write-Host "🚀 Starting Workshop Application..." -ForegroundColor Green
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    uv run python main.py
} else {
    python main.py
}
