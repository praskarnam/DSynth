# DSynth - Synthetic Data Generator

A powerful tool for generating synthetic data from JSON and XML schemas with custom data types and MVEL expressions.

## Features

- **Schema Management**: Support for JSON and XML schemas
- **Custom Data Types**: Create custom data types using MVEL expressions
- **Smart Field Mapping**: Automatic field detection from schema definitions
- **Data Generation**: Generate synthetic data with customizable record counts
- **Live Reload**: Development server with automatic restart on file changes

## Development Setup

### Prerequisites

- Python 3.7+
- pip or pip3

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DSynth
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running with Live Reload

The application includes live reload functionality for development. Any changes to Python, HTML, JavaScript, or CSS files will automatically restart the server.

#### Option 1: Using the development script (Recommended)
```bash
# Unix/macOS
./dev.sh

# Windows
dev.bat
```

#### Option 2: Using Python directly
```bash
python3 dev.py
```

#### Option 3: Using the main script
```bash
python3 main.py
```

### Live Reload Features

- **Automatic Restart**: Server restarts when Python files change
- **File Watching**: Monitors `.py`, `.html`, `.js`, and `.css` files
- **Smart Exclusions**: Ignores `__pycache__`, virtual environments, and compiled files
- **Real-time Logging**: Shows server status and reload events

### Development Workflow

1. Start the development server with live reload
2. Make changes to your code
3. Save the file - the server will automatically restart
4. View changes immediately in your browser

## API Endpoints

- `GET /` - Main application interface
- `GET /api/schemas` - List all schemas
- `POST /api/schemas` - Create a new schema
- `GET /api/schemas/{id}/elements` - Get schema elements for field mapping
- `GET /api/custom-types` - List all custom data types
- `POST /api/schemas/{id}/generate` - Generate synthetic data

## Schema Editor Features

The schema editor now includes intelligent field mapping:

- **Prepopulated Field Names**: Field names are automatically populated from schema elements
- **Auto-population**: Selecting a schema element automatically fills in data type, required status, and description
- **Schema Validation**: Ensures field configurations match the actual schema structure
- **Smart Type Mapping**: Automatically maps schema types to application data types

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with live reload
5. Submit a pull request

## License

[Add your license information here]
