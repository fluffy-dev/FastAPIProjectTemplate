import uuid

from jwt import ExpiredSignatureError, PyJWTError, decode, encode, get_unverified_header
from datetime import datetime, timedelta


from src.auth.dto import UserDTO, RefreshTokenDTO, AccessTokenDTO, BaseUserDTO
from src.config.jwt import settings as jwt_settings
from src.config.security import settings as security_settings
from src.auth.exceptions.token import InvalidSignatureError, InvalidTokenError


class TokenService:
    """
    Service responsible for handling JSON Web Token (JWT) operations.

    This service manages the lifecycle of access and refresh tokens, including
    generation, encoding, decoding, and validation of token signatures and
    algorithms.

    Attributes:
        access_token_lifetime (int): The lifespan of an access token in seconds.
        refresh_token_lifetime (int): The lifespan of a refresh token in seconds.
        secret_key (str): The secret key used for signing tokens.
        algorithm (str): The cryptographic algorithm used for signing (e.g., HS256).
    """

    def __init__(self) -> None:
        """
        Initializes the TokenService by loading configuration settings.

        The settings are retrieved from the global application configuration
        modules (`jwt_settings` and `security_settings`).
        """
        self.access_token_lifetime = jwt_settings.access_token_expire_seconds
        self.refresh_token_lifetime = jwt_settings.refresh_token_lifetime_seconds
        self.secret_key = security_settings.secret_key
        self.algorithm = security_settings.algorithm

    def _validate_token(self, token: str) -> str:
        """
        Validates the token header to ensure the signing algorithm matches the expected configuration.

        This method inspects the unverified header of the JWT. It does not verify the
        signature itself, but rather checks metadata to prevent algorithm confusion attacks.

        Args:
            token (str): The encoded JWT string.

        Returns:
            str: The original token if validation passes.

        Raises:
            InvalidSignatureError: If the algorithm in the token header does not match
                                   the service's configured algorithm.
        """
        token_info = get_unverified_header(token)
        if token_info["alg"] != self.algorithm:
            raise InvalidSignatureError("Key error")
        return token

    async def encode_token(self, payload: dict) -> str:
        """
        Encodes a dictionary payload into a JWT string.

        Args:
            payload (dict): The data to be included in the token claims.

        Returns:
            str: The encoded and signed JWT string.
        """
        return encode(payload, self.secret_key, self.algorithm)

    async def decode_token(self, token: str) -> dict:
        """
        Decodes and verifies a JWT string.

        This method first validates the token header (algorithm check) and then
        attempts to decode the payload using the secret key.

        Args:
            token (str): The encoded JWT string to decode.

        Returns:
            dict: The decoded payload dictionary.
                The payload includes:
                    - `token_type`: Set to "access" or "refresh".
                    - `user`: A dictionary containing `user_id` and `user_name` from the DTO.
                    - `exp`: Expiration timestamp based on `access_token_lifetime` or `refresh_token_lifetime`.
                    - `iat`: Issued-at timestamp.

        Raises:
            ExpiredSignatureError: If the token's expiration time (`exp`) has passed.
            Exception: If the token is malformed or invalid for any other reason.
        """
        try:
            self._validate_token(token)
            return decode(token, self.secret_key, self.algorithm)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token lifetime is expired")
        except PyJWTError:
            raise InvalidTokenError("Token is invalid")

    async def generate_access_token(self, dto: BaseUserDTO) -> AccessTokenDTO:
        """
        Constructs the payload and generates an encoded access token.

        The payload includes:
        - `token_type`: Set to "access".
        - `user`: A dictionary containing `user_id` and `user_name` from the DTO.
        - `exp`: Expiration timestamp based on `access_token_lifetime`.
        - `iat`: Issued-at timestamp.

        Args:
            dto (UserDTO): The user data to embed in the token.

        Returns:
            str: The encoded access token.
        """
        now = datetime.now()
        expire = now + timedelta(seconds=self.access_token_lifetime)
        payload = {
            "token_type": "access",
            "sub": str(dto.id),
            "exp": int(expire.timestamp()),
            "iat": int(
                now.timestamp()
            ),  # The number of seconds that have elapsed since January 1, 1970 (UTC).
        }
        token = await self.encode_token(payload)
        return AccessTokenDTO(token=token)

    async def generate_refresh_token(self, dto: BaseUserDTO) -> RefreshTokenDTO:
        """
        Constructs the payload and generates an encoded refresh token.

        The payload includes:
        - `token_type`: Set to "access" (Note: Logic may imply this should be "refresh").
        - `user`: A dictionary containing `user_id` and `user_name` from the DTO.
        - `exp`: Expiration timestamp based on `refresh_token_lifetime`.
        - `iat`: Issued-at timestamp.

        Args:
            dto (UserDTO): The user data to embed in the token.

        Returns:
            str: The encoded refresh token.
        """
        now = datetime.now()
        expire = now + timedelta(seconds=self.refresh_token_lifetime)
        jti = str(uuid.uuid4())
        payload = {
            "token_type": "refresh",
            "sub": str(dto.id),
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()), #The number of seconds that have elapsed since January 1, 1970 (UTC).
            "jti": jti,
        }
        token = await self.encode_token(payload)
        return RefreshTokenDTO(token=token, jti=jti, expire=expire)

    async def verify_refresh_token(self, token: str) -> dict:
        """
        Validates that a token is a valid Refresh Token.

        This method decodes the token and specifically checks that the
        'token_type' claim is set to "refresh".

        Args:
            token (str): The encoded JWT string.

        Returns:
            dict: The decoded payload if valid.

        Raises:
            InvalidTokenError: If the token is invalid, expired, or has the wrong type.
        """
        payload = await self.decode_token(token)

        if payload.get("token_type") != "refresh":
            raise InvalidTokenError("Invalid token type. Expected 'refresh'.")

        return payload

    async def verify_access_token(self, token: str) -> dict:
        """
        Validates that a token is a valid Access Token.

        This method decodes the token and specifically checks that the
        'token_type' claim is set to "access".

        Args:
            token (str): The encoded JWT string.

        Returns:
            dict: The decoded payload if valid.

        Raises:
            InvalidTokenError: If the token is invalid, expired, or has the wrong type.
        """
        payload = await self.decode_token(token)

        if payload.get("token_type") != "access":
            raise InvalidTokenError("Invalid token type. Expected 'access'.")

        return payload