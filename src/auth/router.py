from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies.auth.service import IAuthService
from src.auth.exceptions import UserNotFound
from src.auth.dto import TokenDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=TokenDTO)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: IAuthService
):
    """
    Provides access and refresh tokens for a valid user.
    """
    try:
        tokens = await service.login(form_data)
        return tokens
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )