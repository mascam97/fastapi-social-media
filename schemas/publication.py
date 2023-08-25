from pydantic import BaseModel, Field
from typing import Optional

class Publication(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    content: str = Field(min_length=15, max_length=50)
    state:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My publication",
                "content": "Publication description",
                "state" : "active"
            }
        }