from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserEntity:
    """Domain entity representing a User.

    Used for data transfer between Service and Repository layers to decouple
    business logic from specific database implementations or API schemas.
    """
    name: str
    login: str
    email: str
    password: str | None = None
    id: int | None = None

@dataclass
class SessionEntity:
    """
    Domain entity representing a Session.

    Used for data transfer between Service and Repository layers to decouple
    business logic from specific database implementations or API schemas.
    """

    user_id: int
    refresh_token_jti: str
    expires_at: datetime
    user_agent: str | None
    ip_address: str | None
