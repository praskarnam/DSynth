@echo off
REM DSynth - Synthetic Data Generation Tool
REM Startup script for Windows with virtual environment

echo Starting DSynth...

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found. Please run this script from the DSynth project directory.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo Error: requirements.txt not found. Please run this script from the DSynth project directory.
    pause
    exit /b 1
)

REM Virtual environment path
set VENV_PATH=venv

REM Create virtual environment if it doesn't exist
if not exist "%VENV_PATH%" (
    echo Creating virtual environment at %VENV_PATH%...
    python -m venv "%VENV_PATH%"
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo Starting server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo Virtual environment: %VENV_PATH%

REM Run the application
python main.py

pause 