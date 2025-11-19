import secrets
import string
from dataclasses import dataclass
from src.config.security import settings
from argon2 import PasswordHasher

from pydantic import EmailStr


@dataclass
class UserEntity:
    name: str
    surname: str
    email: EmailStr
    password: str | None = None

    def __post_init__(self):
        password = self.hash_password(self.password)
        self.password = password

    @staticmethod
    def hash_password(password: str) -> str:
        salt = settings.secret_key
        hashed = PasswordHasher().hash(password.encode("utf-8"), salt=salt.encode("utf-8"))
        return hashed

    @staticmethod
    def create_verify_code(length=16):
        character_sheet = string.ascii_letters + string.digits
        return "".join(secrets.choice(character_sheet) for i in range(length))