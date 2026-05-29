$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
python -m pip install -e . --no-build-isolation
$scriptsPath = python -c "import site, os; print(os.path.join(site.USER_BASE, 'Scripts'))"
Write-Host ""
Write-Host "HumanLang installed."
Write-Host "Try: humanlang run examples\hello.hl"
Write-Host "If Windows cannot find humanlang, add this folder to PATH:"
Write-Host $scriptsPath
