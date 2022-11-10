import os
from dotenv import load_dotenv
from os import environ

from pydantic import BaseSettings

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    I need three environments: for development, testing and production.
    """
    TEST = bool(environ.get("TEST", "True"))
    if TEST:
        APP_HOST = "127.0.0.1"
        APP_PORT = 8080

        POSTGRES_DB = "test_itmo_event"
        POSTGRES_HOST = "127.0.0.1"
        POSTGRES_USER = "test"
        POSTGRES_PORT = "5435"
        POSTGRES_PASSWORD = "test"

    else:
        APP_HOST: str = environ.get("APP_HOST", "127.0.0.1")
        APP_PORT: int = int(environ.get("APP_PORT", 8080))

        POSTGRES_DB: str = environ.get("POSTGRES_DB", "ITMO_Event")
        POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "127.0.0.1")
        POSTGRES_USER: str = environ.get("POSTGRES_USER", "postgres")
        POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432"))
        POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "postgres")

    PATH_PREFIX: str = environ.get("PATH_PREFIX", "")  # api/v1

    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    TBL_EVENTS = environ.get("TBL_EVENTS", "event")
    TBL_USERS = environ.get("TBL_USERS", "user")
    TBL_NOTIFIES = environ.get("TBL_NOTIFIES", "notify")
    TBL_NEWS = environ.get("TBL_NEWS", "news")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def host_address(self):
        return f"http://{self.APP_HOST}:{self.APP_PORT}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
