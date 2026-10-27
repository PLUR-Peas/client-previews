param([string]$Message = 'Publish approved previews')
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & git rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0) { throw 'This folder must first be connected as its own Git repository.' }
    $repositoryRoot = (& git rev-parse --show-toplevel).Trim()
    if ((Resolve-Path -LiteralPath $repositoryRoot).Path -ne (Resolve-Path -LiteralPath $PSScriptRoot).Path) {
        throw 'Refusing to publish from a parent repository.'
    }
    $currentBranch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or !$currentBranch -or $currentBranch -eq 'main') {
        throw 'Create a feature branch first. Direct publishing from main is disabled.'
    }
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) { throw 'Index is not empty. Review or unstage existing changes first.' }
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the Git index.' }
    $prepareArgs = @('scripts/prepare.py')
    if (Test-Path -LiteralPath 'local-projects.json') { $prepareArgs += '--export' }
    & python @prepareArgs
    if ($LASTEXITCODE -ne 0) { throw 'Public file validation failed. Nothing staged.' }
    & python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Safety tests failed. Nothing staged.' }
    $policy = Get-Content -LiteralPath 'security/public-files.json' -Raw | ConvertFrom-Json
    $approvedPaths = @($policy.files | ForEach-Object { 'public/' + $_ })
    & git add -- @approvedPaths
    if ($LASTEXITCODE -ne 0) { throw 'Could not stage preview files.' }
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        & git commit -m $Message
        if ($LASTEXITCODE -ne 0) { throw 'Commit failed.' }
    } elseif ($LASTEXITCODE -ne 0) { throw 'Could not inspect staged changes.' }
    & git push -u origin $currentBranch
    if ($LASTEXITCODE -ne 0) { throw 'Push failed. Remote history was not overwritten.' }
    Write-Host 'Feature branch pushed. Open a pull request and wait for validate.'
    Write-Host 'Push/merge does not publish. Release the approved main SHA through Run workflow.'
} finally { Pop-Location }
