from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    access_token_expire_seconds: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_SECONDS")
    refresh_token_lifetime_seconds: int = Field(..., alias="REFRESH_TOKEN_LIFETIME_SECONDS")
    refresh_token_rotate_min_lifetime: int = Field(..., alias="REFRESH_TOKEN_ROTATE_MIN_LIFETIME")

settings = Settings()