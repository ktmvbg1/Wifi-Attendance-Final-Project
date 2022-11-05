from models import *
from services.auth import check_access_course, check_permission


def add_lecture(session, user_id, course_id, name):
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")

    new_lecture = Lecture(course_id=course_id, name=name)
    session.add(new_lecture)
    session.commit()
    return (True, "Created lecture {}".format(name))


def get_lecture(session, user_id, lecture_id):

    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if not lecture:
        return (False, "Not Found")
    if not check_access_course(session, user_id, lecture.course_id):
        return (False, "Forbidden")
    return (True, lecture)


def update_lecture(session, user_id, lecture_id, course_id=None, name=None):

    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if not lecture:
        return (False, 'Lecture does not exist')
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")

    if course_id:
        lecture.course_id = course_id
    if name:
        lecture.name = name
    session.commit()
    return (True, "Updated {}".format(lecture_id))
