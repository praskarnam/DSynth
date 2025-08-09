@echo off
echo 🚀 Starting DSynth development server with live reload...
echo 📁 Watching for changes in: .
echo 🌐 Server will be available at: http://localhost:8000
echo 🔄 Live reload is enabled - changes will restart the server automatically
echo 🐍 Activating virtual environment...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    if %errorlevel% neq 0 (
        python3 -m venv venv
        if %errorlevel% neq 0 (
            echo ❌ Error: Failed to create virtual environment. Please install Python 3.7+
            pause
            exit /b 1
        )
    )
    echo ✅ Virtual environment created successfully!
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements if they exist
if exist "requirements.txt" (
    echo 📦 Installing/updating requirements...
    pip install -r requirements.txt
) else (
    echo ⚠️  No requirements.txt found. Installing basic dependencies...
    pip install fastapi uvicorn jinja2 pydantic faker
)

echo.
echo ✅ Virtual environment activated and dependencies installed!
echo 🚀 Starting development server...
echo.

REM Start the development server
python dev.py 