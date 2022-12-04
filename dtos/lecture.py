from typing import Optional
from pydantic import BaseModel

class CreateLectureInput(BaseModel):
    course_id: int
    name: str
    description: Optional[str] = None


class UpdateLectureInput(BaseModel):
    course_id: Optional[int]
    name: Optional[str]
    description: Optional[str]