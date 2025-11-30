from fastapi import APIRouter, Response

from src.auth.dependencies.auth.service import IAuthService
from src.auth.dto import TokenDTO, LoginDTO, UserDTO, RegistrationDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenDTO)
async def login(response: Response, dto: LoginDTO, service: IAuthService):
    """
    Provides access and refresh tokens for a valid user.
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
    Registers a new user via RegistrationDTO.
    """
    return await service.register(dto)