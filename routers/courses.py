from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import course
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User
from dtos.course import CreateCourseInput, EnrollCourseInput, UpdateCourseInput


router = APIRouter(prefix="/api/courses",
                   tags=["courses"], dependencies=[Depends(filter_request)])


@router.get("/")
async def get_all_courses(session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.get_courses(session, user.id)
    return data


@router.get("/{course_id}")
async def get_course(course_id: int, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.get_course(session, user.id, course_id)
    return data


@router.post("/")
async def create_course(input: CreateCourseInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.add_course(session, user.id, input.name, input.description)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        data = data
    )

@router.patch("/{course_id}")
async def edit_course(course_id: int, input: UpdateCourseInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.update_course(session, user.id,course_id, input.name, input.description)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        data = data
    )

@router.delete("/{course_id}")
async def delete_course(course_id: int, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.delete_course(session, user.id, course_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        data = data
    )

@router.post("/{course_id}/enroll")
async def enroll_course(course_id: int, input: EnrollCourseInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.enroll_course(session, user.id, course_id, input.users)
    if success:
        return {"success": True, "data": data}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        data = data
    )

@router.delete("/{course_id}/enroll")
async def unenroll_course(course_id: int, input: EnrollCourseInput, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.unenroll_course(session, user.id, course_id, input.users)
    if success:
        return {"success": True, "data": data}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        data = data
    )

@router.get("/{course_id}/enroll")
async def get_enrolled_users(course_id: int, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success, data = course.get_enrolled_users(session, user.id, course_id)
    return data
