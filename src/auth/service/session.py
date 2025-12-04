from typing import Optional
from datetime import datetime

from src.auth.dto import CreateSessionDTO, SessionDTO
from src.auth.entities import SessionEntity
from src.auth.dependencies.session.repository import ISessionRepository


class SessionService:
    def __init__(self, repository: ISessionRepository):
        self.repository = repository

    async def create(self, dto: CreateSessionDTO):
        session_entity = SessionEntity(
            user_id = dto.user_id,
            refresh_token_jti=dto.refresh_token_jti,
            user_agent=dto.user_agent,
            expires_at=dto.expires_at,
            ip_address=dto.ip_address,
        )
        return await self.repository.create(session_entity)

    async def get_by_jti(self, jti: str) -> Optional[SessionDTO]:
        return await self.repository.get_by_jti(jti)


    async def update_jti(self, old_jti: str, new_jti: str, new_expires_at: datetime):
        return await self.repository.update_jti(
            old_jti=old_jti,
            new_jti=new_jti,
            new_expires_at=new_expires_at,
        )