from pydantic import BaseModel

class Option(BaseModel):
    title: str
    resource_path: str