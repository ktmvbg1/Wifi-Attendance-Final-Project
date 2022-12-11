from models import *
from services.auth import check_access_course, check_permission


def get_lectures(session, user_id):
    course_users = session.query(CourseUsers).filter_by(user_id=user_id).all()
    courses = [x.course for x in course_users]
    lectures = []
    for course in courses:
        lectures += course.lectures
    return (True, lectures)

def add_lecture(session, user_id, course_id, name, description):
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")

    new_lecture = Lecture(course_id=course_id, name=name, description=description)
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


def update_lecture(session, user_id, lecture_id, course_id=None, name=None, description=None):

    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if not lecture:
        return (False, 'Lecture does not exist')
    if not check_permission(session, user_id, lecture.course_id):
        return (False, "Forbidden")

    if course_id:
        lecture.course_id = course_id
    if name:
        lecture.name = name
    
    if description:
        lecture.description = description
    session.commit()
    return (True, "Updated {}".format(lecture_id))

def delete_lecture(session, user_id, lecture_id):
    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if not lecture:
        return (False, 'Lecture does not exist')
    if not check_permission(session, user_id, lecture.course_id):
        return (False, "Forbidden")
    session.delete(lecture)
    session.commit()
    return (True, "Deleted lecture {}".format(lecture_id))

def get_sessions(session, user_id, lecture_id):
    lecture = session.query(Lecture).filter_by(id=lecture_id).first()
    if(not lecture):
        return (False, "Not Found")
    if not check_permission(session, user_id, lecture.course_id):
        return (False, "Forbidden")
    sessions = session.query(Session).filter_by(lecture_id=lecture_id).all()
    return (True, sessions)