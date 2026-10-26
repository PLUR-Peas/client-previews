param([string]$Message = 'Publish approved previews')
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & python scripts/prepare.py
    if ($LASTEXITCODE -ne 0) { throw 'Static validation failed. Nothing pushed.' }
    & git rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0) { throw 'This folder must first be connected as its own Git repository.' }
    $repositoryRoot = (& git rev-parse --show-toplevel).Trim()
    if ((Resolve-Path -LiteralPath $repositoryRoot).Path -ne (Resolve-Path -LiteralPath $PSScriptRoot).Path) {
        throw 'Refusing to publish from a parent repository.'
    }
    $currentBranch = (& git branch --show-current).Trim()
    if ($currentBranch -ne 'main') { throw 'Publish must run from main.' }
    & git add -- public scripts .github Publish.ps1 README.md .gitignore .gitattributes
    if ($LASTEXITCODE -ne 0) { throw 'Could not stage preview files.' }
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        & git commit -m $Message
        if ($LASTEXITCODE -ne 0) { throw 'Commit failed.' }
    } elseif ($LASTEXITCODE -ne 0) { throw 'Could not inspect staged changes.' }
    & git push origin main
    if ($LASTEXITCODE -ne 0) { throw 'Push failed. Remote history was not overwritten.' }
    Write-Host 'Source pushed. GitHub Actions will validate and deploy Pages. Wait for the workflow to pass.'
} finally { Pop-Location }
