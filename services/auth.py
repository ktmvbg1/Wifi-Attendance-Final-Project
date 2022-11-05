from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext

from jose import JWTError, jwt

from models import CourseUsers, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def seed(session):
    user = session.query(User).filter_by(username="admin").first()
    if  user:
        return
    admin = User(username="admin", fullname="admin",password=get_password_hash("admin"), account_type=2)
    session.add(admin)
    session.commit()


def login(session, username, password):
    user: User = session.query(User).filter_by(username=username).first()
    if user:
        if not verify_password(password, user.password):
            return (False, "Incorrect Password")
        else:
            data = {
                "fullname": f"{user.fullname}",
                "user_id": f"{user.id}",
                "username": f"{user.username}",
                "account_type": user.account_type
            }
            return (True, create_access_token(data, timedelta(hours=48)))
    elif user == None:
        return (False, "User Not Found")


def check_access_course(session, user_id, course_id):
    permission = session.query(CourseUsers).filter_by(
        user_id=user_id, course_id=course_id).first()
    if not permission:
        return False
    return True


def check_permission(session, user_id, course_id):
    permission = session.query(CourseUsers).filter_by(
        user_id=user_id, course_id=course_id).first()
    if not permission:
        return False
    if permission.role_id != 2:
        return False
    return True


def check_is_teacher(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return False
    if user.role_id != 2:
        return False
    return True
