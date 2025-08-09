#!/bin/bash

# DSynth - Synthetic Data Generation Tool
# Startup script for Unix-like systems with virtual environment

set -e  # Exit on any error

echo "Starting DSynth..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the DSynth project directory."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Please run this script from the DSynth project directory."
    exit 1
fi

# Virtual environment path
VENV_PATH="venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting server on http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo "Virtual environment: $VENV_PATH"

# Run the application
python main.py 