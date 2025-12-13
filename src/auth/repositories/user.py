from typing import Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.auth.entities import UserEntity
from src.auth.exceptions.user import UserAlreadyExist, UserNotFound
from src.config.database.session import ISession
from src.auth.models.user import UserModel
from src.auth.dto import UpdateUserDTO, BaseUserDTO, FindUserDTO


class UserRepository:
    """
    Repository for handling User database operations using SQLAlchemy.
    """

    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, entity: UserEntity) -> BaseUserDTO:
        """
        Persists a new user to the database.

        Args:
            entity (UserEntity): The domain entity containing user data.
                                 Password should already be hashed before reaching here.

        Returns:
            BaseUserDTO: The created user data including the assigned database ID.

        Raises:
            UserAlreadyExist: If a user with the same login or email already exists.
        """
        instance = UserModel(
            name=entity.name,
            login=entity.login,
            email=entity.email,
            password=entity.password,  # Expects hashed password
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
        """
        Retrieves a single user by their primary key ID.

        Args:
            pk (int): The unique identifier of the user.

        Returns:
            Optional[BaseUserDTO]: The user DTO if found, otherwise None.
        """
        instance = await self.session.get(UserModel, pk)
        return self._get_dto(instance) if instance else None

    async def find(self, dto: FindUserDTO) -> Optional[BaseUserDTO]:
        """
        Finds a user based on dynamic criteria.

        This method filters the user table by any field present (not None)
        in the provided DTO. If multiple fields are provided, they are combined
        with AND logic.

        Args:
            dto (FindUserDTO): DTO containing search criteria (id, login, email).

        Returns:
            Optional[BaseUserDTO]: The first matching user, or None if no match found.
        """
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return self._get_dto(instance) if instance else None

    async def get_list(self, limit: int = 100, offset: int = 0) -> List[BaseUserDTO]:
        """
        Retrieves a paginated list of users.

        Args:
            limit (int): The maximum number of records to return. Defaults to 100.
            offset (int): The number of records to skip. Defaults to 0.

        Returns:
            List[BaseUserDTO]: A list of user DTOs. Returns an empty list if no users exist.
        """
        stmt = select(UserModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, dto: UpdateUserDTO, pk: int) -> BaseUserDTO:
        """
        Updates an existing user's information.

        Only fields provided (not None) in the DTO will be updated.

        Args:
            dto (UpdateUserDTO): The data to update.
            pk (int): The primary key of the user to update.

        Returns:
            BaseUserDTO: The updated user DTO.

        Raises:
            UserNotFound: If the user with the given ID does not exist.
        """
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

    async def delete(self, pk: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    @staticmethod
    def _get_dto(instance: UserModel) -> BaseUserDTO:
        """
        Helper method to convert a user instance into a BaseUserDTO.
        """
        return BaseUserDTO(
            id=instance.id,
            name=instance.name,
            login=instance.login,
            email=instance.email,
            password=instance.password,
        )
