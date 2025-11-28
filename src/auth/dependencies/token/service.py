from fastapi import Depends
from typing import Annotated

from src.auth.service.token import TokenService

ITokenService: type[TokenService] = Annotated[TokenService, Depends()]
