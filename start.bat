@echo off
echo ================================================
echo  WebRTC Backend - Production Startup
echo ================================================
echo.

echo [1/2] Running database migrations...
alembic upgrade head

echo.
echo [2/2] Starting Uvicorn server...
uvicorn app.main:app --host 0.0.0.0 --port %PORT:~8000% --workers 4

pause