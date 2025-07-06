from fastapi import HTTPException, status

SESSION_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Session not found."
)

SESSION_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Session has expired. Please log in again."
)
