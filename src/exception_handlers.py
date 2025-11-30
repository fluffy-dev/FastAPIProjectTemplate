from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.auth.exceptions.token import AccessTokenMissing, RefreshTokenMissing
from src.libs.exceptions import NotFound, AlreadyExists, PaginationError
from src.auth.exceptions.token import InvalidSignatureError
from src.auth.exceptions.auth import CredentialsException


async def not_found_exception_handler(request: Request, exc: NotFound):
    """
    Handles NotFound exceptions, returning a 404 response.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "Resource not found."},
    )

async def already_exists_exception_handler(request: Request, exc: AlreadyExists):
    """
    Handles AlreadyExists exceptions, returning a 409 response.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc) or "Resource already exists."},
    )

async def pagination_exception_handler(request: Request, exc: PaginationError):
    """
    Handles PaginationError exceptions, returning a 400 response.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc) or "Pagination error, offset or limit invalid."},
    )

async def token_invalid_signature_exception_handler(request: Request, exc: InvalidSignatureError):
    """
    Handles InvalidSignatureError exceptions, returning a 400 response.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc) or "Token invalid."},
    )


async def credentials_exception_handler(request: Request, exc: CredentialsException):
    """Handles CredentialsError exceptions, returning a 400 response."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc) or "Credentials error, login or password invalid."},
    )

async def access_token_missing_handler(request: Request, exc: AccessTokenMissing):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc) or "Access token missing", "code": "access_token_missing"}
    )

async def refresh_token_missing_handler(request: Request, exc: RefreshTokenMissing):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc) or "Refresh token missing", "code": "refresh_token_missing"}
    )

exception_handlers = {
    NotFound: not_found_exception_handler,
    AlreadyExists: already_exists_exception_handler,
    PaginationError: pagination_exception_handler,
    InvalidSignatureError: token_invalid_signature_exception_handler,
    CredentialsException: credentials_exception_handler,
    AccessTokenMissing: access_token_missing_handler,
    RefreshTokenMissing: refresh_token_missing_handler,
}
