from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core import BaseModel
from src.constants import Usertype
from src.models import Group

class GroupUsertype(BaseModel):
    """ Many-to-many Association model for allowed usertypes in a group """
    __tablename__ = "group_usertypes"

    group_id: Mapped[int] = mapped_column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    usertype: Mapped[Usertype] = mapped_column("usertype", Enum(Usertype, name="usertype_enum"), primary_key=True)

    group: Mapped["Group"] = relationship("Group", back_populates="usertype_associations")