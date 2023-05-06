from logging.config import dictConfig
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pymongo.errors import PyMongoError

from app import api
from app.core.exceptions import AppException, AppExceptionCase, app_exception_handler
from app.core.log import log_config

dictConfig(log_config())

APP_ROOT = Path(__file__).parent.parent


def create_app():
    app = FastAPI()
    register_api_routers(app)
    register_extensions(app)
    return app


def register_api_routers(app: FastAPI):
    api.init_api_v1(app)

    @app.get("/", include_in_schema=False)
    def index():
        return RedirectResponse("/docs")

    return None


def register_extensions(app: FastAPI):
    """Register Flask extensions."""

    @app.exception_handler(HTTPException)
    def handle_http_exception(request, exc):
        return app_exception_handler(exc)

    @app.exception_handler(PyMongoError)
    def handle_db_exception(request, exc):
        return app_exception_handler(exc)

    @app.exception_handler(AppExceptionCase)
    def handle_app_exceptions(request, exc):
        return app_exception_handler(exc)

    return None
