from fastapi import Depends
from typing import Annotated

from src.auth.service.session import SessionService


ISessionService: type[SessionService] = Annotated[SessionService, Depends()]
