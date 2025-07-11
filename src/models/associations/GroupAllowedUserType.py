from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.core.base import BaseModel
from src.constants.user_type import UserType

class GroupAllowedUserType(BaseModel):
    """ Many-to-many Association model for allowed user types in a group """
    __tablename__ = "group_allowed_user_types"

    group_id = Column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    user_type = Column("user_type", Enum(UserType), primary_key=True)

    group = relationship("Group", back_populates="allowed_user_type_associations")