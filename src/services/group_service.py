from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.exceptions import INTEGRITY_ERROR, GROUP_NAME_ALREADY_EXISTS, GROUP_NOT_FOUND, USER_NOT_FOUND, \
    GROUP_USERTYPE_NOT_ALLOWED, GROUP_UNABLE_TO_CREATE, GROUP_USERTYPE_NOT_FOUND, \
    GROUP_MEMBER_EMAILS_EMPTY, NO_VALUE_PROVIDED, GROUP_UNABLE_TO_CREATE_ALLOWED_USERTYPE, \
    GROUP_UNABLE_TO_ADD_USER_TO_GROUP
from src.models import Group, GroupUser, GroupUsertype
from src.schemas import GroupCreateSchema, GroupUsertypeSchema, GroupUserSchema, GroupIsActiveSchema, \
    GroupNameSchema, GroupChangeNameSchema
from src.services import update, get_by_field, create, delete, get_user_obj_by_email, get_by_field_force


async def get_group_by_name(db: AsyncSession, group_name: str) -> Optional[Group]:
    return await get_by_field(db, Group, name=group_name)
async def get_group_by_name_force(db: AsyncSession, group_name: str) -> Optional[Group]:
    return await get_by_field_force(db, Group, name=group_name)


async def update_group_is_active(
        db: AsyncSession,
        schema: GroupIsActiveSchema,
):
    if schema.group_is_active is None:
        raise NO_VALUE_PROVIDED

    group = await get_group_by_name(db, schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    try:
        await update(db, group, is_active=schema.group_is_active)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def toggle_group_allowed_user_type(
        db: AsyncSession,
        schema: GroupUsertypeSchema,
        created_by_user_id: Optional[int] = None,
        add: bool = True,
):
    if not schema.group_usertypes:
        raise GROUP_USERTYPE_NOT_FOUND

    group = await get_group_by_name(db, schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    for usertype in schema.group_usertypes:
        group_allowed_usertype = await get_by_field(db, GroupUsertype, group_id=group.group_id, usertype=usertype)

        if add:
            if group_allowed_usertype is None:
                try:
                    obj = GroupUsertype(
                        group_id=group.group_id,
                        usertype=usertype,
                        created_by_user_id=created_by_user_id,
                    )
                    await create(db, obj)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR
                except Exception:
                    await db.rollback()
                    raise GROUP_UNABLE_TO_CREATE_ALLOWED_USERTYPE
        else:
            if group_allowed_usertype is not None:
                try:
                    await delete(db, group_allowed_usertype)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR


async def toggle_group_user(
        db: AsyncSession,
        schema: GroupUserSchema,
        created_by_user_id: Optional[int] = None,
        add: bool = True
):
    if not schema.group_member_emails:
        raise GROUP_MEMBER_EMAILS_EMPTY

    group = await get_group_by_name(db, schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    for member_email in schema.group_member_emails:
        user = await get_user_obj_by_email(db, str(member_email))
        if user is None:
            raise USER_NOT_FOUND

        if user.usertype not in group.usertypes:
            raise GROUP_USERTYPE_NOT_ALLOWED

        group_user = await get_by_field(db, GroupUser, group_id=group.group_id, user_id=user.user_id)

        if add:
            if group_user is None:
                try:
                    obj = GroupUser(
                        group_id=group.group_id,
                        user_id=user.user_id,
                        created_by_user_id=created_by_user_id,
                    )
                    await create(db, obj)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR
                except Exception:
                    await db.rollback()
                    raise GROUP_UNABLE_TO_ADD_USER_TO_GROUP
        else:
            if group_user is not None:
                try:
                    await delete(db, group_user)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR


async def create_group(
        db: AsyncSession,
        schema: GroupCreateSchema,
        created_by_user_id: Optional[int] = None,
) -> Optional[Group]:
    #  group.name is not available after soft deleting
    group = await get_group_by_name_force(db, schema.group_name)
    if group:
        raise GROUP_NAME_ALREADY_EXISTS
    try:
        group = Group(
            name=schema.group_name,
            is_active=schema.group_is_active,
            created_by_user_id=created_by_user_id,
        )
        await create(db, group)
        if group is None:
            raise GROUP_UNABLE_TO_CREATE
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR
    except Exception:
        await db.rollback()
        raise GROUP_UNABLE_TO_CREATE

    if schema.group_usertypes:
        for usertype in schema.group_usertypes:
            group_allowed_usertype = await get_by_field(db, GroupUsertype, group_id=group.group_id, usertype=usertype)
            if group_allowed_usertype is None:
                try:
                    obj = GroupUsertype(
                        group_id=group.group_id,
                        usertype=usertype,
                        created_by_user_id=created_by_user_id,
                    )
                    await create(db, obj)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR
                except Exception:
                    await db.rollback()
                    raise GROUP_UNABLE_TO_CREATE_ALLOWED_USERTYPE

    if schema.group_member_emails:
        for member_email in schema.group_member_emails:
            user = await get_user_obj_by_email(db, str(member_email))
            if user is None:
                raise USER_NOT_FOUND

            if user.usertype not in group.usertypes:
                raise GROUP_USERTYPE_NOT_ALLOWED

            group_user = await get_by_field(db, GroupUser, group_id=group.group_id, user_id=user.user_id)
            if group_user is None:
                try:
                    obj = GroupUser(
                        group_id=group.group_id,
                        user_id=user.user_id,
                        created_by_user_id=created_by_user_id,
                    )
                    await create(db, obj)
                except IntegrityError:
                    await db.rollback()
                    raise INTEGRITY_ERROR
                except Exception:
                    await db.rollback()
                    raise GROUP_UNABLE_TO_ADD_USER_TO_GROUP
    return group


async def delete_group(
        db: AsyncSession,
        schema: GroupNameSchema,
) -> None:
    """ Function to soft delete a group, setting deleted status """
    group = await get_group_by_name(db, schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    try:
        await delete(db, group)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR


async def update_group_name(
        db: AsyncSession,
        schema: GroupChangeNameSchema,
) -> Optional[Group]:
    group = await get_group_by_name(db, schema.group_name)
    if group is None:
        raise GROUP_NOT_FOUND

    #  check if group.name is available, also among soft deleted groups
    new_name_group = await get_group_by_name_force(db, schema.new_group_name)
    if new_name_group:
        raise GROUP_NAME_ALREADY_EXISTS

    try:
        await update(db, group, name=schema.new_group_name)
    except IntegrityError:
        await db.rollback()
        raise INTEGRITY_ERROR
