from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import user
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User
from dtos.user import UserOutput, CreateUserInput, UpdateUserInput, CreateUsersInput


router = APIRouter(prefix="/api/users",
                   tags=["users"], dependencies=[Depends(filter_request)])


@router.post("/batch", dependencies=[Depends(teacher_endpoints)])
async def create_users(input: CreateUsersInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.add_students(session, input.users)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )

@router.get("/", dependencies=[Depends(teacher_endpoints)])
async def get_users(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = user.get_users(session)
    return [UserOutput(user) for user in data]


@router.post("/", dependencies=[Depends(teacher_endpoints)])
async def create_user(input: CreateUserInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.add_user(
        session, input.fullname, input.username, input.password, input.password, input.account_type)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.patch("/{user_id}", dependencies=[Depends(teacher_endpoints)])
async def edit_user(user_id: int, input: UpdateUserInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.update_user(
        session, user_id, input.username, input.fullname, input.account_type)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.delete("/{user_id}", dependencies=[Depends(teacher_endpoints)])
async def delete_user(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.delete_user(session, user_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.get("/{user_id}", dependencies=[Depends(teacher_endpoints)])
async def get_user(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.get_user(session, user_id)
    if success:
        return {"success": True, "data": UserOutput(data)}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.patch("/{user_id}/reset-password", dependencies=[Depends(teacher_endpoints)])
async def reset_password(user_id: int, password: str, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.reset_password(session, user_id, password)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )

