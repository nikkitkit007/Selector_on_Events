import pytest

import os
from dotenv import load_dotenv
from os import environ
from sqlalchemy_utils import create_database, database_exists, drop_database

from configurations.default import DefaultSettings

# from data_base.base import engine, session

cookies = {'access_token': 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwSVliSmNVLW1wbEdBdzhFMzNSNkNKTUdWa3hZdUQ2eUItdWt3RlBJOXV3In0.eyJleHAiOjE2NzYxMzU0OTgsImlhdCI6MTY3NjEzMzY5OCwiYXV0aF90aW1lIjoxNjc2MTEzNTkzLCJqdGkiOiI1YzNkODNlYy00YmFjLTQ5OWEtYTQ5Mi1iZTlhOWUzMzU4NzAiLCJpc3MiOiJodHRwczovL2lkLml0bW8ucnUvYXV0aC9yZWFsbXMvaXRtbyIsInN1YiI6IjI1ODgzOTE0LWI2MGEtNGY4Zi1hYjUxLTNiOTY4MzYzOTVkNyIsInR5cCI6IkJlYXJlciIsImF6cCI6InN0dWRlbnRzLXByb2plY3QtZXZlbnQtZGV2Iiwic2Vzc2lvbl9zdGF0ZSI6ImQ4MzdmMWY5LTg4YzMtNDZiZC1iZDg5LWY2NTUyZWZmZmE3YSIsImFjciI6IjAiLCJzY29wZSI6Im9wZW5pZCIsInNpZCI6ImQ4MzdmMWY5LTg4YzMtNDZiZC1iZDg5LWY2NTUyZWZmZmE3YSIsImlzdSI6Mjg0Njc5fQ.ZhyifThz55rgZD_V4e4ysNQfKRahF3Gd9fKEOH2Q5DgeTROdORd8wF8p18V13hZOvZKynwpyiwxg7vhaI-1yH-gICwSpOiGLtHGV3IPbCVAkV8QNTbqyPJi9Uz2QzLspKTOyqvxG27JMBDyprBAIYgXuwYy7DmS4FJqMYY047iiK2Pgxuec2UtdIlidjso_tlHDwlWH1SuX3xX6vpHcqfiW2c6H9m8B7231a9Re9DBMWQKedmlqP5UYViJdU9le0gZhQ1Cy2bnQo8wvO0b1ekFzMEol4BsvYHFR0YaZrnwPqqOKVmCAAJxy8Izw9-4218mIgsTZXKdDwgJ6g7ne8lw'}
# cookies = {'access_token': ''}


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

#
# @pytest.fixture()
# def postgres() -> str:
#     """
#     Создает временную БД для запуска теста.
#     """
#     settings = DefaultSettings()
#
#     tmp_name = ".".join(["temp", "pytest"])
#     settings.POSTGRES_DB = tmp_name
#     environ["POSTGRES_DB"] = tmp_name
#
#     tmp_url = settings.database_uri_sync
#     if not database_exists(tmp_url):
#         create_database(tmp_url)
#
#     try:
#         yield settings.database_uri
#     finally:
#         drop_database(tmp_url)
