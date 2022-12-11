from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import session as session_service
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User
from dtos.session import CreateSessionInput


router = APIRouter(prefix="/api/sessions",
                   tags=["sessions"], dependencies=[Depends(filter_request)])


@router.post("/", dependencies=[Depends(teacher_endpoints)])
async def create_session(input: CreateSessionInput, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.add_session(
        session, current_user.id, input.lecture_id, input.name, input.description, input.start, input.end)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.delete("/{session_id}", dependencies=[Depends(teacher_endpoints)])
async def delete_session(session_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.delete_session(
        session, current_user.id, session_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )

