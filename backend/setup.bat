@echo off
setlocal

echo ==================================================
echo AI Creator Studio - Setup Script (Windows)
echo ==================================================

:: Validate Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    exit /b 1
)

:: Validate Pip installation
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Pip is not installed or not in PATH.
    exit /b 1
)

:: Create Virtual Environment
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate Virtual Environment
call venv\Scripts\activate

:: Install Dependencies
echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Create necessary folders
echo [INFO] Ensuring folder structure exists...
if not exist uploads mkdir uploads
if not exist generated mkdir generated
if not exist logs mkdir logs

:: Initialize .env if it doesn't exist
if not exist .env (
    echo [INFO] Initializing .env from .env.example...
    copy .env.example .env
)

echo ==================================================
echo Setup Complete!
echo Starting AI Creator Studio...
echo ==================================================

streamlit run app.py

pause
