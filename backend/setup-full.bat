@echo off
setlocal enabledelayedexpansion

echo.
echo ======================================================
echo         AI Creator Studio - Full Environment Setup
echo ======================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Create virtual environment if needed
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install/update dependencies
echo [INFO] Installing Python dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM Check Ollama
echo.
echo [INFO] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama is not installed or not in PATH.
    echo [INFO] Installing Ollama is recommended. Visit: https://ollama.ai
    choice /C YN /D N /T 5 /M "Continue without Ollama?"
    if !errorlevel! equ 2 (
        pause
        exit /b 0
    )
) else (
    echo [SUCCESS] Ollama detected
    
    REM Check if Mistral model is available
    ollama list 2>nul | find "mistral" >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [INFO] Pulling Mistral model (this may take a few minutes)...
        ollama pull mistral
    ) else (
        echo [SUCCESS] Mistral model found
    )
)

REM Environment setup
if not exist .env (
    echo [INFO] Creating .env file (please configure your API keys)...
    (
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo FLASK_RUN_HOST=0.0.0.0
        echo FLASK_RUN_PORT=5000
        echo GEMINI_API_KEY=your-api-key-here
        echo MONGO_URI=mongodb://localhost:27017/ai_studio
        echo SECRET_KEY=your-secret-key-here
    ) > .env
    echo [ACTION REQUIRED] Update .env with your credentials
)

echo.
echo ======================================================
echo         ✓ Environment Setup Complete!
echo ======================================================
echo.
echo Next steps:
echo 1. Update .env with your GEMINI_API_KEY and MONGO_URI
echo 2. Start Ollama: ollama serve (in another terminal)
echo 3. Run the backend: python run.py
echo.
pause
