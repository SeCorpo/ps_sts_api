from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from base_service import get_by_field, create
from src.exceptions import EMAIL_ALREADY_EXISTS, INTEGRITY_ERROR
from src.models import Person
from src.schemas.person import PersonCreateSchema


async def create_person(db: AsyncSession, schema: PersonCreateSchema) -> Optional[Person]:
    existing = await get_by_field(db, Person, email=schema.email)
    if existing:
        raise EMAIL_ALREADY_EXISTS

    try:
        person = await create(db, Person, schema)
        return person
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR