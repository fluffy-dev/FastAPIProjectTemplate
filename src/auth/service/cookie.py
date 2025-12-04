from fastapi import Response

from src.auth.dto import TokenPairDTO

from src.config.jwt import settings as jwt_settings


def set_auth_cookies(response: Response, tokens: TokenPairDTO) -> None:
    """Sets secure HttpOnly cookies for access and refresh tokens."""
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,  # Set False if developing on localhost without HTTPS
        samesite="lax",
        max_age=jwt_settings.access_token_expire_seconds,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,  # Set False if developing on localhost without HTTPS
        samesite="lax",
        max_age=jwt_settings.refresh_token_rotate_min_lifetime,
    )


def clear_auth_cookies(response: Response) -> None:
    """Clears authentication cookies."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")