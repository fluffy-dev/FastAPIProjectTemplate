class CredentialsException(Exception):
    """
    Raised when authentication fails due to invalid credentials.

    This is typically raised when a login attempt fails (e.g., wrong password,
    user not found) or when a specific authentication flow cannot be completed.

    This usually translates to an HTTP 401 Unauthorized response.
    """

    pass
