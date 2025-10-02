from pydantic import BaseModel, Field
from typing import List


class Settings(BaseModel):
    lines: List[str] = Field(
        default_factory=list,
        example=None
    )
