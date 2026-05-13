@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo      AI Creator Studio - Backend Launcher
echo ====================================================
echo.

REM Check virtual environment
if not exist venv (
    echo [ERROR] Virtual environment not found.
    echo [INFO] Please run setup-full.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check .env file
if not exist .env (
    echo [WARNING] .env file not found. Using defaults.
)

REM Check Ollama
echo Checking Ollama service...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Ollama is offline. Starting Ollama service...
    start "" ollama serve
    timeout /t 3 /nobreak
) else (
    echo [SUCCESS] Ollama is online
)

REM Verify Mistral model
ollama list 2>nul | find "mistral" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Mistral model not found. Pulling...
    ollama pull mistral
)

echo.
echo ====================================================
echo   ✓ All services ready. Starting backend...
echo ====================================================
echo.
echo Backend will run on: http://localhost:5000
echo Health check: http://localhost:5000/api/v1/health
echo.

REM Run Flask app
python run.py

pause
