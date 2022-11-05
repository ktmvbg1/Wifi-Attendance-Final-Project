from sqlalchemy import false
from models import *
from services.auth import check_permission


def add_session(session, user_id, course_id, lecture_id, name, start=None, end=None):
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")

    new_session = Session(name=name, course_id=course_id,
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
