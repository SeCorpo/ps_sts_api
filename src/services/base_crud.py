from typing import Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select
from src.core import BaseModel, get_logger


"""
get_by_field: for normal use, no need to modify deleted objects
get_by_field_force: for use when modifying unique values, e.g. create functions

get_all:
get_all_force:

delete: for normal use
delete_force: for special use, e.g. not storing personal data or when AdminOrganisation (possibly AdminSchool)
"""
logger = get_logger("services.base_crud")

T = TypeVar('T', bound=BaseModel)

async def get_by_field(db: AsyncSession, model: Type[T], **filters) -> Optional[T]:
    """ Get a single object by field(s), excluding deleted """
    try:
        query = select(model).filter_by(**filters, deleted=False)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except (NoResultFound, SQLAlchemyError) as e:
        logger.error(f"Error fetching {model.__name__} with {filters}: {e}")
        return None

async def get_all(db: AsyncSession, model: Type[T], **filters) -> List[T]:
    """ Get all objects for a model, optionally filtered by fields, excluding deleted """
    try:
        query = select(model)
        if filters:
            query = query.filter_by(**filters, deleted=False)
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all {model.__name__} with {filters}: {e}")
        return []

async def create(db: AsyncSession, obj: T) -> Optional[T]:
    """ Create a new object """
    try:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating {type(obj).__name__}: {e}")
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
    """ Set an object as deleted """
    try:
        setattr(obj, 'deleted', True)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error deleting {type(obj).__name__}: {e}")
        return False


async def get_by_field_force(db: AsyncSession, model: Type[T], **filters) -> Optional[T]:
    """ Get a single object by field(s), including objects with deleted=True """
    try:
        query = select(model).filter_by(**filters)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except (NoResultFound, SQLAlchemyError) as e:
        logger.error(f"Error fetching {model.__name__} with {filters}: {e}")
        return None

async def get_all_force(db: AsyncSession, model: Type[T], **filters) -> List[T]:
    """ Get all objects for a model, optionally filtered by fields, including objects with deleted=True """
    try:
        query = select(model)
        if filters:
            query = query.filter_by(**filters)
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all {model.__name__} with {filters}: {e}")
        return []

async def delete_force(db: AsyncSession, obj: T) -> bool:
    """ Delete an object from database """
    try:
        await db.delete(obj)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error deleting {type(obj).__name__}: {e}")
        return False
