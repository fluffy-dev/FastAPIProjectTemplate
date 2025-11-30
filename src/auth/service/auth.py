from typing import Optional

from src.auth.dto import RegistrationDTO, CreateUserDTO
from src.auth.exceptions.auth import CredentialsException
from src.auth.dependencies.user.service import IUserService
from src.auth.dto import FindUserDTO, UserDTO
from src.auth.service.password import PasswordService
from src.auth.dto import TokenDTO, LoginDTO

from src.auth.dependencies.token.service import ITokenService



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