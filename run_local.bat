@echo off
title Taskify Launchpad
cd "%~dp0"

:: Check if python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your system PATH.
    echo Please install Python and try again.
    pause
    exit /b
)

:: Run the python wrapper launcher
python run.py
pause
