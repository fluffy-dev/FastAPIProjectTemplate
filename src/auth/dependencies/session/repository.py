from fastapi import Depends
from typing import Annotated

from src.auth.repositories.session import SessionRepository

ISessionRepository: type[SessionRepository] = Annotated[SessionRepository, Depends()]