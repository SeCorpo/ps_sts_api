from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core import BaseModel
from src.models import Group, User


class GroupUser(BaseModel):
    """ Many-to-many Association model for members """
    __tablename__ = "group_users"

    group_id: Mapped[int] = mapped_column("group_id", Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    group: Mapped["Group"] = relationship("Group", back_populates="member_associations")
    user: Mapped["User"] = relationship("User", back_populates="group_associations", foreign_keys=[user_id])