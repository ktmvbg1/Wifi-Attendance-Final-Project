from models import *
from services.auth import check_access_course, check_is_teacher, check_permission


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
