from typing import Optional, Annotated, Union
from pydantic import BaseModel, EmailStr, StringConstraints


# Token
class TokenDTO(BaseModel):
    """
    DTO for representing JWT access and refresh tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayloadDTO(BaseModel):
    """
    DTO for the payload data encoded within the JWT.
    """
    sub: Optional[str]

class AccessTokenDTO(BaseModel):
    """
    DTO for the access token data.
    """
    access_token: str
    token_type: str = "bearer"

# User
class BaseUserDTO(BaseModel):
    """
    DTO for a user, including sensitive information like a password.
    Password is optional, typically for creation or updates.
    """
    id: Optional[int] = None
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Optional[str] = None


class UserDTO(BaseModel):
    """
    DTO for private view of a user's data, excluding sensitive details like the password.
    """
    id: int
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr

class CreateUserDTO(BaseModel):
    """
    DTO  for creating a new user.
    """
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Annotated[str, StringConstraints(max_length=50)]


class FindUserDTO(BaseModel):
    """
    DTO for searching or finding a user by various optional criteria.
    """
    id: Optional[int] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
    email: Optional[EmailStr] = None

class UpdateUserDTO(BaseModel):
    """
    DTO for updating a user's information. All fields are optional.
    """
    name: Optional[Annotated[str, StringConstraints(max_length=30)]] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None


# Auth
class LoginDTO(BaseModel):
    """
    DTO for logging in.
    """
    login: Union[Annotated[str, StringConstraints(max_length=50)], EmailStr] # Login or Email
    password: str


class RegistrationDTO(BaseModel):
    """
    DTO for registering a new user.
    """
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Optional[str] = None