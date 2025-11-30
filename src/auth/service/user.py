from typing import Optional

from src.auth.dto import FindUserDTO
from src.auth.entities import UserEntity
from src.auth.dependencies.user.repository import IUserRepository
from src.auth.dto import BaseUserDTO, CreateUserDTO, UserDTO
from src.auth.service.password import PasswordService

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.repository = user_repository

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        """
        Creates a new user, correctly hashing the password before saving.
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
        Get a full user dto by its primary key.
        """
        return await self.repository.get(pk)

    async def find(self, dto: FindUserDTO) -> Optional[BaseUserDTO]:
        """
        Find user by FindUserDTO
        """
        return await self.repository.find(dto)
