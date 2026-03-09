$ErrorActionPreference = "Stop"

$base = "SavedGames/playtest"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$output = "SavedGames/playtest/advice_$timestamp.json"

Write-Host "Starting playtest agent..."
Write-Host "Output: $output"
Write-Host "Press Ctrl+C to stop."

python -m hololive_coliseum.tools.playtest_agent --interval 5 --output $output
