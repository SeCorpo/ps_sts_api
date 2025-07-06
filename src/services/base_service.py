from typing import Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select
from src.core.base import BaseModel

from src.core.utils.logger import get_logger

logger = get_logger("services.base_service")

T = TypeVar('T', bound=BaseModel)

async def get_by_field(db: AsyncSession, model: Type[T], **filters) -> Optional[T]:
    """Get a single object by field(s)."""
    try:
        stmt = select(model).filter_by(**filters)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except (NoResultFound, SQLAlchemyError) as e:
        logger.error(f"Error fetching {model.__name__} with {filters}: {e}")
        return None

async def get_all(db: AsyncSession, model: Type[T], **filters) -> List[T]:
    """Get all objects for a model, optionally filtered by fields."""
    try:
        stmt = select(model)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all {model.__name__} with {filters}: {e}")
        return []

async def create(db: AsyncSession, model: Type[T], **data) -> Optional[T]:
    """Create a new object."""
    try:
        obj = model(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating {model.__name__}: {e}")
        return None

async def update(db: AsyncSession, obj: T, **data) -> Optional[T]:
    """Update an object and commit."""
    try:
        for key, value in data.items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error updating {type(obj).__name__}: {e}")
        return None

async def delete(db: AsyncSession, obj: T) -> bool:
    """Delete an object."""
    try:
        await db.delete(obj)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error deleting {type(obj).__name__}: {e}")
        return False
