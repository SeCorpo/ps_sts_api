from src.models.User import User
from src.constants.usertype import Usertype
from sqlalchemy import Column, Integer, ForeignKey

class AdminSchool(User):
    """ School administration user """
    __tablename__ = "admin_school"

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    # extra fields specific to a school admin

    __mapper_args__ = {
        "polymorphic_identity": Usertype.ADMIN_SCHOOL,
    }