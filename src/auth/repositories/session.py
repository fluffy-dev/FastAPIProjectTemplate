from datetime import datetime
from typing import Optional

from sqlalchemy import delete, select, update

from src.auth.exceptions.session import SessionNotFound
from src.auth.dto import SessionDTO
from src.auth.entities import SessionEntity
from src.auth.models.session import UserSessionModel
from src.config.database.session import ISession


class SessionRepository:
    """
    Repository for managing User Sessions using DTOs.
    """

    def __init__(self, session: ISession) -> None:
        self.session = session

    async def create(self, entity: SessionEntity) -> SessionDTO:
        """
        Creates a new session record from a DTO.

        Args:
            entity: The data for the new session.

        Returns:
            The created SessionDTO.
        """
        instance = UserSessionModel(
            user_id=entity.user_id,
        refresh_token_jti=entity.refresh_token_jti,
        expires_at=entity.expires_at,
        user_agent=entity.user_agent,
        ip_address=entity.ip_address,

        )
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_by_jti(self, jti: str) -> Optional[SessionDTO]:
        """
        Retrieves a session by its JTI.

        Args:
            jti: The unique refresh token identifier.

        Returns:
            SessionDTO if found, otherwise None.
        """
        stmt = select(UserSessionModel).where(
            UserSessionModel.refresh_token_jti == jti
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return self._get_dto(instance) if instance else None

    async def update_jti(
        self,
        old_jti: str,
        new_jti: str,
        new_expires_at: datetime
    ) -> None:
        """
        Updates the JTI and expiration of an existing session.

        Args:
            old_jti: The JTI to replace.
            new_jti: The new JTI.
            new_expires_at: The new expiration timestamp.
        """
        stmt = (
            update(UserSessionModel)
            .where(UserSessionModel.refresh_token_jti == old_jti)
            .values(refresh_token_jti=new_jti, expires_at=new_expires_at)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        instance = result.scalar_one_or_none()
        if instance is None:
            raise SessionNotFound

    async def delete_by_jti(self, jti: str) -> None:
        """
        Revokes a session by JTI.

        Args:
            jti: The JTI of the session to delete.
        """
        stmt = delete(UserSessionModel).where(
            UserSessionModel.refresh_token_jti == jti
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_all_for_user(self, user_id: int) -> None:
        """
        Revokes all sessions for a specific user.

        Args:
            user_id: The ID of the user.
        """
        stmt = delete(UserSessionModel).where(
            UserSessionModel.user_id == user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    @staticmethod
    def _get_dto(instance: UserSessionModel):
        """Helper function to transform SQLAlchemy instance to pydantic object"""
        return SessionDTO(
            id = instance.id,
            user_id = instance.user_id,
            refresh_token_jti = instance.refresh_token_jti,
            expires_at = instance.expires_at,
            created_at = instance.created_at,
            user_agent = instance.user_agent,
            ip_address = instance.ip_address,
        )