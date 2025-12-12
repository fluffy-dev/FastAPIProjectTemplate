import pytest
from unittest.mock import AsyncMock
from src.auth.service.auth import AuthService
from src.auth.service.password import PasswordService
from src.auth.dto import LoginDTO, TokenDTO
from src.auth.exceptions.auth import CredentialsException
from src.auth.dependencies.user.service import IUserService
from src.auth.dependencies.token.service import ITokenService

# UPDATE IMPORT
from tests.factories import BaseUserDTOFactory

pytestmark = pytest.mark.asyncio


async def test_login_success(mocker):
    # Arrange
    mock_user_service = AsyncMock(spec=IUserService)
    mock_token_service = AsyncMock(spec=ITokenService)

    user_dto = BaseUserDTOFactory.build(
        password=PasswordService.get_password_hash("secret")
    )
    mock_user_service.find.return_value = user_dto

    expected_tokens = TokenDTO(
        access_token="acc", refresh_token="ref", token_type="bearer"
    )
    mock_token_service.create_tokens.return_value = expected_tokens

    service = AuthService(mock_user_service, mock_token_service)
    login_dto = LoginDTO(login=user_dto.login, password="secret")

    # Act
    result = await service.login(login_dto)

    # Assert
    assert result == expected_tokens


async def test_login_wrong_password_raises_exception(mocker):
    # Arrange
    mock_user_service = AsyncMock(spec=IUserService)
    mock_token_service = AsyncMock(spec=ITokenService)

    # FIX: Use BaseUserDTOFactory
    user_dto = BaseUserDTOFactory.build(
        password=PasswordService.get_password_hash("correct_password")
    )
    mock_user_service.find.return_value = user_dto

    service = AuthService(mock_user_service, mock_token_service)
    login_dto = LoginDTO(login=user_dto.login, password="wrong_password")

    # Act & Assert
    with pytest.raises(CredentialsException):
        await service.login(login_dto)


async def test_login_user_not_found(mocker):
    mock_user_service = AsyncMock(spec=IUserService)
    mock_user_service.find.return_value = None

    service = AuthService(mock_user_service, AsyncMock())
    login_dto = LoginDTO(login="ghost", password="pw")

    with pytest.raises(CredentialsException):
        await service.login(login_dto)
