from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from base_service import get_by_field, create, filtered_schema_for_model, delete
from src.exceptions import INTEGRITY_ERROR, GROUP_NAME_ALREADY_EXISTS, GROUP_NOT_FOUND, USER_NOT_FOUND, \
    GROUP_USER_TYPE_NOT_ALLOWED, GROUP_UNABLE_TO_CREATE, GROUP_USER_TYPE_NOT_FOUND, GROUP_MEMBER_NOT_FOUND
from src.models import Group, Person, User
from src.models.associations import GroupAllowedUserType, GroupUser
from src.schemas import GroupCreateSchema
from src.schemas.group import GroupAllowedUserTypeCreateSchema, GroupUserCreateSchema, FindGroupSchema, \
    FindGroupAllowedUserTypeSchema, FindGroupUserSchema


async def create_group(db: AsyncSession, schema: GroupCreateSchema, created_by_user_id: Optional[int] = None) -> Optional[Group]:
    """ Function to create a new group, and depending on the received schema add allowed user_type restrictions or add members """
    existing = await get_by_field(db, Group, name=schema.name)
    if existing:
        raise GROUP_NAME_ALREADY_EXISTS

    try:
        filtered_schema = filtered_schema_for_model(Group, schema)
        group = await create(db, Group, filtered_schema, created_by_user_id=created_by_user_id)
        if group is None:
            raise GROUP_UNABLE_TO_CREATE

        for user_type in schema.allowed_user_types:
            user_type_schema = GroupAllowedUserTypeCreateSchema(group_id=group.group_id, user_type=user_type)
            await create_group_allowed_user_type(db, user_type_schema, created_by_user_id=created_by_user_id)

        for member_email in schema.member_emails:
            member_email_schema = GroupUserCreateSchema(group_id=group.group_id, user_id=member_email)
            await create_group_user(db, member_email_schema, created_by_user_id=created_by_user_id)

    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def create_group_allowed_user_type(db: AsyncSession, schema: GroupAllowedUserTypeCreateSchema, created_by_user_id: Optional[int] = None) -> Optional[GroupAllowedUserType]:
    """ Function to add a single allowed UserType to the group, group_id could be group name or group_id """
    if isinstance(schema.group_id, str):
        group_existing = await get_by_field(db, Group, name=schema.group_id)
        if group_existing is None:
            raise GROUP_NOT_FOUND
        schema = GroupAllowedUserTypeCreateSchema(
            group_id=group_existing.group_id,
            user_type=schema.user_type
        )

    else:
        group_existing = await get_by_field(db, Group, group_id=schema.group_id)
        if group_existing is None:
            raise GROUP_NOT_FOUND

    existing = await get_by_field(db, GroupAllowedUserType, group_id=schema.group_id, user_type=schema.user_type)
    if existing:
        return existing

    try:
        group_allowed_user_type = await create(db, GroupAllowedUserType, schema, created_by_user_id=created_by_user_id)
        return group_allowed_user_type
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def create_group_user(db: AsyncSession, schema: GroupUserCreateSchema, created_by_user_id: Optional[int] = None) -> Optional[GroupUser]:
    """ Function to add a single User to a group, group_id could be group name or group_id """
    if isinstance(schema.group_id, str):
        group_existing = await get_by_field(db, Group, name=schema.group_id)
        if group_existing is None:
            raise GROUP_NOT_FOUND

    else:
        group_existing = await get_by_field(db, Group, group_id=schema.group_id)
        if group_existing is None:
            raise GROUP_NOT_FOUND

    #  make sure the person (by email (named user_id in schema)) exists and has a user
    person_existing = await get_by_field(db, Person, email=schema.user_id)
    if person_existing is None or not person_existing.user:
        raise USER_NOT_FOUND
    user = person_existing.user

    if user.user_type not in group_existing.allowed_user_types:
        raise GROUP_USER_TYPE_NOT_ALLOWED

    schema = GroupUserCreateSchema(
        group_id=group_existing.group_id,
        user_id=user.user_id,
    )

    existing = await get_by_field(db, GroupUser, group_id=schema.group_id, user_id=schema.user_id)
    if existing:
        return existing

    try:
        group_user = await create(db, GroupUser, schema, created_by_user_id=created_by_user_id)
        return group_user
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def delete_group(db: AsyncSession, schema: FindGroupSchema) -> None:
    """ Function to delete a group, including associated objects """
    group = await get_by_field(db, Group, name=schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    try:
        await delete(db, group)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def delete_group_allowed_user_type(db: AsyncSession, schema: FindGroupAllowedUserTypeSchema) -> None:
    """ Function to remove a single allowed UserType from a group """
    group = await get_by_field(db, Group, name=schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    group_allowed_user_type = await get_by_field(db, GroupAllowedUserType, group_id=group.group_id, user_type=schema.user_type)
    if group_allowed_user_type is None:
        raise GROUP_USER_TYPE_NOT_FOUND

    try:
        await delete(db, group_allowed_user_type)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def delete_group_user(db: AsyncSession, schema: FindGroupUserSchema) -> None:
    """ Function to remove a single User from a group """
    #  get group_id
    group = await get_by_field(db, Group, name=schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND
    #  get user_id
    person = await get_by_field(db, Person, email=schema.user_email)
    if person is None or not person.user:
        raise USER_NOT_FOUND
    user = person.user

    group_user = await get_by_field(db, GroupUser, group_id=group.group_id, user_id=user.user_id)
    if group_user is None:
        raise GROUP_MEMBER_NOT_FOUND

    try:
        await delete(db, group_user)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR