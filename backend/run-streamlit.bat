@echo off
setlocal enabledelayedexpansion

echo.
echo ======================================================
echo  AI Creator Studio - Streamlit + Ollama Launcher
echo ======================================================
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
echo ======================================================
echo   ✓ Services Ready. Starting Streamlit...
echo ======================================================
echo.
echo Streamlit will open at: http://localhost:8501
echo.
echo Press Ctrl+C in this terminal to stop Streamlit
echo (Ollama will keep running in the background)
echo.

REM Run Streamlit
streamlit run app_ollama_integrated.py

pause
