import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from src.auth.models.user import UserModel
from src.auth.service.password import PasswordService
from tests.factories import RegistrationDTOFactory

pytestmark = pytest.mark.asyncio


async def test_register_user_endpoint(client: AsyncClient, db_session):
    """
    Verifies the /auth/register endpoint creates a user and returns the public DTO.
    """
    # Arrange
    payload = RegistrationDTOFactory.build(password="secure123123..")
    data = payload.model_dump()
    data["email"] = str(payload.email)  # Ensure email is string

    # Act
    response = await client.post("/v1/auth/register", json=data)

    # Assert
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["email"] == data["email"]
    assert "password" not in json_resp

    # Verify DB side effect
    stmt = select(UserModel).where(UserModel.email == data["email"])
    result = await db_session.execute(stmt)
    assert result.scalar_one_or_none() is not None


async def test_login_sets_cookies(client: AsyncClient, db_session):
    """
    Verifies that /auth/login returns tokens and sets HttpOnly cookies.
    """
    # Arrange: Seed DB
    password = "securePassword123"
    hashed = PasswordService.get_password_hash(password)
    user = UserModel(
        name="Login User", login="login_user", email="login@test.com", password=hashed
    )
    db_session.add(user)
    await db_session.commit()

    # Act
    response = await client.post(
        "/v1/auth/login", json={"login": "login_user", "password": password}
    )

    # Assert
    assert response.status_code == 200

    # Check Body
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # Check Cookies
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert response.cookies["access_token"] == data["access_token"]


async def test_get_me_requires_auth(client: AsyncClient):
    """
    Verifies that /auth/me returns 401 if no cookies are present.
    """
    response = await client.get("/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["code"] == "access_token_missing"


async def test_refresh_token_flow(client: AsyncClient, db_session):
    """
    Verifies the full refresh flow using cookies.
    """
    # 1. Setup User
    password = "pw"
    user = UserModel(
        name="Refresher",
        login="refresher",
        email="refresh@test.com",
        password=PasswordService.get_password_hash(password),
    )
    db_session.add(user)
    await db_session.commit()

    # 2. Login to get initial cookies
    login_resp = await client.post(
        "/v1/auth/login", json={"login": "refresher", "password": password}
    )
    original_access = login_resp.cookies["access_token"]
    original_refresh = login_resp.cookies["refresh_token"]

    # 3. Call Refresh Endpoint (client automatically sends cookies from jar)
    # We clear the access token to simulate expiration, but keep refresh token
    del client.cookies["access_token"]

    await asyncio.sleep(1)  # to imitate time delta

    refresh_resp = await client.post("/v1/auth/refresh")

    assert refresh_resp.status_code == 200

    new_access = refresh_resp.cookies["access_token"]
    new_refresh = refresh_resp.cookies["refresh_token"]

    assert new_access != original_access
    assert new_refresh != original_refresh
