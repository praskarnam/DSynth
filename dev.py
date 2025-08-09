#!/usr/bin/env python3
"""
Development server with enhanced live reload functionality
"""
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."],
        reload_includes=["*.py", "*.html", "*.js", "*.css"],
        reload_excludes=["__pycache__", "*.pyc", "venv/*", "test_venv/*"],
        log_level="info",
        access_log=True
    ) 