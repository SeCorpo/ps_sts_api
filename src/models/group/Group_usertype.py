from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.core import BaseModel
from src.constants import Usertype

class GroupUsertype(BaseModel):
    """ Many-to-many Association model for allowed usertypes in a group """
    __tablename__ = "group_usertypes"

    group_id = Column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    usertype = Column("usertype", Enum(Usertype), primary_key=True)

    group = relationship("Group", back_populates="usertype_associations")