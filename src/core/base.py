from sqlalchemy.orm import declarative_base, DeclarativeMeta
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func

Base: DeclarativeMeta = declarative_base()

class AuditMixin:
    """ Mixin for created/updated timestamps """
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreatedByMixin:
    """Mixin for created_by_user_id field """
    created_by_user_id = Column("created_by_user_id", Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)

class SoftDeleteMixin:
    """ Mixin for deleted field """
    deleted = Column("deleted", Boolean, default=False, nullable=False)

class BaseModel(Base, AuditMixin, CreatedByMixin, SoftDeleteMixin):
    """ Abstract base class for all models """
    __abstract__ = True
