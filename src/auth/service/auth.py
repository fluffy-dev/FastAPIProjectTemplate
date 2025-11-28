from src.auth.dependencies.user.repository import IUserRepository
from src.auth.dto import FindUserDTO
from src.auth.exceptions import UserNotFound
from src.auth.service.password import PasswordService
from src.auth.service.token import TokenService
from src.auth.dto import TokenDTO, LoginDTO

class AuthService:
    """
    Service layer for authentication logic.
    """
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def login(self, login_form: LoginDTO) -> TokenDTO:
        """
        Authenticates a user and issues JWT tokens.

        Args:
            login_form: The user's login and password.

        Returns:
            TokenDTO: A DTO containing the access and refresh tokens.

        Raises:
            UserNotFound: If the user does not exist or password is incorrect.
        """
        user = await self.user_repo.find(FindUserDTO(login=login_form.login))

        if not user:
            user = await self.user_repo.find(FindUserDTO(email=login_form.login))

        if not user:
            raise UserNotFound

        if not PasswordService.verify_password(login_form.password, user.password):
            raise UserNotFound

        access_token = TokenService.create_access_token(data={"sub": str(user.id)})
        refresh_token = TokenService.create_refresh_token(data={"sub": str(user.id)})

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    #TODO: Add registration endpoint

    async def register(self, form_data) -> TokenDTO:
        ...