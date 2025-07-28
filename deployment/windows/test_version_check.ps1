# Test script to verify Python version checking logic in PowerShell
# This script tests the version checking with various Python versions

Write-Host "Testing Python version checking logic..." -ForegroundColor Cyan
Write-Host ""

function Test-PythonVersion {
    param([string]$TestVersion)
    
    Write-Host "Testing version: $TestVersion" -ForegroundColor Yellow
    
    if ($TestVersion -match "Python (\d+)\.(\d+)") {
        $majorVersion = [int]$matches[1]
        $minorVersion = [int]$matches[2]
        
        if ($majorVersion -eq 3 -and $minorVersion -ge 8) {
            Write-Host "  ✓ PASS - Version $TestVersion is supported" -ForegroundColor Green
            return $true
        } elseif ($majorVersion -gt 3) {
            Write-Host "  ✓ PASS - Version $TestVersion is supported (future Python)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "  ✗ FAIL - Version $TestVersion is not supported (need 3.8+)" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "  ✗ FAIL - Could not parse version: $TestVersion" -ForegroundColor Red
        return $false
    }
}

# Test various Python versions
Write-Host "Testing various Python versions:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$testVersions = @(
    "Python 3.7.9",
    "Python 3.8.0",
    "Python 3.8.10",
    "Python 3.9.0",
    "Python 3.9.18",
    "Python 3.10.0",
    "Python 3.10.12",
    "Python 3.11.0",
    "Python 3.11.7",
    "Python 3.12.0",
    "Python 3.12.1",
    "Python 3.13.0",
    "Python 3.13.1",
    "Python 3.14.0",
    "Python 3.15.0",
    "Python 2.7.18",
    "Python 4.0.0"
)

foreach ($version in $testVersions) {
    Test-PythonVersion $version
    Write-Host ""
}

Write-Host "Expected results:" -ForegroundColor Cyan
Write-Host "- Python 3.7.x and below: FAIL" -ForegroundColor White
Write-Host "- Python 3.8.x and above: PASS" -ForegroundColor White
Write-Host "- Python 2.x: FAIL" -ForegroundColor White
Write-Host "- Python 4.x and above: PASS" -ForegroundColor White
Write-Host ""

# Test with actual Python installation
Write-Host "Testing with your actual Python installation:" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

try {
    $actualVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Your Python version: $actualVersion" -ForegroundColor Yellow
        $result = Test-PythonVersion $actualVersion
        Write-Host ""
        
        if ($result) {
            Write-Host "✓ Your Python installation is compatible!" -ForegroundColor Green
        } else {
            Write-Host "✗ Your Python installation needs to be updated to 3.8+" -ForegroundColor Red
        }
    } else {
        Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    }
} catch {
    Write-Host "Error checking Python: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

