from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List, Any, Optional
import json
import uuid
from datetime import datetime
import random

from models import (
    SchemaConfig, DataType, CustomDataType, 
    DataGenerationRequest, PaginatedResponse
)
from data_generator import DataGenerator
from schema_parser import SchemaParser
from storage import Storage

app = FastAPI(title="DSynth - Synthetic Data Generator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize components
storage = Storage()
data_generator = DataGenerator()
schema_parser = SchemaParser()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with portal interface"""
    schemas = storage.get_all_schemas()
    custom_types = storage.get_all_custom_types()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "schemas": schemas, "custom_types": custom_types}
    )

@app.post("/api/schemas")
async def create_schema(schema: SchemaConfig):
    """Create a new schema configuration"""
    schema.id = str(uuid.uuid4())
    schema.created_at = datetime.now()
    schema.updated_at = datetime.now()
    
    # Validate schema
    try:
        schema_parser.validate_schema(schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    storage.save_schema(schema)
    return {"message": "Schema created successfully", "id": schema.id}

@app.get("/api/schemas")
async def get_schemas():
    """Get all schema configurations"""
    return storage.get_all_schemas()

@app.get("/api/schemas/{schema_id}")
async def get_schema(schema_id: str):
    """Get a specific schema configuration"""
    schema = storage.get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema

@app.get("/api/schemas/{schema_id}/elements")
async def get_schema_elements(schema_id: str):
    """Get schema elements that can be mapped to fields"""
    schema = storage.get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    
    try:
        # Extract field information from the schema content
        elements = schema_parser.extract_field_info(schema.schema_content, schema.schema_type)
        return {"elements": elements}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing schema: {str(e)}")

@app.put("/api/schemas/{schema_id}")
async def update_schema(schema_id: str, schema: SchemaConfig):
    """Update a schema configuration"""
    existing_schema = storage.get_schema(schema_id)
    if not existing_schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    
    schema.id = schema_id
    schema.updated_at = datetime.now()
    
    # Validate schema
    try:
        schema_parser.validate_schema(schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    storage.save_schema(schema)
    return {"message": "Schema updated successfully"}

@app.delete("/api/schemas/{schema_id}")
async def delete_schema(schema_id: str):
    """Delete a schema configuration"""
    if not storage.get_schema(schema_id):
        raise HTTPException(status_code=404, detail="Schema not found")
    
    storage.delete_schema(schema_id)
    return {"message": "Schema deleted successfully"}

@app.post("/api/schemas/{schema_id}/generate")
async def generate_data(schema_id: str, request: DataGenerationRequest):
    """Generate data based on schema configuration"""
    schema = storage.get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    
    try:
        data = data_generator.generate_data(schema, request.count)
        return {"data": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/data/{schema_id}")
async def get_data(
    schema_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    seed: Optional[int] = Query(None)
):
    """Get paginated data for a schema"""
    schema = storage.get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    
    try:
        # Set seed if provided
        if seed is not None:
            random.seed(seed)
            data_generator.set_seed(seed)
        
        # Generate data
        all_data = data_generator.generate_data(schema, schema.seed_count)
        
        # Paginate
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_data = all_data[start_idx:end_idx]
        
        total_pages = (len(all_data) + size - 1) // size
        
        return PaginatedResponse(
            data=paginated_data,
            page=page,
            size=size,
            total=len(all_data),
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/custom-types")
async def create_custom_type(custom_type: CustomDataType):
    """Create a custom data type"""
    custom_type.id = str(uuid.uuid4())
    custom_type.created_at = datetime.now()
    
    # Test the custom type
    try:
        test_data = data_generator.test_custom_type(custom_type)
        custom_type.test_result = {"success": True, "sample_data": test_data}
    except Exception as e:
        custom_type.test_result = {"success": False, "error": str(e)}
    
    storage.save_custom_type(custom_type)
    return {"message": "Custom type created successfully", "id": custom_type.id}

@app.get("/api/custom-types")
async def get_custom_types():
    """Get all custom data types"""
    return storage.get_all_custom_types()

@app.get("/api/custom-types/{type_id}")
async def get_custom_type(type_id: str):
    """Get a specific custom data type"""
    custom_type = storage.get_custom_type(type_id)
    if not custom_type:
        raise HTTPException(status_code=404, detail="Custom type not found")
    return custom_type

@app.put("/api/custom-types/{type_id}")
async def update_custom_type(type_id: str, custom_type: CustomDataType):
    """Update a custom data type"""
    existing_type = storage.get_custom_type(type_id)
    if not existing_type:
        raise HTTPException(status_code=404, detail="Custom type not found")
    
    custom_type.id = type_id
    custom_type.created_at = existing_type.created_at
    
    # Test the custom type
    try:
        test_data = data_generator.test_custom_type(custom_type)
        custom_type.test_result = {"success": True, "sample_data": test_data}
    except Exception as e:
        custom_type.test_result = {"success": False, "error": str(e)}
    
    storage.save_custom_type(custom_type)
    return {"message": "Custom type updated successfully"}

@app.delete("/api/custom-types/{type_id}")
async def delete_custom_type(type_id: str):
    """Delete a custom data type"""
    if not storage.get_custom_type(type_id):
        raise HTTPException(status_code=404, detail="Custom type not found")
    
    storage.delete_custom_type(type_id)
    return {"message": "Custom type deleted successfully"}

@app.post("/api/custom-types/{type_id}/test")
async def test_custom_type(type_id: str):
    """Test a custom data type"""
    custom_type = storage.get_custom_type(type_id)
    if not custom_type:
        raise HTTPException(status_code=404, detail="Custom type not found")
    
    try:
        test_data = data_generator.test_custom_type(custom_type)
        return {"success": True, "sample_data": test_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/default-types")
async def get_default_types():
    """Get all default data types"""
    return data_generator.get_default_types()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, reload_dirs=["."]) 