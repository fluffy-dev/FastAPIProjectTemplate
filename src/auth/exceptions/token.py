
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