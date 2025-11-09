# app/application/exceptions/base.py
from fastapi import HTTPException, status


class ApplicationError(HTTPException):
    def __init__(self, detail: str = "Application error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class InvalidCredentialsError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
        )


class UserAlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidTokenError(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class DocumentNotFoundError(HTTPException):
    def __init__(self, detail: str = "Document not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
