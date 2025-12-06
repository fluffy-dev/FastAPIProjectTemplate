from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.auth.dto import RegistrationDTO, UserDTO, TokenDTO
from src.auth.models.user import UserModel


class RegistrationDTOFactory(ModelFactory[RegistrationDTO]):
    """Factory for generating RegistrationDTO payloads (Pydantic)."""
    __model__ = RegistrationDTO


class UserDTOFactory(ModelFactory[UserDTO]):
    """Factory for generating UserDTO objects (Pydantic)."""
    __model__ = UserDTO


class TokenDTOFactory(ModelFactory[TokenDTO]):
    """Factory for generating TokenDTO objects (Pydantic)."""
    __model__ = TokenDTO


class UserModelFactory(SQLAlchemyFactory[UserModel]):
    """Factory for generating SQLAlchemy User models (ORM)."""
    __model__ = UserModel