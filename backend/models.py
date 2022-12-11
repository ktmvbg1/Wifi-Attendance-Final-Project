from datetime import timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    account_type = Column(Integer)  # 1 = student, 2 = teacher
    username = Column(String(200), nullable=False)
    password = Column(String(1000), nullable=False)
    fullname = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    courses = relationship(
        "CourseUsers", back_populates="user", cascade="all, delete")
    checkins = relationship(
        "Checkin", back_populates="user", cascade="all, delete")
    devices = relationship(
        "UserDevice", back_populates="user", cascade="all, delete")


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship(
        "CourseUsers", back_populates="course", cascade="all, delete")
    lectures = relationship(
        "Lecture", back_populates="course", cascade="all, delete")
    sessions = relationship(
        "Session", back_populates="course", cascade="all, delete")
    checkins = relationship(
        "Checkin", back_populates="course", cascade="all, delete")


class Lecture(Base):  # a course consists of many lectures
    __tablename__ = 'lectures'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(
        'courses.id'), nullable=False)
    name = Column(String(2000), nullable=False)
    description = Column(String(2000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("Course")
    sessions = relationship(
        "Session", back_populates="lecture", cascade="all, delete")
    checkins = relationship(
        "Checkin", back_populates="lecture", cascade="all, delete")


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(
        'courses.id'), nullable=False)
    lecture_id = Column(Integer, ForeignKey(
        'lectures.id'), nullable=False)
    name = Column(String(2000), nullable=False)
    description = Column(String(2000), nullable=True)
    start = Column(DateTime(timezone=True), server_default=func.now())
    end = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("Course")
    lecture = relationship("Lecture")
    checkins = relationship(
        "Checkin", back_populates="session", cascade="all, delete")


class Checkin(Base):  # a Lecture consists of many check-in sessions
    __tablename__ = 'check_in'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(
        'courses.id'), nullable=False)
    lecture_id = Column(Integer, ForeignKey(
        'lectures.id'), nullable=False)
    session_id = Column(Integer, ForeignKey(
        'sessions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
    course = relationship("Course")
    lecture = relationship("Lecture")
    session = relationship("Session")


class UserDevice(Base):  # a user can have many devices
    __tablename__ = 'user_devices'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    mac_address = Column(String(200))
    ip_address = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")


class CourseUsers(Base):  # a user can have many courses
    __tablename__ = 'course_users'
    user_id = Column(Integer, ForeignKey(
        'users.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey(
        'courses.id'), primary_key=True)
    role_id = Column(Integer, nullable=False)  # 1 = student, 2 = teacher
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="courses")
    course = relationship("Course", back_populates="users")
