from typing import Annotated, Union
from fastapi import Depends, Cookie
from src.auth.dependencies.token.service import ITokenService
from src.auth.dependencies.user.service import IUserService
from src.auth.dto import UserDTO
from src.auth.exceptions.token import InvalidTokenError

async def get_current_user(
        user_service: IUserService,
        token_service: ITokenService,
        access_token: Annotated[Union[str, None], Cookie()] = None
) -> UserDTO:
    """
    Dependency to get the current user from a JWT token.

    Verifies the token, extracts the user ID, and fetches the user
    from the database.

    Raises:
        HTTPException(401): If the token is invalid or the user is not found.


    The payload includes:
        - `token_type`: Set to "access" or "refresh".
        - `user`: A dictionary containing `user_id` and `user_name` from the DTO.
        - `exp`: Expiration timestamp based on `access_token_lifetime` or `refresh_token_lifetime`.
        - `iat`: Issued-at timestamp.
    """

    payload: dict = await token_service.decode_token(access_token)

    user_id = payload.get("user").get("user_id")

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