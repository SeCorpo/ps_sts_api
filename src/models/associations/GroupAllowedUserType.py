from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.core.base import BaseModel
from src.models.user_types.UserType import UserType

class GroupAllowedUserType(BaseModel):
    """ Many-to-many Association model for allowed user types in a group """
    __tablename__ = "group_allowed_user_types"

    group_id = Column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    user_type = Column("user_type", Enum(UserType), primary_key=True)
    created_by_user_id = Column("created_by_user_id", Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)

    group = relationship("Group", back_populates="allowed_user_types")
    created_by = relationship("User", foreign_keys=[created_by_user_id])