import requests
from starlette import status

from tests.conftest import cookies


class TestHealth:
    def test_index(self, get_base_url):
        response = requests.get(get_base_url+"/api/", cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_ping_app(self, get_base_url):
        method = "/api/health/app"
        response = requests.get(get_base_url + method)

        assert response.status_code == status.HTTP_200_OK

    def test_ping_db(self, get_base_url):
        method = "/api/health/db"
        response = requests.get(get_base_url + method)

        assert response.status_code == status.HTTP_200_OK


