from pydantic import BaseModel

## Example PipeCo Models
class ExampleCSVModel(BaseModel):
    csv_path: str
    
class ExampleDictModel(BaseModel):
    structured_dict: dict

class ExampleConfigModel(BaseModel):
    delimiter: str = ","
    header: bool = True
    
## Nones
class Nothing(BaseModel):
    pass
