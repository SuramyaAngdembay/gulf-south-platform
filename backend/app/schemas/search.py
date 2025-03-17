from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class SearchResult(BaseModel):
    id: int
    type: str
    title: str
    description: str
    date: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True 