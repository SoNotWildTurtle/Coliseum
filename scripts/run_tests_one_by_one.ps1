# Run pytest one file at a time so failures are isolated.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_tests_one_by_one.ps1
$ErrorActionPreference = "Stop"

$testRoot = Join-Path $PSScriptRoot ".." "tests"
$tests = Get-ChildItem -Path $testRoot -Filter "test_*.py" -File | Sort-Object Name

if (-not $tests) {
  Write-Host "No test_*.py files found in $testRoot"
  exit 1
}

$failed = @()
$passed = 0

foreach ($test in $tests) {
  Write-Host ("Running {0}" -f $test.Name) -ForegroundColor Cyan
  & pytest -q $test.FullName
  if ($LASTEXITCODE -ne 0) {
    $failed += $test.Name
  } else {
    $passed++
  }
}

if ($failed.Count -gt 0) {
  Write-Host ("Failed: {0}" -f $failed.Count) -ForegroundColor Red
  $failed | ForEach-Object { Write-Host (" - {0}" -f $_) -ForegroundColor Red }
  exit 1
}

Write-Host ("All tests passed ({0} files)." -f $passed) -ForegroundColor Green
