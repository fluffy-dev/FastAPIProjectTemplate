import pytest
from unittest.mock import AsyncMock
from src.auth.dependencies.current_user import get_current_user
from src.auth.exceptions.token import AccessTokenMissing, InvalidTokenError
from src.auth.dto import UserDTO

pytestmark = pytest.mark.asyncio


async def test_get_current_user_success():
    """Verify dependency returns user when everything is valid."""
    # Arrange
    mock_user_service = AsyncMock()
    mock_token_service = AsyncMock()

    token = "valid_token"
    mock_token_service.decode_token.return_value = {"user": {"user_id": "1"}}

    expected_user = UserDTO(id=1, name="A", login="a", email="a@a.com")
    mock_user_service.get.return_value = expected_user

    # Act
    # We call the function directly as if FastAPI invoked it
    result = await get_current_user(mock_user_service, mock_token_service, access_token=token)

    # Assert
    assert result == expected_user
    mock_user_service.get.assert_called_with(1)


async def test_get_current_user_missing_cookie():
    """Verify missing cookie raises error."""
    mock_user_service = AsyncMock()
    mock_token_service = AsyncMock()

    with pytest.raises(AccessTokenMissing):
        await get_current_user(mock_user_service, mock_token_service, access_token=None)


async def test_get_current_user_invalid_payload():
    """Verify token without user_id raises error."""
    mock_token_service = AsyncMock()
    mock_token_service.decode_token.return_value = {}  # Empty payload

    with pytest.raises(InvalidTokenError):
        await get_current_user(AsyncMock(), mock_token_service, access_token="token")