import logging
import logging.config

from fastapi import FastAPI

from src.config.project import settings as main_settings
from src.config.swagger import settings as swagger_settings
from src.config.logging import settings as logging_settings, logger_config

from src.lifespan import lifespan

from src.middleware import init_middleware

from src.exception_handlers import exception_handlers

from src.routes import router


def get_app() -> FastAPI:
    if logging_settings.logging_on:
        logging.config.dictConfig(logger_config)  # noqa

    app = FastAPI(
        title=swagger_settings.title,
        # description=get_description(swagger_settings.description),
        summary=swagger_settings.summary,
        version=main_settings.version,
        terms_of_service=swagger_settings.terms_of_service,
        contact=swagger_settings.contact,
        license_info=swagger_settings.license,
        lifespan=lifespan,
        root_path=main_settings.root_path,
        debug=main_settings.debug,
        docs_url=swagger_settings.docs_url if main_settings.debug else None,
        redoc_url=swagger_settings.redoc_url if main_settings.debug else None,
        openapi_url=f"{swagger_settings.docs_url}/openapi.json"
        if main_settings.debug
        else None,
        exception_handlers=exception_handlers,
    )

    init_middleware(app)

    app.include_router(router)

    return app


app = get_app()
