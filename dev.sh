#!/bin/bash

echo "🚀 Starting DSynth development server with live reload..."
echo "📁 Watching for changes in: ."
echo "🌐 Server will be available at: http://localhost:8000"
echo "🔄 Live reload is enabled - changes will restart the server automatically"
echo "🐍 Activating virtual environment..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created successfully!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "❌ Virtual environment is corrupted. Please delete 'venv' folder and run again."
    exit 1
fi

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "📦 Installing/updating requirements..."
    pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found. Installing basic dependencies..."
    pip install fastapi uvicorn jinja2 pydantic faker
fi

echo ""
echo "✅ Virtual environment activated and dependencies installed!"
echo "🚀 Starting development server..."
echo ""

# Check if Python is available in the virtual environment
if command -v python &> /dev/null; then
    python dev.py
else
    echo "❌ Error: Python not found in virtual environment"
    exit 1
fi 