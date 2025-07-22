from datetime import date
from typing import Optional, Literal
from pydantic import EmailStr, constr, field_validator
from src.core import BaseSchema


class PersonEmailSchema(BaseSchema):
    email: EmailStr

    @field_validator("email", mode="before")
    def normalize_email(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if not v:
                raise ValueError("Email address cannot be empty.")
        return v


class PersonCreateSchema(PersonEmailSchema):
    """ Address not required for now """
    first_name: constr(min_length=1, max_length=64)
    infix: Optional[constr(max_length=32)] = None
    last_name: constr(min_length=1, max_length=64)
    date_of_birth: date
    sex: Literal['m', 'f', 'o']

    street: Optional[constr(max_length=64)] = None
    house_number: Optional[constr(max_length=6)] = None
    postal_code: Optional[constr(max_length=6)] = None
    city: Optional[constr(max_length=64)] = None
    country: Optional[constr(max_length=64)] = None


class PersonUpdateSchema(PersonEmailSchema):
    """ Complete schema, with all fields optional, not for creating """
    first_name: Optional[constr(min_length=1, max_length=64)] = None
    infix: Optional[constr(max_length=32)] = None
    last_name: Optional[constr(min_length=1, max_length=64)] = None
    date_of_birth: Optional[date] = None
    sex: Optional[Literal['m', 'f', 'o']] = None

    street: Optional[constr(max_length=64)] = None
    house_number: Optional[constr(max_length=6)] = None
    postal_code: Optional[constr(max_length=6)] = None
    city: Optional[constr(max_length=64)] = None
    country: Optional[constr(max_length=64)] = None
