from fastapi import HTTPException, status

EMAIL_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="An account with this email already exists."
)

USERNAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="An account with this username already exists."
)

WEAK_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Password does not meet complexity requirements."
)

INVALID_EMAIL_FORMAT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid email format."
)
