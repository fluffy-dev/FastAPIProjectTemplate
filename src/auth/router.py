from typing import Annotated, Union

from fastapi import APIRouter, Response, Cookie, Request, Header

from src.auth.exceptions.token import RefreshTokenMissing
from src.auth.dependencies.auth.service import IAuthService
from src.auth.dto import TokenPairDTO, LoginDTO, UserDTO, RegistrationDTO, UserSessionInfoDTO
from src.auth.dependencies.current_user import ICurrentUser
from src.auth.service.cookie import set_auth_cookies, clear_auth_cookies
router = APIRouter(prefix="/auth", tags=["Authentication"])



@router.post(
    "/login",
    response_model=TokenPairDTO,
)
async def login(
    response: Response,
    request: Request,
    dto: LoginDTO,
    service: IAuthService,
    user_agent: Annotated[str | None, Header()] = None,
):
    """
    Authenticates a user and sets secure cookies.

    This endpoint verifies credentials and returns JWT tokens in the response body.
    Additionally, it sets `HttpOnly` cookies for `access_token` and `refresh_token`
    to support browser-based clients securely.

    Args:
        response (Response): FastAPI response object used to set cookies.
        dto (LoginDTO): The user credentials.
        service (IAuthService): The authentication service dependency.
        request (Request): The incoming HTTP request.
        user_agent (Headers): data about user client.

    Returns:
        TokenDTO: The access and refresh tokens.
    """
    session_info = UserSessionInfoDTO(
        user_agent=user_agent,
        ip_address=request.client.host if request.client else None,
    )

    tokens = await service.login(
        login_dto=dto,
        user_session_dto=session_info
    )

    set_auth_cookies(response, tokens)

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

@router.post("/refresh", response_model=TokenPairDTO)
async def refresh(
        response: Response,
        service: IAuthService,
        refresh_token: Annotated[Union[str, None], Cookie()] = None
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

    set_auth_cookies(response, new_tokens)

    return new_tokens

@router.post("/logout")
async def logout(
        response: Response,
        service: IAuthService,
        refresh_token: Annotated[Union[str, None], Cookie()] = None
):
    """
    Logs out the user by revoking the specific session.
    """

    if refresh_token:
        await service.logout(refresh_token)

    clear_auth_cookies(response)
    return {"message": "Logged out successfully"}


@router.post("/logout_all_sessions")
async def logout_all_sessions(
        response: Response,
        service: IAuthService,
        refresh_token: Annotated[Union[str, None], Cookie()] = None
):
    """
    Logs out all user sessions.
    """
    if refresh_token:
        await service.logout_all_sessions_for_user(refresh_token)

    clear_auth_cookies(response)
    return {"message": "Logged out successfully"}
