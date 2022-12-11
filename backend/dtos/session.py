from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CreateSessionInput(BaseModel):
    lecture_id: int
    name: str
    description: str = ""
    start: Optional[datetime]
    end: Optional[datetime]
