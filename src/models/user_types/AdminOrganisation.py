from src.models.User import User
from src.constants.user_type import UserType
from sqlalchemy import Column, Integer, ForeignKey

class AdminOrganisation(User):
    """ Application admin """
    __tablename__ = "admin_organisation"

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    # extra fields specific to an organisation admin

    __mapper_args__ = {
        "polymorphic_identity": UserType.ADMIN_ORGANISATION,
    }