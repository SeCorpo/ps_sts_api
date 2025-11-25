from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Integer, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class AuditMixin:
    """ Mixin for created/updated timestamps """
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class CreatedByMixin:
    """Mixin for created_by_user_id field """
    created_by_user_id: Mapped[Optional[int]] = mapped_column(
        "created_by_user_id",
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
    )

class SoftDeleteMixin:
    """ Mixin for deleted field """
    deleted: Mapped[bool] = mapped_column(
        "deleted",
        Boolean,
        default=False,
        nullable=False,
    )

class BaseModel(DeclarativeBase, AuditMixin, CreatedByMixin, SoftDeleteMixin):
    """ Abstract base class for all models """
    __abstract__ = True
