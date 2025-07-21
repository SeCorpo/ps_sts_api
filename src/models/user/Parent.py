from src.models import User
from src.constants import Usertype
from sqlalchemy import Column, Integer, ForeignKey

class Parent(User):
    """ Parent user """
    __tablename__ = "parent"

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    # extra fields specific to a parent

    __mapper_args__ = {
        "polymorphic_identity": Usertype.PARENT,
    }