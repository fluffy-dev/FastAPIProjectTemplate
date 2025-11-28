from typing import Annotated
from fastapi import Depends, HTTPException, status

from src.auth.service.token import TokenService
from src.auth.dependencies.user_repository import IUserRepository
from src.auth.dto import BaseUserDTO, AccessTokenDTO
from src.auth.exceptions import UserNotFound


async def get_current_user(token: AccessTokenDTO, user_repo: IUserRepository) -> BaseUserDTO:
    """
    Dependency to get the current user from a JWT token.

    Verifies the token, extracts the user ID, and fetches the user
    from the database.

    Raises:
        HTTPException(401): If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = token.access_token

    payload = TokenService.verify_token(access_token)

    if payload is None or payload.sub is None:
        raise credentials_exception

    user_id = int(payload.sub)
    try:
        user = await user_repo.get(user_id) #TODO restrict using repository from interface level, instead use service
        return user
    except UserNotFound:
        raise credentials_exception

ICurrentUser: type[BaseUserDTO] = Annotated[BaseUserDTO, Depends(get_current_user)]