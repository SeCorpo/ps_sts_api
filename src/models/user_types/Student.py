from ..User import User
from src.constants.user_type import UserType
from sqlalchemy import Column, Integer, ForeignKey

class Student(User):
    """ Student user """
    __tablename__ = "student"

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    # extra fields specific to a student

    __mapper_args__ = {
        "polymorphic_identity": UserType.STUDENT,
    }