Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        Starting RailPulse AI (SIH26028)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python main.py"
Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm run dev"
Start-Sleep -Seconds 3

Start-Process "http://localhost:3000"
Write-Host "RailPulse AI launched successfully at http://localhost:3000" -ForegroundColor Green
