# ==============================================================================
# RecallBox - Unified PowerShell Startup Script
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "               Starting RecallBox Development Servers" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$rootDir = $PSScriptRoot

# Launch Backend in new window
Write-Host "`nLaunching Backend (FastAPI on port 8000)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k cd /d `"$rootDir\backend`" && .\venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

# Launch Frontend in new window
Write-Host "Launching Frontend (React + Vite on port 5173)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k cd /d `"$rootDir\frontend`" && npm run dev"

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host " Both servers have been launched in separate windows:" -ForegroundColor Green
Write-Host "   - Frontend UI:    http://localhost:5173" -ForegroundColor Green
Write-Host "   - Backend API:    http://localhost:8000" -ForegroundColor Green
Write-Host "   - API Docs:       http://localhost:8000/docs" -ForegroundColor Green
Write-Host "   - API Health:     http://localhost:8000/api/v1/health" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "`nTo stop a server, close its terminal window or press Ctrl+C inside it." -ForegroundColor Gray
