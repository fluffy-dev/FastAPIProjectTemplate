from typing import Optional, Annotated, Union

from pydantic import BaseModel, EmailStr, StringConstraints


class FindUserDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    surname: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    email: Optional[EmailStr] = None


class UserBaseDTO(BaseModel):
    name: Annotated[str, StringConstraints(max_length=20)]
    surname: Annotated[str, StringConstraints(max_length=20)]
    email: Union[EmailStr, Annotated[str, StringConstraints(max_length=50)]]


class UserDTO(UserBaseDTO):
    id: int
    is_active: bool
    password: str


class CreateUserDTO(UserBaseDTO):
    pass


class GetUserListDTO(UserBaseDTO):
    id: int


class GetUserDTO(UserBaseDTO):
    id: int


class UpdateUserDTO(UserBaseDTO):
    pass


class UpdatePasswordDTO(BaseModel):
    password: str