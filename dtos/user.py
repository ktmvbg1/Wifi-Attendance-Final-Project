
from models import User
from pydantic import BaseModel

class UserOutput:
    id: int
    username: str
    fullname: str

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.fullname = user.fullname
    
