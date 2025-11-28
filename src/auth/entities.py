from dataclasses import dataclass


@dataclass
class UserEntity:
    name: str
    login: str
    email: str
    password: str | None