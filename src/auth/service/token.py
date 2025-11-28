from jwt import ExpiredSignatureError, PyJWTError, decode, encode, get_unverified_header

from src.auth.dto import TokenDTO, UserDTO
from datetime import datetime, timedelta
from src.config.jwt import settings as jwt_settings
from src.config.security import settings as security_settings
from src.auth.exceptions.token import InvalidSignatureError


class TokenService:
    def __init__(self) -> None:
        self.access_token_lifetime = jwt_settings.access_token_expire_seconds
        self.refresh_token_lifetime = jwt_settings.refresh_token_lifetime_seconds
        self.secret_key = security_settings.secret_key
        self.algorithm = security_settings.algorithm

    async def create_tokens(self, dto: UserDTO) -> TokenDTO:
        access_token = await self.generate_access_token(dto)
        refresh_token = await self.generate_refresh_token(dto)
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    def _validate_token(self, token: str):
        token_info = get_unverified_header(token)
        if token_info["alg"] != self.algorithm:
            raise InvalidSignatureError("Key error")
        return token

    async def encode_token(self, payload: dict) -> str:
        return encode(payload, self.secret_key, self.algorithm)

    async def decode_token(self, token: str) -> dict:
        try:
            self._validate_token(token)
            return decode(token, self.secret_key, self.algorithm)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token lifetime is expired")
        except PyJWTError:
            raise Exception("Token is invalid")

    async def generate_access_token(self, dto: UserDTO):
        expire = datetime.now() + timedelta(seconds=self.access_token_lifetime)
        payload = {
            "token_type": "access",
            "user": {"user_id": str(dto.id), "user_name": str(dto.name)},
            "exp": str(expire),
            "iat": str(datetime.now()),
        }
        return await self.encode_token(payload)

    async def generate_refresh_token(self, dto: UserDTO):
        expire = datetime.now() + timedelta(seconds=self.refresh_token_lifetime)
        payload = {
            "token_type": "access",
            "user": {"user_id": str(dto.id), "user_name": str(dto.name)},
            "exp": str(expire),
            "iat": str(datetime.now()),
        }
        return await self.encode_token(payload)
