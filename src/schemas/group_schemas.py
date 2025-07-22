from typing import Optional, Set
from pydantic import field_validator, constr, EmailStr, Field
from src.constants import Usertype
from src.core import BaseSchema


class GroupNameSchema(BaseSchema):
    name: constr(max_length=64)

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        if v is None:
            raise ValueError("Group name cannot be empty.")
        return v


class GroupSchema(GroupNameSchema):
    """ No need for a GroupCreateSchema or GroupUpdateSchema, since Group doesn't have 'normal' information fields (for now) """
    is_active: Optional[bool]
    group_usertypes: Optional[Set[Usertype]] = Field(default_factory=set)
    group_member_emails: Optional[Set[EmailStr]] = Field(default_factory=set)


class GroupChangeNameSchema(GroupNameSchema):
    new_name: constr(max_length=64)

    @field_validator("new_name", mode="before")
    def validate_name(cls, v):
        if v is None:
            raise ValueError("Group name cannot be empty.")
        return v