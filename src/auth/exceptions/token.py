class InvalidSignatureError(Exception):
    """
    Raised when a JWT signature verification fails.

    This occurs if the token was tampered with, or if the secret key/algorithm
    used to sign the token does not match the server's configuration.
    """

    pass


class InvalidTokenError(Exception):
    """
    Raised when a JWT is malformed, expired, or contains invalid claims.

    This is a general exception for token validation failures, such as
    decoding errors or missing required payload fields (like 'user_id').
    """

    pass


class TokenMissingError(Exception):
    """
    Base exception for cases where a required token is not present in the request.
    """

    pass


class AccessTokenMissing(TokenMissingError):
    """
    Raised when the Access Token is required but missing.

    This typically happens in the `get_current_user` dependency when the
    'access_token' cookie is not found in the HTTP request headers.

    This should usually result in an HTTP 401 Unauthorized response,
    prompting the client to attempt a token refresh.
    """

    pass


class RefreshTokenMissing(TokenMissingError):
    """
    Raised when the Refresh Token is required but missing.

    This typically happens in the `/auth/refresh` endpoint when the
    'refresh_token' cookie is not found.

    This should usually result in an HTTP 401 Unauthorized response,
    forcing the user to log in again (redirect to login page).
    """

    pass
