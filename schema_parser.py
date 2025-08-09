import json
import re
from typing import List, Dict, Any, Optional
from models import SchemaConfig, FieldConfig

# Try to import lxml first, fallback to defusedxml for Python 3.13+
try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    try:
        from defusedxml import ElementTree as ET
        LXML_AVAILABLE = False
    except ImportError:
        import xml.etree.ElementTree as ET
        LXML_AVAILABLE = False

class SchemaParser:
    def __init__(self):
        pass
    
    def validate_schema(self, schema: SchemaConfig) -> bool:
        """Validate the schema configuration"""
        if not schema.name or not schema.schema_content:
            return False
        
        try:
            # Parse the schema content to extract field information
            parsed_fields = self.extract_field_info(schema.schema_content, schema.schema_type)
            
            # Validate that configured fields match parsed fields
            if schema.fields:
                return self._validate_field_consistency(parsed_fields, schema.fields)
            
            return True
        except Exception as e:
            print(f"Schema validation error: {e}")
            return False
    
    def _parse_json_schema(self, schema_content: str) -> List[Dict[str, Any]]:
        """Parse JSON schema and extract field information"""
        try:
            schema = json.loads(schema_content)
            fields = []
            
            if 'properties' in schema:
                required_fields = set(schema.get('required', []))
                
                for field_name, field_def in schema['properties'].items():
                    field_type = field_def.get('type', 'string')
                    
                    # Map JSON schema types to our data types
                    data_type_mapping = {
                        'string': 'string',
                        'integer': 'integer',
                        'number': 'float',
                        'boolean': 'boolean',
                        'array': 'string',  # Simplified handling
                        'object': 'string'  # Simplified handling
                    }
                    
                    fields.append({
                        'name': field_name,
                        'type': data_type_mapping.get(field_type, 'string'),
                        'required': field_name in required_fields,
                        'description': field_def.get('description', ''),
                        'pattern': field_def.get('pattern', ''),
                        'min_value': field_def.get('minimum'),
                        'max_value': field_def.get('maximum'),
                        'min_length': field_def.get('minLength'),
                        'max_length': field_def.get('maxLength')
                    })
            
            return fields
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON schema: {e}")
    
    def _parse_xml_schema(self, schema_content: str) -> List[Dict[str, Any]]:
        """Parse XML schema content"""
        try:
            if LXML_AVAILABLE:
                # Try to parse as XSD first
                try:
                    root = etree.fromstring(schema_content.encode('utf-8'))
                    if root.tag.endswith('schema') or 'schema' in root.tag:
                        return self._parse_xsd_schema(root)
                except:
                    pass
                
                # Parse as generic XML
                root = etree.fromstring(schema_content.encode('utf-8'))
                return self._parse_xml_document(root)
            else:
                # Use defusedxml or built-in ElementTree
                root = ET.fromstring(schema_content)
                return self._parse_xml_document(root)
                
        except Exception as e:
            raise ValueError(f"Invalid XML schema: {e}")
    
    def _parse_xsd_schema(self, root) -> List[Dict[str, Any]]:
        """Parse XSD schema elements"""
        fields = []
        
        # Look for element definitions
        for element in root.xpath('.//xs:element', namespaces={'xs': 'http://www.w3.org/2001/XMLSchema'}):
            field_name = element.get('name', '')
            field_type = element.get('type', 'string')
            min_occurs = element.get('minOccurs', '1')
            
            if field_name:
                fields.append({
                    'name': field_name,
                    'type': self._infer_xml_field_type(element),
                    'required': min_occurs != '0',
                    'description': element.get('annotation', ''),
                    'pattern': '',
                    'min_value': None,
                    'max_value': None,
                    'min_length': None,
                    'max_length': None
                })
        
        return fields
    
    def _parse_xml_document(self, root) -> List[Dict[str, Any]]:
        """Parse generic XML document structure"""
        fields = []
        
        def extract_fields(element, prefix=''):
            for child in element:
                field_name = prefix + child.tag if prefix else child.tag
                
                # Check if this field already exists
                existing_field = next((f for f in fields if f['name'] == field_name), None)
                if not existing_field:
                    fields.append({
                        'name': field_name,
                        'type': self._infer_xml_field_type(child),
                        'required': True,  # Assume required for XML
                        'description': '',
                        'pattern': '',
                        'min_value': None,
                        'max_value': None,
                        'min_length': None,
                        'max_length': None
                    })
                
                # Recursively process child elements
                if len(child) > 0:
                    extract_fields(child, field_name + '.')
        
        extract_fields(root)
        return fields
    
    def _infer_xml_field_type(self, element) -> str:
        """Infer the data type from XML element content"""
        if len(element) > 0:
            return 'object'  # Has child elements
        
        text = element.text or ''
        text = text.strip()
        
        if not text:
            return 'string'
        
        # Try to infer type from content
        if text.lower() in ['true', 'false']:
            return 'boolean'
        elif self._is_float(text):
            return 'float'
        elif text.isdigit():
            return 'integer'
        elif self._is_date(text):
            return 'date'
        else:
            return 'string'
    
    def _is_float(self, text: str) -> bool:
        """Check if text represents a float"""
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    def _is_date(self, text: str) -> bool:
        """Check if text represents a date"""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}/\d{2}/\d{2}'   # YYYY/MM/DD
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, text):
                return True
        return False
    
    def _validate_field_consistency(self, parsed_fields: List[Dict[str, Any]], configured_fields: List[FieldConfig]) -> bool:
        """Validate that configured fields are consistent with parsed schema"""
        parsed_field_names = {field['name'] for field in parsed_fields}
        configured_field_names = {field.name for field in configured_fields}
        
        # Check if all configured fields exist in the parsed schema
        for field in configured_fields:
            if field.name not in parsed_field_names:
                print(f"Warning: Configured field '{field.name}' not found in schema")
        
        return True
    
    def extract_field_info(self, schema_content: str, schema_type: str) -> List[Dict[str, Any]]:
        """Extract field information from schema content"""
        if schema_type.lower() == 'json':
            return self._parse_json_schema(schema_content)
        elif schema_type.lower() == 'xml':
            return self._parse_xml_schema(schema_content)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")
    
    def generate_sample_schema(self, schema_type: str) -> str:
        """Generate a sample schema for the specified type"""
        if schema_type.lower() == 'json':
            return '''{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "email": {"type": "string"},
    "active": {"type": "boolean"}
  },
  "required": ["id", "name", "email"]
}'''
        elif schema_type.lower() == 'xml':
            return '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="user">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="id" type="xs:integer"/>
        <xs:element name="name" type="xs:string"/>
        <xs:element name="email" type="xs:string"/>
        <xs:element name="active" type="xs:boolean"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>'''
        else:
            return "Unsupported schema type" 