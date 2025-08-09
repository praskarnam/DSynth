#!/usr/bin/env python3
"""
DSynth - Synthetic Data Generation Tool
Startup script for easy application launching with virtual environment
"""

import argparse
import sys
import os
import subprocess
import venv
from pathlib import Path

def create_venv(venv_path):
    """Create a virtual environment if it doesn't exist"""
    if not venv_path.exists():
        print(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)
        return True
    return False

def install_requirements(venv_path, requirements_file):
    """Install requirements in the virtual environment"""
    pip_path = venv_path / "bin" / "pip"
    if os.name == "nt":  # Windows
        pip_path = venv_path / "Scripts" / "pip.exe"
    
    if not pip_path.exists():
        print("Error: pip not found in virtual environment")
        return False
    
    print("Installing dependencies...")
    try:
        subprocess.run([str(pip_path), "install", "-r", requirements_file], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def run_in_venv(venv_path, host, port, reload, workers):
    """Run the application using the virtual environment's Python"""
    python_path = venv_path / "bin" / "python"
    if os.name == "nt":  # Windows
        python_path = venv_path / "Scripts" / "python.exe"
    
    if not python_path.exists():
        print("Error: Python not found in virtual environment")
        return False
    
    # Change to the project directory and run
    os.chdir(Path(__file__).parent)
    
    try:
        subprocess.run([
            str(python_path), "-m", "uvicorn", "main:app",
            "--host", host, "--port", str(port),
            "--reload" if reload else "",
            "--workers", str(workers)
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        return False
    except KeyboardInterrupt:
        print("\nShutting down DSynth...")
        return True

def main():
    parser = argparse.ArgumentParser(description='DSynth - Synthetic Data Generation Tool')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--workers', type=int, default=1, help='Number of worker processes (default: 1)')
    parser.add_argument('--venv-path', default='venv', help='Virtual environment path (default: venv)')
    
    args = parser.parse_args()
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("Error: main.py not found. Please run this script from the DSynth project directory.")
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("Error: requirements.txt not found. Please run this script from the DSynth project directory.")
        sys.exit(1)
    
    venv_path = Path(args.venv_path)
    
    # Create virtual environment if it doesn't exist
    is_new_venv = create_venv(venv_path)
    
    # Install requirements
    if not install_requirements(venv_path, 'requirements.txt'):
        print("Failed to install requirements. Exiting.")
        sys.exit(1)
    
    print(f"Starting DSynth on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    # Run the application in the virtual environment
    if not run_in_venv(venv_path, args.host, args.port, args.reload, args.workers):
        sys.exit(1)

if __name__ == "__main__":
    main() 