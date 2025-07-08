from pydantic import BaseModel, constr, EmailStr, field_validator, Field
from typing import Set, Optional, Union
from src.models.user_types.UserType import UserType

class GroupCreateSchema(BaseModel):
    name: constr(max_length=128)
    allowed_user_types: Set[UserType] = Field(default_factory=set)
    member_emails: Set[EmailStr] = Field(default_factory=set)
    is_active: Optional[bool] = True

    @field_validator("name", mode="before")
    def normalize_name(cls, v):
        return v.strip() if isinstance(v, str) else v


class GroupAllowedUserTypeCreateSchema(BaseModel):
    group_id: Union[int, constr(max_length=128)]
    user_type: UserType

    @field_validator("group", mode="before")
    def validate_group(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Group name cannot be empty.")
        return v


class GroupUserCreateSchema(BaseModel):
    group_id: Union[int, constr(max_length=128)]
    user_id: EmailStr

    @field_validator("group", mode="before")
    def validate_group(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Group name cannot be empty.")
        return v