from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.auth.dto import RegistrationDTO, UserDTO, TokenDTO, BaseUserDTO
from src.auth.models.user import UserModel


class RegistrationDTOFactory(ModelFactory[RegistrationDTO]):
    """Factory for generating RegistrationDTO payloads."""
    __model__ = RegistrationDTO

    @classmethod
    def get_provider_map(cls):
        providers = super().get_provider_map()
        providers[str] = lambda: "secure_test_password"
        return providers


class UserDTOFactory(ModelFactory[UserDTO]):
    """Factory for public UserDTO objects (No password)."""
    __model__ = UserDTO


class BaseUserDTOFactory(ModelFactory[BaseUserDTO]):
    """Factory for internal BaseUserDTO objects (With password)."""
    __model__ = BaseUserDTO


class TokenDTOFactory(ModelFactory[TokenDTO]):
    """Factory for generating TokenDTO objects."""
    __model__ = TokenDTO


class UserModelFactory(SQLAlchemyFactory[UserModel]):
    """Factory for generating SQLAlchemy User models."""
    __model__ = UserModel