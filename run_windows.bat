@echo off
REM ========================================================================
REM Syntax Roulette - Windows Run Script
REM Starts the application in the virtual environment
REM ========================================================================

echo.
echo ========================================================================
echo   Syntax Roulette - Starting Application
echo ========================================================================
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run "setup_windows.bat" first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/2] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo Please run "setup_windows.bat" again.
    echo.
    pause
    exit /b 1
)
echo.

REM Check if main.py exists
if not exist main.py (
    echo [ERROR] main.py not found!
    echo Make sure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

echo [2/2] Launching Syntax Roulette...
echo.
echo ========================================================================
echo   Application is starting...
echo   Please wait, this may take a moment...
echo.
echo   The web interface will open automatically in your browser.
echo   If it doesn't, open: http://localhost:7860
echo.
echo   To stop the application, press Ctrl+C or close this window.
echo ========================================================================
echo.

REM Run the application
python main.py

REM If we get here, the application has stopped
echo.
echo ========================================================================
echo   Application stopped.
echo ========================================================================
pause

