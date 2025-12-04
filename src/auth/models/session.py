from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.libs.base_model import Base


class UserSessionModel(Base):
    """
    SQLAlchemy model for user_sessions table.

    Attributes:
        id: Primary key.
        user_id: Foreign key to users table.
        refresh_token_jti: Unique UUID for the refresh token.
        expires_at: Absolute expiration timestamp.
        created_at: Creation timestamp.
        user_agent: Client browser info.
        ip_address: Client IP address.
    """
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    refresh_token_jti: Mapped[str] = mapped_column(
        String(36), unique=True, index=True
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    user = relationship("UserModel", backref="sessions")