from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.libs.exceptions import AlreadyExistsError
from src.user.entity import UserEntity
from src.config.database.session import ISession
from src.user.models.user import UserModel
from src.user.dto import UpdateUserDTO, UserDTO, FindUserDTO


class UserRepository:
    """Repository layer class for User Model manipulations"""
    def __init__(self, session: ISession):
        self.session = session

    async def create(self, user: UserEntity):
        """Create a new user from UserEntity"""
        instance = UserModel(**user.__dict__)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistsError(f'{instance.email} is already exist')

        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_user(self, dto: FindUserDTO):
        """Get user by FindUserDTO fields, automatically removes none values"""
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()
        return self._get_dto(result) if result else None

    async def get_list(self, limit: int, offset: int):
        """Get all users from `offset` and `limit` """
        stmt = select(UserModel).limit(limit).offset(offset)
        raw = await self.session.execute(stmt)
        return raw.scalars()

    async def get(self, pk: int):
        """Get user by pk"""
        stmt = select(UserModel).filter_by(id=pk)
        raw = await self.session.execute(stmt)
        return raw.scalar_one_or_none()

    async def update(self, dto: UpdateUserDTO, pk: int):
        """Update user by pk and set UpdateUserDTO values"""
        stmt = update(UserModel).values(**dto.model_dump()).filter_by(id=pk).returning(UserModel)
        raw = await self.session.execute(stmt)
        await self.session.commit()
        return raw.scalar_one()

    async def delete(self, pk: int) -> None:
        """Delete user by pk"""
        stmt = delete(UserModel).where(UserModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_active(self, active: bool, pk: int):
        """Change user active status by pk"""
        stmt = update(UserModel).values(is_active=active).filter_by(id=pk).returning(UserModel)
        raw = await self.session.execute(stmt)
        await self.session.commit()
        return raw.scalar_one()

    async def update_pass(self, new_password: str, pk: int):
        """Change user password by pk"""
        stmt = update(UserModel).values(password=new_password).filter_by(id=pk).returning(UserModel)
        raw = await self.session.execute(stmt)
        await self.session.commit()
        return raw.scalar_one()

    @staticmethod
    def _get_dto(row: UserModel) -> UserDTO:
        return UserDTO(
            id=row.id,
            is_active=row.is_active,
            surname=row.surname,
            password=row.password,
            name=row.name,
            email=row.email,
        )
