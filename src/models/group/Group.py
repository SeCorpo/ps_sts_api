from sqlalchemy import Column, Integer, VARCHAR, Boolean
from sqlalchemy.orm import relationship
from src.core import BaseModel
from sqlalchemy.ext.associationproxy import association_proxy


class Group(BaseModel):
    """ Group of users, usertype is managed manually """
    __tablename__ = "groups"

    group_id = Column("group_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(64), unique=True, nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)

    # Link to association objects
    usertype_associations = relationship("GroupUsertype", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to Usertype (enum) objects
    usertypes = association_proxy("usertype_associations", "usertype")
    # Link to association objects
    member_associations = relationship("GroupUser", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to User objects
    members = association_proxy('member_associations', 'user')