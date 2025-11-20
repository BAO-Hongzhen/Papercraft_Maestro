@echo off
REM ========================================================================
REM Syntax Roulette - Windows Setup Script
REM This script sets up the virtual environment and installs dependencies
REM ========================================================================

echo.
echo ========================================================================
echo   Syntax Roulette - Setup for Windows
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo [ERROR] Python 3.8 or higher is required!
    echo Please upgrade your Python installation.
    echo.
    pause
    exit /b 1
)

echo [2/5] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q .venv
)

python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    echo.
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo.

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [5/5] Installing dependencies...
echo This may take several minutes on first run...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Troubleshooting tips:
    echo - Check your internet connection
    echo - Try running as Administrator
    echo - Check if requirements.txt exists
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   Setup completed successfully!
echo ========================================================================
echo.
echo Next steps:
echo   1. Run "run_windows.bat" to start the application
echo   2. Wait for the browser to open automatically
echo   3. Start creating amazing images!
echo.
echo Note: First run will download AI models (~4GB, one-time only)
echo This may take 5-15 minutes depending on your internet connection.
echo.
echo ========================================================================
pause

