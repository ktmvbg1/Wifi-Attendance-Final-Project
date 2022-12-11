from fastapi import APIRouter, Depends, HTTPException, status
from services import auth, user
from dtos.auth import LoginInput, LoginOutput, ChangePasswordInput, ChangePasswordOutput
from dtos.user import UpdateUserInput, UserOutput
from jose import JWTError
from dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from models import User


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
async def login(input: LoginInput, session: Session = Depends(get_db)):
    success, data = auth.login(session, input.username, input.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return LoginOutput(access_token=data, token_type="bearer")


@router.post("/change-password")
async def change_password(input: ChangePasswordInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.change_password(
        session, current_user.username, input.password, input.new_password, input.confirm_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return ChangePasswordOutput(message=data)


@router.post("/update-profile")
async def update_profile(input: UpdateUserInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = user.update_user(
        session, current_user.id, current_user.username, input.fullname, current_user.account_type)
    if (success):
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserOutput(current_user)

@router.get("/seed")
async def create_user(session: Session = Depends(get_db)):
    auth.seed(session)
    return {"message": "success"}
