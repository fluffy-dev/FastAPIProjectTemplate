from typing import Optional

from src.auth.dto import (
    CreateSessionDTO, UserSessionInfoDTO, SessionDTO,
    RefreshTokenDTO, AccessTokenDTO, TokenPairDTO,
    LoginDTO, RegistrationDTO, CreateUserDTO,
    FindUserDTO, UserDTO, BaseUserDTO

)
from src.auth.exceptions.session import SessionNotFound
from src.auth.exceptions.auth import CredentialsException
from src.auth.exceptions.token import InvalidTokenError
from src.auth.exceptions.user import UserNotFound

from src.auth.dependencies.user.service import IUserService
from src.auth.dependencies.token.service import ITokenService
from src.auth.dependencies.session.service import ISessionService

from src.auth.service.password import PasswordService


class AuthService:
    """
    Service layer responsible for high-level authentication flows.
    """
    def __init__(self, user_service: IUserService, token_service: ITokenService, session_service: ISessionService):
        self.user_service = user_service
        self.token_service = token_service
        self.session_service = session_service

    async def login(self, login_dto: LoginDTO, user_session_dto: UserSessionInfoDTO) -> TokenPairDTO:
        """
        Authenticates a user and generates JWT tokens.

        Args:
            login_dto (LoginDTO): login data, username and password
            user_session_dto (UserSessionInfoDTO): info about user browser session, ip_address, user_agent, ... .

        Returns:
            TokenPairDTO: JWT tokens, access and refresh tokens

        Raise:
            CredentialsException: if the credentials are invalid, username not found, or password not match
        """
        user: Optional[BaseUserDTO] = await self.user_service.find(FindUserDTO(login=login_dto.login))

        if not user or not PasswordService.verify_password(login_dto.password, user.password):
            raise CredentialsException

        user: BaseUserDTO = user

        access_token: AccessTokenDTO = await self.token_service.generate_access_token(user)
        refresh_token: RefreshTokenDTO = await self.token_service.generate_refresh_token(user)

        session_dto = CreateSessionDTO(
            user_id = user.id,
            refresh_token_jti=refresh_token.jti,
            expires_at=refresh_token.expire,
            user_agent=user_session_dto.user_agent,
            ip_address=user_session_dto.ip_address,
        )
        await self.session_service.create(session_dto)

        return TokenPairDTO(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

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

    async def refresh_session(self, refresh_token: str) -> TokenPairDTO:
        payload = await self.token_service.verify_refresh_token(refresh_token)

        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            raise InvalidTokenError("Token payload invalid")

        user = await self.user_service.get(int(user_id))

        if not user:
            raise UserNotFound("User associated with this token no longer exists")

        session: Optional[SessionDTO] = await self.session_service.get_by_jti(jti=jti)

        if not session:
            raise SessionNotFound("Session associated with this token no longer exists")


        access_token: AccessTokenDTO = await self.token_service.generate_access_token(user)
        refresh_token: RefreshTokenDTO = await self.token_service.generate_refresh_token(user)

        await self.session_service.update_jti(
            old_jti=jti,
            new_jti=refresh_token.jti,
            new_expires_at=refresh_token.expire,
        )

        return TokenPairDTO(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

    async def logout(self, refresh_token: str) -> None:
        payload = await self.token_service.verify_refresh_token(refresh_token)

        jti = payload.get("jti")

        if not jti:
            raise InvalidTokenError("Token payload invalid")

        await self.session_service.delete_by_jti(
            jti=jti
        )

        return None

    async def logout_all_sessions_for_user(self, refresh_token: str) -> None:
        payload = await self.token_service.verify_refresh_token(refresh_token)

        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            raise InvalidTokenError("Token payload invalid")

        user_id = int(user_id)

        user = await self.user_service.get(user_id)

        if not user:
            raise UserNotFound("User associated with this token no longer exists")

        await self.session_service.delete_all_for_user(user_id)

        return None

