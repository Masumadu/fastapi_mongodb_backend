import os

from dotenv import load_dotenv
from pydantic import BaseSettings

from app import constants


class BaseConfig(BaseSettings):
    # reminder: general application settings
    fastapi_config: str = ""
    app_name: str = constants.APPLICATION_NAME
    secret_key: str = ""
    log_header: str = constants.LOG_HEADER
    # reminder: postgres database config
    db_host: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    db_port: int = 5432
    # reminder: redis server config
    redis_server: str = ""
    redis_port: int = 6379
    redis_password: str = ""
    # reminder: jwt config
    jwt_algorithm: str = "HS256"

    # MAIL CONFIGURATION
    mail_server: str = ""
    mail_server_port: str = ""
    default_mail_sender_address: str = ""
    default_mail_sender_password: str = ""
    admin_mail_addresses: str = ""

    class Config:
        env_file = ".env"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


def get_settings():
    load_dotenv(".env")
    config_cls_dict = {
        constants.DEVELOPMENT_ENVIRONMENT: DevelopmentConfig,
        constants.PRODUCTION_ENVIRONMENT: ProductionConfig,
        constants.TESTING_ENVIRONMENT: TestingConfig,
    }
    config_name = os.getenv("FASTAPI_CONFIG", default=constants.DEVELOPMENT_ENVIRONMENT)
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
