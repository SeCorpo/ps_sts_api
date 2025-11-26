from sqlalchemy.orm import mapped_column, Mapped
from src.models import User
from src.constants import Usertype
from sqlalchemy import Integer, ForeignKey

class Teacher(User):
    """ Teacher user """
    __tablename__ = "teacher"

    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    # extra fields specific to a teacher

    __mapper_args__ = {
        "polymorphic_identity": Usertype.TEACHER,
    }