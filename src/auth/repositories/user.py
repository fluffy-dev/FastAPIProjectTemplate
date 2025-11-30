from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from src.auth.entities import UserEntity
from src.auth.exceptions.user import UserAlreadyExist, UserNotFound
from src.config.database.session import ISession
from src.auth.models.user import UserModel
from src.auth.dto import UpdateUserDTO, BaseUserDTO, FindUserDTO


class UserRepository:
    """
    Repository for user data access, operating with DTOs.
    """
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, entity: UserEntity) -> BaseUserDTO:
        """
        Create a new user using user entity
        """
        instance = UserModel(
            name=entity.name,
            login=entity.login,
            email=entity.email,
            password=entity.password # Expects hashed password
        )
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExist

    async def get(self, pk: int) -> Optional[BaseUserDTO]:
        instance = await self.session.get(UserModel, pk)
        return self._get_dto(instance) if instance else None

    async def find(self, dto: FindUserDTO) -> Optional[BaseUserDTO]:
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return self._get_dto(instance) if instance else None

    async def get_list(self, limit: int = 100, offset: int = 0) -> List[BaseUserDTO]:
        stmt = select(UserModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, dto: UpdateUserDTO, pk: int) -> BaseUserDTO:
        stmt = (
            update(UserModel)
            .values(**dto.model_dump(exclude_none=True))
            .where(UserModel.id == pk)
            .returning(UserModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    @staticmethod
    def _get_dto(instance: UserModel) -> BaseUserDTO:
        return BaseUserDTO(
            id=instance.id,
            name=instance.name,
            login=instance.login,
            email=instance.email,
            password=instance.password
        )
