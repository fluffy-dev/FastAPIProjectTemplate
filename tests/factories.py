from polyfactory.factories.pydantic_factory import ModelFactory
from src.auth.dto import RegistrationDTO, UserDTO, TokenDTO
from src.auth.models.user import UserModel

class RegistrationDTOFactory(ModelFactory[RegistrationDTO]):
    """Factory for generating RegistrationDTO payloads."""
    __model__ = RegistrationDTO

class UserDTOFactory(ModelFactory[UserDTO]):
    """Factory for generating UserDTO objects."""
    __model__ = UserDTO

class UserModelFactory(ModelFactory[UserModel]):
    """Factory for generating SQLAlchemy User models."""
    __model__ = UserModel