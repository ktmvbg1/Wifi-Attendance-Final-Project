from models import *
from services.auth import check_access_course, check_is_teacher, check_permission
from dtos.user import UserOutput

def add_course(session, user_id, course_name, description):
    if not check_is_teacher(session, user_id):
        return (False, "Forbidden")
    new_course = Course(name=course_name, description=description)
    session.add(new_course)
    session.commit()
    session.refresh(new_course)
    new_course_user = CourseUsers(
        role_id=2, user_id=user_id, course_id=new_course.id)
    session.add(new_course_user)
    session.commit()
    return (True, "Created {}".format(course_name))


def get_courses(session, user_id):
    course_users = session.query(CourseUsers).filter_by(user_id=user_id).all()
    courses = [x.course for x in course_users]
    return (True, courses)

def get_course(session, user_id, course_id):
    if not check_access_course(session, user_id, course_id):
        return (False, "Forbidden")
    course = session.query(Course).filter_by(id=course_id).first()
    if (not course):
        return (False, "Not found")
    return (True, course)


def update_course(session, user_id, course_id, name, description):
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        return (False, 'Course does not exist')
    if(name):
        course.name = name  
    if(description):
        course.description = description
    session.commit()
    return (True, "Updated course {}".format(course_id))


def delete_course(session, user_id, course_id):
    if not check_permission(session, user_id, course_id):
        return (False, "Forbidden")
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        return (False, 'Course does not exist')
    session.delete(course)
    session.commit()
    return (True, "Deleted course {}".format(course_id))

def enroll_course(session, teacher_id, course_id, users):
    if not check_permission(session, teacher_id, course_id):
        return (False, "Forbidden")
    count = 0
    for user_id in users:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            continue
        course_user = session.query(CourseUsers).filter_by(course_id=course_id, user_id=user_id).first()
        if course_user:
            continue
        new_course_user = CourseUsers(
            role_id=1, user_id=user_id, course_id=course_id)
        session.add(new_course_user)
        count += 1
    session.commit()
    return (True, "Enrolled {} users".format(count))

def unenroll_course(session, teacher_id, course_id, users):
    if not check_permission(session, teacher_id, course_id):
        return (False, "Forbidden")
    count = 0
    for user_id in users:
        if user_id == teacher_id:
            continue
        course_user = session.query(CourseUsers).filter_by(course_id=course_id, user_id=user_id).first()
        if not course_user:
            continue
        session.delete(course_user)
        count += 1
    session.commit()
    return (True, "Remove {} users from course {}".format(count, course_id))

def get_enrolled_users(session, user_id, course_id):
    if not check_access_course(session, user_id, course_id):
        return (False, "Forbidden")
    course_users = session.query(CourseUsers).filter_by(course_id=course_id).all()
    users = [UserOutput(x.user) for x in course_users]
    return (True, users)

def get_lectures(session, user_id, course_id):
    if not check_access_course(session, user_id, course_id):
        return (False, "Forbidden")
    lectures = session.query(Lecture).filter_by(course_id=course_id).all()
    return (True, lectures)

def get_sessions(session, user_id, course_id):
    if not check_access_course(session, user_id, course_id):
        return (False, "Forbidden")
    sessions = session.query(Session).filter_by(course_id=course_id).all()
    return (True, sessions)
