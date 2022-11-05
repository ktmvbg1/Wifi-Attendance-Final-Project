from models import *
import re
from services import auth


def change_password(session, username, password, newpassword, confirmpassword):
    if  newpassword != confirmpassword:
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

def add_user(session, username, password, confirm_password, fullname):
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
	
	new_user = User(username = username, password = auth.get_password_hash(password), fullname = fullname)
	session.add(new_user)
	session.commit()
	return (True, "Created {}".format(username))

def get_user(session, username):
	user = session.query(User).filter_by(username=username).first()
	return user

def update_user(session, username, fullname):
	user = session.query(User).filter_by(username=username).first()
	if not user:
		return (False, 'User does not exist')
	user.fullname = fullname
	session.commit()
	return (True, "Updated {}".format(username))

def delete_user(session, username):
	user = session.query(User).filter_by(username=username).first()
	if not user:
		return (False, 'User does not exist')
	session.delete(user)
	session.commit()
	return (True, "Deleted {}".format(username))

def add_students(session, student_ids):
	count = 0
	for student_id in student_ids:
		student = session.query(User).filter_by(username=student_id).first() 
		if student:
			continue
		new_student = User(username = student_id, password = auth.get_password_hash('123456'), fullname = student_id)
		session.add(new_student)
		count += 1
	session.commit()
	return (True, "Created {} user(s".format(count))