from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, null
from sqlalchemy.sql import func
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    account_type = Column(Integer, server_default=1) # 1 = student, 2 = teacher
    username = Column(String(200), nullable = False)
    password = Column(String(1000), nullable = False)
    fullname = Column(String(200), nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
