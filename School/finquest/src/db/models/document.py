"""
This module contains the Document model.
"""
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Document(Document):
    _id: PydanticObjectId
    title: str
    content: str
    author: str
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime    