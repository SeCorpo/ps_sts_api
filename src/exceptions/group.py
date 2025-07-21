from fastapi import HTTPException, status

GROUP_NAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A group with this name already exists."
)

GROUP_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Group not found."
)

GROUP_INACTIVE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="This group is inactive."
)

GROUP_MEMBER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This user is already a member of the group."
)

GROUP_MEMBER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Group member not found."
)

GROUP_OPERATION_FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to perform this group operation."
)

GROUP_USERTYPE_NOT_ALLOWED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="This usertype is not allowed for this group."
)

GROUP_UNABLE_TO_CREATE = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unable to create group due to an internal error."
)

GROUP_USERTYPE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="This group does not have the specified usertype."
)

GROUP_MEMBER_EMAILS_EMPTY = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No member emails were provided for the group."
)

GROUP_UNABLE_TO_CREATE_ALLOWED_USERTYPE = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unable to add allowed usertype to the group."
)

GROUP_UNABLE_TO_ADD_USER_TO_GROUP = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unable to add user to the group."
)
