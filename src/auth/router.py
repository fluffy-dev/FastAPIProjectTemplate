from fastapi import APIRouter

from src.auth.dependencies.auth.service import IAuthService
from src.auth.dto import TokenDTO, LoginDTO, UserDTO, RegistrationDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenDTO)
async def login(dto: LoginDTO,service: IAuthService):
    """
    Provides access and refresh tokens for a valid user.
    """
    return await service.login(dto)


@router.post("/register", response_model=UserDTO)
async def register(dto: RegistrationDTO, service: IAuthService):
    """
    Registers a new user via RegistrationDTO.
    """
    return await service.register(dto)