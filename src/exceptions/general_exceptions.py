from fastapi import HTTPException, status

INTEGRITY_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unable to process your request due to a data conflict."
)

NO_VALUE_PROVIDED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Required input value was not provided."
)