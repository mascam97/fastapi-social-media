from pydantic import BaseModel, Field


class Publication(BaseModel):
  title: str = Field(min_length=5, max_length=25)
  content: str = Field(min_length=10, max_length=155)
  state: str = Field(min_length=5, max_length=20)

  class Config:
    schema_extra = {
        "example": {
            "title": "My publication",
            "content": "Publication description",
            "state": "active"
        }
    }
