from typing import Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select
from src.core.base import BaseModel
from pydantic import BaseModel as PydanticBaseModel

from src.core.utils.logger import get_logger
from src.models import User, Person

"""
get_by_field: for normal use, no need to modify deleted objects
get_by_field_force: for use when modifying unique values, e.g. create functions

get_all:
get_all_force:

delete: for normal use
delete_force: for special use, e.g. not storing personal data or when AdminOrganisation (possibly AdminSchool)
"""
logger = get_logger("services.base_service")

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


def filtered_schema_for_model(model: Type[T], schema: PydanticBaseModel) -> PydanticBaseModel:
    """ Helper function for when the received schema includes fields that are not in the model, to prevent typeerror """
    """
    Return a generic Pydantic BaseModel instance containing only the fields
    that are valid columns on the SQLAlchemy model.
    """
    model_fields = {field: getattr(schema, field)
                    for field in model.__table__.columns.keys()
                    if hasattr(schema, field)}
    return PydanticBaseModel.model_validate(model_fields)


async def get_user_obj_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """ Function to get user via its persons email, only for use in service layer (after schema) """
    person = await get_by_field(db, Person, email=email)
    if person and person.user:
        return person.user
    return None