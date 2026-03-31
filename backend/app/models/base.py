from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.orm import declared_attr
from ..core.database import Base


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)


class IDMixin:
    """Simple id-only mixin for banner-like models."""
    id = Column(Integer, primary_key=True, autoincrement=True)


class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
