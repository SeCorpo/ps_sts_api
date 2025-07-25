from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import PERSON_EMAIL_NOT_AVAILABLE, PERSON_UNABLE_TO_CREATE, INTEGRITY_ERROR
from src.models import Person
from src.schemas import PersonSchema
from src.services import get_by_field, get_by_field_force, create


async def get_person_by_email(db: AsyncSession, email: str) -> Optional[Person]:
    return await get_by_field(db, Person, email=email)
async def get_person_by_email_force(db: AsyncSession, email: str) -> Optional[Person]:
    return await get_by_field_force(db, Person, email=email)


async def create_person(
        db: AsyncSession,
        schema: PersonSchema,
        created_by_user_id: Optional[int] = None,
) -> PersonSchema:
    person = await get_person_by_email_force(db, str(schema.email))
    if person is None:
        try:
            obj = schema.to_model(Person)
            obj.created_by_user_id = created_by_user_id
            person = await create(db, obj)
            if person is None:
                raise PERSON_UNABLE_TO_CREATE
            return PersonSchema.from_orm(person)
        except IntegrityError:
            await db.rollback()
            raise INTEGRITY_ERROR
        except Exception:
            await db.rollback()
            raise PERSON_UNABLE_TO_CREATE
    raise PERSON_EMAIL_NOT_AVAILABLE