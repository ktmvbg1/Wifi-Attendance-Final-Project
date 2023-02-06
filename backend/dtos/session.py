from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CreateSessionInput(BaseModel):
    lecture_id: int
    name: str
    description: str = ""
    start: Optional[datetime]
    end: Optional[datetime]

class UpdateSessionInput(BaseModel):
    name: Optional[str]
    description: str = ""
    start: Optional[datetime]
    end: Optional[datetime]

class SessionOutput(BaseModel):
    id: int
    session_name: str
    session_description: str
    start: datetime
    end: datetime
    teacher_id: int
    teacher_name: str
    course_id: int
    course_name: str
    lecture_id: int
    lecture_name: str

class CheckinOutput(BaseModel):
    id: int
    user_id: int
    session_id: int
    session_name: str
    lecture_id: int
    lecture_name: str
    course_id: int
    course_name: str
    created_at: datetime
    
    

class Attendee(BaseModel):
    id: int
    name: str
    username: str
    account_type: int
    checkin_time: Optional[datetime]