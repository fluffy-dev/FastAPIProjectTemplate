from typing import Optional

from src.auth.dto import RegistrationDTO, CreateUserDTO
from src.auth.exceptions.auth import CredentialsException
from src.auth.dependencies.user.service import IUserService
from src.auth.dto import FindUserDTO, UserDTO
from src.auth.service.password import PasswordService
from src.auth.dto import TokenDTO, LoginDTO

from src.auth.dependencies.token.service import ITokenService
from src.auth.exceptions.token import InvalidTokenError
from src.auth.exceptions.user import UserNotFound


class AuthService:
    """
    Service layer responsible for high-level authentication flows.
    """
    def __init__(self, user_service: IUserService, token_service: ITokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def login(self, dto: LoginDTO) -> TokenDTO:
        """
        Authenticates a user and generates JWT tokens.

        1. Finds the user by login.
        2. Verifies the provided password against the stored hash.
        3. Generates access and refresh tokens.

        Args:
            dto (LoginDTO): The login credentials (username/email and password).

        Returns:
            TokenDTO: The generated access and refresh tokens.

        Raises:
            CredentialsException: If the user is not found or the password is incorrect.
        """
        user: Optional[UserDTO] = await self.user_service.find(FindUserDTO(login=dto.login))

        if not user:
            raise CredentialsException

        if not PasswordService.verify_password(dto.password, user.password):
            raise CredentialsException

        user: UserDTO = user
        return await self.token_service.create_tokens(user)

    async def register(self, dto: RegistrationDTO) -> UserDTO:
        """
        Registers a new user in the system.

        Maps the RegistrationDTO to a CreateUserDTO and delegates creation
        to the UserService.

        Args:
            dto (RegistrationDTO): The registration details.

        Returns:
            UserDTO: The newly created user profile (safe view).
        """
        create_user_dto = CreateUserDTO(
            name=dto.name,
            login=dto.login,
            email=dto.email,
            password=dto.password,
        )

        return await self.user_service.create(create_user_dto)

    async def refresh_session(self, refresh_token: str) -> TokenDTO:
        """
        Refreshes the user session using a valid refresh token.

        1. Validates the refresh token signature and type.
        2. Extracts the user ID.
        3. Verifies the user still exists in the database.
        4. Generates a fresh pair of Access and Refresh tokens.

        Args:
            refresh_token (str): The JWT refresh token string.

        Returns:
            TokenDTO: A new pair of tokens.

        Raises:
            InvalidTokenError: If token is invalid or expired.
            UserNotFound: If the user ID in the token no longer exists.
        """
        payload = await self.token_service.verify_refresh_token(refresh_token)

        user_data = payload.get("user", {})
        user_id = user_data.get("user_id")

        if not user_id:
            raise InvalidTokenError("Token payload missing user_id")

        user = await self.user_service.get(int(user_id))
        if not user:
            raise UserNotFound("User associated with this token no longer exists")

        user_dto = UserDTO(
            id=user.id,
            name=user.name,
            login=user.login,
            email=user.email
        )

        return await self.token_service.create_tokens(user_dto)