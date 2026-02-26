@echo off
REM ================================================
REM AutoGen Framework - Interactive Mode Launcher
REM ================================================

echo.
echo =====================================
echo  AutoGen Framework Launcher
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Creating .env from .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo Created .env file. Please edit it with your API credentials.
    ) else (
        echo Error: .env.example not found!
        pause
        exit /b 1
    )
)

REM Check if required dependencies are installed
echo Checking dependencies...
pip list | find "pyautogen" >nul
if %errorlevel% neq 0 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the framework
echo.
echo Starting AutoGen Framework...
echo.
python main.py

REM Pause if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Error occurred during execution. Press any key to exit...
    pause
    exit /b 1
)
