from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from db.models.document import PyObjectId

class Embeddings(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    document_id: str
    embeddings: List[float]
    created_at: Optional[str] = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}