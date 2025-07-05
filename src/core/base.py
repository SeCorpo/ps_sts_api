from sqlalchemy.orm import declarative_base, DeclarativeMeta
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

Base: DeclarativeMeta = declarative_base()

class AuditMixin:
    """ Mixin for created/updated timestamps """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class BaseModel(AuditMixin, Base):
    """ Abstract base class for all models. Only includes audit fields """
    __abstract__ = True
