from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import lecture
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User
from dtos.lecture import CreateLectureInput, UpdateLectureInput


router = APIRouter(prefix="/api/lectures",
                   tags=["lectures"], dependencies=[Depends(filter_request)])


@router.get("/")
async def get_all_lectures(session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = lecture.get_lectures(session, user.id)
    return data



@router.get("/{lecture_id}")
async def get_lecture(lecture_id: int, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = lecture.get_lecture(session, user.id, lecture_id)
    return data


@router.post("/")
async def create_lecture(input: CreateLectureInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = lecture.add_lecture(session, user.id, input.course_id, input.name, input.description)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.patch("/{lecture_id}")
async def edit_lecture(lecture_id: int, input: UpdateLectureInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = lecture.update_lecture(session, user.id, lecture_id, input.course_id, input.name, input.description)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.delete("/{lecture_id}")
async def delete_lecture(lecture_id: int, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = lecture.delete_lecture(session, user.id, lecture_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
    )
