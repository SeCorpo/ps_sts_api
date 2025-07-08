from sqlalchemy import Column, Integer, VARCHAR, Boolean
from sqlalchemy.orm import relationship
from src.core.base import BaseModel
from sqlalchemy.ext.associationproxy import association_proxy


class Group(BaseModel):
    """ Group of users, user_type is managed manually """
    __tablename__ = "groups"

    group_id = Column("group_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(128), unique=True, nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)

    # Link to association objects
    allowed_user_type_associations = relationship("GroupAllowedUserType", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to UserType (enum) objects
    allowed_user_types = association_proxy("allowed_user_type_associations", "user_type")
    # Link to association objects
    member_associations = relationship("GroupUser", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to User objects
    members = association_proxy('member_associations', 'user')