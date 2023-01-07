import requests
from starlette import status

from sqlalchemy_utils import database_exists


class TestHealth:
    def test_ping_app(self, get_base_url):
        method = "/health_app"
        response = requests.get(get_base_url + method)

        assert response.status_code == status.HTTP_200_OK

    def test_ping_db(self, get_base_url):
        method = "/health_db"
        response = requests.get(get_base_url + method)

        # db_uri = get_db_uri
        # assert database_exists(db_uri) == 1
        assert response.status_code == status.HTTP_200_OK


