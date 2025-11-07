# Start MongoDB Service
Write-Host "Attempting to start MongoDB service..." -ForegroundColor Cyan

try {
    # Try to start as service first
    Start-Service -Name "MongoDB" -ErrorAction Stop
    Write-Host "✓ MongoDB service started successfully!" -ForegroundColor Green
    Write-Host "MongoDB is now running on mongodb://localhost:27017/" -ForegroundColor Green
}
catch {
    Write-Host "✗ Could not start MongoDB service (requires admin privileges)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Start MongoDB manually" -ForegroundColor Cyan
    Write-Host "1. Open MongoDB Compass" -ForegroundColor White
    Write-Host "2. Click 'Connect' with connection string: mongodb://localhost:27017/" -ForegroundColor White
    Write-Host "3. Or run this PowerShell as Administrator and try again" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
