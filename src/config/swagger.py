from pydantic import (
    Field,
    EmailStr,
    AnyUrl,
)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    title: str = Field(default="PROJECT_NAME", alias="APP_TITLE") #TODO set project name
    description: str | None = Field(default=None, alias="APP_DESCRIPTION")
    summary: str | None = Field(None, alias="APP_SUMMARY")
    terms_of_service: str | None = Field(None, alias="APP_TERMS_OF_SERVICE")
    licence_name: str = Field("MIT", alias="APP_LICENSE_NAME")
    licence_identifier: str = Field("MIT", alias="APP_LICENSE_IDENTIFIER")
    licence_url: AnyUrl | None = Field("https://rem.mit-license.org/license.txt", alias="APP_LICENSE_URL")
    contact_name: str | None = Field("John Doe", alias="APP_CONTACT_NAME") #TODO set contact name
    contact_url: AnyUrl | None = Field("https://example.com", alias="APP_CONTACT_URL") #TODO set contact url
    contact_email: EmailStr | None = Field("John@Doe.com", alias="APP_CONTACT_EMAIL") #TODO set contact email
    docs_url: str | None = Field("/docs", alias="APP_DOCS_URL")
    redoc_url: str | None = Field("/redoc", alias="APP_REDOC_URL") # noqa

    @property
    def contact(self) -> dict:
        return {
            "name": self.contact_name,
            "url": self.contact_url,
            "email": self.contact_email
        }

    @property
    def license(self) -> dict:
        return {
            "name": self.licence_name,
            "url": self.licence_url,
            "identifier": self.licence_identifier
        }


settings = Settings()
