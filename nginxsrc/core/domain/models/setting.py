from pydantic import BaseModel
from typing import List


class Settings(BaseModel):
    lines: List[str]
