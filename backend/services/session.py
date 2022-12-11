from sqlalchemy import false
from models import *
from services.auth import check_permission


def add_session(session, user_id, lecture_id, name, description, start=None, end=None):
    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if (not lecture):
        return (False, "Not found")
    if not check_permission(session, user_id, lecture.course_id):
        return (False, "Forbidden")

    new_session = Session(name=name, course_id=lecture.course_id, description=description,
                          lecture_id=lecture_id)
    if (start):
        new_session.start = start
    if (end):
        new_session.end = end
    session.add(new_session)
    session.commit()
    return (True, "Created session {}".format(new_session.id))


def delete_session(session, user_id, session_id):
    s = session.query(Session).filter_by(id=session_id).first()
    if (not s):
        return (False, "Not found")
    if not check_permission(session, user_id, s.course_id):
        return (False, "Forbidden")

    session.delete(s)
    session.commit()
    return (True, "Deleted session {}".format(s.id))
