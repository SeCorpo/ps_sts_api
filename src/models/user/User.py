from src.core import BaseModel
from src.constants import Usertype
from sqlalchemy import Column, Integer, Enum, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class User(BaseModel):
    """ Abstract base User class, for authentication and account information (needs Person) """
    __tablename__ = "users"
    __abstract__ = True

    user_id = Column("user_id", Integer, ForeignKey('persons.person_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    password_hash = Column("password_hash", LargeBinary(length=60), nullable=False)
    salt = Column("salt", LargeBinary(length=16), nullable=False)
    email_verified = Column("email_verified", Boolean, default=False, nullable=False)
    usertype = Column("usertype", Enum(Usertype), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": usertype,
        "with_polymorphic": "*"
    }

    person = relationship("Person", back_populates="user", uselist=False)

    # Link to association objects
    group_associations = relationship("GroupUser", back_populates="user", cascade="all, delete-orphan")
    # Direct proxy to Group objects
    groups = association_proxy('group_associations', 'group')