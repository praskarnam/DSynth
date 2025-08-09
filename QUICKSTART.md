# Quick Start Guide

Get DSynth up and running in 3 simple steps! The scripts automatically handle virtual environment creation and dependency installation.

## Step 1: Prerequisites

Make sure you have Python 3.7+ installed:
```bash
python3 --version
# or
python --version
```

## Step 2: Start the Application

Choose one of these methods based on your platform:

**Option A: Python script (cross-platform, recommended)**
```bash
python run.py
```

**Option B: Shell script (Unix/Mac/Linux)**
```bash
./run.sh
```

**Option C: Windows batch file**
```cmd
run.bat
```

**Option D: Direct execution (manual setup)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Unix/Mac)
source venv/bin/activate
# OR (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## What Happens Automatically

The startup scripts will:
1. ✅ Check for Python installation
2. ✅ Create a virtual environment (`venv/`)
3. ✅ Install/upgrade pip
4. ✅ Install all required dependencies
5. ✅ Start the DSynth application

## Step 3: Open Your Browser

Navigate to: `http://localhost:8000`

## What You'll See

- **Schemas Tab**: Upload and manage JSON/XML schemas
- **Custom Types Tab**: Create custom data generation rules using expressions
- **API Documentation**: Available at `http://localhost:8000/docs`

## First Steps

1. **Create a Schema**: Upload a JSON or XML file
2. **Configure Fields**: Map schema fields to data types
3. **Generate Data**: Set seed count and generate test data
4. **Access via API**: Use the REST endpoints for programmatic access

## Example: Quick Test

1. Start the application using any of the scripts above
2. Go to the Schemas tab
3. Click "Create New Schema"
4. Choose "JSON" as schema type
5. Paste this sample schema:
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "email": {"type": "string"},
    "age": {"type": "integer"}
  }
}
```
6. Configure fields:
   - name → "name" type
   - email → "email" type  
   - age → "integer" type (min: 18, max: 65)
7. Set seed count to 100
8. Save and generate data!

## Virtual Environment

- **Location**: `venv/` directory in your project folder
- **Automatic**: Created and activated by the startup scripts
- **Dependencies**: All packages are installed in the virtual environment
- **Clean**: Your system Python remains unaffected

## Troubleshooting

**"Permission denied" on Unix/Mac:**
```bash
chmod +x run.sh
```

**Virtual environment issues:**
```bash
# Remove and recreate
rm -rf venv/
python run.py
```

**Port already in use:**
```bash
python run.py --port 8001
```

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- API documentation is available at `/docs` when the server is running
- Open an issue on the project repository for support 