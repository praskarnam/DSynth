import random
import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from faker import Faker
from models import SchemaConfig, FieldConfig, CustomDataType, DataTypeEnum

class DataGenerator:
    def __init__(self):
        self.faker = Faker()
        self.custom_types = {}
        self._seed = None
    
    def set_seed(self, seed: int):
        """Set the seed for reproducible data generation"""
        self._seed = seed
        random.seed(seed)
        self.faker.seed_instance(seed)
    
    def get_default_types(self):
        """Get information about all supported built-in data types"""
        return [
            {"name": "string", "description": "Random string", "category": "text"},
            {"name": "integer", "description": "Random integer", "category": "number"},
            {"name": "float", "description": "Random float", "category": "number"},
            {"name": "boolean", "description": "Random boolean", "category": "boolean"},
            {"name": "date", "description": "Random date", "category": "date"},
            {"name": "datetime", "description": "Random datetime", "category": "date"},
            {"name": "email", "description": "Random email address", "category": "text"},
            {"name": "phone", "description": "Random phone number", "category": "text"},
            {"name": "name", "description": "Random person name", "category": "text"},
            {"name": "address", "description": "Random street address", "category": "text"},
            {"name": "city", "description": "Random city name", "category": "text"},
            {"name": "country", "description": "Random country name", "category": "text"},
            {"name": "zipcode", "description": "Random zip code", "category": "text"},
            {"name": "company", "description": "Random company name", "category": "text"},
            {"name": "job", "description": "Random job title", "category": "text"},
            {"name": "url", "description": "Random URL", "category": "text"},
            {"name": "ip_address", "description": "Random IP address", "category": "text"},
            {"name": "uuid", "description": "Random UUID", "category": "text"},
            {"name": "custom", "description": "Custom data type", "category": "custom"}
        ]
    
    def generate_data(self, schema: SchemaConfig, count: int) -> List[Dict[str, Any]]:
        """Generate synthetic data based on the schema configuration"""
        if self._seed is not None:
            self.set_seed(self._seed)
        
        data = []
        for i in range(count):
            record = {}
            for field in schema.fields:
                try:
                    value = self._generate_field_value(field)
                    if field.nullable and random.random() < 0.1:  # 10% chance of null
                        value = None
                    record[field.name] = value
                except Exception as e:
                    print(f"Error generating value for field {field.name}: {e}")
                    record[field.name] = self._get_default_value(field)
            data.append(record)
        
        return data
    
    def _generate_field_value(self, field: FieldConfig) -> Any:
        """Generate a value for a specific field"""
        # Check if field has MVEL expression
        if field.mvel_expression:
            return self._evaluate_custom_expression(field.mvel_expression)
        
        # Check if field has custom data type
        if field.data_type == "custom" or (isinstance(field.data_type, str) and field.data_type not in [dt.value for dt in DataTypeEnum]):
            return self._generate_custom_type_value(field)
        
        # Use built-in data type
        return self._generate_builtin_type_value(field)
    
    def _generate_builtin_type_value(self, field: FieldConfig) -> Any:
        """Generate value for built-in data types"""
        data_type = field.data_type
        
        if data_type == DataTypeEnum.STRING:
            return self._generate_string(field)
        elif data_type == DataTypeEnum.INTEGER:
            return self._generate_integer(field)
        elif data_type == DataTypeEnum.FLOAT:
            return self._generate_float(field)
        elif data_type == DataTypeEnum.BOOLEAN:
            return random.choice([True, False])
        elif data_type == DataTypeEnum.DATE:
            return self._generate_date(field)
        elif data_type == DataTypeEnum.DATETIME:
            return self._generate_datetime(field)
        elif data_type == DataTypeEnum.EMAIL:
            return self.faker.email()
        elif data_type == DataTypeEnum.PHONE:
            return self.faker.phone_number()
        elif data_type == DataTypeEnum.NAME:
            return self.faker.name()
        elif data_type == DataTypeEnum.ADDRESS:
            return self.faker.address()
        elif data_type == DataTypeEnum.CITY:
            return self.faker.city()
        elif data_type == DataTypeEnum.COUNTRY:
            return self.faker.country()
        elif data_type == DataTypeEnum.ZIPCODE:
            return self.faker.zipcode()
        elif data_type == DataTypeEnum.COMPANY:
            return self.faker.company()
        elif data_type == DataTypeEnum.JOB:
            return self.faker.job()
        elif data_type == DataTypeEnum.URL:
            return self.faker.url()
        elif data_type == DataTypeEnum.IP_ADDRESS:
            return self.faker.ipv4()
        elif data_type == DataTypeEnum.UUID:
            return str(uuid.uuid4())
        else:
            return self._get_default_value(field)
    
    def _generate_string(self, field: FieldConfig) -> str:
        """Generate a string value"""
        if field.pattern:
            return self._generate_pattern_string(field.pattern)
        
        min_length = getattr(field, 'min_length', 5)
        max_length = getattr(field, 'max_length', 20)
        length = random.randint(min_length, max_length)
        
        return self.faker.text(max_nb_chars=length).replace('\n', ' ').strip()
    
    def _generate_integer(self, field: FieldConfig) -> int:
        """Generate an integer value"""
        min_value = getattr(field, 'min_value', 0)
        max_value = getattr(field, 'max_value', 100)
        return random.randint(min_value, max_value)
    
    def _generate_float(self, field: FieldConfig) -> float:
        """Generate a float value"""
        min_value = getattr(field, 'min_value', 0.0)
        max_value = getattr(field, 'max_value', 100.0)
        return round(random.uniform(min_value, max_value), 2)
    
    def _generate_date(self, field: FieldConfig) -> str:
        """Generate a date value"""
        start_date = getattr(field, 'start_date', '2020-01-01')
        end_date = getattr(field, 'end_date', '2024-12-31')
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            days_between = (end - start).days
            random_days = random.randint(0, days_between)
            random_date = start + timedelta(days=random_days)
            return random_date.strftime('%Y-%m-%d')
        except:
            return self.faker.date()
    
    def _generate_datetime(self, field: FieldConfig) -> str:
        """Generate a datetime value"""
        start_date = getattr(field, 'start_date', '2020-01-01')
        end_date = getattr(field, 'end_date', '2024-12-31')
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            time_between = (end - start).total_seconds()
            random_seconds = random.randint(0, int(time_between))
            random_datetime = start + timedelta(seconds=random_seconds)
            return random_datetime.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return self.faker.date_time().strftime('%Y-%m-%d %H:%M:%S')
    
    def _generate_pattern_string(self, pattern: str) -> str:
        """Generate a string matching a simple pattern (simplified regex)"""
        # This is a simplified pattern matcher
        # For production use, consider using a proper regex library
        if pattern == r'\d{3}-\d{3}-\d{4}':  # Phone pattern
            return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        elif pattern == r'\d{5}':  # 5-digit zip
            return str(random.randint(10000, 99999))
        elif pattern == r'\d{3}':  # 3-digit code
            return str(random.randint(100, 999))
        else:
            return self.faker.text(max_nb_chars=10)
    
    def _generate_custom_type_value(self, field: FieldConfig) -> Any:
        """Generate value for custom data types"""
        custom_type_name = field.data_type if isinstance(field.data_type, str) else "custom"
        
        if custom_type_name in self.custom_types:
            custom_type = self.custom_types[custom_type_name]
            try:
                return self._evaluate_custom_expression(custom_type.mvel_expression)
            except:
                return self._get_default_value(field)
        
        return self._get_default_value(field)
    
    def _evaluate_custom_expression(self, expression: str) -> Any:
        """Evaluate a custom expression (simplified MVEL-like evaluator)"""
        expression = expression.strip().lower()
        
        try:
            # Handle random integer ranges: random(1, 100)
            if expression.startswith('random(') and expression.endswith(')'):
                args = expression[7:-1].split(',')
                if len(args) == 2:
                    min_val = int(args[0].strip())
                    max_val = int(args[1].strip())
                    return random.randint(min_val, max_val)
            
            # Handle random float ranges: random(0.0, 1.0)
            if expression.startswith('random(') and expression.endswith(')') and '.' in expression:
                args = expression[7:-1].split(',')
                if len(args) == 2:
                    min_val = float(args[0].strip())
                    max_val = float(args[1].strip())
                    return round(random.uniform(min_val, max_val), 2)
            
            # Handle date ranges: date('2023-01-01', '2023-12-31')
            if expression.startswith("date('") and expression.endswith("')"):
                args = expression[6:-2].split("', '")
                if len(args) == 2:
                    start_date = datetime.strptime(args[0], '%Y-%m-%d').date()
                    end_date = datetime.strptime(args[1], '%Y-%m-%d').date()
                    days_between = (end_date - start_date).days
                    random_days = random.randint(0, days_between)
                    random_date = start_date + timedelta(days=random_days)
                    return random_date.strftime('%Y-%m-%d')
            
            # Handle choice: choice('option1', 'option2', 'option3')
            if expression.startswith("choice('") and expression.endswith("')"):
                args = expression[8:-2].split("', '")
                return random.choice(args)
            
            # Handle simple arithmetic: 1 + 2, 10 * 5, etc.
            if any(op in expression for op in ['+', '-', '*', '/', '**']):
                # Basic safety check - only allow simple expressions
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expression):
                    return eval(expression)
            
            # Default: return the expression as-is if it's a simple string
            return expression
            
        except Exception as e:
            print(f"Error evaluating expression '{expression}': {e}")
            return expression
    
    def _get_default_value(self, field: FieldConfig) -> Any:
        """Get a default value if generation fails"""
        if field.nullable:
            return None
        
        data_type = field.data_type
        if data_type == DataTypeEnum.STRING:
            return "default_value"
        elif data_type == DataTypeEnum.INTEGER:
            return 0
        elif data_type == DataTypeEnum.FLOAT:
            return 0.0
        elif data_type == DataTypeEnum.BOOLEAN:
            return False
        elif data_type == DataTypeEnum.DATE:
            return "2024-01-01"
        elif data_type == DataTypeEnum.DATETIME:
            return "2024-01-01 00:00:00"
        else:
            return "default_value"
    
    def test_custom_type(self, custom_type: CustomDataType) -> bool:
        """Test a custom data type by attempting to generate a sample value"""
        try:
            result = self._evaluate_custom_expression(custom_type.mvel_expression)
            return result is not None
        except:
            return False
    
    def add_custom_type(self, custom_type: CustomDataType):
        """Add a custom data type to the generator"""
        self.custom_types[custom_type.name] = custom_type
    
    def remove_custom_type(self, type_name: str):
        """Remove a custom data type from the generator"""
        if type_name in self.custom_types:
            del self.custom_types[type_name] 