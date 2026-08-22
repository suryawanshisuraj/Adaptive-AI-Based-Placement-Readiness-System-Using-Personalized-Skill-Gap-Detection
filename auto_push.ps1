# =============================================================
# auto_push.ps1 — One-click: Save changes → GitHub → Vercel
# Double-click this file or run: powershell -ExecutionPolicy Bypass -File auto_push.ps1
# =============================================================

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AUTO PUSH: GitHub + Vercel Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if there are any changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "[INFO] No changes to push. Everything is up to date!" -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

# Show what changed
Write-Host "[CHANGES DETECTED]" -ForegroundColor Yellow
git status --short
Write-Host ""

# Ask for commit message
$commitMsg = Read-Host "Enter commit message (or press Enter for auto-timestamp)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMsg = "update: auto-push at $timestamp"
}

Write-Host ""
Write-Host "[1/3] Staging all changes..." -ForegroundColor Yellow
git add .

Write-Host "[2/3] Committing: $commitMsg" -ForegroundColor Yellow
git commit -m $commitMsg

Write-Host "[3/3] Pushing to GitHub (Vercel will auto-deploy)..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS!" -ForegroundColor Green
    Write-Host "  GitHub: Updated" -ForegroundColor Green
    Write-Host "  Vercel: Auto-deploying now (~2 min)" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check your live site at Vercel dashboard!" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "[ERROR] Push failed. Check your internet connection." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
