@echo off
title RecallBox Launcher
echo ======================================================================
echo                     Starting RecallBox Development Servers
echo ======================================================================
echo.
echo Launching Backend (FastAPI on port 8000)...
start "RecallBox Backend (FastAPI - Port 8000)" cmd /k "cd /d "%~dp0backend" && .\venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

echo Launching Frontend (React + Vite on port 5173)...
start "RecallBox Frontend (Vite - Port 5173)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ======================================================================
echo  Both servers have been launched in separate windows:
echo    - Frontend UI:    http://localhost:5173
echo    - Backend API:    http://localhost:8000
echo    - API Docs:       http://localhost:8000/docs
echo    - API Health:     http://localhost:8000/api/v1/health
echo ======================================================================
echo.
echo To stop a server, close its respective terminal window or press Ctrl+C.
echo.
pause
