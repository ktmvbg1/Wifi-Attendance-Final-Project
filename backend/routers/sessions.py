from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import session as session_service
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User
from dtos.session import Attendee, CreateSessionInput, SessionOutput, UpdateSessionInput


router = APIRouter(prefix="/api/sessions",
                   tags=["sessions"], dependencies=[Depends(filter_request)])


@router.get("/active-sessions")
async def get_active_sessions(db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.get_active_sessions(
        db_session, current_user.id)

    if success:
        sessions = [SessionOutput(
            id=session.id,
            session_name=session.name,
            session_description=session.description,
            start=session.start,
            end=session.end,
            course_id=session.course.id,
            course_name=session.course.name,
            lecture_id=session.lecture.id,
            lecture_name=session.lecture.name,
            teacher_id=session.teacher.id,
            teacher_name=session.teacher.fullname
        )
            for session in data]
        return {"success": True, "data": sessions}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.post("/", dependencies=[Depends(teacher_endpoints)])
async def create_session(input: CreateSessionInput, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.add_session(
        db_session, current_user.id, input.lecture_id, input.name, input.description, input.start, input.end)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.patch("/{session_id}", dependencies=[Depends(teacher_endpoints)])
async def update_session(session_id: int, input: UpdateSessionInput, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.update_session(
        db_session, current_user.id, session_id, input.name, input.description, input.start, input.end)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.delete("/{session_id}", dependencies=[Depends(teacher_endpoints)])
async def delete_session(session_id: int, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.delete_session(
        db_session, current_user.id, session_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.post("/{session_id}/checkin")
async def checkin(session_id: int, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.checkin(
        db_session, current_user.id, session_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.patch("/{session_id}/end", dependencies=[Depends(teacher_endpoints)])
async def end_session(session_id: int, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.end_session(
        db_session, current_user.id, session_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )


@router.get("/{session_id}/attendees")
async def get_attendees(session_id: int, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success, data = session_service.get_attendees(
        db_session, current_user.id, session_id)
    if success:
        attendees = [Attendee(id=checkin_data.user.id, name=checkin_data.user.fullname, username=checkin_data.user.username,
                              account_type=checkin_data.user.account_type, checkin_time=checkin_data.created_at) for checkin_data in data]
        return {"success": True, "data": attendees}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"},
        detail=data
    )
