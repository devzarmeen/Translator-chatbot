@echo off
REM Virtual Environment Setup Script for AI Translator Chatbot (Windows)
REM This script creates and configures a Python virtual environment for the project.

setlocal enabledelayedexpansion

REM Project root directory
set "PROJECT_ROOT=%~dp0"
set "VENV_NAME=venv"
set "VENV_PATH=%PROJECT_ROOT%%VENV_NAME%"
set "REQUIREMENTS_FILE=%PROJECT_ROOT%requirements.txt"

echo ============================================================
echo AI TRANSLATOR CHATBOT - Virtual Environment Setup
echo ============================================================
echo Project root: %PROJECT_ROOT%
echo.

REM Step 1: Check Python version
echo ============================================================
echo STEP 1: Checking Python Version
echo ============================================================
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo Python version check passed
echo.

REM Step 2: Create virtual environment
echo ============================================================
echo STEP 2: Creating Virtual Environment
echo ============================================================
if exist "%VENV_PATH%" (
    echo Virtual environment already exists at: %VENV_PATH%
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q "%VENV_PATH%"
    ) else (
        echo Using existing virtual environment.
        goto :verify
    )
)

echo Creating virtual environment at: %VENV_PATH%
python -m venv "%VENV_PATH%"
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    exit /b 1
)
echo Virtual environment created successfully!
echo.

:verify
REM Step 3: Verify virtual environment
echo ============================================================
echo STEP 3: Verifying Virtual Environment
echo ============================================================
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo ERROR: Python executable not found in virtual environment!
    exit /b 1
)
echo Virtual environment verified successfully!
echo    Python: %VENV_PATH%\Scripts\python.exe
echo.

REM Step 4: Upgrade pip
echo ============================================================
echo STEP 4: Upgrading pip
echo ============================================================
"%VENV_PATH%\Scripts\python.exe" -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo Warning: Failed to upgrade pip, continuing...
) else (
    echo pip upgraded successfully!
)
echo.

REM Step 5: Install requirements
echo ============================================================
echo STEP 5: Installing Required Packages
echo ============================================================
if not exist "%REQUIREMENTS_FILE%" (
    echo ERROR: requirements.txt not found at: %REQUIREMENTS_FILE%
    exit /b 1
)

echo Installing packages from: %REQUIREMENTS_FILE%
echo This may take a few minutes...
"%VENV_PATH%\Scripts\pip.exe" install -r "%REQUIREMENTS_FILE%"
if errorlevel 1 (
    echo ERROR: Failed to install packages!
    echo.
    echo Troubleshooting tips:
    echo 1. Check your internet connection
    echo 2. Try upgrading pip: python -m pip install --upgrade pip
    echo 3. For pyaudio, you may need to install it separately:
    echo    pip install pipwin
    echo    pipwin install pyaudio
    exit /b 1
)
echo All packages installed successfully!
echo.

REM Step 6: Print instructions
echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo To activate the virtual environment:
echo    PowerShell: %VENV_PATH%\Scripts\Activate.ps1
echo    Command Prompt: %VENV_PATH%\Scripts\activate.bat
echo    Or simply: .\venv\Scripts\activate
echo.
echo To deactivate the virtual environment:
echo    deactivate
echo.
echo To run the application:
echo    python run.py
echo    OR
echo    streamlit run frontend/app.py
echo.
echo To verify virtual environment is active:
echo    where python  # Should show venv path
echo    pip list      # Should show installed packages
echo.
echo ============================================================

endlocal
