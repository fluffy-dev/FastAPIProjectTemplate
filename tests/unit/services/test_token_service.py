import pytest
import jwt
from datetime import datetime, timedelta
from src.auth.service.token import TokenService
from src.auth.exceptions.token import InvalidTokenError, InvalidSignatureError
from src.auth.dto import UserDTO

# Mock settings just for this test file
from src.config.security import settings as security_settings
from src.config.jwt import settings as jwt_settings


@pytest.fixture
def token_service():
    return TokenService()


async def test_generate_access_token_structure(token_service):
    """Verify access token contains correct claims and structure."""
    user_dto = UserDTO(id=123, name="Test", login="test", email="t@t.com")

    token = await token_service.generate_access_token(user_dto)

    # Manually decode to check payload without verification first
    payload = jwt.decode(token, security_settings.secret_key, algorithms=[security_settings.algorithm])

    assert payload["token_type"] == "access"
    assert payload["user"]["user_id"] == "123"
    assert "exp" in payload
    assert "iat" in payload


async def test_decode_valid_token(token_service):
    """Verify service can decode its own tokens."""
    user_dto = UserDTO(id=1, name="A", login="a", email="a@a.com")
    token = await token_service.generate_access_token(user_dto)

    payload = await token_service.decode_token(token)
    assert payload["user"]["user_id"] == "1"


async def test_decode_expired_token(token_service, mocker):
    """Verify expired tokens raise specific errors."""
    # 1. Generate a token that is already expired
    # We cheat by manually encoding a payload with past time
    past = datetime.now() - timedelta(hours=1)
    payload = {
        "token_type": "access",
        "exp": int(past.timestamp()),
        "user": {}
    }
    expired_token = await token_service.encode_token(payload)

    # 2. Attempt to decode
    with pytest.raises(jwt.ExpiredSignatureError):
        await token_service.decode_token(expired_token)


async def test_verify_refresh_token_logic(token_service):
    """Verify refresh logic rejects access tokens."""
    # Create an ACCESS token
    user_dto = UserDTO(id=1, name="A", login="a", email="a@a.com")
    access_token = await token_service.generate_access_token(user_dto)

    # Try to pass it as a REFRESH token
    with pytest.raises(InvalidTokenError) as exc:
        await token_service.verify_refresh_token(access_token)

    assert "Expected 'refresh'" in str(exc.value)