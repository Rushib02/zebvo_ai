@echo off
setlocal

REM Start Ollama in background and save PID
echo Starting Ollama service...

REM Check if Ollama is already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Ollama is already running.
    echo.
    echo Verifying models...
    ollama list
    echo.
    echo You can now run the backend: python run.py
) else (
    echo Launching Ollama server...
    start "" ollama serve
    echo.
    echo Waiting for Ollama to initialize...
    timeout /t 3 /nobreak
    echo.
    echo Checking Ollama status...
    :retry_loop
    ollama list >nul 2>&1
    if %errorlevel% neq 0 (
        echo Ollama is still starting up, please wait...
        timeout /t 2 /nobreak
        goto retry_loop
    )
    echo.
    echo ✓ Ollama is running!
    ollama list
    echo.
    echo You can now run the backend in another terminal: python run.py
    echo.
    echo Note: Close this window when you're done, and Ollama will continue running in the background.
)

pause
