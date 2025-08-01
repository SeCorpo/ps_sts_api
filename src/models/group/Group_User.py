from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core import BaseModel


class GroupUser(BaseModel):
    """ Many-to-many Association model for members """
    __tablename__ = "group_users"

    group_id = Column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    group = relationship("Group", back_populates="member_associations")
    user = relationship("User", back_populates="group_associations", foreign_keys=[user_id])