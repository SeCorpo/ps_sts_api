from typing import List
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core import BaseModel
from sqlalchemy.ext.associationproxy import association_proxy
from src.models import GroupUsertype, GroupUser


class Group(BaseModel):
    """ Group of users, usertype is managed manually """
    __tablename__ = "groups"

    group_id: Mapped[int] = mapped_column("group_id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", String(64), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column("is_active", Boolean, default=True, nullable=False)

    # Link to association objects
    usertype_associations: Mapped[List["GroupUsertype"]] = relationship("GroupUsertype", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to Usertype (enum) objects
    usertypes = association_proxy("usertype_associations", "usertype")
    # Link to association objects
    member_associations: Mapped[List["GroupUser"]] = relationship("GroupUser", back_populates="group", cascade="all, delete-orphan")
    # Direct proxy to User objects
    members = association_proxy('member_associations', 'user')