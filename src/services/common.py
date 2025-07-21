from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User, Person
from src.services import get_by_field


async def get_user_obj_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """ Function to get user via its persons email, only for use in service layer (after schema) """
    person = await get_by_field(db, Person, email=email)
    if person and person.user:
        return person.user
    return None
