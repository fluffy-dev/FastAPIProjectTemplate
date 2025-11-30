from fastapi import APIRouter, Response

from src.auth.dependencies.auth.service import IAuthService
from src.auth.dto import TokenDTO, LoginDTO, UserDTO, RegistrationDTO
from src.auth.dependencies.current_user import ICurrentUser

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
        samesite="none",
        secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
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