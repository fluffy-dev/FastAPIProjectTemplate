from fastapi import Depends
from typing import Annotated
from src.auth.service.user import UserService

IUserService: type[UserService] = Annotated[UserService, Depends()]