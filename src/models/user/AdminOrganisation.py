from sqlalchemy.orm import mapped_column, Mapped
from src.models import User
from src.constants import Usertype
from sqlalchemy import Integer, ForeignKey

class AdminOrganisation(User):
    """ Application admin """
    __tablename__ = "admin_organisation"

    user_id: Mapped[int] = mapped_column("user_id",Integer,ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    # extra fields specific to an organisation admin

    __mapper_args__ = {
        "polymorphic_identity": Usertype.ADMIN_ORGANISATION,
    }