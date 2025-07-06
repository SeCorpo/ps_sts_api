from fastapi import HTTPException, status

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password."
)

INACTIVE_ACCOUNT = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Account is inactive."
)

ACCOUNT_LOCKED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Account is locked due to too many failed attempts."
)

EMAIL_NOT_VERIFIED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Please verify your email address before logging in."
)

PASSWORD_EXPIRED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Password has expired, please reset your password."
)

TOO_MANY_ATTEMPTS = HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Too many login attempts. Please wait and try again later."
)
