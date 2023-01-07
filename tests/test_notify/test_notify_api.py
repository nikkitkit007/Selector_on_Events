import requests
from starlette import status

from tests.conftest import cookies


notify_id = 1


class TestEvent:
    def test_add(self, get_base_url, get_one_notify):
        method = "/api/notify/add"
        notify = get_one_notify

        response = requests.post(get_base_url + method, json=notify, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, get_base_url):
        method = "/api/notify/delete"

        # event_id = get_one_event["event_id"]
        notify_id_dict = {'notify_id': notify_id}

        response = requests.delete(get_base_url + method, json=notify_id_dict, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK
