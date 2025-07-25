from fastapi import HTTPException, status

PERSON_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Person not found."
)

PERSON_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A person with this identifier already exists."
)

PERSON_INACTIVE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Person record is inactive."
)

PERSON_NOT_PERMITTED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to access this person."
)

PERSON_INVALID_DATA = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Provided person data is invalid."
)

PERSON_AGE_INVALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Provided age is invalid."
)

PERSON_EMAIL_INVALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Provided email address for person is invalid."
)

PERSON_DELETED = HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="Person record has been deleted."
)

PERSON_EMAIL_NOT_VERIFIED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Person's email address is not verified."
)

PERSON_EMAIL_NOT_AVAILABLE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="This email address is unavailable."
)

PERSON_UNABLE_TO_CREATE = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failure to create the person."
)