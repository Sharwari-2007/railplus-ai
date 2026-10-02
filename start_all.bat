@echo off
echo ========================================================
echo        Starting RailPulse AI (SIH26028)
echo ========================================================
echo.

echo Starting FastAPI Backend on port 8000...
start "RailPulse AI Backend" cmd /k "cd /d %~dp0backend && python main.py"

timeout /t 2 >nul

echo Starting Next.js Frontend on port 3000...
start "RailPulse AI Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 3 >nul

echo Opening browser at http://localhost:3000...
start http://localhost:3000

echo.
echo Both services are running!
echo Frontend: http://localhost:3000
echo Backend:  http://127.0.0.1:8000
echo ========================================================
