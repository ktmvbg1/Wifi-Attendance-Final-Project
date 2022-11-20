from typing import Optional
from pydantic import BaseModel

class CreateCourseInput(BaseModel):
    name: str
    description: Optional[str] = None


class UpdateCourseInput(BaseModel):
    name: Optional[str]
    description: Optional[str]