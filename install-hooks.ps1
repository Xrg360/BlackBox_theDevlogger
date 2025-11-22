# Install Blackbox Git Hooks (PowerShell)
# This script installs hooks to automatically track git activity

Write-Host "Installing Blackbox Git Hooks..." -ForegroundColor Cyan

# Check if we're in a git repository
if (-not (Test-Path .git)) {
    Write-Host "Error: Not in a git repository" -ForegroundColor Red
    Write-Host "Please run this script from the root of your git repository"
    exit 1
}

# Get the script directory (where hooks are stored)
$SCRIPT_DIR = Split-Path -Parent $PSCommandPath
$HOOKS_DIR = Join-Path $SCRIPT_DIR "hooks"
$GIT_HOOKS_DIR = ".git\hooks"

# Check if hooks directory exists
if (-not (Test-Path $HOOKS_DIR)) {
    Write-Host "Error: hooks directory not found at $HOOKS_DIR" -ForegroundColor Red
    exit 1
}

# Install each hook
$hooks = @("post-commit", "pre-commit", "post-checkout")

foreach ($hook in $hooks) {
    $SOURCE = Join-Path $HOOKS_DIR $hook
    $TARGET = Join-Path $GIT_HOOKS_DIR $hook
    
    if (Test-Path $SOURCE) {
        Write-Host "Installing $hook..." -ForegroundColor Yellow
        Copy-Item $SOURCE $TARGET -Force
        Write-Host "  $hook installed" -ForegroundColor Green
    }
    else {
        Write-Host "  $hook not found, skipping" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Blackbox hooks installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "What happens now:" -ForegroundColor Cyan
Write-Host "  - Every commit will be logged as an event"
Write-Host "  - Branch switches will be tracked"
Write-Host "  - Users and projects are auto-created from git config"
Write-Host ""

try {
    $gitUser = git config user.name 2>$null
    $projectName = Split-Path -Leaf (git rev-parse --show-toplevel 2>$null)
    Write-Host "Your git username: $gitUser" -ForegroundColor Yellow
    Write-Host "Your project name: $projectName" -ForegroundColor Yellow
}
catch {
    Write-Host "Could not read git config" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Tip: Make sure the Blackbox API server is running:" -ForegroundColor Cyan
Write-Host "  python -m uvicorn backend.main:app --reload" -ForegroundColor White
