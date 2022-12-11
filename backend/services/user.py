from models import *
import re
from services import auth


def change_password(session, username, password, newpassword, confirmpassword):
    if newpassword != confirmpassword:
        return (False, "Incorrrect confirmation of new password")
    user = session.query(User).filter_by(username=username).first()
    if not auth.verify_password(password, user.password):
        return (False, "Incorrect Password")
    elif password == newpassword:
        return (False, "New password must be different from current password")
    else:
        newpasswordhash = auth.get_password_hash(newpassword)
        user.password = newpasswordhash
        session.commit()
        return (True, "Change Successful")


def add_user(session, fullname, username, password, confirm_password, account_type):
    regex_user = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
    if not re.search(regex_user, username):
        return (False, 'Invalid Username')

    regex_username = '[^a-zA-Z\d\s:]'
    if re.search(regex_username, fullname):
        return (False, 'Invalid Name')
    if len(password) < 6:
        return (False, 'Password is too short')
    if password != confirm_password:
        return (False, 'The password confirmation does not match')

    user = session.query(User).filter_by(username=username).first()
    if user:
        return (False, 'Username already exists')

    new_user = User(username=username, password=auth.get_password_hash(
        password), fullname=fullname, account_type=account_type)
    session.add(new_user)
    session.commit()
    return (True, "Created {}".format(username))


def get_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if (not user):
        return (False, "User does not exist")
    return (True, user)


def get_user_by_username(session, username):
    user = session.query(User).filter_by(username=username).first()
    if (not user):
        return (False, "User does not exist")
    return (True, user)


def get_users(session):
    users = session.query(User).all()
    return users


def update_user(session, user_id, username, fullname, account_type):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    if (username):
        user.username = username
    if (fullname):
        user.fullname = fullname
    if (account_type):
        user.account_type = account_type
    session.commit()
    return (True, "Updated {}".format(username))


def reset_password(session, user_id, password):
    user = session.query(User).filter_by(id=user_id).first()
    if (not user):
        return (False, "User does not exist")

    user.password = auth.get_password_hash(password)
    session.commit()
    return (True, "Password reset successful")


def delete_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    session.delete(user)
    session.commit()
    return (True, "Deleted {}".format(user_id))


def add_students(session, student_ids):
    count = 0
    for student_id in student_ids:
        student = session.query(User).filter_by(username=student_id).first()
        if student:
            continue
        new_student = User(username=student_id, password=auth.get_password_hash(
            '123456'), fullname=student_id, account_type=1)
        session.add(new_student)
        count += 1
    session.commit()
    return (True, "Created {} user(s)".format(count))
