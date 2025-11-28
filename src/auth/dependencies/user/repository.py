from fastapi import Depends
from typing import Annotated
from src.auth.repositories.user import UserRepository

IUserRepository: type[UserRepository] = Annotated[UserRepository, Depends()]