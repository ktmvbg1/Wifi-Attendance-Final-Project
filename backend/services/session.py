from datetime import datetime
from models import *
from services.auth import check_access_course, check_permission


def add_session(session, user_id, lecture_id, name, description, start=None, end=None):
    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if (not lecture):
        return (False, "Not found")
    if not check_permission(session, user_id, lecture.course_id):
        return (False, "Forbidden")

    new_session = Session(name=name, course_id=lecture.course_id, description=description,
                          lecture_id=lecture_id, teacher_id=user_id)
    if (start):
        new_session.start = start
    if (end):
        new_session.end = end
        
    session.add(new_session)
    session.commit()
    return (True, "Created session {}".format(new_session.id))

def update_session(session, user_id, session_id, name=None, description=None, start=None, end=None):
    s = session.query(Session).filter_by(id=session_id).first()
    if (not s):
        return (False, "Not found")
    if not check_permission(session, user_id, s.course_id):
        return (False, "Forbidden")
    s.teacher_id = user_id
    if (name):
        s.name = name
    if (description):
        s.description = description
    if (start):
        s.start = start
    if (end):
        s.end = end
    session.commit()
    return (True, "Updated session {}".format(s.id))

def delete_session(session, user_id, session_id):
    s = session.query(Session).filter_by(id=session_id).first()
    if (not s):
        return (False, "Not found")
    if not check_permission(session, user_id, s.course_id):
        return (False, "Forbidden")

    session.delete(s)
    session.commit()
    return (True, "Deleted session {}".format(s.id))

def end_session(session, user_id, session_id):
    s = session.query(Session).filter_by(id=session_id).first()
    if (not s):
        return (False, "Not found")
    if not check_permission(session, user_id, s.course_id):
        return (False, "Forbidden")
    if(s.end.timestamp() < datetime.now().timestamp()):
        return (True, "Session already ended")
    s.end = datetime.now()
    session.commit()
    return (True, "Ended session {}".format(s.id))

def get_active_sessions(session, user_id):
    user_courses = session.query(CourseUsers).filter_by(user_id=user_id).all()
    sessions = []
    for course in user_courses:
        sessions += session.query(Session).filter_by(course_id=course.course_id).filter(Session.start <= datetime.now()).filter(Session.end >= datetime.now()).all()
    return (True, sessions)

def checkin(session, user_id, session_id):
    l_session = session.query(Session).filter_by(id=session_id).first()
    if (not l_session):
        return (False, "Not found")
    if not check_access_course(session, user_id, l_session.course_id):
        return (False, "Forbidden")

    if(l_session.end.timestamp() < datetime.now().timestamp()):
        return (False, "Session already ended")
    
    if(l_session.start.timestamp() > datetime.now().timestamp()):
        return (False, "Session not started yet")
    
    check_if_exists = session.query(Checkin).filter_by(user_id=user_id, session_id=session_id).first()
    if(check_if_exists):
        return (False, "Already checked in")
    
    
    checkin = Checkin(user_id=user_id, session_id=session_id, course_id=l_session.course_id, lecture_id=l_session.lecture_id)
    session.add(checkin)
    session.commit()
    return (True, "Checked in")
    

def get_attendees(session, user_id, session_id):
    l_session = session.query(Session).filter_by(id=session_id).first()
    if (not l_session):
        return (False, "Not found")
    if not check_permission(session, user_id, l_session.course_id):
        return (False, "Forbidden")

    attendees = session.query(Checkin).filter_by(session_id=session_id).all()
    return (True, attendees)