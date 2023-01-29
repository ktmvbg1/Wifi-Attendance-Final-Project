
from typing import List, Optional
from models import User
from pydantic import BaseModel

class UserOutput:
    id: int
    username: str
    fullname: str
    account_type: int

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.fullname = user.fullname
        self.account_type = user.account_type

class UserCourseOutput:
    id: int
    username: str
    fullname: str
    account_type: str
    role_id: int
    
    def __init__(self, user: User, role_id: int):
        self.id = user.id
        self.username = user.username
        self.fullname = user.fullname
        self.account_type = user.account_type
        self.role_id = role_id
    
class CreateUserInput(BaseModel):
    username: str
    fullname: str
    password: str
    account_type: int

class UpdateUserInput(BaseModel):
    username: Optional[str]
    fullname: Optional[str]
    password: Optional[str]
    account_type: Optional[int]
class CreateUsersInput(BaseModel):
    users: List[str]
