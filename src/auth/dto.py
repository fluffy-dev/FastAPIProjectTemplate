from typing import Optional, Annotated, Union
from pydantic import BaseModel, EmailStr, StringConstraints

# Token
class TokenDTO(BaseModel):
    """
    Data Transfer Object for returning JWT authentication tokens to the client.

    Attributes:
        access_token (str): The JWT access token used for accessing protected resources.
        refresh_token (str): The JWT refresh token used to obtain a new access token.
        token_type (str): The type of token, typically "bearer". Defaults to "bearer".
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayloadDTO(BaseModel):
    """
    Data Transfer Object representing the decoded payload of a JWT.

    Attributes:
        sub (Optional[str]): The subject of the token (typically user ID or login).
    """
    sub: Optional[str]


# User
class BaseUserDTO(BaseModel):
    """
    Base DTO for User data, containing all potential fields including sensitive ones.

    This class serves as a superclass or internal representation. Care should be
    taken when exposing instances of this class to the API response to avoid
    leaking the password.

    Attributes:
        id (Optional[int]): The database primary key.
        name (str): The display name of the user (max 30 chars).
        login (str): The unique username (max 50 chars).
        email (EmailStr): The valid email address.
        password (Optional[str]): The hashed password string.
    """
    id: Optional[int] = None
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Optional[str] = None


class UserDTO(BaseModel):
    """
    Public-facing DTO for User data.

    This model is safe to return in API responses as it strictly excludes
    sensitive information like the password.

    Attributes:
        id (int): The database primary key.
        name (str): The display name of the user.
        login (str): The unique username.
        email (EmailStr): The user's email address.
    """
    id: int
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr


class CreateUserDTO(BaseModel):
    """
    Data Transfer Object used internally for creating a new user.

    This is typically constructed from a RegistrationDTO and passed to the
    service layer.

    Attributes:
        name (str): The display name.
        login (str): The desired username.
        email (EmailStr): The user's email.
        password (str): The plain-text password (to be hashed by the service).
    """
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Annotated[str, StringConstraints(max_length=50)]


class FindUserDTO(BaseModel):
    """
    Criteria DTO for searching for a user.

    Fields are optional; if multiple fields are provided, the search
    logic typically treats them as an AND condition (or OR depending on implementation).

    Attributes:
        id (Optional[int]): Search by ID.
        login (Optional[str]): Search by username.
        email (Optional[EmailStr]): Search by email.
    """
    id: Optional[int] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
    email: Optional[EmailStr] = None


class UpdateUserDTO(BaseModel):
    """
    Data Transfer Object for partial updates to a user profile.

    All fields are optional. Only fields that are not None should be updated
    in the database.

    Attributes:
        name (Optional[str]): New display name.
        login (Optional[str]): New username.
    """
    name: Optional[Annotated[str, StringConstraints(max_length=30)]] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None


# Auth
class LoginDTO(BaseModel):
    """
    Data Transfer Object for user authentication requests.

    Attributes:
        login (Union[str, EmailStr]): Accepts either a username or an email address.
        password (str): The plain-text password.
    """
    login: Union[Annotated[str, StringConstraints(max_length=50)], EmailStr]
    password: str


class RegistrationDTO(BaseModel):
    """
    Data Transfer Object for the public registration endpoint.

    Attributes:
        name (str): The user's full name.
        login (str): The desired username.
        email (EmailStr): The user's email address.
        password (Optional[str]): The plain-text password.
    """
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Optional[str] = None