import requests
from starlette import status
from tests.conftest import cookies

event_id = 1
# cookies = {'access_token': 'lol_lol_lol'}


class TestEvent:
    def test_add(self, get_base_url, get_one_event):
        method = "/api/event"
        event = get_one_event

        response = requests.post(get_base_url + method, json=event,  cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, get_base_url, get_one_event):
        method = "/api/event"
        # event_id = get_one_event["event_id"]
        event_id_dict = {'event_id': event_id}

        response = requests.get(get_base_url + method, params=event_id_dict, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_get_all(self, get_base_url):
        method = "/api/event"
        event_id_dict = {'event_id': event_id, "all": True}

        response = requests.get(get_base_url + method, params=event_id_dict, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_update(self, get_base_url, get_update_event):
        method = "/api/event"
        data_update = get_update_event

        response = requests.put(get_base_url + method, json=data_update, cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, get_base_url, get_one_event):
        method = "/api/event"

        # event_id = get_one_event["event_id"]
        event_id_dict = {'event_id': event_id}

        response = requests.delete(get_base_url + method, json=event_id_dict, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK
