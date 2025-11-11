"""Example Pydantic models for PipeCo pipeline demonstrations."""
from pydantic import BaseModel

class ExampleCSVModel(BaseModel):
    """Input model containing path to a CSV file."""
    csv_path: str
    
class ExampleDictModel(BaseModel):
    """Model containing structured data as a dictionary."""
    structured_dict: dict

class ExampleConfigModel(BaseModel):
    """Configuration for CSV parsing options."""
    delimiter: str = ","
    header: bool = True
    
class Nothing(BaseModel):
    """Empty model."""
    pass
