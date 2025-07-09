from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional, Literal
from datetime import date

class PersonCreateSchema(BaseModel):
    email: EmailStr
    first_name: constr(max_length=64)
    infix: Optional[constr(max_length=32)] = None
    last_name: constr(max_length=64)
    date_of_birth: date
    sex: Literal['m', 'f', 'o']

    street: Optional[constr(max_length=64)] = None
    house_number: Optional[constr(max_length=6)] = None
    postal_code: Optional[constr(max_length=6)] = None
    city: Optional[constr(max_length=64)] = None
    country: Optional[constr(max_length=64)] = None

    @field_validator("email", mode="before")
    def normalize_email(cls, v):
        return v.lower().strip() if isinstance(v, str) else v