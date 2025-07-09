from typing import Optional, Set
from pydantic import BaseModel, field_validator, constr, EmailStr, Field
from src.models import UserType


class GroupNameSchema(BaseModel):
    group_name: constr(max_length=64)

    @field_validator("group_name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Group name cannot be empty.")
        return v

class GroupIsActiveSchema(GroupNameSchema):
    group_is_active: Optional[bool]

class GroupAllowedUserTypeSchema(GroupNameSchema):
    group_allowed_user_types: Optional[Set[UserType]] = Field(default_factory=set)

class GroupUserSchema(GroupNameSchema):
    group_member_emails: Optional[Set[EmailStr]] = Field(default_factory=set)


class GroupCreateSchema(GroupNameSchema):
    group_is_active: Optional[bool]
    group_allowed_user_types: Optional[Set[UserType]] = Field(default_factory=set)
    group_member_emails: Optional[Set[EmailStr]] = Field(default_factory=set)

class GroupChangeNameSchema(GroupNameSchema):
    new_group_name: constr(max_length=64)

    @field_validator("new_group_name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Group name cannot be empty.")
        return v