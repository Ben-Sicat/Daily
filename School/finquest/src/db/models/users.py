from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

from .document import PyObjectId

class Users(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    password: str
    full_name: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}