from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
import re

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
	


