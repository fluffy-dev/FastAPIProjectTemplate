from typing import Optional

from src.auth.dto import FindUserDTO
from src.auth.entities import UserEntity
from src.auth.dependencies.user.repository import IUserRepository
from src.auth.dto import BaseUserDTO, CreateUserDTO, UserDTO
from src.auth.service.password import PasswordService

class UserService:
    """
    Service for managing user lifecycle events (creation, retrieval).
    """
    def __init__(self, user_repository: IUserRepository):
        self.repository = user_repository

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        """
        Orchestrates the creation of a new user.

        This method handles:
        1. Hashing the plain-text password.
        2. Converting the DTO to a Domain Entity.
        3. Persisting the entity via the repository.

        Args:
            dto (CreateUserDTO): The raw user creation data (with plain password).

        Returns:
            UserDTO: The created user without the password field.
        """
        hashed_password = PasswordService.get_password_hash(dto.password)
        user_entity = UserEntity(
            name=dto.name,
            login=dto.login,
            email=str(dto.email),
            password=hashed_password,
        )
        created_user: BaseUserDTO = await self.repository.create(user_entity)
        return UserDTO(
            id=created_user.id,
            name=created_user.name,
            login=created_user.login,
            email=created_user.email,
        )

    async def get(self, pk: int) -> Optional[BaseUserDTO]:
        """
        Retrieves a user by ID.

        Args:
            pk (int): The database ID of the user.

        Returns:
            Optional[BaseUserDTO]: The user DTO containing all fields (including password hash).
        """
        return await self.repository.get(pk)

    async def find(self, dto: FindUserDTO) -> Optional[BaseUserDTO]:
        """
        Searches for a user based on specific criteria.

        Args:
            dto (FindUserDTO): The search criteria (e.g., login, email).

        Returns:
            Optional[BaseUserDTO]: The matching user DTO or None.
        """
        return await self.repository.find(dto)
