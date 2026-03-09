$ErrorActionPreference = "Stop"

$env:HOLO_PLAYTEST = "1"
$env:HOLO_TELEMETRY = "1"
if (-not $env:HOLO_TELEMETRY_VALIDATE) {
    $env:HOLO_TELEMETRY_VALIDATE = "1"
}

Write-Host "Playtest mode enabled:"
Write-Host "  HOLO_PLAYTEST=1"
Write-Host "  HOLO_TELEMETRY=1"
Write-Host ""
Write-Host "In another terminal run:"
Write-Host "  .\\scripts\\run_playtest_agent.ps1"
Write-Host ""

python main.py
