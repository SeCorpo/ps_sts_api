from sqlalchemy import Column, Integer, VARCHAR, Boolean
from sqlalchemy.orm import relationship
from src.core.base import BaseModel
from sqlalchemy.ext.associationproxy import association_proxy


class Group(BaseModel):
    """ Group of users, user_type is managed manually """
    __tablename__ = "groups"

    group_id = Column("group_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(128), nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)

    allowed_user_types = relationship("GroupAllowedUserType", back_populates="group", cascade="all, delete-orphan")

    # Link to association objects
    member_associations = relationship("GroupUser", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to User objects
    members = association_proxy('member_associations', 'user')