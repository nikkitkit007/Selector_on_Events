import requests
from starlette import status

from tests.conftest import cookies


news_id = 1


class TestNews:
    def test_add(self, get_base_url, get_one_news):
        method = "/api/news/add"
        news = get_one_news

        response = requests.post(get_base_url + method, json=news, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, get_base_url, get_one_news):
        method = "/api/news/get"
        # news_id = get_one_news["news_id"]
        news_id_dict = {'news_id': news_id}

        response = requests.get(get_base_url + method, params=news_id_dict, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_get_all(self, get_base_url):
        method = "/api/news/get_all"

        response = requests.get(get_base_url + method, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_update(self, get_base_url, get_update_news):
        method = "/api/news/update"
        data_update = get_update_news

        response = requests.post(get_base_url + method, json=data_update, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, get_base_url, get_one_news):
        method = "/api/news/delete"

        # news_id = get_one_news["news_id"]
        news_id_dict = {'news_id': news_id}

        response = requests.delete(get_base_url + method, json=news_id_dict, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK
