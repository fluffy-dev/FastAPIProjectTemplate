from typing import Annotated, Union
from fastapi import Depends, Cookie
from src.auth.dependencies.token.service import ITokenService
from src.auth.dependencies.user.service import IUserService
from src.auth.dto import UserDTO
from src.auth.exceptions.token import InvalidTokenError, AccessTokenMissing


async def get_current_user(
    user_service: IUserService,
    token_service: ITokenService,
    access_token: Annotated[Union[str, None], Cookie()] = None,
) -> UserDTO:
    """
    FastAPI Dependency to retrieve the authenticated user from a Cookie.

    1. Extracts the 'access_token' cookie.
    2. Decodes and verifies the JWT signature and expiration.
    3. Extracts the 'user_id' from the token payload.
    4. Fetches the full user record from the database.

    Args:
        user_service (IUserService): Service to fetch user data.
        token_service (ITokenService): Service to decode tokens.
        access_token (str, optional): The JWT string extracted from cookies.

    Returns:
        UserDTO: The authenticated user's data.

    Raises:
        InvalidTokenError: If the token is missing, invalid, expired, or the user
                           ID in the payload does not exist in the database.
    """

    if access_token is None:
        raise AccessTokenMissing()

    payload: dict = await token_service.decode_token(access_token)

    user_id = payload.get("user", {}).get("user_id")

    if user_id is None:
        raise InvalidTokenError

    user_id = int(user_id)

    user = await user_service.get(user_id)

    if user is None:
        raise InvalidTokenError

    return UserDTO(
        id=user.id,
        name=user.name,
        login=user.login,
        email=user.email,
    )


ICurrentUser: type[UserDTO] = Annotated[UserDTO, Depends(get_current_user)]
