import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from models import SchemaConfig, CustomDataType

class Storage:
    """Handles persistence of schemas and custom data types"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.schemas_file = os.path.join(data_dir, "schemas.json")
        self.custom_types_file = os.path.join(data_dir, "custom_types.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize storage files if they don't exist
        self._init_storage_files()
    
    def _init_storage_files(self):
        """Initialize storage files with empty data if they don't exist"""
        if not os.path.exists(self.schemas_file):
            self._save_json_file(self.schemas_file, [])
        
        if not os.path.exists(self.custom_types_file):
            self._save_json_file(self.custom_types_file, [])
    
    def _load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json_file(self, file_path: str, data: List[Dict[str, Any]]):
        """Save data to a JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=self._json_serializer)
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for datetime objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _json_deserializer(self, data: Dict[str, Any], model_class):
        """Custom JSON deserializer for datetime objects"""
        if 'created_at' in data and data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return model_class(**data)
    
    # Schema management methods
    def save_schema(self, schema: SchemaConfig):
        """Save a schema configuration"""
        schemas = self._load_json_file(self.schemas_file)
        
        # Check if schema already exists
        existing_index = None
        for i, existing_schema in enumerate(schemas):
            if existing_schema.get('id') == schema.id:
                existing_index = i
                break
        
        if existing_index is not None:
            # Update existing schema
            schemas[existing_index] = schema.dict()
        else:
            # Add new schema
            schemas.append(schema.dict())
        
        self._save_json_file(self.schemas_file, schemas)
    
    def get_schema(self, schema_id: str) -> Optional[SchemaConfig]:
        """Get a schema configuration by ID"""
        schemas = self._load_json_file(self.schemas_file)
        
        for schema_data in schemas:
            if schema_data.get('id') == schema_id:
                return self._json_deserializer(schema_data, SchemaConfig)
        
        return None
    
    def get_all_schemas(self) -> List[SchemaConfig]:
        """Get all schema configurations"""
        schemas = self._load_json_file(self.schemas_file)
        return [self._json_deserializer(schema_data, SchemaConfig) for schema_data in schemas]
    
    def delete_schema(self, schema_id: str):
        """Delete a schema configuration"""
        schemas = self._load_json_file(self.schemas_file)
        schemas = [s for s in schemas if s.get('id') != schema_id]
        self._save_json_file(self.schemas_file, schemas)
    
    def search_schemas(self, query: str) -> List[SchemaConfig]:
        """Search schemas by name or description"""
        schemas = self.get_all_schemas()
        query_lower = query.lower()
        
        return [
            schema for schema in schemas
            if (query_lower in schema.name.lower() or 
                (schema.description and query_lower in schema.description.lower()))
        ]
    
    # Custom data type management methods
    def save_custom_type(self, custom_type: CustomDataType):
        """Save a custom data type"""
        custom_types = self._load_json_file(self.custom_types_file)
        
        # Check if custom type already exists
        existing_index = None
        for i, existing_type in enumerate(custom_types):
            if existing_type.get('id') == custom_type.id:
                existing_index = i
                break
        
        if existing_index is not None:
            # Update existing custom type
            custom_types[existing_index] = custom_type.dict()
        else:
            # Add new custom type
            custom_types.append(custom_type.dict())
        
        self._save_json_file(self.custom_types_file, custom_types)
    
    def get_custom_type(self, type_id: str) -> Optional[CustomDataType]:
        """Get a custom data type by ID"""
        custom_types = self._load_json_file(self.custom_types_file)
        
        for type_data in custom_types:
            if type_data.get('id') == type_id:
                return self._json_deserializer(type_data, CustomDataType)
        
        return None
    
    def get_custom_type_by_name(self, type_name: str) -> Optional[CustomDataType]:
        """Get a custom data type by name"""
        custom_types = self._load_json_file(self.custom_types_file)
        
        for type_data in custom_types:
            if type_data.get('name') == type_name:
                return self._json_deserializer(type_data, CustomDataType)
        
        return None
    
    def get_all_custom_types(self) -> List[CustomDataType]:
        """Get all custom data types"""
        custom_types = self._load_json_file(self.custom_types_file)
        return [self._json_deserializer(type_data, CustomDataType) for type_data in custom_types]
    
    def delete_custom_type(self, type_id: str):
        """Delete a custom data type"""
        custom_types = self._load_json_file(self.custom_types_file)
        custom_types = [t for t in custom_types if t.get('id') != type_id]
        self._save_json_file(self.custom_types_file, custom_types)
    
    def search_custom_types(self, query: str) -> List[CustomDataType]:
        """Search custom types by name or description"""
        custom_types = self.get_all_custom_types()
        query_lower = query.lower()
        
        return [
            custom_type for custom_type in custom_types
            if (query_lower in custom_type.name.lower() or 
                (custom_type.description and query_lower in custom_type.description.lower()))
        ]
    
    # Utility methods
    def get_schema_count(self) -> int:
        """Get the total number of schemas"""
        schemas = self._load_json_file(self.schemas_file)
        return len(schemas)
    
    def get_custom_type_count(self) -> int:
        """Get the total number of custom types"""
        custom_types = self._load_json_file(self.custom_types_file)
        return len(custom_types)
    
    def backup_data(self, backup_dir: str = "backups"):
        """Create a backup of all data"""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Backup schemas
        schemas_backup = os.path.join(backup_dir, f"schemas_{timestamp}.json")
        if os.path.exists(self.schemas_file):
            import shutil
            shutil.copy2(self.schemas_file, schemas_backup)
        
        # Backup custom types
        custom_types_backup = os.path.join(backup_dir, f"custom_types_{timestamp}.json")
        if os.path.exists(self.custom_types_file):
            import shutil
            shutil.copy2(self.custom_types_file, custom_types_backup)
        
        return {
            "schemas_backup": schemas_backup,
            "custom_types_backup": custom_types_backup,
            "timestamp": timestamp
        }
    
    def restore_data(self, schemas_backup: str, custom_types_backup: str):
        """Restore data from backup files"""
        if os.path.exists(schemas_backup):
            import shutil
            shutil.copy2(schemas_backup, self.schemas_file)
        
        if os.path.exists(custom_types_backup):
            import shutil
            shutil.copy2(custom_types_backup, self.custom_types_file)
    
    def clear_all_data(self):
        """Clear all stored data (use with caution!)"""
        self._save_json_file(self.schemas_file, [])
        self._save_json_file(self.custom_types_file, [])
    
    def export_data(self, export_dir: str = "exports"):
        """Export all data to a directory"""
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export schemas
        schemas_export = os.path.join(export_dir, f"schemas_{timestamp}.json")
        schemas = self._load_json_file(self.schemas_file)
        with open(schemas_export, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, default=self._json_serializer)
        
        # Export custom types
        custom_types_export = os.path.join(export_dir, f"custom_types_{timestamp}.json")
        custom_types = self._load_json_file(self.custom_types_file)
        with open(custom_types_export, 'w', encoding='utf-8') as f:
            json.dump(custom_types, f, indent=2, default=self._json_serializer)
        
        return {
            "schemas_export": schemas_export,
            "custom_types_export": custom_types_export,
            "timestamp": timestamp
        } 