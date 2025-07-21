from fastapi import HTTPException, status

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found."
)

USER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with this email already exists."
)

USER_INACTIVE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User account is inactive."
)

USER_NOT_PERMITTED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User does not have permission for this action."
)

USER_INVALID_EMAIL = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Provided email address is invalid."
)

USERTYPE_INVALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Provided usertype is invalid."
)

USER_EMAIL_NOT_VERIFIED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User email address is not verified."
)

USER_DELETED = HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="User account has been deleted."
)
