@echo off
echo Starting WebRTC Communication App...
echo Make sure you have installed the required dependencies:
echo pip install -r requirements.txt
echo.
echo Starting the backend server...
cd /d "%~dp0"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload