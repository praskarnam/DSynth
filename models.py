from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

class DataTypeEnum(str, Enum):
    """Built-in data types"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    EMAIL = "email"
    PHONE = "phone"
    NAME = "name"
    ADDRESS = "address"
    CITY = "city"
    COUNTRY = "country"
    ZIPCODE = "zipcode"
    COMPANY = "company"
    JOB = "job"
    URL = "url"
    IP_ADDRESS = "ip_address"
    UUID = "uuid"
    CUSTOM = "custom"

class FieldConfig(BaseModel):
    """Configuration for a single field"""
    name: str
    data_type: Union[DataTypeEnum, str]  # Can be built-in type or custom type name
    required: bool = True
    nullable: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    mvel_expression: Optional[str] = None
    custom_config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class SchemaConfig(BaseModel):
    """Schema configuration for data generation"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    schema_type: str = "json"  # json, xml
    schema_content: str  # The actual schema content
    fields: List[FieldConfig]
    seed_count: int = 100  # Default number of records to generate
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True

class CustomDataType(BaseModel):
    """Custom data type definition"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    mvel_expression: str
    validation_rules: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    test_result: Optional[Dict[str, Any]] = None
    is_active: bool = True

class DataGenerationRequest(BaseModel):
    """Request for data generation"""
    count: int = Field(1, ge=1, le=10000)
    seed: Optional[int] = None
    custom_params: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    data: List[Dict[str, Any]]
    page: int
    size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

class DataType(BaseModel):
    """Data type information"""
    name: str
    type: str
    description: str
    examples: List[str]
    configurable: bool 