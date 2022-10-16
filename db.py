from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session
from models import *
import re
import auth

def init_db():
	engine = create_engine('sqlite:///test.db')
	Base.metadata.bind = engine
	Base.metadata.create_all()

def get_session():
	engine = create_engine('sqlite:///test.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker()
	DBSession.bind = engine
	return DBSession()
	
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
