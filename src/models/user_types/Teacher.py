from ..User import User
from src.constants.usertype import Usertype
from sqlalchemy import Column, Integer, ForeignKey

class Teacher(User):
    """ Teacher user """
    __tablename__ = "teacher"

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    # extra fields specific to a teacher

    __mapper_args__ = {
        "polymorphic_identity": Usertype.TEACHER,
    }