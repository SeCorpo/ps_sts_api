from typing import Optional, List
from src.core import BaseModel
from src.constants import Usertype
from sqlalchemy import Integer, Enum, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.associationproxy import association_proxy

from src.models import Person, GroupUser


class User(BaseModel):
    """ Abstract base User class, for authentication and account information (needs Person) """
    __tablename__ = "users"
    __abstract__ = True

    user_id: Mapped[int] = mapped_column("user_id",Integer,ForeignKey("persons.person_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column("password_hash", LargeBinary(length=60), nullable=False)
    salt: Mapped[bytes] = mapped_column("salt", LargeBinary(length=16), nullable=False)
    email_verified: Mapped[bool] = mapped_column("email_verified", Boolean, default=False, nullable=False)
    usertype: Mapped[Usertype] = mapped_column("usertype", Enum(Usertype, name="usertype_enum"), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": usertype,
        "with_polymorphic": "*"
    }

    person: Mapped[Optional["Person"]] = relationship("Person", back_populates="user", uselist=False)

    # Link to association objects
    group_associations: Mapped[List["GroupUser"]] = relationship("GroupUser", back_populates="user", cascade="all, delete-orphan")
    # Direct proxy to Group objects
    groups = association_proxy('group_associations', 'group')