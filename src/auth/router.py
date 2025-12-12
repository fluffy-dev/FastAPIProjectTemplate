from typing import Annotated, Union

from fastapi import APIRouter, Response, Cookie

from src.auth.exceptions.token import RefreshTokenMissing
from src.auth.dependencies.auth.service import IAuthService
from src.auth.dto import TokenDTO, LoginDTO, UserDTO, RegistrationDTO
from src.auth.dependencies.current_user import ICurrentUser
from src.config.jwt import settings as jwt_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenDTO)
async def login(response: Response, dto: LoginDTO, service: IAuthService):
    """
    Authenticates a user and sets secure cookies.

    This endpoint verifies credentials and returns JWT tokens in the response body.
    Additionally, it sets `HttpOnly` cookies for `access_token` and `refresh_token`
    to support browser-based clients securely.

    Args:
        response (Response): FastAPI response object used to set cookies.
        dto (LoginDTO): The user credentials.
        service (IAuthService): The authentication service dependency.

    Returns:
        TokenDTO: The access and refresh tokens.
    """
    tokens = await service.login(dto)

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_settings.access_token_expire_seconds,
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_settings.refresh_token_rotate_min_lifetime,
    )

    return tokens


@router.post("/register", response_model=UserDTO)
async def register(dto: RegistrationDTO, service: IAuthService):
    """
    Registers a new user account.

    Args:
        dto (RegistrationDTO): The user registration information.
        service (IAuthService): The authentication service dependency.

    Returns:
        UserDTO: The created user's public profile information.
    """
    return await service.register(dto)


@router.get("/me", response_model=UserDTO, summary="Get current user profile")
async def read_users_me(current_user: ICurrentUser):
    """
    Retrieves the profile of the currently authenticated user.

    This endpoint requires a valid JWT token (via cookie or header).

    Args:
        current_user (UserDTO): The authenticated user (injected by dependency).

    Returns:
        UserDTO: The user's profile data.
    """
    return current_user


@router.post("/refresh", response_model=TokenDTO)
async def refresh_token(
    response: Response,
    service: IAuthService,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
):
    """
    Refreshes the Access Token using a HttpOnly Refresh Token.

    This endpoint is called when the Access Token expires. It reads the
    'refresh_token' cookie, verifies it, and issues a new pair of tokens.

    Args:
        response (Response): FastAPI response to set the new cookies.
        service (IAuthService): The auth service logic.
        refresh_token (str, optional): Automatically extracted from cookies.

    Returns:
        TokenDTO: The new tokens (also sets them in cookies).

    Raises:
        HTTPException(401): If the refresh token is missing, invalid, or expired.
    """
    if not refresh_token:
        raise RefreshTokenMissing()

    new_tokens = await service.refresh_session(refresh_token)

    response.set_cookie(
        key="access_token",
        value=new_tokens.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_settings.access_token_expire_seconds,
    )

    response.set_cookie(
        key="refresh_token",
        value=new_tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_settings.refresh_token_rotate_min_lifetime,
    )

    return new_tokens
