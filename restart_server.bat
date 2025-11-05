@echo off
echo.
echo ================================================
echo  WebRTC App - Fresh Database Restart
echo ================================================
echo.

cd backend

echo [1/3] Stopping any running servers...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] Deleting old database...
if exist test.db (
    del /F /Q test.db
    echo     Database deleted successfully!
) else (
    echo     No existing database found
)

echo [3/3] Starting server with fresh database...
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
