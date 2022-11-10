import pytest

import os
from dotenv import load_dotenv
from os import environ

# from data_base.base import engine, session


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@pytest.fixture
def get_base_url():
    app_host = environ.get("APP_HOST", "localhost")
    app_port = environ.get("APP_PORT", 8080)

    address = f"http://{app_host}:{app_port}"

    return address


@pytest.fixture
def get_db_uri():
    user = environ.get("POSTGRES_USER", "postgres")
    password = environ.get("POSTGRES_PASSWORD", "postgres")
    host = environ.get("POSTGRES_HOST", "127.0.0.1")
    port = environ.get("POSTGRES_PORT", "5432")
    database = environ.get("POSTGRES_DB", "ITMO_Event")

    db_uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return db_uri


# @pytest.fixture
# def get_session_to_db():
#     with session(bind=engine) as local_session:
#         yield local_session
