from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SSL(BaseModel):
    active: Optional[bool] = False
    expiry: Optional[datetime] = None
    email: Optional[str] = None