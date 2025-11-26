from sqlalchemy.orm import Mapped, mapped_column
from src.models import User
from src.constants import Usertype
from sqlalchemy import Integer, ForeignKey

class AdminSchool(User):
    """ School administration user """
    __tablename__ = "admin_school"

    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    # extra fields specific to a school admin

    __mapper_args__ = {
        "polymorphic_identity": Usertype.ADMIN_SCHOOL,
    }